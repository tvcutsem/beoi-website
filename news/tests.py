# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

class NewsTest(TestCase):
    """
    Tests of ``news`` application.
    """
    fixtures = ['test_data']

    def test_entry_archive_index(self):
        """
        Tests ``entry_archive`` view.
        """
        responsefr = self.client.get(reverse('home-fr'))
        responsenl = self.client.get(reverse('home-nl'))

		# check related to the test date (fixture), only 1 news in total, in the right lang
        self.assertContains(responsefr, 'News in French', 1, status_code=200)  
        self.assertNotContains(responsefr, 'News in Dutch')

        self.assertContains(responsenl, 'News in Dutch', 1, status_code=200) 
        self.assertNotContains(responsenl, 'News in French')



