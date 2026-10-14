KOMPAS – TESTIRANJE FUNKCIONALNOSTI

Tester: Milica Pavlović
Testirani deo: funkcionalnosti koje je implementirala Anastasija Ljubičić
Django aplikacija: careers

OBUHVAT TESTIRANJA

1. Favorites
- pristup stranici samo prijavljenom korisniku
- prikaz samo favorita trenutno prijavljenog korisnika
- prikaz omiljenih oglasa
- prikaz omiljenih karijera
- prebacivanje između tabova Job Ads i Careers
- dodavanje karijere u favorite
- uklanjanje karijere iz favorita
- uklanjanje i ponovno dodavanje oglasa u favorite
- ponašanje kada korisnik nema nijednu omiljenu stavku
- odbijanje neispravnog tipa favorita

2. Skill Match
- zabrana pristupa neprijavljenom korisniku
- prikaz dostupnih veština
- izbor veština i podešavanje nivoa znanja
- pokretanje analize
- izračunavanje procenata podudaranja
- sortiranje rezultata od najvećeg ka najmanjem procentu
- prikaz karijera i oglasa u rezultatima
- prikaz skill gap-a
- prikaz preporučenih resursa za nedostajuće veštine
- filtriranje rezultata samo na karijere
- dodavanje karijere u favorite iz rezultata analize

VRSTE TESTOVA

- 10 Django unit/integration testova
- 5 Selenium WebDriver UI testova
- ukupno 15 automatizovanih testova

POKRETANJE

Potrebno:
- aktivno Python virtuelno okruženje
- instaliran Django
- instaliran Selenium
- dostupan Google Chrome

Instalacija Selenium biblioteke:
python -m pip install selenium

Iz foldera compass_app pokrenuti sve testove:
python manage.py test careers.tests -v 2

Posebno pokretanje Django testova:
python manage.py test careers.tests.CareersUnitTests -v 2

Posebno pokretanje Selenium testova:
python manage.py test careers.tests.CareersSeleniumTests -v 2

OČEKIVANI REZULTAT

Ran 15 tests
OK

NAPOMENA

Django tokom testiranja pravi privremenu bazu test_kompas i po završetku je briše.
Testovi ne menjaju podatke iz glavne razvojne baze kompas.
Selenium testovi koriste Chrome u headless režimu, pa se prozor pregledača ne mora prikazati.