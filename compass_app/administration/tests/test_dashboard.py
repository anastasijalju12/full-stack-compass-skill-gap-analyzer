# Author: Anastasija Ljubicic 0312/2023

import time

from django.test import TestCase, Client, SimpleTestCase
from django.urls import resolve, reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.hashers import make_password
from accounts.models import User, Company
from careers.models import Career, JobAd
from administration.views import dashboard
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestUrls(SimpleTestCase):

    def test_dashboard_is_resolved(self):
        url = reverse('administration:dashboard')
        self.assertEqual(resolve(url).func, dashboard)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_dashboard_GET_neulogovan(self):
        response = self.client.get(reverse('administration:dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

    def test_dashboard_GET_ulogovan_kao_obican_korisnik(self):
        User.objects.create(
            first_name='Marko',
            last_name='Markovic',
            username='marko_user',
            email='marko@example.com',
            password=make_password('Lozinka123'),
            status='active',
            role='user',
        )

        self.client.post(reverse('login'), data={
            'username': 'marko_user',
            'password': 'Lozinka123',
        })

        response = self.client.get(reverse('administration:dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_login_admin_POST(self):
        User.objects.create(
            first_name='Ana',
            last_name='Admin',
            username='admin_test',
            email='admin_test@example.com',
            password=make_password('Test1234'),
            status='active',
            role='admin',
        )

        response = self.client.post(reverse('login'), data={
            'username': 'admin_test',
            'password': 'Test1234',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

class TestLoggedInCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create(
            first_name='Ana',
            last_name='Admin',
            username='admin_test',
            email='admin_test@example.com',
            password=make_password('Test1234'),
            status='active',
            role='admin',
        )
        self.client.post(reverse('login'), data={
            'username': 'admin_test',
            'password': 'Test1234',
        })

    def tearDown(self):
        self.client.get(reverse('logout_view'))

    def test_dashboard_GET(self):
        response = self.client.get(reverse('administration:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Administratorski panel', html=True)

    def test_dashboard_broj_zahteva_firmi_ispravan(self):
        Company.objects.create(
            name='Firma Na Cekanju',
            username='firma_cekanje',
            email='cekanje@example.com',
            password=make_password('lozinka123'),
            status='pending',
        )

        response = self.client.get(reverse('administration:dashboard'))

        self.assertContains(response, '<div class="statusNumber">\n                            1\n                        </div>', html=True)

    def test_dashboard_broj_karijera_ispravan(self):
        Career.objects.create(
            name='Test inzenjer',
            description='Opis karijere za testiranje.',
        )

        response = self.client.get(reverse('administration:dashboard'))

        self.assertEqual(response.context['careers_count'], 1)


class FunctionalTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.dashboardUrl = self.live_server_url + reverse('administration:dashboard')
        self.loginUrl = self.live_server_url + reverse('login')

        self.admin_password = 'Test1234'
        User.objects.create(
            first_name='Ana',
            last_name='Admin',
            username='admin_test',
            email='admin_test@example.com',
            password=make_password(self.admin_password),
            status='active',
            role='admin',
        )

        self.active_company = Company.objects.create(
            name='Aktivna Firma',
            username='aktivna_firma',
            email='aktivna@example.com',
            password=make_password('lozinka123'),
            status='active',
        )

    def tearDown(self):
        self.browser.close()

    def _js_click(self, element):
        self.browser.execute_script('arguments[0].click();', element)

    def test_dashboard_prikazuje_naslov_i_aktivan_link(self):
        self.browser.get(self.loginUrl)

        username = self.browser.find_element(By.NAME, 'username')
        username.send_keys('admin_test')
        password = self.browser.find_element(By.NAME, 'password')
        password.send_keys(self.admin_password)
        submit = self.browser.find_element(By.XPATH, '//input[@type="submit"]')
        submit.click()
        time.sleep(2)

        self.browser.get(self.dashboardUrl)
        time.sleep(2)

        naslov = self.browser.find_element(By.CSS_SELECTOR, '.page-header h1')
        self.assertEqual(naslov.text.strip(), 'Administratorski panel')

        aktivan_link = self.browser.find_element(By.CSS_SELECTOR, '.admin-subnav-link.active')
        self.assertEqual(aktivan_link.text.strip(), 'Admin panel')

    def test_klik_na_kreiranje_naloga_kartica_vodi_na_ispravnu_stranicu(self):
        self.browser.get(self.loginUrl)

        username = self.browser.find_element(By.NAME, 'username')
        username.send_keys('admin_test')
        password = self.browser.find_element(By.NAME, 'password')
        password.send_keys(self.admin_password)
        submit = self.browser.find_element(By.XPATH, '//input[@type="submit"]')
        submit.click()
        time.sleep(2)
        self.browser.get(self.dashboardUrl)
        time.sleep(2)

        kartica = self.browser.find_element(
            By.XPATH,
            '//div[contains(@class, "dashboardActionCard")]'
            '[.//div[@class="actionTitle" and normalize-space(text())="Kreiranje naloga"]]',
        )
        dugme = kartica.find_element(By.CSS_SELECTOR, '.actionBtn')
        self._js_click(dugme)
        time.sleep(2)

        self.assertIn(reverse('administration:create_account'), self.browser.current_url)