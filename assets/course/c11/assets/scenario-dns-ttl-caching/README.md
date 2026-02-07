# Scenario DNS – TTL și caching

## Obiectiv
Observarea mecanismului de caching DNS și a efectului TTL.

## Ce se întâmplă
- un resolver recursiv interoghează un server authoritative
- răspunsurile sunt cache-uite
- zona DNS este modificată

## Ce trebuie observat
- când apare noul IP
- cum influențează TTL propagarea

## Rulare
docker compose up --build

## Întrebări
- de ce DNS nu este “instant”
- ce compromis face TTL
