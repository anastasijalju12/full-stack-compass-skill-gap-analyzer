# Autor: Anastasija Ljubicic 0312/2023

import time

from django.test import TestCase, Client, SimpleTestCase
from django.urls import resolve, reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.hashers import make_password

from selenium import webdriver
from selenium.webdriver.common.by import By

from accounts.models import User, Company
from administration.views import manage_accounts

# Create your tests here.

class TestUrls(SimpleTestCase):

    def test_manage_accounts_is_resolved(self):
        url = reverse('administration:manage_accounts')
        self.assertEqual(resolve(url).func, manage_accounts)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_manage_accounts_GET_neulogovan(self):
        response = self.client.get(reverse('administration:manage_accounts'))

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

        self.user = User.objects.create(
            first_name='Marko', last_name='Markovic', username='marko_user',
            email='marko@example.com', password=make_password('lozinka123'),
            status='active', role='user'
        )

        self.company = Company.objects.create(
            name='Aktivna Firma', username='aktivna_firma',
            email='aktivna@example.com', password=make_password('lozinka123'),
            status='active'
        )

        self.client.post(reverse('login'), data = {
            'username' : 'admin_test',
            'password' : 'Test1234'
        })

    def tearDown(self):
        self.client.get(reverse('logout_view'))

    def test_manage_accounts_GET(self):
        response = self.client.get(reverse('administration:manage_accounts'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Accounts &amp; roles', html=True)

    def test_update_user_account(self):
        response = self.client.post(
            reverse('administration:update_user_account', args=[self.user.id]),
            data = {
                'first_name' : 'Marko',
                'last_name' : 'Markovic',
                'email' : 'novi_marko@example.com',
                'username' : 'marko_user',
                'contact' : ''
            }
        )

        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'novi_marko@example.com')

    def test_delete_company_account(self):
        response = self.client.post(
            reverse('administration:delete_company_account', args=[self.company.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Company.objects.filter(id=self.company.id).exists())


class FunctionalTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.appUrl = self.live_server_url + reverse('administration:manage_accounts')
        self.loginUrl = self.live_server_url + reverse('login')

        self.password = 'Test1234'
        User.objects.create(
            first_name='Ana', last_name='Admin', username='admin_test',
            email='admin_test@example.com', password=make_password(self.password),
            status='active', role='admin'
        )

        self.user = User.objects.create(
            first_name='Marko', last_name='Markovic', username='marko_user',
            email='marko@example.com', password=make_password('lozinka123'),
            status='active', role='user'
        )

    def tearDown(self):
        self.browser.close()

    def test_izmena_podataka_korisnika(self):
        self.browser.get(self.loginUrl)

        username = self.browser.find_element(By.NAME, 'username')
        username.send_keys('admin_test')
        password = self.browser.find_element(By.NAME, 'password')
        password.send_keys(self.password)
        submit = self.browser.find_element(By.XPATH, '//input[@type="submit"]')
        submit.click()
        time.sleep(5)

        self.browser.get(self.appUrl + f'?type=user&id={self.user.id}')
        time.sleep(5)

        last_name = self.browser.find_element(By.ID, 'userLastName')
        last_name.clear()
        last_name.send_keys('Markovic-Izmenjeno')

        save = self.browser.find_element(By.XPATH, '//button[normalize-space(text())="Save changes"]')
        self.browser.execute_script('arguments[0].scrollIntoView(true);', save)
        self.browser.execute_script('arguments[0].click();', save)
        time.sleep(5)

        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, 'Markovic-Izmenjeno')