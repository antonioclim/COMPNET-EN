# Scenario FTP – NAT și firewall

## Obiectiv
Înțelegerea limitărilor FTP în rețele moderne cu NAT și firewall.

## Ce se întâmplă
- clientul comunică cu serverul FTP printr-un NAT
- se testează active vs passive
- se observă unde și de ce pot apărea blocaje

## Ce trebuie observat
- cine inițiază conexiunea de date
- ce porturi sunt folosite
- de ce passive mode este preferat

## Rulare
docker compose up --build

## Discuție
- de ce FTP este dificil de securizat
- de ce SFTP/HTTPS sunt preferate
