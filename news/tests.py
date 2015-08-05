from django.test import TestCase
from news.parser import parse_title


class ParseTest(TestCase):

    def test_parse_google_title(self):
        google_title = parse_title('http://www.google.com')
        self.assertEqual('Google', google_title)
