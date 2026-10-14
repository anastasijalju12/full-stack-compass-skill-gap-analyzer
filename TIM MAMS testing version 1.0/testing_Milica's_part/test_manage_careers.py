# Autor: Anastasija Ljubicic 0312/2023

import time

from django.test import TestCase, Client, SimpleTestCase
from django.urls import resolve, reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.hashers import make_password

from selenium import webdriver
from selenium.webdriver.common.by import By

from accounts.models import User
from careers.models import Career
from administration.views import manage_careers

# Create your tests here.

class TestUrls(SimpleTestCase):

    def test_manage_careers_is_resolved(self):
        url = reverse('administration:manage_careers')
        self.assertEqual(resolve(url).func, manage_careers)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_manage_careers_GET_neulogovan(self):
        response = self.client.get(reverse('administration:manage_careers'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))


class TestLoggedInCase(TestCase):

    def setUp(self):
        self.client = Client()

        admin = User.objects.create(
            first_name='Ana', last_name='Admin', username='admin_test',
            email='admin_test@example.com', password=make_password('Test1234'),
            status='active', role='admin'
        )

        self.career = Career.objects.create(
            name='Programer', description='Opis karijere'
        )

        self.client.post(reverse('login'), data = {
            'username' : 'admin_test',
            'password' : 'Test1234'
        })

    def tearDown(self):
        self.client.get(reverse('logout_view'))

    def test_manage_careers_GET(self):
        response = self.client.get(reverse('administration:manage_careers'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Programer')

    def test_create_career(self):
        response = self.client.post(reverse('administration:create_career'), data = {
            'name' : 'Dizajner',
            'description' : 'Opis nove karijere',
            'skills' : 'Figma, Photoshop'
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Career.objects.filter(name='Dizajner').exists())

    def test_delete_career(self):
        response = self.client.post(
            reverse('administration:delete_career', args=[self.career.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Career.objects.filter(id=self.career.id).exists())


class FunctionalTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.appUrl = self.live_server_url + reverse('administration:manage_careers')
        self.loginUrl = self.live_server_url + reverse('login')

        self.password = 'Test1234'
        User.objects.create(
            first_name='Ana', last_name='Admin', username='admin_test',
            email='admin_test@example.com', password=make_password(self.password),
            status='active', role='admin'
        )

    def tearDown(self):
        self.browser.close()

    def test_dodavanje_nove_karijere(self):
        self.browser.get(self.loginUrl)

        username = self.browser.find_element(By.NAME, 'username')
        username.send_keys('admin_test')
        password = self.browser.find_element(By.NAME, 'password')
        password.send_keys(self.password)
        submit = self.browser.find_element(By.XPATH, '//input[@type="submit"]')
        submit.click()
        time.sleep(6)

        self.browser.get(self.appUrl + '?new=1')
        time.sleep(6)

        self.browser.find_element(By.ID, 'newCareerName').send_keys('Testerka')
        self.browser.find_element(By.ID, 'newCareerDescription').send_keys('Opis nove karijere za testiranje')
        self.browser.find_element(By.ID, 'newCareerSkills').send_keys('Selenium, Django')

        save = self.browser.find_element(By.XPATH, '//button[normalize-space(text())="Save new career"]')
        self.browser.execute_script('arguments[0].scrollIntoView(true);', save)
        self.browser.execute_script('arguments[0].click();', save)
        time.sleep(6)

        self.assertTrue(Career.objects.filter(name='Testerka').exists())