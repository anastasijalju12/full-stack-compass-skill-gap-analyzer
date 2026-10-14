from django.core.management.base import BaseCommand
from careers.models import (
    Vestina, Karijera, KarijeraVestina,
    Resurs, ProjekatZanimanje
)


class Command(BaseCommand):
    help = 'Puni tabele careers app-a početnim podacima'

    def handle(self, *args, **options):
        self.stdout.write('Brišem stare podatke...')
        ProjekatZanimanje.objects.all().delete()
        Resurs.objects.all().delete()
        KarijeraVestina.objects.all().delete()
        Karijera.objects.all().delete()
        Vestina.objects.all().delete()

        self.seed_vestine()
        self.seed_karijere()
        self.seed_karijera_vestina()
        self.seed_resursi()
        self.seed_projekti()

        self.stdout.write(self.style.SUCCESS('\nSeed uspešno završen!'))

    # ------------------------------------------------------------------
    # SKILLS
    # ------------------------------------------------------------------
    def seed_vestine(self):
        vestine = [
            ('HTML',         'Markup jezik za strukturu web stranica'),
            ('CSS',          'Stilizovanje i layout web stranica'),
            ('JavaScript',   'Programski jezik za frontend i backend'),
            ('TypeScript',   'JavaScript sa statičkim tipovima'),
            ('React',        'JavaScript biblioteka za UI komponente'),
            ('Node.js',      'JavaScript runtime za server-side programiranje'),
            ('Python',       'Višenamjenski jezik, popularan u data science i backend-u'),
            ('Django',       'Python web framework za brzi razvoj aplikacija'),
            ('Java',         'Objektno-orijentisani programski jezik'),
            ('SQL',          'Jezik za upravljanje relacionim bazama podataka'),
            ('MySQL',        'Relacioni sistem za upravljanje bazom podataka'),
            ('MongoDB',      'NoSQL baza podataka'),
            ('Git',          'Sistem za kontrolu verzija koda'),
            ('Docker',       'Platforma za kontejnerizaciju aplikacija'),
            ('Linux',        'Operativni sistem koji se koristi na serverima'),
            ('Figma',        'Alat za dizajn korisničkih interfejsa'),
            ('Kotlin',       'Programski jezik za Android razvoj'),
            ('React Native', 'Framework za mobilne aplikacije (iOS i Android)'),
            ('Excel',        'Alat za tabelarnu analizu podataka'),
            ('C++',          'Sistemski programski jezik visokih performansi'),
        ]
        for naziv, opis in vestine:
            Vestina.objects.get_or_create(naziv=naziv, defaults={'opis': opis})
        self.stdout.write('  ✓ Veštine (20)')

    # ------------------------------------------------------------------
    # CAREERS
    # ------------------------------------------------------------------
    def seed_karijere(self):
        karijere = [
            (
                'Frontend Developer',
                'Razvija korisnički interfejs web aplikacija '
                'koristeći HTML, CSS i JavaScript.'
            ),
            (
                'Backend Developer',
                'Razvija serversku logiku, baze podataka i '
                'API-je za web i mobilne aplikacije.'
            ),
            (
                'Web Developer',
                'Radi i na frontendu i na backendu — odgovoran '
                'za ceo web projekat od interfejsa do servera.'
            ),
            (
                'Web Designer',
                'Osmišljava vizuelni izgled i korisničko iskustvo '
                'web stranica, od rasporeda do tipografije.'
            ),
            (
                'Mobile Developer',
                'Razvija aplikacije za Android i iOS platforme, '
                'nativno ili cross-platform rešenjima.'
            ),
            (
                'Data Analyst',
                'Analizira skupove podataka, otkriva obrasce i '
                'donosi poslovne uvide kroz vizualizacije i izveštaje.'
            ),
            (
                'DevOps Engineer',
                'Automatizuje razvoj, testiranje i deployment procesa; '
                'upravlja serverskom infrastrukturom i CI/CD pipeline-ima.'
            ),
        ]
        for naziv, opis in karijere:
            Karijera.objects.get_or_create(naziv=naziv, defaults={'opis': opis})
        self.stdout.write('  ✓ Karijere (7)')

    # ------------------------------------------------------------------
    # CAREER–SKILL links  (career, skill, required_level 1-5, weight)
    # weight shows how much the skill affects the match %
    # ------------------------------------------------------------------
    def seed_karijera_vestina(self):
        mappings = [
            # Frontend Developer
            ('Frontend Developer', 'HTML',       4, 0.20),
            ('Frontend Developer', 'CSS',        4, 0.20),
            ('Frontend Developer', 'JavaScript', 4, 0.25),
            ('Frontend Developer', 'React',      3, 0.20),
            ('Frontend Developer', 'Git',        2, 0.10),
            ('Frontend Developer', 'Figma',      2, 0.05),

            # Backend Developer
            ('Backend Developer',  'Python',  4, 0.20),
            ('Backend Developer',  'Django',  3, 0.20),
            ('Backend Developer',  'SQL',     4, 0.20),
            ('Backend Developer',  'MySQL',   3, 0.15),
            ('Backend Developer',  'Git',     3, 0.10),
            ('Backend Developer',  'Docker',  2, 0.10),
            ('Backend Developer',  'Java',    2, 0.05),

            # Web Developer
            ('Web Developer', 'HTML',       3, 0.15),
            ('Web Developer', 'CSS',        3, 0.10),
            ('Web Developer', 'JavaScript', 4, 0.25),
            ('Web Developer', 'React',      3, 0.15),
            ('Web Developer', 'Node.js',    3, 0.15),
            ('Web Developer', 'SQL',        2, 0.10),
            ('Web Developer', 'Git',        3, 0.10),

            # Web Designer
            ('Web Designer', 'Figma',      5, 0.40),
            ('Web Designer', 'CSS',        4, 0.30),
            ('Web Designer', 'HTML',       3, 0.20),
            ('Web Designer', 'JavaScript', 2, 0.10),

            # Mobile Developer
            ('Mobile Developer', 'Kotlin',       4, 0.35),
            ('Mobile Developer', 'Java',         3, 0.20),
            ('Mobile Developer', 'React Native', 3, 0.30),
            ('Mobile Developer', 'Git',          2, 0.15),

            # Data Analyst
            ('Data Analyst', 'Python',  3, 0.30),
            ('Data Analyst', 'SQL',     4, 0.35),
            ('Data Analyst', 'Excel',   4, 0.20),
            ('Data Analyst', 'MongoDB', 2, 0.15),

            # DevOps Engineer
            ('DevOps Engineer', 'Docker', 4, 0.30),
            ('DevOps Engineer', 'Linux',  4, 0.30),
            ('DevOps Engineer', 'Git',    4, 0.20),
            ('DevOps Engineer', 'Python', 3, 0.15),
            ('DevOps Engineer', 'MySQL',  2, 0.05),
        ]

        count = 0
        for kar_naziv, ves_naziv, nivo, tezina in mappings:
            try:
                k = Karijera.objects.get(naziv=kar_naziv)
                v = Vestina.objects.get(naziv=ves_naziv)
                KarijeraVestina.objects.get_or_create(
                    karijera=k,
                    vestina=v,
                    defaults={'potreban_nivo': nivo, 'tezina': tezina}
                )
                count += 1
            except (Karijera.DoesNotExist, Vestina.DoesNotExist) as e:
                self.stdout.write(self.style.WARNING(f'    Preskočeno: {e}'))

        self.stdout.write(f'  ✓ Karijera–veština veze ({count})')

    # ------------------------------------------------------------------
    # RESOURCES  (skill, name, url, level)
    # ------------------------------------------------------------------
    def seed_resursi(self):
        resursi = [
            # HTML
            ('HTML', 'MDN Web Docs – HTML osnove',
             'https://developer.mozilla.org/en-US/docs/Web/HTML', 'pocetni'),
            ('HTML', 'freeCodeCamp – Responsive Web Design',
             'https://www.freecodecamp.org/learn/responsive-web-design/', 'pocetni'),

            # CSS
            ('CSS', 'CSS-Tricks – kompletan vodič',
             'https://css-tricks.com/snippets/css/complete-guide-grid/', 'srednji'),
            ('CSS', 'Flexbox Froggy – učenje kroz igru',
             'https://flexboxfroggy.com', 'pocetni'),

            # JavaScript
            ('JavaScript', 'javascript.info – moderni JS',
             'https://javascript.info', 'pocetni'),
            ('JavaScript', 'The Odin Project – JavaScript kurs',
             'https://www.theodinproject.com/paths/full-stack-javascript', 'srednji'),

            # TypeScript
            ('TypeScript', 'TypeScript zvanična dokumentacija',
             'https://www.typescriptlang.org/docs/', 'srednji'),

            # React
            ('React', 'React zvanična dokumentacija',
             'https://react.dev', 'srednji'),
            ('React', 'Scrimba – Learn React besplatno',
             'https://scrimba.com/learn/learnreact', 'pocetni'),

            # Python
            ('Python', 'Python.org – zvanična dokumentacija',
             'https://docs.python.org/3/', 'pocetni'),
            ('Python', 'Real Python – praktični tutorijali',
             'https://realpython.com', 'srednji'),

            # Django
            ('Django', 'Zvanična Django dokumentacija',
             'https://docs.djangoproject.com', 'srednji'),
            ('Django', 'Django Girls Tutorial',
             'https://tutorial.djangogirls.org', 'pocetni'),

            # SQL
            ('SQL', 'SQLZoo – interaktivni SQL',
             'https://sqlzoo.net', 'pocetni'),
            ('SQL', 'Mode SQL Tutorial',
             'https://mode.com/sql-tutorial/', 'srednji'),

            # MySQL
            ('MySQL', 'MySQL zvanična dokumentacija',
             'https://dev.mysql.com/doc/', 'srednji'),

            # Git
            ('Git', 'Pro Git knjiga (besplatna)',
             'https://git-scm.com/book/en/v2', 'pocetni'),
            ('Git', 'Learn Git Branching – vizuelno',
             'https://learngitbranching.js.org', 'pocetni'),

            # Docker
            ('Docker', 'Docker Getting Started',
             'https://docs.docker.com/get-started/', 'pocetni'),
            ('Docker', 'Play with Docker – online sandbox',
             'https://labs.play-with-docker.com', 'srednji'),

            # Linux
            ('Linux', 'The Linux Command Line (besplatna knjiga)',
             'https://linuxcommand.org/tlcl.php', 'pocetni'),
            ('Linux', 'OverTheWire – Bandit (wargame za učenje)',
             'https://overthewire.org/wargames/bandit/', 'srednji'),

            # Figma
            ('Figma', 'Figma Learn – zvanični kurs',
             'https://help.figma.com/hc/en-us/articles/360038510773', 'pocetni'),
            ('Figma', 'Designcode.io – UI/UX sa Figmom',
             'https://designcode.io', 'srednji'),

            # Kotlin
            ('Kotlin', 'Kotlin Koans – interaktivni zadaci',
             'https://kotlinlang.org/docs/koans.html', 'pocetni'),
            ('Kotlin', 'Android Developers – Kotlin kurs',
             'https://developer.android.com/kotlin', 'srednji'),

            # React Native
            ('React Native', 'React Native zvanična dokumentacija',
             'https://reactnative.dev/docs/getting-started', 'pocetni'),

            # Excel
            ('Excel', 'Microsoft Excel – zvanična podrška',
             'https://support.microsoft.com/en-us/excel', 'pocetni'),
            ('Excel', 'ExcelJet – formule i trikovi',
             'https://exceljet.net', 'srednji'),
        ]

        count = 0
        for ves_naziv, naziv, url, nivo in resursi:
            try:
                v = Vestina.objects.get(naziv=ves_naziv)
                Resurs.objects.get_or_create(
                    vestina=v,
                    naziv=naziv,
                    defaults={'url': url, 'nivo': nivo}
                )
                count += 1
            except Vestina.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'    Veština ne postoji: {ves_naziv}'))

        self.stdout.write(f'  ✓ Resursi ({count})')

    # ------------------------------------------------------------------
    # PROJECTS PER CAREER
    # ------------------------------------------------------------------
    def seed_projekti(self):
        projekti = [
            # Frontend Developer
            ('Frontend Developer', 'Portfolio sajt',
             'Napravi lični portfolio sa sekcijama: O meni, Projekti, Kontakt. '
             'Responsive dizajn, CSS animacije, bez framework-a.',
             'pocetni', None),
            ('Frontend Developer', 'Todo aplikacija sa React-om',
             'Todo app sa dodavanjem, brisanjem i označavanjem zadataka. '
             'Koristi useState i useEffect, podaci se čuvaju u localStorage.',
             'srednji', None),

            # Backend Developer
            ('Backend Developer', 'REST API za blog',
             'Django REST API sa CRUD operacijama za postove i komentare. '
             'Autentifikacija tokenom, paginacija, filtriranje po kategoriji.',
             'srednji', None),
            ('Backend Developer', 'Sistem za autentifikaciju',
             'Registracija, login, logout i reset lozinke u Djangu. '
             'Koristi Django auth sistem, email potvrda, session management.',
             'pocetni', None),

            # Web Developer
            ('Web Developer', 'Aplikacija za ankete',
             'Full-stack app: korisnik kreira anketu, drugi glasaju, '
             'rezultati se prikazuju grafički. Django backend + JavaScript frontend.',
             'srednji', None),
            ('Web Developer', 'E-commerce prototip',
             'Prodavnica sa listom proizvoda, pretragom, korpom i '
             'simulacijom plaćanja. Django + React ili plain JS.',
             'napredni', None),

            # Web Designer
            ('Web Designer', 'Redesign poznatog sajta u Figmi',
             'Odaberi sajt sa lošim UX-om, analiziraj probleme i '
             'uradi kompletan redesign u Figmi sa mobile i desktop verzijom.',
             'pocetni', None),
            ('Web Designer', 'Design sistem sa komponentama',
             'Napravi konzistentni design sistem u Figmi: tipografija, boje, '
             'ikonografija i set UI komponenti (dugmad, forme, kartice).',
             'srednji', None),

            # Mobile Developer
            ('Mobile Developer', 'Android kalkulator',
             'Kalkulator aplikacija u Kotlinu sa osnovnim operacijama. '
             'Rukovanje greškama (deljenje nulom), landscape i portrait mod.',
             'pocetni', None),
            ('Mobile Developer', 'Aplikacija za praćenje navika',
             'Mobilna app za kreiranje navika, svakodnevno označavanje '
             'i prikaz streak-a. Room baza podataka, RecyclerView.',
             'srednji', None),

            # Data Analyst
            ('Data Analyst', 'Analiza prodajnih podataka',
             'Preuzmi javni CSV dataset prodaje, očisti podatke u pandas-u '
             'i napravi vizualizacije (matplotlib/seaborn): trendovi, top proizvodi.',
             'pocetni', None),
            ('Data Analyst', 'COVID-19 trend analiza',
             'Koristi javne COVID podatke (Our World in Data), '
             'analiziraj trendove po državama i napravi interaktivni dashboard.',
             'srednji', None),

            # DevOps Engineer
            ('DevOps Engineer', 'Dockerizacija Django aplikacije',
             'Uzmi Django projekat i napravi Dockerfile + docker-compose.yml '
             'sa web serverom (nginx) i bazom (MySQL). Pokreni sve jednom komandom.',
             'pocetni', None),
            ('DevOps Engineer', 'CI/CD pipeline sa GitHub Actions',
             'Postavi GitHub Actions workflow koji automatski pokreće testove '
             'pri svakom push-u i deploye na server pri merge-u u main.',
             'napredni', None),
        ]

        count = 0
        for kar_naziv, naziv, opis, nivo, fajl_path in projekti:
            try:
                k = Karijera.objects.get(naziv=kar_naziv)
                ProjekatZanimanje.objects.get_or_create(
                    karijera=k,
                    naziv=naziv,
                    defaults={'opis': opis, 'nivo': nivo, 'fajl_path': fajl_path}
                )
                count += 1
            except Karijera.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'    Karijera ne postoji: {kar_naziv}'))

        self.stdout.write(f'  ✓ Projekti ({count})')