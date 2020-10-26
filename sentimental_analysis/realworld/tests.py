from django.test import TestCase
from realworld import views

from realworld import utilityFunctions

class TestCases(TestCase):
    def test_1(self):
        self.assertEqual(1,1)

    def test_detailed(self):
        result = views.detailed_analysis(['horrible'])
        self.assertEqual(result['neg'],1.0)

    def test_detailed_2(self):
        result = views.detailed_analysis(['bad'])
        self.assertEqual(result['neg'],1.0)

    def test_detailed_3(self):
        result = views.detailed_analysis(['good'])
        self.assertEqual(result['pos'],1.0)

    def test_detailed_4(self):
        result = views.detailed_analysis(['nice'])
        self.assertEqual(result['pos'],1.0)

    def test_detailed_5(self):
        result = views.detailed_analysis(['normal'])
        self.assertEqual(result['neu'],1.0)

    def test_detailed_6(self):
        result = views.detailed_analysis(['horrible','great'])
        self.assertEqual(result['neg'],0.5)
        self.assertEqual(result['pos'],0.5)

    def test_cleantext(self):
        result = views.get_clean_text("bad to do this task")
        self.assertEqual(result,'bad task')

    def test_cleantext_2(self):
        result = views.get_clean_text("better products are there")
        self.assertEqual(result,"better products")


    def test_cleantext_3(self):
        result = views.get_clean_text("to do")
        self.assertEqual(result,'')


    def test_cleantext_4(self):
        result = views.get_clean_text("to nice")
        self.assertEqual(result,'nice')

    def test_cleantest_5(self):
        result = views.get_clean_text("adding new products is necessary to this range")
        self.assertEqual(result, "adding new products necessary range")

    def test_rmlink(self):
        result = utilityFunctions.removeLinks("http://abc.com good")
        self.assertEqual(result,' good')
