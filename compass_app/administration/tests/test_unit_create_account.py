# Author: Anastasija Ljubicic 0312/2023

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from accounts.models import User


class TestCreateAccountLegalnaKlasa(TestCase):

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

    def test_lozinka_granica_tacno_8_karaktera(self):
        response = self.client.post(reverse('administration:create_account'), data = {
            'account_type' : 'user',
            'user-first_name' : 'Marko',
            'user-last_name' : 'Markovic',
            'user-username' : 'marko_8',
            'user-email' : 'marko8@example.com',
            'user-contact' : '',
            'user-password' : 'Sifra123',
            'user-password_confirm' : 'Sifra123'
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='marko_8').exists())


class TestCreateAccountNelegalneKlase(TestCase):

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

    def test_lozinka_kraca_od_8_karaktera(self):
        response = self.client.post(reverse('administration:create_account'), data = {
            'account_type' : 'user',
            'user-first_name' : 'Marko',
            'user-last_name' : 'Markovic',
            'user-username' : 'marko_7',
            'user-email' : 'marko7@example.com',
            'user-contact' : '',
            'user-password' : 'Sifra12',
            'user-password_confirm' : 'Sifra12'
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='marko_7').exists())

    def test_prazno_ime(self):
        response = self.client.post(reverse('administration:create_account'), data = {
            'account_type' : 'user',
            'user-first_name' : '',
            'user-last_name' : 'Markovic',
            'user-username' : 'marko_prazno',
            'user-email' : 'markoprazno@example.com',
            'user-contact' : '',
            'user-password' : 'Sifra1234',
            'user-password_confirm' : 'Sifra1234'
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='marko_prazno').exists())

    def test_lozinke_se_ne_poklapaju(self):
        response = self.client.post(reverse('administration:create_account'), data = {
            'account_type' : 'user',
            'user-first_name' : 'Marko',
            'user-last_name' : 'Markovic',
            'user-username' : 'marko_pass',
            'user-email' : 'markopass@example.com',
            'user-contact' : '',
            'user-password' : 'Sifra1234',
            'user-password_confirm' : 'Sifra9999'
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='marko_pass').exists())

    def test_korisnicko_ime_vec_zauzeto(self):
        User.objects.create(
            first_name='Petar', last_name='Petrovic', username='zauzeto',
            email='zauzeto@example.com', password=make_password('lozinka123'),
            status='active', role='user'
        )

        response = self.client.post(reverse('administration:create_account'), data = {
            'account_type' : 'user',
            'user-first_name' : 'Marko',
            'user-last_name' : 'Markovic',
            'user-username' : 'zauzeto',
            'user-email' : 'markozauzeto@example.com',
            'user-contact' : '',
            'user-password' : 'Sifra1234',
            'user-password_confirm' : 'Sifra1234'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username='zauzeto').count(), 1)

    def test_email_nije_validnog_formata(self):
        response = self.client.post(reverse('administration:create_account'), data = {
            'account_type' : 'user',
            'user-first_name' : 'Marko',
            'user-last_name' : 'Markovic',
            'user-username' : 'marko_email',
            'user-email' : 'nijeemail',
            'user-contact' : '',
            'user-password' : 'Sifra1234',
            'user-password_confirm' : 'Sifra1234'
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='marko_email').exists())

    def test_email_vec_registrovan(self):
        User.objects.create(
            first_name='Petar', last_name='Petrovic', username='petar_email',
            email='zauzet@example.com', password=make_password('lozinka123'),
            status='active', role='user'
        )
        response = self.client.post(reverse('administration:create_account'), data = {
            'account_type' : 'user',
            'user-first_name' : 'Marko',
            'user-last_name' : 'Markovic',
            'user-username' : 'marko_novi',
            'user-email' : 'zauzet@example.com',
            'user-contact' : '',
            'user-password' : 'Sifra1234',
            'user-password_confirm' : 'Sifra1234'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='marko_novi').exists())