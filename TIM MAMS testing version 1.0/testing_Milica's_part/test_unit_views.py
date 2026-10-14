# Autor: Anastasija Ljubicic 0312/2023

from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Company, Administrator
from careers.models import Career, CareerSkill, JobAd
from django.contrib.auth.hashers import make_password



class TestDashboardView(TestCase):

    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create(
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

    def test_dashboard_neulogovan(self):
        self.client.get(reverse('logout_view'))

        response = self.client.get(reverse('administration:dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

    def test_dashboard_GET(self):
        response = self.client.get(reverse('administration:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['careers_count'], 0)


class TestCreateAccountView(TestCase):

    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create(
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

    def test_create_account_POST_kreira_korisnika(self):
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

    def test_create_account_POST_kreira_firmu(self):
        response = self.client.post(reverse('administration:create_account'), data = {
            'account_type' : 'company',
            'company-name' : 'Nova Firma',
            'company-username' : 'nova_firma',
            'company-email' : 'novafirma@example.com',
            'company-industry' : '',
            'company-contact' : '',
            'company-description' : '',
            'company-password' : 'Sifra1234',
            'company-password_confirm' : 'Sifra1234'
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Company.objects.filter(username='nova_firma').exists())

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


class TestCompanyRequestsViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create(
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

    def test_approve_company(self):
        response = self.client.post(
            reverse('administration:approve_company', args=[self.company.id])
        )

        self.company.refresh_from_db()
        self.assertEqual(self.company.status, 'active')

    def test_reject_company_bez_razloga(self):
        response = self.client.post(
            reverse('administration:reject_company', args=[self.company.id]),
            data = {'rejection_reason' : ''}
        )

        self.company.refresh_from_db()
        self.assertEqual(self.company.status, 'pending')

    def test_reject_company_sa_razlogom(self):
        response = self.client.post(
            reverse('administration:reject_company', args=[self.company.id]),
            data = {'rejection_reason' : 'Nepotpuna dokumentacija'}
        )

        self.company.refresh_from_db()
        self.assertEqual(self.company.status, 'rejected')

    def test_keep_company_pending(self):
        self.company.status = 'rejected'
        self.company.save()

        response = self.client.post(
            reverse('administration:keep_company_pending', args=[self.company.id])
        )
        self.company.refresh_from_db()
        self.assertEqual(self.company.status, 'pending')


class TestModerationViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create(
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

    def test_remove_job_ad_bez_razloga(self):
        response = self.client.post(
            reverse('administration:remove_job_ad', args=[self.job_ad.id]),
            data = {'admin_note' : ''}
        )

        self.job_ad.refresh_from_db()
        self.assertEqual(self.job_ad.status, 'pending')

    def test_remove_job_ad_sa_razlogom(self):
        response = self.client.post(
            reverse('administration:remove_job_ad', args=[self.job_ad.id]),
            data = {'admin_note' : 'Neprimeren sadrzaj'}
        )

        self.job_ad.refresh_from_db()
        self.assertEqual(self.job_ad.status, 'inactive')
        self.assertEqual(self.job_ad.removal_reason, 'Neprimeren sadrzaj')

    def test_mark_job_ad_outdated(self):
        response = self.client.post(
            reverse('administration:mark_job_ad_outdated', args=[self.job_ad.id]),
            data = {'admin_note' : ''}
        )

        self.job_ad.refresh_from_db()
        self.assertEqual(self.job_ad.status, 'inactive')
        self.assertEqual(self.job_ad.removal_reason, 'Outdated job ad.')

    def test_keep_job_ad_active(self):
        self.job_ad.status = 'inactive'
        self.job_ad.removal_reason = 'Outdated job ad.'
        self.job_ad.save()

        response = self.client.post(
            reverse('administration:keep_job_ad_active', args=[self.job_ad.id])
        )

        self.job_ad.refresh_from_db()
        self.assertEqual(self.job_ad.status, 'active')
        self.assertIsNone(self.job_ad.removal_reason)


class TestManageAccountsViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create(
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

    def test_update_user_account(self):
        response = self.client.post(
            reverse('administration:update_user_account', args=[self.user.id]),
            data = {
                'first_name' : 'Marko',
                'last_name' : 'Markovic',
                'email' : 'novi_marko@example.com',
                'username' : 'marko_user',
                'contact' : '0641234567'
            }
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'novi_marko@example.com')

    def test_update_user_account_prazna_obavezna_polja(self):
        response = self.client.post(
            reverse('administration:update_user_account', args=[self.user.id]),
            data = {
                'first_name' : '',
                'last_name' : 'Markovic',
                'email' : 'novi_marko@example.com',
                'username' : 'marko_user',
                'contact' : ''
            }
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'marko@example.com')

    def test_update_company_account(self):
        response = self.client.post(
            reverse('administration:update_company_account', args=[self.company.id]),
            data = {
                'name' : 'Izmenjena Firma',
                'email' : 'aktivna@example.com',
                'username' : 'aktivna_firma',
                'industry' : 'IT',
                'contact' : '',
                'description' : ''
            }
        )

        self.company.refresh_from_db()
        self.assertEqual(self.company.name, 'Izmenjena Firma')

    def test_change_user_role_na_admin(self):
        response = self.client.post(
            reverse('administration:change_user_role', args=[self.user.id]),
            data = {'new_role' : 'admin'}
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, 'admin')
        self.assertTrue(Administrator.objects.filter(user=self.user).exists())

    def test_change_user_role_ne_moze_sebi_da_ukine_admin(self):
        response = self.client.post(
            reverse('administration:change_user_role', args=[self.admin.id]),
            data = {'new_role' : 'user'}
        )

        self.admin.refresh_from_db()
        self.assertEqual(self.admin.role, 'admin')

    def test_delete_user_account(self):
        response = self.client.post(
            reverse('administration:delete_user_account', args=[self.user.id])
        )
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_delete_user_account_ne_moze_sam_sebe(self):
        response = self.client.post(
            reverse('administration:delete_user_account', args=[self.admin.id])
        )
        self.assertTrue(User.objects.filter(id=self.admin.id).exists())

    def test_delete_company_account(self):
        response = self.client.post(
            reverse('administration:delete_company_account', args=[self.company.id])
        )

        self.assertFalse(Company.objects.filter(id=self.company.id).exists())


class TestManageCareersViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create(
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

    def test_create_career(self):
        response = self.client.post(reverse('administration:create_career'), data = {
            'name' : 'Dizajner',
            'description' : 'Opis nove karijere',
            'skills' : 'Figma, Photoshop'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Career.objects.filter(name='Dizajner').exists())

    def test_create_career_bez_vestina(self):
        response = self.client.post(reverse('administration:create_career'), data = {
            'name' : 'Bez Vestina',
            'description' : 'Opis',
            'skills' : ''
        })

        self.assertFalse(Career.objects.filter(name='Bez Vestina').exists())

    def test_create_career_duplirano_ime(self):
        response = self.client.post(reverse('administration:create_career'), data = {
            'name' : 'Programer',
            'description' : 'Opis',
            'skills' : 'Python'
        })
        self.assertEqual(Career.objects.filter(name='Programer').count(), 1)

    def test_update_career(self):
        response = self.client.post(
            reverse('administration:update_career', args=[self.career.id]),
            data = {
                'name' : 'Programer',
                'description' : 'Izmenjen opis',
                'skills' : 'Python | 4 | 1.00'
            }
        )
        self.career.refresh_from_db()
        self.assertEqual(self.career.description, 'Izmenjen opis')
        self.assertTrue(CareerSkill.objects.filter(career=self.career).exists())

    def test_delete_career(self):
        response = self.client.post(
            reverse('administration:delete_career', args=[self.career.id])
        )

        self.assertFalse(Career.objects.filter(id=self.career.id).exists())