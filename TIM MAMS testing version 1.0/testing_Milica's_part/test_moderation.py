# Autor: Anastasija Ljubicic 0312/2023

import time

from django.test import TestCase, Client, SimpleTestCase
from django.urls import resolve, reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.hashers import make_password

from selenium import webdriver
from selenium.webdriver.common.by import By

from accounts.models import User, Company
from careers.models import JobAd
from administration.views import moderation

# Create your tests here.

class TestUrls(SimpleTestCase):

    def test_moderation_is_resolved(self):
        url = reverse('administration:moderation')
        self.assertEqual(resolve(url).func, moderation)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_moderation_GET_neulogovan(self):
        response = self.client.get(reverse('administration:moderation'))

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
            name='Aktivna Firma', username='aktivna_firma',
            email='aktivna@example.com', password=make_password('lozinka123'),
            status='active'
        )

        self.job_ad = JobAd.objects.create(
            company=self.company, name='Praksa - Testiranje',
            type='internship', status='pending'
        )

        self.client.post(reverse('login'), data = {
            'username' : 'admin_test',
            'password' : 'Test1234'
        })

    def tearDown(self):
        self.client.get(reverse('logout_view'))

    def test_moderation_GET(self):
        response = self.client.get(reverse('administration:moderation'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Job moderation', html=True)
        self.assertContains(response, 'Praksa - Testiranje')

    def test_remove_job_ad_sa_razlogom(self):
        response = self.client.post(
            reverse('administration:remove_job_ad', args=[self.job_ad.id]),
            data = {'admin_note' : 'Neprimeren sadrzaj'}
        )

        self.assertEqual(response.status_code, 302)

        self.job_ad.refresh_from_db()
        self.assertEqual(self.job_ad.status, 'inactive')

    def test_keep_job_ad_active(self):
        response = self.client.post(
            reverse('administration:keep_job_ad_active', args=[self.job_ad.id])
        )

        self.assertEqual(response.status_code, 302)

        self.job_ad.refresh_from_db()
        self.assertEqual(self.job_ad.status, 'active')


class FunctionalTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.appUrl = self.live_server_url + reverse('administration:moderation')
        self.loginUrl = self.live_server_url + reverse('login')

        self.password = 'Test1234'
        User.objects.create(
            first_name='Ana', last_name='Admin', username='admin_test',
            email='admin_test@example.com', password=make_password(self.password),
            status='active', role='admin'
        )

        self.company = Company.objects.create(
            name='Aktivna Firma', username='aktivna_firma',
            email='aktivna@example.com', password=make_password('lozinka123'),
            status='active'
        )

        self.job_ad = JobAd.objects.create(
            company=self.company, name='Praksa - Testiranje',
            type='internship', status='pending'
        )

    def tearDown(self):
        self.browser.close()

    def test_oznacavanje_oglasa_kao_zastarelog(self):
        self.browser.get(self.loginUrl)

        username = self.browser.find_element(By.NAME, 'username')
        username.send_keys('admin_test')
        password = self.browser.find_element(By.NAME, 'password')
        password.send_keys(self.password)
        submit = self.browser.find_element(By.XPATH, '//input[@type="submit"]')
        submit.click()
        time.sleep(4)

        self.browser.get(self.appUrl + f'?ad={self.job_ad.id}')
        time.sleep(4)

        outdated = self.browser.find_element(By.XPATH, '//button[normalize-space(text())="Mark as outdated"]')
        self.browser.execute_script('arguments[0].scrollIntoView(true);', outdated)
        self.browser.execute_script('arguments[0].click();', outdated)
        time.sleep(4)

        self.job_ad.refresh_from_db()
        self.assertEqual(self.job_ad.status, 'inactive')