CD_03 – JOBS MODELI

Sadržaj:
- CD_03_Jobs.puml – editabilni PlantUML izvor
- CD_03_Jobs.svg – vektorski prikaz
- CD_03_Jobs.png – PNG prikaz
- CD_03_Jobs.dot – pomoćni Graphviz izvor
- README.txt – opis

Klase:
1. JobAd
2. JobAdSkill
3. Application
4. FavoriteJobAd
5. FavoriteCandidate
6. Company – spoljna referenca iz accounts aplikacije
7. User – spoljna referenca iz accounts aplikacije
8. Skill – spoljna referenca iz careers aplikacije

Prikazane veze:
- Company 1 — 0..* JobAd
- JobAd 1 — 0..* JobAdSkill
- Skill 1 — 0..* JobAdSkill
- User 1 — 0..* Application
- JobAd 1 — 0..* Application
- User 1 — 0..* FavoriteJobAd
- JobAd 1 — 0..* FavoriteJobAd
- Company 1 — 0..* FavoriteCandidate
- User 1 — 0..* FavoriteCandidate
- JobAd 1 — 0..* FavoriteCandidate

Posebna pravila:
- JobAdSkill je vezna klasa za odnos oglasa i potrebnih veština.
- required_level mora biti u opsegu od 1 do 5.
- Jedan korisnik može imati najviše jednu prijavu za isti oglas.
- FavoriteCandidate koristi složeni ključ company_id + user_id + job_ad_id.

Fizička lokacija modela u projektu:
- JobAd, JobAdSkill, Application i FavoriteJobAd:
  compass_app/careers/models.py
- FavoriteCandidate:
  compass_app/jobs/models.py

Modeli su prikazani zajedno u CD_03_Jobs zato što poslovno pripadaju
podsistemu oglasa, prijava i rada firme sa kandidatima.

Na samom dijagramu nema tekstualnog okvira sa napomenama, da sadržaj
ostane pregledan pri otvaranju PNG ili SVG fajla.
