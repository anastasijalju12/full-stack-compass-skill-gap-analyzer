KOMPAS – TESTIRANJE FUNKCIONALNOSTI

Tester: Sofija Nikolić
Testirani deo: funkcionalnosti koje je implementirala Mina Ostojić
Django aplikacija: jobs

OBUHVAT TESTIRANJA

1. Prijava na oglas
- uspešna prijava registrovanog korisnika na aktuelan oglas
- prijava bez unosa opcione poruke za poslodavca
- korisnik je već prijavljen na dati oglas (sprečavanje duplikata)
- prijava bez ulogovanog korisnika
- prijava na nepostojeći oglas
- prikaz detalja karijere (career_details), uključujući nepostojeći career_id

2. Izmena aktuelnog oglasa
- uspešna izmena sopstvenog oglasa
- izmena nepostojećeg oglasa
- izmena oglasa koji ne pripada firmi koja je ulogovana

3. Brisanje aktuelnog oglasa
- uspešno brisanje sopstvenog oglasa
- brisanje nepostojećeg oglasa
- brisanje oglasa koji ne pripada firmi koja je ulogovana

4. Objavljivanje oglasa firme
- uspešno kreiranje oglasa sa svim obaveznim poljima
- kreiranje oglasa sa nazivom koji već postoji (sprečavanje duplikata)
- kreiranje oglasa bez obaveznog polja (tip angažmana)

5. Pregled zainteresovanih kandidata
- promena statusa prijave (accepted/denied)
- promena statusa preko AJAX zahteva
- odbijanje nedozvoljene vrednosti statusa
- označavanje kandidata kao favorita
- uklanjanje oznake favorita
- pokušaj favorizacije bez obaveznih parametara
- prikaz company_main, company_ads, careers, companies, job_ads_candidate_view

VRSTE TESTOVA
- 27 Django unit/integration testova
- 5 Selenium WebDriver UI testova
- ukupno 32 automatizovana testa

POKRETANJE

Potrebno:
- aktivno Python virtuelno okruženje
- instaliran Django
- instaliran Selenium
- dostupan Google Chrome
- ChromeDriver (verzija koja odgovara instaliranom Chrome-u) — podesiti
  putanju u CHROMEDRIVER_PATH na vrhu Selenium dela tests.py

Instalacija Selenium biblioteke:
py -m pip install selenium

Iz foldera compass_app pokrenuti sve testove:
py manage.py test jobs -v 2

Posebno pokretanje Django testova (bez Selenium dela):
py manage.py test jobs.tests.ApplyForJobTests jobs.tests.UpdateJobAdTests jobs.tests.DeleteJobAdTests jobs.tests.AddJobAdTests jobs.tests.ChangeApplicationStatusTests jobs.tests.ToggleFavoriteCandidateTests jobs.tests.CareerDetailsTests jobs.tests.CompanyAdsAndListingTests -v 2

Posebno pokretanje Selenium testova:
py manage.py test jobs.tests.JobsSeleniumTests -v 2

OČEKIVANI REZULTAT
Ran 32 tests
OK

NAPOMENA
Django tokom testiranja pravi privremenu bazu test_kompas i po završetku je briše.
Testovi ne menjaju podatke iz glavne razvojne baze kompas.
Testovi ne koriste Django-ov ugrađeni auth sistem — sesija se direktno
postavlja (session['company_id'] / session['user_id']), jer je tako
implementiran custom (dual) auth u accounts/jobs app-u. Isti princip se
koristi i za Selenium testove — Django sesija se kreira direktno u bazi, a
njen ključ se prenese Selenium browseru preko kolačića.
Selenium testovi koriste Chrome u headless režimu, pa se prozor pregledača ne mora prikazati.
CHROMEDRIVER_PATH u tests.py je podešen za Sofijin računar
(C:\Users\Lenovo\webdrivers\chromedriver.exe) — ko god pokreće Selenium
testove na svom računaru treba tu putanju da izmeni na svoju lokalnu lokaciju
chromedriver.exe.

NALAZI OTKRIVENI TESTIRANJEM (potvrđeno pokretanjem testova, ne pretpostavka)
Ovo su stvarni problemi u trenutnom kodu jobs/views.py, prijaviti Mini pre predaje:

1. toggle_favorite_candidate ima tvrdo ukucano "my_id = 1" (prava linija
   "#my_id = request.session['company_id']" je zakomentarisana), pa
   funkcionalnost favorita trenutno radi ispravno samo za firmu čiji je
   id=1 — za bilo koju drugu firmu puca sa JobAd.DoesNotExist (500 greška).
   Ovo je i eksperimentalno potvrđeno pri pokretanju testova. Tu su ostali
   i debug print() pozivi koje treba ukloniti pre predaje.
2. update_job_ad i delete_job_ad ne proveravaju da li oglas pripada
   ulogovanoj firmi — bilo koja firma trenutno može izmeniti ili obrisati
   tuđi oglas ako sazna ad_id.
3. Nema get_object_or_404 u update_job_ad, delete_job_ad i career_details —
   pozivi sa nepostojećim id-jem izazivaju 500 grešku umesto lepe 404 stranice.
4. Provera duplikata u add_job_ad gleda samo polje name, globalno za sve
   firme, ne kompletnu kombinaciju polja kao što SSU opisuje ("identičan oglas").
5. apply_for_job čita request.session['user_id'] direktno (bez .get()), pa
   neulogovan korisnik dobija 500 grešku umesto redirekta na login.

Poslednji test run (pre navedenih ispravki testa): Ran 27 tests, 24 prošlo,
2 errors (potvrđen nalaz #1) i 1 failure (pogrešna pretpostavka u testu,
description nije obavezno polje — ispravljeno, sada se testira "type").
