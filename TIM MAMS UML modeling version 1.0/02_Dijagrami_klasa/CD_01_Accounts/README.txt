CD_01 – ACCOUNTS MODELI

Sadržaj:
- CD_01_Accounts.puml – editabilni PlantUML izvor
- CD_01_Accounts.svg – vektorski prikaz
- CD_01_Accounts.png – PNG prikaz
- CD_01_Accounts.dot – pomoćni Graphviz izvor
- README.txt – opis

Klase:
1. User
2. Company
3. Administrator
4. Subscription
5. PasswordReset

Prikazane veze:
- User 1 — 0..* Administrator
- User 1 — 0..* Subscription
- Company 1 — 0..* Subscription
- User 1 — 0..* PasswordReset
- Company 1 — 0..* PasswordReset

Dijagram je napravljen prema stvarnim Django modelima iz:
compass_app/accounts/models.py

Važna napomena:
U modelu su polja user i company unutar Subscription i PasswordReset opcionalna.
Poslovno pravilo je da konkretan zapis pripada odgovarajućem tipu naloga.

Administrator je fizički definisan u accounts/models.py, iako se njegove
administratorske funkcionalnosti realizuju u aplikaciji administration.
