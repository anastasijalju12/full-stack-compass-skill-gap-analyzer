DIJAGRAM SEKVENCE REALIZACIJE - PRIJAVA NA SISTEM (DUAL AUTHENTICATION)

Autor: Sofija Nikolić
Deo sistema: accounts app - login_view()
Projekat Kompas

OPIS
Dijagram prikazuje realizaciju scenarija prijave na sistem, koji podržava
dvostruku autentifikaciju (dual authentication) - isti login_view() proverava
prvo User tabelu (obični korisnici i administratori), a zatim Company tabelu
(firme), pošto se ne koristi Django-ov ugrađeni auth sistem već sopstvena
sesijska implementacija (request.session['role'], ['user_id'], ['company_id']).

OBUHVAĆENE GRANE
- forma nije validna (prazna polja) - ostaje na login.html sa greškama
- username pronađen u User tabeli, tačna lozinka - uspešan login (user/admin)
- username pronađen u User tabeli, pogrešna lozinka - greška
- username nije u User tabeli, pronađen u Company tabeli, tačna lozinka,
  status 'pending' - upozorenje, nalog još nije odobren
- isto, status 'rejected' - prikaz razloga odbijanja
- isto, status 'active' - uspešan login (company)
- username nije u User tabeli, pronađen u Company tabeli, pogrešna lozinka - greška
- username nije pronađen ni u jednoj tabeli - ista generička greška
  ("Incorrect username or password"), namerno bez otkrivanja da li username
  postoji (sigurnosna praksa, isti princip kao kod forgot_password_view)

FAJLOVI
- login_realizacija.puml - izvorni PlantUML kod dijagrama
- Prijava_dual_auth_realizacija.png - renderovana slika (PNG)
- Prijava_dual_auth_realizacija.svg - renderovana slika (SVG, vektorska)

NAPOMENA
Dijagram je izveden direktno iz stvarnog koda login_view() (accounts/views.py),
ne iz uopštenog/pretpostavljenog toka.
