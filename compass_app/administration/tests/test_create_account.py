# Author: Anastasija Ljubicic 0312/2023

import time

from django.test import TestCase, Client, SimpleTestCase
from django.urls import resolve, reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.hashers import make_password

from selenium import webdriver
from selenium.webdriver.common.by import By

from accounts.models import User
from administration.views import create_account


class TestUrls(SimpleTestCase):

    def test_create_account_is_resolved(self):
        url = reverse('administration:create_account')
        self.assertEqual(resolve(url).func, create_account)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_create_account_GET_neulogovan(self):
        response = self.client.get(reverse('administration:create_account'))
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

        self.client.post(reverse('login'), data = {
            'username' : 'admin_test',
            'password' : 'Test1234'
        })

    def tearDown(self):
        self.client.get(reverse('logout_view'))

    def test_create_account_GET(self):
        response = self.client.get(reverse('administration:create_account'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kreiranje naloga', html=True)

    def test_create_account_POST(self):
        response = self.client.post(reverse('administration:create_account'), data = {
            'account_type' : 'user',
            'user-first_name' : 'Petar',
            'user-last_name' : 'Petrovic',
            'user-username' : 'petar_petrovic',
            'user-email' : 'petar@example.com',
            'user-contact' : '',
            'user-password' : 'Sifra1234',
            'user-password_confirm' : 'Sifra1234'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='petar_petrovic').exists())


class FunctionalTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.appUrl = self.live_server_url + reverse('administration:create_account')
        self.loginUrl = self.live_server_url + reverse('login')

        self.password = 'Test1234'
        User.objects.create(
            first_name='Ana', last_name='Admin', username='admin_test',
            email='admin_test@example.com', password=make_password(self.password),
            status='active', role='admin'
        )

    def tearDown(self):
        self.browser.close()

    def test_kreiranje_korisnika(self):
        self.browser.get(self.loginUrl)

        username = self.browser.find_element(By.NAME, 'username')
        username.send_keys('admin_test')
        password = self.browser.find_element(By.NAME, 'password')
        password.send_keys(self.password)
        submit = self.browser.find_element(By.XPATH, '//input[@type="submit"]')
        submit.click()
        time.sleep(2)

        self.browser.get(self.appUrl + '?type=user')
        time.sleep(2)

        self.browser.find_element(By.NAME, 'user-first_name').send_keys('Jovana')
        self.browser.find_element(By.NAME, 'user-last_name').send_keys('Jovanovic')
        self.browser.find_element(By.NAME, 'user-username').send_keys('jovana_jovanovic')
        self.browser.find_element(By.NAME, 'user-email').send_keys('jovana@example.com')
        self.browser.find_element(By.NAME, 'user-password').send_keys('Sifra1234')
        self.browser.find_element(By.NAME, 'user-password_confirm').send_keys('Sifra1234')

        submit = self.browser.find_element(By.XPATH, '//button[@type="submit"]')
        self.browser.execute_script('arguments[0].scrollIntoView(true);', submit)
        self.browser.execute_script('arguments[0].click();', submit)
        time.sleep(5)

        self.assertTrue(User.objects.filter(username='jovana_jovanovic').exists())
