# Author: Anastasija Ljubicic 0312/2023

import time

from django.test import TestCase, Client, SimpleTestCase
from django.urls import resolve, reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.hashers import make_password

from selenium import webdriver
from selenium.webdriver.common.by import By

from accounts.models import User, Company
from administration.views import company_requests


class TestUrls(SimpleTestCase):

    def test_company_requests_is_resolved(self):
        url = reverse('administration:company_requests')
        self.assertEqual(resolve(url).func, company_requests)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_company_requests_GET_neulogovan(self):
        response = self.client.get(reverse('administration:company_requests'))

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

        self.company = Company.objects.create(
            name='Firma Na Cekanju', username='firma_cekanje',
            email='cekanje@example.com', password=make_password('lozinka123'),
            status='pending'
        )

        self.client.post(reverse('login'), data = {
            'username' : 'admin_test',
            'password' : 'Test1234'
        })

    def tearDown(self):
        self.client.get(reverse('logout_view'))

    def test_company_requests_GET(self):
        response = self.client.get(reverse('administration:company_requests'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Registracije firmi', html=True)
        self.assertContains(response, 'Firma Na Cekanju')

    def test_approve_company(self):
        response = self.client.post(
            reverse('administration:approve_company', args=[self.company.id])
        )

        self.assertEqual(response.status_code, 302)

        self.company.refresh_from_db()
        self.assertEqual(self.company.status, 'active')

    def test_reject_company_bez_razloga(self):
        response = self.client.post(
            reverse('administration:reject_company', args=[self.company.id]),
            data = {'rejection_reason' : ''}
        )

        self.assertEqual(response.status_code, 302)

        self.company.refresh_from_db()
        self.assertEqual(self.company.status, 'pending')

    def test_reject_company_sa_razlogom(self):
        response = self.client.post(
            reverse('administration:reject_company', args=[self.company.id]),
            data = {'rejection_reason' : 'Nepotpuna dokumentacija'}
        )

        self.assertEqual(response.status_code, 302)

        self.company.refresh_from_db()
        self.assertEqual(self.company.status, 'rejected')


class FunctionalTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.appUrl = self.live_server_url + reverse('administration:company_requests')
        self.loginUrl = self.live_server_url + reverse('login')

        self.password = 'Test1234'
        User.objects.create(
            first_name='Ana', last_name='Admin', username='admin_test',
            email='admin_test@example.com', password=make_password(self.password),
            status='active', role='admin'
        )

        self.company = Company.objects.create(
            name='Firma Na Cekanju', username='firma_cekanje',
            email='cekanje@example.com', password=make_password('lozinka123'),
            status='pending'
        )

    def tearDown(self):
        self.browser.close()

    def test_odobravanje_firme(self):
        self.browser.get(self.loginUrl)

        username = self.browser.find_element(By.NAME, 'username')
        username.send_keys('admin_test')
        password = self.browser.find_element(By.NAME, 'password')
        password.send_keys(self.password)
        submit = self.browser.find_element(By.XPATH, '//input[@type="submit"]')
        submit.click()
        time.sleep(2)

        self.browser.get(self.appUrl + f'?company={self.company.id}')
        time.sleep(2)

        odobri = self.browser.find_element(By.XPATH, '//button[normalize-space(text())="Odobri registraciju"]')
        self.browser.execute_script('arguments[0].scrollIntoView(true);', odobri)
        self.browser.execute_script('arguments[0].click();', odobri)
        time.sleep(2)

        self.company.refresh_from_db()
        self.assertEqual(self.company.status, 'active')