CD_02 – CAREERS MODELI

Sadržaj:
- CD_02_Careers.puml – editabilni PlantUML izvor
- CD_02_Careers.svg – vektorski prikaz
- CD_02_Careers.png – PNG prikaz
- CD_02_Careers.dot – pomoćni Graphviz izvor
- README.txt – opis

Klase:
1. Career
2. Skill
3. CareerSkill
4. UserSkill
5. Resource
6. CareerProject
7. FavoriteCareer
8. User – spoljna referenca iz accounts aplikacije

Prikazane veze:
- Career 1 — 0..* CareerSkill
- Skill 1 — 0..* CareerSkill
- User 1 — 0..* UserSkill
- Skill 1 — 0..* UserSkill
- Skill 1 — 0..* Resource
- Career 1 — 0..* CareerProject
- User 1 — 0..* FavoriteCareer
- Career 1 — 0..* FavoriteCareer

CareerSkill je vezna klasa za M:N vezu između karijera i veština.
Pored stranih ključeva čuva potreban nivo od 1 do 5 i težinu veštine.

UserSkill je vezna klasa za M:N vezu između korisnika i veština.
Pored stranih ključeva čuva nivo znanja korisnika od 1 do 5.

Dijagram je napravljen prema stvarnim Django modelima iz:
compass_app/careers/models.py

Modeli JobAd, JobAdSkill, Application, FavoriteJobAd i FavoriteCandidate
nalaze se u istom models.py fajlu, ali će radi preglednosti biti prikazani
u posebnom dijagramu CD_03_Jobs.
