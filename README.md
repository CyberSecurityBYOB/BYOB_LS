# Python Botnet 

##Requisiti progetto: 
###A.2. Build Your Own Botnet v. 1(Giovanni Bottazzi).
Si sviluppi un software per workstation (no mobile) [9].
####Obiettivo principale
1. Il software deve essere in grado di contattare (http GET) una o più URL
INTERNET. 
2. Per ciascuna URL bisogna prevedere una serie di variabili:

  2. dettaglio delle URL da contattare (minimo 2 diverse);
  3. periodicità di contatto, che può essere fissa (tempo impostato in secondi)
o random in un intervallo min-max fisso (tempo sempre impostato in
secondi);
  3. numero massimo di contatti per ciascuna URL;
  4. impostazione di uno “sleep mode”, da intendere come insieme di
condizioni per non effettuare alcuna azione (es. giorni dispari della
settimana, orario AM o PM, ecc.);
  5. personalizzazione del campo user-agent (es.: “BYOB v. 1”).

6. I valori delle variabili dovranno essere impostati attraverso un file (txt) di
configurazione.
7. I contatti ed i parametri di configurazione dovranno esser loggati in un file di
testo contenente, oltre alle informazioni di configurazione, anche il timestamp di
contatto delle URL ed il dettaglio delle URL contattate.



8. [Estensione] Le variabili precedenti dovranno essere impostate dall’utente tramite GUI.
9. [Estensione] Aggiungere inoltre tra le variabili impostabili anche l’indirizzo di un proxy
pubblico (URL o IP) da usare per i contatti.
10. [Estensioni] Raccogliere e scrivere su un file TXT le informazioni relative al Sistema
Operativo e al/i browser presenti sulla postazione su cui il software è installato.

11. [NostraEstensione] Gestire l'introduzione di url malformati
12. [NostraEstensione] Rendere la BotNet eseguibile in ambienti senza interprete Python
13. [NostraEstensione] Gestire la configurazione di default dei campi non immessi di ogni botnet
