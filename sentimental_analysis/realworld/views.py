from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from django.template.defaulttags import register
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from .utilityFunctions import *
import os
import json
import speech_recognition as sr
from nltk.stem import PorterStemmer


def pdfparser(data):

    fp = open(data, "rb")
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data = retstr.getvalue()

    text_file = open("Output.txt", "w", encoding="utf-8")
    text_file.write(data)

    text_file = open("Output.txt", "r", encoding="utf-8")
    a = ""
    for x in text_file:
        if len(x) > 2:
            b = x.split()
            for i in b:
                a += " " + i
    final_comment = a.split(".")
    return final_comment


def analysis(request):
    return render(request, "realworld/analysis.html")


def get_clean_text(text):
    text = removeLinks(text)
    text = stripEmojis(text)
    text = removeSpecialChar(text)
    text = stripPunctuations(text)
    text = stripExtraWhiteSpaces(text)

    # Tokenize using nltk
    tokens = nltk.word_tokenize(text)

    # Import stopwords
    stop_words = set(stopwords.words("english"))
    stop_words.add("rt")
    stop_words.add("")

    # Remove tokens which are in stop_words
    newtokens = [item for item in tokens if item not in stop_words]

    textclean = " ".join(newtokens)
    return textclean


def detailed_analysis(result):
    result_dict = {}
    neg_count = 0
    pos_count = 0
    neu_count = 0
    total_count = len(result)

    for item in result:
        print(item)
        cleantext = get_clean_text(str(item))
        print(cleantext)
        sentiment = sentiment_scores(cleantext)
        print(sentiment)
        compound_score = sentiment["compound"]

        pos_count += sentiment["pos"]
        neu_count += sentiment["neu"]
        neg_count += sentiment["neg"]

    towords = {}
    for i in set(result):
        i = get_clean_text(i)
        i = i.lower()
        uwords = [
            "more",
            "at",
            "so",
            "although",
            "some",
            "to",
            "the",
            "of",
            "can",
            "but",
            "thi",
            "kind",
            "realli",
            "thus",
            "some",
            "part",
            "there",
            "which",
            "make",
            "it",
            "need",
        ]
        for j in i.split(" "):
            j = PorterStemmer().stem(j)
            if not j in uwords:
                if not j in towords.keys():
                    towords[str(j)] = 1
                else:
                    towords[str(j)] += 1
    towords = {k: v for k, v in sorted(towords.items(), key=lambda x: x[1])}

    total = pos_count + neu_count + neg_count
    result_dict["pos"] = pos_count / total
    result_dict["neu"] = neu_count / total
    result_dict["neg"] = neg_count / total
    print(towords)
    return result_dict, towords


def input(request):
    if request.method == "POST":
        file = request.FILES["document"]
        fs = FileSystemStorage()
        fs.save(file.name, file)
        pathname = "media/"
        extension_name = file.name
        extension_name = extension_name[len(extension_name) - 3 :]
        path = pathname + file.name
        result = {}
        if extension_name == "pdf":
            value = pdfparser(path)
            result, towords = detailed_analysis(value)
        elif extension_name == "txt":
            text_file = open(path, "r", encoding="utf-8")
            a = ""
            for x in text_file:
                if len(x) > 2:
                    b = x.split()
                    for i in b:
                        a += " " + i
            final_comment = a.split(".")
            result, towords = detailed_analysis(final_comment)
        elif extension_name == "wav":
            r = sr.Recognizer()
            with sr.AudioFile(path) as source:
                # listen for the data (load audio to memory)
                audio_data = r.record(source)
                # recognize (convert from speech to text)
                text = r.recognize_google(audio_data)
                value = text.split(".")
                result, towords = detailed_analysis(value)
        # Sentiment Analysis
        os.system(
            "cd /Users/nischalkashyap/Downloads/Projects/CELT/SE_Project1/sentimental_analysis/media/ && rm -rf *"
        )
        return render(
            request,
            "realworld/sentiment_graph.html",
            {"sentiment": result, "towords": towords},
        )
    else:
        note = "Please Enter the file you want to analyze"
        return render(request, "realworld/home.html", {"note": note})


def productanalysis(request):
    if request.method == "POST":
        blogname = request.POST.get("blogname", "")
        text_file = open(
            "/home/mnagdev/NCSU Courses/SE/Sentiment_Analysis/SE_Project1/Amazon_Comments_Scrapper/amazon_reviews_scraping/amazon_reviews_scraping/spiders/ProductAnalysis.txt",
            "w",
        )
        text_file.write(blogname)
        text_file.close()
        os.system(
            "scrapy runspider /home/mnagdev/NCSU Courses/SE/Sentiment_Analysis/SE_Project1/Amazon_Comments_Scrapper/amazon_reviews_scraping/amazon_reviews_scraping/spiders/amazon_review.py -o reviews.json"
        )
        final_comment = []
        with open(
            "/home/mnagdev/NCSU Courses/SE/Sentiment_Analysis/SE_Project1/sentimental_analysis/realworld/reviews.json"
        ) as json_file:
            data = json.load(json_file)
            for p in range(1, len(data) - 1):
                a = data[p]["comment"]
                final_comment.append(a)

        # final_comment is a list of strings!
        result, towords = detailed_analysis(final_comment)
        print(result)
        return render(
            request,
            "realworld/sentiment_graph.html",
            {"sentiment": result, "towords": towords},
        )

    else:
        note = "Please Enter the product blog link for analysis"
        return render(request, "realworld/productanalysis.html", {"note": note})


# Custom template filter to retrieve a dictionary value by key.


def textanalysis(request):
    if request.method == "POST":
        text_data = request.POST.get("Text", "")
        final_comment = text_data.split(".")

        # final_comment is a list of strings!
        result, towords = detailed_analysis(final_comment)
        print(result)
        return render(
            request,
            "realworld/sentiment_graph.html",
            {"sentiment": result, "towords": towords},
        )
    else:
        note = "Text to be analysed!"
        return render(request, "realworld/textanalysis.html", {"note": note})


def moviereviewanalysis(request):
    if request.method == "POST":
        movie = request.POST.get("movie", "")
        text_file = open(
            "/home/mnagdev/NCSU Courses/SE/Sentiment_Analysis/SE_Project1/sentimental_analysis/movie_review_link.txt",
            "w",
        )
        text_file.write(movie)
        text_file.close()
        os.system("python3 movie_scrap.py")
        review_file = open("movie_reviews.txt", "r")
        final_comment = review_file.read().split(".")

        # final_comment is a list of strings!
        result, towords = detailed_analysis(final_comment)
        print(result)
        return render(
            request,
            "realworld/sentiment_graph.html",
            {"sentiment": result, "towords": towords},
        )
    else:
        note = "Please Enter the movie review link for analysis"
        return render(request, "realworld/moviereviewanalysis.html", {"note": note})


@register.filter(name="get_item")
def get_item(dictionary, key):
    return dictionary.get(key, 0)
