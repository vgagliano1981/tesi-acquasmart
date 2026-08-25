Università telematica eCampus


Facoltà di Ingegneria Informatica e dell’Automazione

Corso di Laurea in
Sistemi di Elaborazione e Controllo


Progettazione e sviluppo di una piattaforma IoT per il monitoraggio e l'analisi dei consumi energetici negli edifici pubblici


Relatore:                                                
Prof. Kuznetsov Oleksandr
                                                               Tesi di Laurea di:
                                                                       Vito Gagliano                                 
                                                                 Matricola n° 1857837

Anno Accademico 2025/2026


AUTORIZZAZIONE ALLA CONSULTAZIONE DELLA TESI DI LAUREA

Il/la sottoscritto Vito Gagliano
N° di matricola 1857837 nato a Catania il 09/11/1981
autore della tesi dal titolo: Progettazione e sviluppo di una piattaforma IoT per il monitoraggio e l'analisi dei consumi energetici negli edifici pubblici
  AUTORIZZA
la consultazione della tesi stessa, fatto divieto di riprodurre, parzialmente o integralmente, il contenuto.

Dichiara inoltre di:
 AUTORIZZARE
per quanto necessita l’università telematica e-Campus, ai sensi della legge n. 196/2003, al trattamento, comunicazione, diffusione e pubblicazione in Italia e all’estero dei propri dati personali per le finalità ed entro i limiti illustrati dalla legge.


Data________________ Firma__________________


SPAZIO RISERVATO ALL’UFFICIO SEGRETERIA:
Laureato/a il ______________
Con la votazione di ______/ 110
Indice

Introduzione.
La progressione evolutiva delle tecnologie digitali ha determinato un sostanziale cambiamento nei processi produttivi, organizzativi e sociali, favorendo la nascita di nuovi modelli che si basano sull’automazione e condivisione intelligente. In tale contesto l’Internet of Things (IoT)[1] costituisce l’infrastruttura di base per la transizione digitale di molti ambienti fisici. Dotando di sensori e dispositivi intelligenti gli oggetti di uso quotidiano, i macchinari industriali, ecc., tramite l’utilizzo della IoT possiamo raccogliere e gestire un’enorme quantità di dati in tempo reale, creando così nuovi modelli gestionali.
Grazie allo Smart Building Management[2] è possibile ottimizzare in modo autonomo le prestazioni energetiche di un edificio civile o industriale. Se nel settore privato questa evoluzione è ormai consolidata, lo stesso non si può dire per la Pubblica Amministrazione (PA) Italiana, dove la transizione ancora è frammentata o del tutto assente.  Eppure, esistono direttive europee sull’efficienza energetica e strumenti programmatici come il PNRR [3] e il Codice dell’Amministrazione Digitale, che impongono le PA a un radicale e repentino cambiamento in tal senso. E’ proprio in questo scenario che la gestione delle risorse idriche rappresenta una criticità prioritaria. In un territorio come il nostro, dove la carenza di acqua potabile è sempre più frequente e prolungata, non possiamo permetterci di avere dispersioni idriche, le quali generano, oltre a una difficoltà oggettiva, un danno economico significativo. Implementare un sistema di monitoraggio tramite l’IoT negli edifici pubblici significherebbe superare la manutenzione reattiva e adottare un modello predittivo guidato dai dati (data-driven)[4]. L’ideazione e progettazione di questo sistema non rappresenta solo un esercizio accademico, bensì nasce da un’esigenza operativa e concreta che ho riscontrato e affrontato sul campo, in risposta alle criticità gestionali rilevate dalla direzione Patrimonio e Politiche Scolastiche della Città Metropolitana di Catania [5]. L’Ente preso in esame ha in gestione la manutenzione (ordinaria e straordinaria) di 63 edifici scolastici secondari di secondo grado. A causa della sua vasta estensione, il territorio catanese è ripartito in quattro macro-aree (Metropolitana, Ionica, Pedemontana e Calatina). Su tale superficie, la gestione tecnica del patrimonio scolastico è resa particolarmente complessa da una forte frammentazione logistica: non è raro, infatti, che un singolo istituto comprenda una sede principale situata nel capoluogo e diverse succursali dislocate in comuni periferici o in aree geografiche completamente differenti. Allo stato attuale dei fatti, il monitoraggio dei consumi idrici pecca di una grave inefficienza di natura amministrativa. Infatti, i contatori non sono intestati a un'unica anagrafe centralizzata, bensì ai singoli istituti scolastici. Le fatturazioni, spesso basate su stime di consumo e soggetti a conguagli o oneri di mora, rendendo difficile, se non quasi impossibile, la gestione delle risorse. In fase di analisi, abbiamo valutato l’unificazione contrattuale di tutti i contatori, ma questa soluzione richiedeva un iter burocratico troppo lungo per un’esigenza cosi urgente. Da qui è nata la necessità di una soluzione rapida che aggirasse tutti i vincoli. La totale assenza di sistemi di telelettura, che impedisce di rilevare tempestivamente micro-perdite o rotture accidentali (spesso scoperte solo a fatto avvenuto), mi ha portato a creare il sistema AcquaSmart. Grazie all’installazione di flussimetri intelligenti agli ingressi delle reti idriche principali e secondarie, ho fatto in modo che tutti i dati convogliassero verso un’infrastruttura Cloud, potendo così sviluppare una dashboard operativa (disponibile all’indirizzo https://tesi-acquasmart.onrender.com). Cosi, per la prima volta, l’ente dispone di uno strumento di controllo capillare e in tempo reale, capace di abbattere drasticamente i tempi di intervento.
   Per rispondere al meglio a questa sfida, il mio lavoro si è concentrato sulla progettazione, sullo sviluppo e sulla verifica sperimentale di AcquaSmart: una piattaforma IoT chiavi in mano (end-to-end) per la raccolta e l’analisi in maniera automatizzata dei consumi negli edifici pubblici. Il valore aggiunto non è da ricercarsi nella semplice digitalizzazione del dato, ma nell’utilizzo di algoritmi di Machine Learning [6]come supporto decisionale, i quali permettono di analizzare i flussi in tempo reale per individuare tempestivamente anomalie, micro-perdite o utilizzi imprevisti all'interno della rete idrica. 
La mia ricerca si è articolata in diverse fasi operative. Inizialmente, ho condotto un’analisi critica sullo stato dell’arte, esaminando le piattaforme già esistenti per il building management [7] e ponendo particolare attenzione ai protocolli di messaggistica leggeri e alle tecniche di anomaly detection[8] sui dati storici. Successivamente, sono passato alla progettazione dell’architettura di sistema, definendo un flusso dati sicuro e scalabile che parta dai sensori Edge, passi per i broker MQTT[9]  e, infine,  approdi al database di backend.
L’attività è proseguita con lo sviluppo e il deployment del prototipo, mettendo molta attenzione all’interfaccia utente, affinché risultasse di facile utilizzo per gli operatori dell’ente. Un modulo centrale del progetto è costituito nell’implementazione dell’algoritmo di Isolation Forest[10], scelto per la sua velocità di calcolo su flussi dati non supervisionati. Infine, ho completato il lavoro con una validazione sperimentale quantitativa, misurando le latenze dell’architettura e verificando l’accuratezza del modello nel distinguere pattern di consumo anomali, minimizzando così i falsi positivi.
L'elaborato si sviluppa in sei capitoli che guideranno il lettore dalla definizione teorica del problema fino ai risultati sperimentali.
Nel Capitolo 1 si delinea lo stato dell'arte, analizzando il paradigma IoT e il quadro normativo di riferimento, e ponendo le basi teoriche sulle tecniche di rilevamento anomalie attraverso la letteratura scientifica.
Il Capitolo 2 è dedicato alla progettazione concettuale. Vengono definiti i requisiti di sistema, giustifico la scelta dello stack tecnologico, (tra cui il broker MQTT e il framework di backend) e illustro il modello relazionale dei dati.
Il Capitolo 3 descrive la fase di implementazione pratica di AcquaSmart, illustrando le configurazioni server, i meccanismi di acquisizione e l'architettura della dashboard operativa. 
Il Capitolo 4 descrive le procedure di addestramento del modello, viene definito il Ground Truth e presentato un'analisi critica delle performance basata su metriche standard come Precision, Recall e F1-Score. 
Il Capitolo 5 traccia le conclusioni, valutando il raggiungimento degli obiettivi e definendo una roadmap per futuri sviluppi, in particolare per l'integrazione della piattaforma nei sistemi BMS già in uso presso l'ente.





Capitolo 1 – Stato dell'arte e tecnologie di riferimento
1.1 IoT e Smart Building: architetture e paradigmi
In un passato recente, i sistemi di automazione degli edifici si basavano su logiche molto rigide. I tradizionali Building Management System (BMS)[7] venivano concepiti come compartimenti stagni che lavoravano esclusivamente su reti cablate, spesso fisicamente inaccessibili, e protocolli proprietari che rendevano quasi impossibile far dialogare sistemi diversi tra loro. L'avvento dell'Internet of Things (IoT) ha portato flessibilità dove prima c'era chiusura. In contesti operativi complessi, dove si gestiscono decine di edifici storici o frammentati sul territorio, questo cambiamento ha portato enormi vantaggi.
Le nuove strategie IoT hanno superato i limiti fisici del passato, basandosi su reti distribuite di sensori e attuatori (i cosiddetti Cyber-Physical Systems[11]), capaci di comunicare utilizzando standard aperti. In un'infrastruttura reale e funzionante, l'architettura di uno Smart Building viene solitamente suddivisa in tre livelli logici ben distinti:
Perception Layer (Livello Fisico): È il punto di contatto con l'ambiente reale. È costituito dall'hardware installato fisicamente sul campo, come i flussimetri intelligenti posizionati sui tubi e i microcontrollori che hanno il compito di intercettare il dato grezzo direttamente dalla rete idrica.
Network Layer (Livello di Rete): Responsabile della trasmissione sicura e affidabile dei dati, utilizzando connettività wireless o filare (cablata)
Application Layer (Livello Applicativo): È il vero "cervello" del sistema, ospitato su un server on-premise o in Cloud. Qui i dati vengono aggregati, storicizzati e analizzati per fornire strumenti concreti a chi gestisce la manutenzione, come dashboard di monitoraggio visivo e sistemi di allerta (alert) automatici in caso di perdite.
Il grande vantaggio operativo di questo modello a strati è la sua naturale scalabilità. Permette, infatti, di partire con un progetto pilota per poi integrare progressivamente plessi scolastici. Basterà quindi aggiungere nuovi nodi alla rete periferica, senza mai dover stravolgere o riprogettare l'infrastruttura centrale di base.

1.2 Protocolli di comunicazione per l'IoT (MQTT, CoAP, HTTP)
La scelta del protocollo di messaggistica è cruciale soprattutto in determinati scenari. I protocolli del web a volte sono inadeguati e per tale motivo si devono ricercare soluzioni ottimali
Tabella 1Analisi comparativa dei protocolli di rete (HTTP, CoAP, MQTT) per le architetture IoT.

Tra le opzioni riportate in tabella 1, MQTT (Message Queuing Telemetry Transport[9]) si è ormai imposto come lo standard indiscusso per le applicazioni IoT, sia in ambito industriale che civile. Il suo vero punto di forza risiede nell'architettura. La struttura è centralizzata sul Broker, che ha il compito di smistare i messaggi. Questo meccanismo separa nettamente chi produce l'informazione (il Publisher, nel nostro caso il sensore sul tubo) da chi la deve leggere o elaborare (il Subscriber, ovvero il server o la dashboard). In situazioni critiche delle strutture idriche dove la copertura di rete è scarsa, utilizzare sensori MQTT ci viene incontro perché trasmette “pacchetti” dati leggerissimi e soprattutto protegge i dati dai cali di connessione evitando che il sistema vada in blocco in caso di disconnessione e trasmettendo i dati non appena il dispositivo torna online.

1.3 Piattaforme IoT per il building management
Analizzando le attuali opzioni disponibili sul mercato, si trova un’ampia scelta di sistemi per il building management. Soluzioni commerciali offerte da AWS IoT o Microsoft Azure IoT, o architetture open-source come ThingsBoard o Home Assistant. Naturalmente questi sistemi vantano un’infrastruttura solida con potenti strumenti integrati per l’analisi dei dati. Eppure il loro modello può risultare inadatto ad alcune Amministrazioni Pubbliche sia per i costi sostenuti delle licenze annuali, sia per gli strumenti da essi proposti, il più delle volte standardizzati su parametri già prefissati e magari non rispettando le reali necessità dell’ente. È per superare questi ostacoli che nasce il progetto custom adottato in questo lavoro di tesi. Impiegando framework di sviluppo moderni e allo stesso tempo “leggeri”, è stato possibile costruire da zero una piattaforma sagomata sulle reali esigenze di monitoraggio idrico degli edifici scolastici. Uno strumento scalabile capace di essere implementato o modificato secondo le esigenze future, totalmente libero da licenze proprietarie ed esente da vincoli contrattuali di assistenza annuale. 

1.4 L'IoT nella Pubblica Amministrazione: normative e direttive europee sull'efficienza
Rendere gli edifici pubblici più efficienti e digitalizzati, non rappresenta una semplice opzione di ammodernamento tecnologico, ma risponde a un preciso obbligo normativo. Concentrandoci su uno scenario europeo, è proprio la Direttiva sulle Prestazioni Energetiche degli Edifici (EPDB- Energy Performance of Buildings Directive[12]) ad accelerare l’impiego di sistemi intelligenti capaci di misurare e governare i consumi in modo minuzioso. Anche sul fronte nazionale questa direttiva Europea ha trovato un’applicazione attraverso il Piano Nazionale di Ripresa e Resilienza (PNRR). Attraverso le Missioni 1 e 2 del medesimo Piano, sono stati destinati considerevoli fondi economici alla transizione digitale delle P.A. e alla riqualificazione del patrimonio immobiliare. A questo si affianca il Codice dell’Amministrazione Digitale (CAD)[13], che sancisce che le scelte devono essere guidate dai fatti (data-driven decision making). Questo significa che le istituzioni sono chiamate a basare i propri processi amministrativi e manutentivi su dati oggettivi e misurabili e non approssimativi. Considerato ciò, affidarsi alla lettura stimata dei contatori idrici è una pratica che deve essere superata definitivamente. Pertanto diventa una tappa obbligatoria l’utilizzo di sistemi di telemetria e monitoraggio automatizzato.

1.5 Tecniche di Anomaly Detection in ambito IoT: rassegna della letteratura
L’acquisizione dei dati è il punto di partenza. La vera sfida consiste nel trasformarli in valore operativo. Quando parliamo di efficienza idrica all’interno degli istituti scolastici, lo scopo fondamentale è trovare tempestivamente guasti, micro-perdite o utilizzi imprevisti (flussi d’acqua durante la notte o giorni di chiusura degli istituti). Dal punto di vista tecnico questi tipi di problemi rientrano nel campo dell’Anomaly Detection (rilevamento delle anomalie) applicato alle serie storiche. Analizzando gli studi di settore, per intercettare queste deviazioni si possono individuare tre macro-categorie:
Sistemi basati su regole (Rule-based): Un approccio tradizionale, che prevede l’impostazione di soglie massime prefissate o finestra temporali di allarme. Immediati e facili da implementare ma a volte troppo rigidi. Tendono a generare un alto numero di falsi positivi, soprattutto quando per questioni interne all’istituto scolastico variano i consumi abituali, rendendo il sistema di allerta poco credibile per chi deve gestirlo.
Modelli Supervisionati: Sono degli algoritmi di Machine Learning che vengono addestrati partendo da un set di dati già etichettati preventivamente come un consumo fisiologico o un’anomalia. Nella realtà operativa di un ente pubblico, questa soluzione è quasi sempre impercorribile, visto che è improbabile avere un database storico dettagliato su cui poter addestrare il sistema in modo efficace.
Modelli Non Supervisionati: In questo caso, l’algoritmo è in grado di studiare autonomamente lo storico dei dati. Deduce quindi quale sia il comportamento abituale dell’impianto segnalando solo le misure che si discostano in modo netto dalla normalità. Proprio per la flessibilità e adattamento in assenza di dati storici, questa famiglia di algoritmi rappresenta la soluzione più concreta e idonea per i flussi di telemetria IoT

1.6 Analisi comparativa degli algoritmi (Isolation Forest, One-Class SVM, Z-score)
Per individuare il motore più adatto all’architettura di AcquaSmart, ho condotto un’analisi comparativa dei principali algoritmi non supervisionati.
Z-Score (approccio Statistico)
Questo algoritmo quantifica di quante deviazioni standard una determinata misurazione si discosta dal valore medio della distribuzione. Da un punto di vista matematico, possiamo definire:
 
Il suo principale vantaggio è senz’altro l’estrema leggerezza di calcolo. Tuttavia, questo metodo assume che i dati seguano una distribuzione normale (Gaussiana). I consumi idrici all’interno di un istituto scolastico, presentano invece dinamiche non lineari. Infatti si presentano spesso picchi improvvisi o cali drastici dei consumi in base a giornate, ore o attività scolastiche o extra scolastiche. Pertanto questo algoritmo è fortemente inadeguato per il nostro contesto.
One-Class SVM (Support Vector Machine)
Questo algoritmo cerca di disegnare un confine sferico attorno alle misure “normali”, proiettandole in uno spazio a più dimensioni. Sebbene garantisca un’elevata precisione nel riconoscimento dei modelli complessi, presenta un grosso limite architetturale nel consumo delle risorse di calcolo. Quindi è risaputo che al crescere del volume dei dati da elaborare i tempi di calcolo aumentano drasticamente. Una simile latenza non è accettabile e compatibile con un sistema che lavora in tempo reale.
Isolation Forest
Questo algoritmo ribalta la logica dei metodi di rilevamento tradizionali. Anziché analizzare matematicamente il comportamento “normale”, mira a isolare in modo diretto le anomalie. Il modello sfrutta un insieme di alberi decisionali casuali, per ricavarne previsioni molto precise. Quindi si deduce che i dati anomali sono rari e presentano valori distanti dal dataset. Questa dinamica si traduce in una straordinaria efficienza prestazionale, garantendo una complessità temporale di tipo logaritmico:
O(n log n)
Per la propria rapidità di esecuzione, la capacità di adattamento alla  variazioni periodiche dei consumi idrici senza richiedere ulteriori addestramenti dell’algoritmo, si è scelto di utilizzare Isolation Forest come motore di rilevamento di AcquaSmart.
1.7 Dimensione dei modelli e deployment su dispositivi a risorse limitate (Edge Computing)
Un’ulteriore considerazione progettuale di rilievo è stata rivolta alla distribuzione del carico computazionale. Anche se le piattaforme Cloud mettono a disposizione una capacità di calcolo teoricamente inesauribile, trasmettere ogni singola misurazione grezza dai vari sensori IoT al server centrale per applicare il modello di calcolo, rischia di saturare la banda di rete, introducendo della latenza del tutto evitabile.
Il modello dell’Edge Computing, risolve questa criticità spostando la fase di elaborazione o di esecuzione dei modelli pre-addestrati direttamente a ridosso delle sorgenti dei dati (gateway o IoT locali). È proprio in questo scenario che algoritmi come Isolation Forest si rivelano veramente vantaggiosi: il loro ridotto impatto sulla memoria (memory footprint) ne facilita l’implementazione anche su dispositivi con risorse hardware limitate.



Capitolo 2 – Progettazione dell’architettura del sistema

La progettazione dell’infrastruttura tecnologica necessaria alla piattaforma AcquaSmart, ha richiesto un attenta analisi delle specifiche tecniche e dei vincoli imposti dagli edifici scolastici in questione. In questo capitolo verranno quindi definiti le scelte architetturali, le motivazioni delle tecnologiche adottate e, infine , il modello dei dati che governa i flussi di comunicazione tra i vari moduli del sistema.

2.1 Requisiti di sistema e architettura generale
Lo sviluppo di una piattaforma IoT per il building management in ambito pubblico impone il rispetto di severi criteri di affidabilità, scalabilità e sicurezza.
Durante la prima fase di raccolta dei dati, si sono individuati degli obiettivi operativi e funzionali:
Acquisizione in tempo reale (Real-time data ingestion)[14]: il sistema deve permettere un monitoraggio continua dello stato delle reti idriche ricevendo ed elaborando grandi quantità di dati da remoto con latenze minime.
Rilevamento intelligente delle anomalie (Anomaly Detection): oltre a salvare i dati, l’applicativo deve valutare ogni singola misurazione, per identificare variazioni significative, rispetto al comportamento nominale (perdita occulte, guasti o consumi fuori orario), utilizzando sia una logica a soglia rigida che anche dei modelli di Machine Learning.
Scalabilità e disaccoppiamento: l’architettura deve supportare sia l’inserimento di nuovi istituti scolastici, sia l’installazione quindi monitoraggio di centinaia di nuovi sensori, senza richiedere interventi strutturali sul nucleo del sistema.
Accessibilità e sicurezza: le informazioni e i dati, devono essere consultabili dagli operatori tecnici e anche dai dirigenti della Pubblica Amministrazione attraverso una dashboard intuitiva e sicura, accessibile via web senza aver nessun vincolo di installazioni software o di client dedicati.
Per far si che tutti questi requisiti fossero soddisfatti, è stato adottato un’architettura a livelli (multi-tier). Soluzione simili sono già adottate e consolidata negli ecosistemi IoT più moderni. Il sistema AcquaSmart si divide in 3 macro-livelli connessi tra loro:
Livello di Campo (Edge): comprende l’hardware di rilevamento fisico, come flussimetri intelligenti e sonde di monitoraggio (pressione, torbidità, conducibilità) installati presso i vari snodi idrici dei plessi scolastici.
Livello di Trasporto (Middleware): costituito da un broker per la gestione personalizzata della messaggistica, che funge da collegamento tra le sonde sul campo e l’infrastruttura server.
Livello Applicativo (Backend e Frontend): il motore centrale della piattaforma, proposto all’aggregazione dei dati, dall’elaborazione predittiva, all’ archiviazione, e della visualizzazione tramite API RESTful.
Questa scelta architetturale favorisce l’affidabilità del sistema, infatti eventuali malfunzionamenti o di una sonda periferica o manutenzioni sul database, non compromettono la stabilità e integrità dell’intera infrastruttura.

2.2 Topologia della rete di sensori
Il monitoraggio dei consumi idrici nelle scuole superiori, impone l’adozione di una topologia di rete capace di mappare il più fedelmente possibile l’infrastruttura idrica. Per tale motivo, la rete di sensori è stata progettata secondo un modello ibrido a stella-albero.
Ciascun plesso scolastico si configura come un nodo primario di aggregazione logica. In corrispondenza dell’allaccio principale all’acquedotto Sidra S.P.A. (società idrica Catanese), è prevista l’installazione di un sensore principale (chiamato Contatore Principale o Master Sensor), che ha il compito di misurare il consumo idrico complessivo dell’istituto. A valle di questo misuratore, la rete si dirama verso i sotto-sensori  (chiamati Sensori secondari o Sub-Sensors), distribuiti secondo una logica ben precisa nei punti di erogazione a maggior rischio o consumo ( esempio: servizi igienici di piano, spogliatoi palestre, laboratori e nelle vasche di raccolta per il sistema antincendio) .
Questa suddivisione ci permette di ottenere informazioni estremamente dettagliate, e soprattutto in presenza di anomalie grazie a un raffronto incrociato con i sotto-sensori consente di isolare fisicamente l’area interessata dal guasto, abbattendo drasticamente i tempi di intervento della manutenzione. 
Oltre ai misuratori di portata volumetrica (Acqua), sono state previste sonde per il controllo della qualità e della stabilità (pressione) dell’impianto. Quindi l’infrastruttura si configura, pertanto, come uno strumento multifunzionale: le misure di pressione monitorano continuamente l’efficienza degli impianti di spinta (autoclavi), mentre i valori ottenuti dai sensori di torbidità e conducibilità controllano costantemente lo stato igienico-sanitario dell’acqua.

2.3 Scelta e giustificazione dello stack tecnologico
La scelta architetturali alla base della piattaforma sono state dettate dalla necessità di realizzare un sistema robusto, performante e basato su tecnologia open-source, liberando l’Amministrazione da vincoli commerciali e licenze proprietarie. 
Per l’instradamento e la gestione dei flussi telemetrici, si è optato per Mosquitto [15] come broker MQTT (in ascolto sulla porta standard 1883). Questa scelta nasce dal ridotto impatto sulle risorse di memoria e dalla capacità di mantenere stabili migliaia di connessioni concorrenti. Il broker assolve esclusivamente alla funzione di instradare i messaggi sui relativi topic (canali telematici), demandando ai livelli superiori la logica applicativa e compensando le frequenti instabilità di connessione che si manifestano nei locali tecnici delle scuole.  
Il nucleo logico (Backend) è stato sviluppato interamente in Python[16] sfruttando il framework FastApi[17]. La decisione di preferire Python ad altri linguaggi tradizionali utilizzati solitamente nel web enterprise (java o C) è motivata da due esigenze tecnologiche. L’adozione di FastApi risponde a due necessità primarie: la gestione efficiente e nativa delle operazioni di I/O asincrone, supportata dalla sua architettura ASGI, e la totale interoperabilità con le librerie dedicate al Machine Learning, 


Essendo il rilevamento anomalie basato su librerie scientifiche quali *scikit-learn* e *pandas* (per l'algoritmo *Isolation Forest*), l'uso di Python ha consentito di integrare il motore inferenziale direttamente nel flusso di elaborazione backend. Questo approccio architetturale ha evitato l'overhead di comunicazione tipico dei sistemi a microservizi separati, annullando di fatto le latenze in fase di previsione.

Per la gestione della persistenza dei dati, si è adottato un approccio ibrido relazionale implementato tramite l'ORM (Object-Relational Mapping) **SQLAlchemy**. L'architettura dati è stata concepita per operare agilmente su un database *file-based* come **SQLite** per le fasi di test, prototipazione e rilascio leggero. Allo stesso tempo, l'astrazione garantita dall'ORM assicura una migrazione trasparente (*zero-rewrite*) verso DBMS enterprise come **PostgreSQL**, requisito essenziale per gestire moli di dati strutturati su base pluriennale in un'ottica di ampliamento futuro.

Infine, per il livello di presentazione (Frontend), si è progettata una Web-Dashboard basata su tecnologie standard HTML, CSS e JavaScript asincrono (*Vanilla JS*). Questo garantisce interfacce leggere, altamente reattive e *mobile-friendly*, servite in modo diretto dal backend senza appesantire l'infrastruttura con complessi framework lato client.

### 2.4 Modello dei dati e flussi di comunicazione

L'efficienza di una piattaforma orientata ai dati (*data-driven*) risiede in un modello entità-relazione solido e in un flusso di comunicazione intrinsecamente sicuro. Il database di *AcquaSmart* è stato strutturato per ottimizzare le query spaziali (relazioni anagrafiche) e temporali (*time-series* delle letture).

Le principali entità del dominio applicativo sono:
*   **Scuole:** Gestisce l'anagrafica degli istituti, memorizzando coordinate, indirizzi e codici meccanografici governativi.
*   **Sensori:** Entità in relazione gerarchica (1 a N) con le Scuole. Mappa ogni dispositivo hardware al proprio identificativo di rete (*topic MQTT*), alla tipologia di misurazione (Acqua, Pressione, ecc.) e stabilisce tramite flag logici il ruolo topologico del sensore (principale o secondario).
*   **Letture:** Rappresenta la tabella transazionale con il più alto volume di scritture. Associa a ogni sensore un valore quantitativo, il *timestamp* esatto di misurazione e i metadati restituiti dal modello di intelligenza artificiale (flag di anomalia e punteggio probabilistico).
*   **Utenti / Dati Reali:** Sottosistemi dedicati all'autenticazione sicura tramite token JWT (*JSON Web Token*) con gestione dei privilegi (amministratore vs *guest*), e all'incameramento dei dati reali di fatturazione (bollette) necessari per le fasi di confronto e validazione.

Il ciclo di vita del dato (*Data Pipeline*), dal mondo fisico alla dashboard, è scandito da un flusso di comunicazione asincrono ma rigorosamente orchestrato:
1.  **Pubblicazione (Publish):** I sensori hardware si connettono al broker e trasmettono pacchetti JSON leggeri. I topic fungono da indirizzamento gerarchico (ad esempio: `tesi/catania/scuole/1/sensore_acqua_main`).
2.  **Ingestione (Subscribe):** Un *demone* in background, integrato nel server FastAPI, resta costantemente in ascolto. Alla ricezione del payload, il backend normalizza il dato e individua l'identificativo del sensore.
3.  **Inferenza e Scoring:** Il dato di consumo idrico viene incanalato in tempo reale al modulo di Machine Learning pre-addestrato (*Isolation Forest*), che restituisce un indice di devianza (*Anomaly Score*). Per le grandezze non idriche, vengono applicate rigide soglie normative.
4.  **Persistenza e Notifica:** La lettura, arricchita dai risultati inferenziali, viene finalizzata nel database. In caso di classificazione positiva dell'anomalia, l'architettura applicativa scatena parallelamente eventi di *alerting* sull'interfaccia utente e trigger per l'invio automatizzato di comunicazioni (email) ai responsabili della manutenzione.
5.  **Esposizione:** I dati grezzi vengono aggregati su base oraria, giornaliera e mensile, ed esposti in modo sicuro alla dashboard tramite endpoint REST, trasformando le matrici numeriche in cruscotti visivi e grafici interattivi.











Materiali e metodi
Max 500 parole

Analisi dei risultati
Max 750 parole

Discussione e conclusioni
Max 750 parole















Bibliografia
[1]	E. Sisinni, A. Saifullah, S. Han, U. Jennehag, e M. Gidlund, «Industrial Internet of Things: Challenges, Opportunities, and Directions», IEEE Trans. Ind. Inform., vol. 14, fasc. 11, pp. 4724–4734, nov. 2018, doi: 10.1109/TII.2018.2852491.
[2]	D. Minoli, K. Sohraby, e B. Occhiogrosso, «IoT Considerations, Requirements, and Architectures for Smart Buildings—Energy Optimization and Next-Generation Building Management Systems», IEEE Internet Things J., vol. 4, fasc. 1, pp. 269–283, feb. 2017, doi: 10.1109/JIOT.2017.2647881.
[3]	P. Malavasi, PNRR e formazione. La via della transizione ecologica. ITA, 2022. Consultato: 2 agosto 2026. [Online]. Disponibile su: https://publicatt.unicatt.it/handle/10807/218188?mode=simple
[4]	D. J. Patil e H. Mason, Data Driven. O’Reilly Media, Inc., 2015.
[5]	R. Papa, C. Gargiulo, e R. Battarra, Città Metropolitane e Smart Governance: Iniziative di successo e nodi critici verso la Smart City. in Smart City, Urban Planning for a Sustainable Future. FedOAPress, 2016. [Online]. Disponibile su: https://books.google.it/books?id=NipADwAAQBAJ
[6]	Z.-H. Zhou, Machine Learning. Springer Nature, 2021.
[7]	P. V. Paulo, F. Branco, e J. De Brito, «BuildingsLife: a building management system», Struct. Infrastruct. Eng., vol. 10, fasc. 3, pp. 388–397, mar. 2014, doi: 10.1080/15732479.2012.756919.
[8]	G. ANSALDO, «Anomaly Detection: Metodi, Applicazioni e Sperimentazione su Dati Reali», lug. 2025, Consultato: 2 agosto 2026. [Online]. Disponibile su: https://thesis.unipd.it/handle/20.500.12608/88502
[9]	B. Mishra e A. Kertesz, «The Use of MQTT in M2M and IoT Systems: A Survey», IEEE Access, vol. 8, pp. 201071–201086, 2020, doi: 10.1109/ACCESS.2020.3035849.
[10]	W. S. Al Farizi, I. Hidayah, e M. N. Rizal, «Isolation Forest Based Anomaly Detection: A Systematic Literature Review», in 2021 8th International Conference on Information Technology, Computer and Electrical Engineering (ICITACEE), Semarang, Indonesia: IEEE, set. 2021, pp. 118–122. doi: 10.1109/ICITACEE53184.2021.9617498.
[11]	W. Wolf, «Cyber-physical Systems», Computer, vol. 42, fasc. 3, pp. 88–89, mar. 2009, doi: 10.1109/MC.2009.81.
[12]	E. Burman, D. Mumovic, e J. Kimpian, «Towards measurement and verification of energy performance under the framework of the European directive for energy performance of buildings», Energy, vol. 77, pp. 153–163, dic. 2014, doi: 10.1016/j.energy.2014.05.102.
[13]	I. Macrì, U. Macrì, e G. Pontevolpe, Il nuovo Codice dell’amministrazione digitale. IPSOA, 2011.
[14]	G. Pal, G. Li, e K. Atkinson, «Big Data Real Time Ingestion and Machine Learning», in 2018 IEEE Second International Conference on Data Stream Mining & Processing (DSMP), Lviv: IEEE, ago. 2018, pp. 25–31. doi: 10.1109/DSMP.2018.8478598.
[15]	G. C. Hillar, MQTT Essentials - A Lightweight IoT Protocol: The preferred IoT publish-subscribe lightweight messaging protocol. Packt Publishing Ltd, 2017.
[16]	«Why is Python a dynamic language and also a strongly typed language - Python Wiki», wiki.python.org, [Online]. Disponibile su: https://wiki.python.org/moin/Why%20is%20Python%20a%20dynamic%20language%20and%20also%20a%20strongly%20typed%20language
[17]	B. Lubanovic, FastAPI. O’Reilly Media, Inc., 2023.







pagina 10 guassiana, e anche one-class svm,  isolatation forest
pagina 11 dataset, edge computing, memory footprint, 

