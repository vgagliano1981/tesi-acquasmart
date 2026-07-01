# Relazione di Progetto: Piattaforma IoT per il Monitoraggio Idrico

**Studente:** Vito Gagliano  
**Relatore:** Prof. Kuznetsov  
**Progetto:** Progettazione e sviluppo di una piattaforma IoT per il monitoraggio e l'analisi dei consumi idrici negli edifici pubblici (Città Metropolitana di Catania).  

---

## 1. Panoramica del Progetto
Il progetto consiste in una piattaforma web completa pensata per monitorare in tempo reale i consumi di acqua all'interno degli istituti scolastici della Città Metropolitana di Catania. L'obiettivo principale è fornire uno strumento semplice ma efficace per individuare sprechi, perdite occulte e anomalie, confrontando i dati raccolti dai sensori con i consumi reali fatturati nelle bollette. 

Per rendere il sistema il più realistico possibile, ho sviluppato un simulatore che genera costantemente dati verosimili per ogni scuola, imitando il comportamento di veri contatori intelligenti (smart meter).

## 2. Funzionamento dei Sensori e Protocollo MQTT
Per la trasmissione dei dati dai contatori alla piattaforma, ho scelto di utilizzare il **protocollo MQTT**. 
Si tratta di un sistema di comunicazione molto leggero e veloce, diventato lo standard mondiale per l'Internet of Things (IoT). Funziona con un meccanismo di "pubblicazione e iscrizione": 
1. I **sensori** (nel nostro caso simulati dal software) leggono la quantità d'acqua che scorre nei tubi e "pubblicano" questo dato su un canale specifico (chiamato *topic*).
2. Il **server centrale** è "iscritto" a questi canali: non appena un sensore invia un nuovo dato, il server lo riceve istantaneamente, lo analizza per capire se ci sono anomalie (come un consumo eccessivo di notte, tipico di un tubo rotto) e lo salva nel database.

Questo approccio permette di avere grafici aggiornati in tempo reale sulla dashboard senza appesantire la rete.

## 3. Sistema di Accesso: Amministratore e Guest
Trattandosi di una piattaforma che gestisce dati sensibili (come le anagrafiche delle scuole e i consumi fatturati), ho implementato un sistema di **Login sicuro** basato su ruoli. 

Ho creato due tipologie di utenti:
- **Amministratore:** Ha il controllo totale della piattaforma. Può aggiungere nuove scuole, installare nuovi sensori, eliminare dati vecchi e gestire gli accessi di altre persone.
- **Guest (Ospite):** Ha un accesso limitato in "sola lettura". È un ruolo pensato, ad esempio, per un dipendente scolastico o un cittadino a cui vogliamo mostrare i consumi senza però dargli il potere di modificare o cancellare i dati dell'impianto.

La differenziazione dei ruoli impedisce modifiche accidentali o non autorizzate, garantendo l'integrità del database.

## 4. Guida alle Pagine del Sito
Una volta effettuato l'accesso, la piattaforma è divisa in diverse sezioni. L'interfaccia si adatta dinamicamente in base a chi sta guardando lo schermo:

- **Pagina di Login:** È la porta d'ingresso. Mostra il logo della Città Metropolitana e richiede le credenziali. Nessuno può vedere i dati senza aver prima fatto l'accesso.
- **Dashboard:** È il cuore operativo. Mostra un grafico in tempo reale dei consumi d'acqua. Sia l'Amministratore che il Guest possono vedere l'andamento dei litri d'acqua consumati e usare il cursore per andare indietro nel tempo e rivedere i dati storici.
- **Storico Allarmi:** Un registro dove vengono salvate tutte le anomalie rilevate (es. consumo fuori norma). Entrambi gli utenti possono consultare questa lista per capire quando e dove si è verificata una perdita.
- **Gestione Anagrafe:** Questa è la rubrica degli edifici. 
  - *Se sei Guest:* Puoi solo scorrere la lista delle scuole e vedere quanti sensori hanno. I tasti per eliminare o aggiungere sensori sono nascosti.
  - *Se sei Amministratore:* Compaiono i tasti per aggiungere un nuovo plesso scolastico, installare un nuovo contatore (il sistema genererà subito un nuovo flusso di dati MQTT per quel sensore) o eliminare una scuola dal database.
- **Inserimento Dati Reali:** Permette di inserire a mano i dati delle bollette cartacee e salvarli nel database. Lo scopo è creare un registro storico per confrontare i "Totale Fatturati" (bolletta) con le stime dei sensori. Entrambi gli utenti possono consultare le bollette registrate in un comodo elenco diviso per pagine.
- **Gestione Utenti:** Questa pagina è **completamente invisibile** per l'utente Guest. Solo l'Amministratore può vederla e usarla per creare nuovi account, scegliendo username, password e ruolo, oppure per revocare l'accesso eliminando un utente esistente.

## 5. Riferimenti per il Test della Piattaforma

Il progetto è attualmente online e testabile da qualsiasi dispositivo connesso a internet.

- **Indirizzo del sito:** [https://tesi-acquasmart.onrender.com/](https://tesi-acquasmart.onrender.com/)

**Credenziali di accesso preimpostate:**

*Accesso come Amministratore (Controllo completo)*
- **Username:** `amministratore`
- **Password:** `amministratore`

*Accesso come Guest (Sola visualizzazione)*
- **Username:** `guest`
- **Password:** `guest`
