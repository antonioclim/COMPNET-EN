### Exercițiu

Realizați următorul mini-scenariu pentru a demonstra înțelegerea diferențelor TCP/UDP:

1. Porniți un server TCP pe portul **9100**. Conectați un client și trimiteți:
   * un mesaj scurt,
   * apoi un mesaj cu mai multe linii.
2. Porniți un server UDP pe portul **9101**. Trimiteți două mesaje distincte folosind comenzi separate.
3. Comparați comportamentul:
   * Ce se întâmplă în TCP dacă țineți conexiunea deschisă?
   * Ce se întâmplă în UDP dacă serverul este pornit după trimiterea unui mesaj?

**Dovadă necesară**
Creați fișierul `netcat_activity_output.txt` care trebuie să conțină:

* comenzile folosite,
* outputul terminalului pentru TCP,
* outputul terminalului pentru UDP,
* o scurtă comparație (3–5 propoziții) între comportamentul TCP și UDP observat în exercițiu.

Fișierul va fi încărcat ulterior ca dovadă de finalizare.
