from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from accounts.models import User, Company


class Command(BaseCommand):
    help = "Populates the database with test users and companies for the accounts app (password for all: test1234)"

    def handle(self, *args, **options):
        users_data = [
            {
                "first_name": "Sofija",
                "last_name": "Nikolic",
                "username": "sofija_user",
                "email": "sofija.user@example.com",
                "contact": "060-111-1111",
                "status": "active",
                "role": "user",
            },
            {
                "first_name": "Marko",
                "last_name": "Markovic",
                "username": "marko_user",
                "email": "marko.user@example.com",
                "contact": "060-222-2222",
                "status": "active",
                "role": "user",
            },
            {
                "first_name": "Ana",
                "last_name": "Anic",
                "username": "ana_admin",
                "email": "ana.admin@example.com",
                "contact": "060-333-3333",
                "status": "active",
                "role": "admin",
            },
        ]

        companies_data = [
            {
                "name": "Nimbus Software",
                "username": "nimbus_company",
                "email": "contact@nimbus-software.example.com",
                "industry": "IT",
                "contact": "011-444-4444",
                "description": "A software development company.",
                "status": "active",
            },
            {
                "name": "DataForge Analytics",
                "username": "dataforge_company",
                "email": "contact@dataforge.example.com",
                "industry": "Data Science",
                "contact": "011-555-5555",
                "description": "A data analytics company.",
                "status": "pending",
            },
        ]

        created_users = 0
        for data in users_data:
            _, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    **data,
                    "password": make_password("test1234"),
                },
            )
            if created:
                created_users += 1

        created_companies = 0
        for data in companies_data:
            _, created = Company.objects.get_or_create(
                username=data["username"],
                defaults={
                    **data,
                    "password": make_password("test1234"),
                },
            )
            if created:
                created_companies += 1

        self.stdout.write(self.style.SUCCESS(
            f"Created {created_users} new users and {created_companies} new companies. "
            f"Password for all: test1234"
        ))
