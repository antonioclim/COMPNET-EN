# Scenario SSH – provisionare simplă

## Obiectiv
Utilizarea SSH ca mecanism general de control și automatizare.

## Ce se întâmplă
- un controller Python citește un plan JSON
- se conectează prin SSH
- execută comenzi
- transferă fișiere

## Ce trebuie observat
- SSH ca protocol de control
- canale multiple peste o conexiune
- similaritatea cu unelte DevOps reale

## Rulare
docker compose up --build

## Discuție
- ce face SSH atât de versatil
- de ce multe unelte se bazează pe SSH
