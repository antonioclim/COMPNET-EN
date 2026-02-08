### Introducere

În această etapă vom explora trei utilitare de bază disponibile în aproape orice sistem de operare: `ping`, `netstat` și `nslookup`. Scopul lor este să ofere vizibilitate asupra conectivității, stării conexiunilor și procesului de rezolvare DNS. Aceste instrumente sunt fundamentale pentru orice activitate de analiză de rețea.

---

### Explorarea comenzilor

#### 1. Verificarea conectivității cu `ping`

```
ping -c 4 google.com
```

#### 2. Afișarea conexiunilor și porturilor cu `netstat`

##### A. Afișarea conexiunilor și porturilor cu `netstat` sub linux/unix
```
netstat -tulnp
```
##### B. Afișarea conexiunilor și porturilor cu `Get-NetTCPConnection` & ~Get-NetUDPEndpoint~ sub Windows
```
$(Get-NetTCPConnection -State Listen; Get-NetUDPEndpoint) | 
Select-Object LocalAddress, LocalPort, OwningProcess, 
    @{Name="ProcessName";Expression={(Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue).Name}}, 
    @{Name="Protocol";Expression={if($_.CreationTime){"TCP"}else{"UDP"}}} | 
Sort-Object LocalAddress, LocalPort | 
Format-Table -Property LocalPort, Protocol, ProcessName, OwningProcess -GroupBy LocalAddress
```

```
netstat --tcp --udp --listening --program --numeric
```

#### 3. Interogarea DNS cu `nslookup`

```
nslookup google.com
```

---

### Observații

Notă că:

* `ping` verifică dacă un host răspunde și oferă timpi de latență. Dacă rezolvarea adresei prin DNS funcționează, numele va fi transformat automat în adresă IP. Dacă nu, `ping` poate eșua încă înainte de trimiterea ICMP.
* `netstat` îți arată ce porturi sunt ascultate și ce conexiuni sunt deschise. Opțiunea `-tulnp` combină TCP, UDP, listening sockets și numele proceselor care le folosesc.
* `nslookup` permite diagnosticarea problemelor DNS: poți vedea serverul DNS folosit, adresele IP ale domeniului și eventualele erori de rezoluție.
