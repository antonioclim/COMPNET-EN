# Scenario FTP – control vs data

## Obiectiv
Înțelegerea modului de funcționare FTP prin observarea separării dintre:
- conexiunea de control
- conexiunea de date

## Ce se întâmplă
- rulează un server FTP real (pyftpdlib)
- un client FTP Python se conectează
- se execută LIST, STOR, RETR
- se compară mod pasiv vs activ

## Ce trebuie observat
- porturile folosite
- când apar conexiunile de date
- diferența dintre PASV și PORT

## Rulare
docker compose up --build

## Întrebări
- De ce există două conexiuni?
- De ce active mode e problematic?
