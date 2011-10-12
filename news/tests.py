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
        responsefr = self.client.get(reverse('home',kwargs={"language":"fr"}))
        # responsenl = self.client.get(reverse('home',kwargs={"language":"nl"}))

		# check related to the test date (fixture), only 1 news in total, in the right lang
        self.assertContains(responsefr, 'News in French', 1, status_code=200)  
        self.assertNotContains(responsefr, 'News in Dutch')

        # self.assertContains(responsenl, 'News in Dutch', 1, status_code=200) 
        # self.assertNotContains(responsenl, 'News in French')

    def test_pagination(self):
        
        response = self.client.get(reverse('home',kwargs={"language":"fr"}))
        self.assertContains(response, 'News2', 1, status_code=200)  
        self.assertContains(response, 'News5', 1, status_code=200)  
        self.assertNotContains(response, 'News1')  
        
        # response = self.client.get(reverse('home', kwargs={"language":"fr"}, args=[1]))
        # self.assertContains(response, 'News2', 1, status_code=200)  
        # self.assertContains(response, 'News5', 1, status_code=200)  
        # self.assertNotContains(response, 'News1')
        # 
        # response = self.client.get(reverse('home',kwargs={"language":"fr"}, args=[2]))
        # self.assertContains(response, 'News1', 1, status_code=200)  
        # self.assertNotContains(response, 'News2')  
        # self.assertNotContains(response, 'News5')  
        
        response = self.client.get(reverse('home', kwargs={"language":"fr"}))
        self.assertContains(response, 'News2', 1, status_code=200)  
        self.assertContains(response, 'News5', 1, status_code=200)  
        self.assertNotContains(response, 'News1')  
        
        # response = self.client.get(reverse('home', args=[1], kwargs={"language":"nl"}))
        # self.assertContains(response, 'News2', 1, status_code=200)  
        # self.assertContains(response, 'News5', 1, status_code=200)  
        # self.assertNotContains(response, 'News1')
        # 
        # response = self.client.get(reverse('home',args=[2], kwargs={"language":"nl"}))
        # self.assertContains(response, 'News1', 1, status_code=200)  
        # self.assertNotContains(response, 'News2')  
        # self.assertNotContains(response, 'News5')  

