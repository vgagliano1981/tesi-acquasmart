# Introduzione

## 1.1 Contesto e Motivazioni
La progressione evolutiva delle tecnologie digitali ha determinato un sostanziale cambiamento nei processi produttivi, organizzativi e sociali, favorendo l'affermazione di nuovi modelli basati sull’automazione e sulla condivisione intelligente delle informazioni. In tale contesto, l’Internet of Things (IoT) [1] costituisce l’infrastruttura portante per la transizione digitale degli ambienti fisici. Attraverso l'integrazione di sensori e dispositivi intelligenti negli oggetti di uso quotidiano e negli impianti industriali, l'IoT consente di raccogliere e gestire un’enorme quantità di dati in tempo reale, abilitando paradigmi gestionali innovativi.

Grazie allo *Smart Building Management* [2] è possibile ottimizzare in modo autonomo le prestazioni energetiche di un edificio civile o industriale. Se nel settore privato questa evoluzione risulta ormai consolidata, nella Pubblica Amministrazione (PA) italiana la transizione verso modelli intelligenti appare ancora frammentata o del tutto assente. Eppure, direttive europee sull’efficienza energetica e strumenti programmatici quali il PNRR [3] e il Codice dell’Amministrazione Digitale impongono alle PA un radicale e tempestivo rinnovamento.

All'interno di questo scenario orientato all'ottimizzazione dei consumi energetici globali degli edifici pubblici (come indicato dal titolo della presente tesi), il monitoraggio e la gestione delle risorse idriche si inseriscono come un caso applicativo specifico e di prioritaria importanza. In territori caratterizzati da frequenti e prolungate carenze di acqua potabile, la riduzione delle dispersioni idriche è fondamentale non solo per mitigare una criticità ambientale oggettiva, ma anche per limitare danni economici significativi. Implementare un sistema IoT negli edifici pubblici permette di superare le logiche di manutenzione reattiva in favore di un modello predittivo e guidato dai dati (*data-driven*) [4].

L’ideazione e la progettazione del sistema presentato in questo elaborato non rappresentano un mero esercizio accademico, bensì nascono da un’esigenza operativa concreta, riscontrata in risposta alle criticità gestionali rilevate dalla Direzione Patrimonio e Politiche Scolastiche della Città Metropolitana di Catania [5]. L’Ente gestisce la manutenzione (ordinaria e straordinaria) di 63 edifici scolastici secondari di secondo grado. Il territorio catanese, a causa della sua vasta estensione, è ripartito in quattro macro-aree (Metropolitana, Ionica, Pedemontana e Calatina). Su tale superficie, la gestione tecnica del patrimonio scolastico è resa complessa da una forte frammentazione logistica: frequentemente, infatti, un singolo istituto comprende una sede principale situata nel capoluogo e diverse succursali dislocate in comuni periferici.

Allo stato attuale, il monitoraggio dei consumi idrici sconta una grave inefficienza amministrativa. I contatori non sono centralizzati in un'unica anagrafica, bensì intestati ai singoli istituti scolastici. Le fatturazioni, spesso basate su stime di consumo e soggette a onerosi conguagli, rendono complessa la gestione razionale delle risorse. La totale assenza di sistemi di telelettura impedisce, inoltre, di rilevare tempestivamente micro-perdite o rotture accidentali, spesso individuate solo a danno avvenuto.

Per rispondere a questa sfida, il presente lavoro di tesi si concentra sulla progettazione e sullo sviluppo di *AcquaSmart*: una piattaforma IoT integrata (end-to-end) per la raccolta, l'analisi automatizzata e il monitoraggio dei consumi. Al fine di distinguere chiaramente il perimetro dell'implementazione, è fondamentale precisare che **la piattaforma software (architettura cloud, database, algoritmi di Machine Learning e dashboard utente) è stata interamente sviluppata e verificata sperimentalmente**. Al contrario, **la rete fisica di sensori (flussimetri intelligenti) è stata oggetto di simulazione software**, al fine di generare flussi di dati verosimili per testare l'infrastruttura. L'installazione fisica dei dispositivi sul campo è invece proposta come sviluppo futuro del progetto.

Il valore aggiunto di *AcquaSmart* non risiede esclusivamente nella digitalizzazione del dato, ma nell’integrazione di algoritmi di Machine Learning [6] a supporto dei processi decisionali. Tali algoritmi analizzano i flussi di dati in tempo reale per individuare tempestivamente anomalie, perdite occulte o utilizzi imprevisti all'interno della rete idrica.

L'elaborato è strutturato seguendo le macro-aree tipiche di una tesi progettuale e sperimentale:
*   **Introduzione:** delinea il contesto, il caso di studio e lo stato dell'arte delle tecnologie IoT e dei modelli di *Anomaly Detection* (in cui sono integrati i paragrafi del Capitolo 1).
*   **Materiali e metodi:** descrive la progettazione concettuale dell'architettura di sistema, giustificando lo stack tecnologico adottato e il modello relazionale dei dati.
*   **Analisi dei risultati:** illustra la fase di implementazione pratica, le configurazioni server, l'addestramento del modello predittivo e l'analisi critica delle performance.
*   **Discussione e conclusioni:** valuta il raggiungimento degli obiettivi, proponendo roadmap per futuri sviluppi e per l'effettiva installazione hardware presso l'Ente.

## 1.2 Stato dell'arte: IoT e Smart Building

### 1.2.1 Architetture e paradigmi
Nei sistemi di automazione tradizionali, i *Building Management System* (BMS) [7] operavano spesso come ecosistemi chiusi, basati su reti cablate e protocolli proprietari, limitando fortemente l'interoperabilità. L'avvento dell'Internet of Things ha introdotto grande flessibilità, offrendo vantaggi determinanti in contesti operativi complessi che gestiscono decine di edifici distribuiti sul territorio.

Le moderne architetture IoT si basano su reti distribuite di sensori e attuatori (i cosiddetti *Cyber-Physical Systems* [11]), capaci di comunicare attraverso standard aperti. In un'infrastruttura *Smart Building* reale, l'architettura è tipicamente suddivisa in tre livelli logici:
1.  **Perception Layer (Livello Fisico):** Il punto di contatto con l'ambiente reale, costituito dall'hardware installato sul campo (es. flussimetri intelligenti e microcontrollori) per intercettare i dati grezzi.
2.  **Network Layer (Livello di Rete):** Responsabile della trasmissione sicura e affidabile dei dati tramite connettività wireless o cablata.
3.  **Application Layer (Livello Applicativo):** Il nucleo del sistema, ospitato su server *on-premise* o in Cloud, dove i dati vengono aggregati, storicizzati e analizzati per alimentare dashboard di monitoraggio e sistemi di *alerting* automatici.

Questo modello a strati garantisce una naturale scalabilità, permettendo di avviare progetti pilota e integrare progressivamente nuovi nodi senza dover riprogettare l'infrastruttura centrale.

### 1.2.2 Protocolli di comunicazione per l'IoT
La scelta del protocollo di messaggistica è cruciale in scenari IoT, dove i tradizionali protocolli web possono risultare inadeguati. Tra le opzioni principali (come HTTP, CoAP, e MQTT), l'MQTT (*Message Queuing Telemetry Transport* [9]) si è imposto come standard di riferimento. 
Il suo punto di forza risiede nell'architettura centralizzata su un *Broker* che smista i messaggi, separando nettamente chi produce l'informazione (*Publisher*) da chi la riceve (*Subscriber*). Nelle strutture idriche, dove la copertura di rete può essere precaria, l'uso di MQTT garantisce l'invio di pacchetti dati estremamente leggeri, preservando il sistema da blocchi dovuti a cali di connessione e consentendo la trasmissione asincrona non appena il dispositivo torna online.

### 1.2.3 Piattaforme IoT per il building management
Il mercato offre un’ampia scelta di piattaforme per il *building management*, dalle soluzioni commerciali *cloud-based* (come AWS IoT o Microsoft Azure IoT) ai sistemi *open-source* (come ThingsBoard). Pur vantando infrastrutture solide, tali soluzioni possono risultare inadatte per alcune Pubbliche Amministrazioni, a causa degli elevati costi di licenza o dell'eccessiva standardizzazione delle funzionalità.
Per superare questi limiti, *AcquaSmart* è stata concepita come una piattaforma *custom*, sviluppata con framework moderni e leggeri. Questo approccio ha permesso di realizzare uno strumento scalabile, privo di licenze proprietarie e perfettamente aderente alle specifiche esigenze di monitoraggio degli edifici scolastici.

### 1.2.4 L'IoT nella Pubblica Amministrazione: normative sull'efficienza
L'efficientamento energetico e idrico degli edifici pubblici risponde a precisi obblighi normativi. A livello europeo, la Direttiva sulle Prestazioni Energetiche degli Edifici (EPBD [12]) promuove l’impiego di sistemi intelligenti per la misurazione dei consumi. In Italia, tali obiettivi sono perseguiti attraverso il PNRR, che destina cospicui fondi alla transizione digitale e alla riqualificazione del patrimonio immobiliare della PA. 
Il Codice dell’Amministrazione Digitale (CAD) [13] impone inoltre processi decisionali *data-driven*, richiedendo di basare le scelte manutentive su dati oggettivi. Pertanto, il superamento delle letture stimate a favore della telemetria automatizzata rappresenta un adeguamento normativo ormai improcrastinabile.

### 1.2.5 Tecniche di Anomaly Detection in ambito IoT
Trasformare i dati grezzi in valore operativo è la sfida principale dell'IoT. Nell'ambito dell'efficienza idrica, l'obiettivo è rilevare tempestivamente guasti e perdite. Dal punto di vista tecnico, queste problematiche rientrano nel campo dell'*Anomaly Detection* applicata alle serie storiche, declinabile in tre macro-categorie [8]:
1.  **Sistemi basati su regole (Rule-based):** Utilizzano soglie prefissate. Sebbene di facile implementazione, risultano rigidi e inclini a generare numerosi falsi positivi a fronte di variazioni fisiologiche dei consumi.
2.  **Modelli Supervisionati:** Algoritmi di Machine Learning addestrati su dataset etichettati. Nella PA, l'assenza di dati storici dettagliati rende questo approccio difficilmente percorribile.
3.  **Modelli Non Supervisionati:** Algoritmi in grado di apprendere autonomamente il comportamento "normale" dell'impianto, segnalando le deviazioni significative. Questa flessibilità li rende ideali per i flussi di telemetria IoT.

### 1.2.6 Analisi comparativa degli algoritmi
Per *AcquaSmart*, sono stati valutati i principali algoritmi non supervisionati:
*   **Z-Score (approccio statistico):** Estremamente leggero dal punto di vista computazionale, quantifica la deviazione standard dalla media. Tuttavia, assumendo una distribuzione normale (Gaussiana) dei dati, si rivela inadeguato per i consumi idrici scolastici, caratterizzati da dinamiche fortemente non lineari.
*   **One-Class SVM:** Proietta le misurazioni in uno spazio multidimensionale per isolare le anomalie. Nonostante l'elevata precisione, comporta tempi di calcolo che crescono esponenzialmente all'aumentare dei dati, rendendolo incompatibile con l'elaborazione *real-time*.
*   **Isolation Forest [10]:** A differenza dei metodi tradizionali, mira a isolare direttamente le anomalie utilizzando insiemi di alberi decisionali casuali. Partendo dal presupposto che i dati anomali siano rari e distanti dalla norma, garantisce una complessità temporale logaritmica ($O(n \log n)$). 

Data la sua rapidità di esecuzione e la capacità di adattarsi alle variazioni periodiche senza richiedere riaddestramenti continui, *Isolation Forest* è stato selezionato come motore di rilevamento di *AcquaSmart*.

### 1.2.7 Edge Computing e risorse computazionali
Un'ultima considerazione progettuale riguarda la distribuzione del carico computazionale. Trasmettere ogni misurazione grezza al server centrale rischia di saturare la banda di rete e introdurre latenze evitabili. Il paradigma dell'*Edge Computing* risolve questa criticità spostando l'esecuzione dei modelli inferenziali a ridosso delle sorgenti dei dati (gateway locali). Algoritmi come *Isolation Forest*, grazie al loro ridotto impatto sulla memoria (*memory footprint*), si prestano in modo ottimale a questo tipo di implementazione distribuita su dispositivi con risorse hardware limitate.
