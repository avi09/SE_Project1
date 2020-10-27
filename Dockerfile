FROM python:3.7

RUN pip install --upgrade pip

ADD . /my-django-app

WORKDIR /my-django-app

RUN pip install -r requirements.txt

RUN python3 ./sentimental_analysis/manage.py migrate

CMD python3 ./sentimental_analysis/manage.py runserver 0.0.0.0:5000