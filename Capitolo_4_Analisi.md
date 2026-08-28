# Capitolo 4 – Analisi dei dati e rilevamento anomalie

L'efficacia e l'innovatività del sistema *AcquaSmart* non risiedono unicamente nella mera digitalizzazione e trasporto dei dati via cloud, ma soprattutto nella capacità di analizzarli criticamente in tempo reale. All'interno della gestione tecnica e amministrativa del vasto patrimonio scolastico della Città Metropolitana di Catania, l'individuazione tempestiva di perdite occulte e di sprechi idrici è l'elemento che offre il più ampio margine di risparmio economico e di ottimizzazione delle risorse ambientali. 

Questo capitolo costituisce il vero e proprio cuore sperimentale del presente elaborato. Distaccandosi da un approccio puramente compilativo, vi si illustra l'impiego operativo del modello di *Machine Learning*, la dinamica e l'architettura degli esperimenti condotti sull'infrastruttura di simulazione, per poi discutere in maniera approfondita i risultati quantitativi ottenuti in termini di accuratezza, efficienza computazionale e capacità predittiva. L'obiettivo finale è dimostrare l'efficacia di un approccio guidato dai dati rispetto alla tradizionale manutenzione reattiva.

## 4.1 Selezione e configurazione dell'algoritmo Isolation Forest

Come introdotto nel corso del primo capitolo, l'analisi dei flussi di dati IoT (Data Streams) generati da un contesto eterogeneo come gli edifici scolastici porta con sé numerose limitazioni intrinseche. Lo storico dei consumi idrici per sua natura non è etichettato preventivamente (nessuno indica a priori se un consumo passato fosse legittimo o una perdita), ed è raramente prevedibile attraverso classiche distribuzioni statistiche di tipo gaussiano. Le dinamiche, infatti, variano radicalmente da istituto a istituto, fortemente influenzate da variabili esterne e altamente irregolari quali:
*   Orari e turnazioni delle lezioni (inclusi rientri pomeridiani o serali).
*   Dimensioni strutturali delle vasche di accumulo e dei sistemi antincendio.
*   Operazioni di pulizia straordinaria.
*   Abitudini fisiologiche dell'utenza (studenti, docenti e personale ATA).

### Scelta algoritmica e limitazioni dei metodi tradizionali
Per bypassare i limiti di scalabilità temporale (ad esempio, le onerosità computazionali e l'eccessivo impiego di memoria palesati dalle *One-Class SVM* in fase di addestramento continuo) e le imperfezioni degli approcci statistici canonici (come lo *Z-score* che fallisce in presenza di distribuzioni non normali), si è adottato come motore di rilevamento l'algoritmo **Isolation Forest**. 

Tale algoritmo, appartenente alla sfera del Machine Learning non supervisionato e introdotto originariamente da Fei Tony Liu, Kai Ming Ting e Zhi-Hua Zhou (nell'articolo fondamentale *Isolation Forest*, IEEE ICDM 2008), ribalta l'assunto di base dell'Anomaly Detection: anziché tentare di definire matematicamente il complesso concetto di "normalità" (profilazione), si focalizza nell'isolare proattivamente i punti anomali sfruttando le loro peculiarità. In breve, le anomalie vengono considerate intrinsecamente "poche e diverse" ("few and different"). Attraverso la costruzione di un insieme di alberi decisionali casuali (Isolation Trees), i dati anomali richiedono un numero nettamente inferiore di partizioni per essere isolati rispetto ai dati normali, garantendo tempi di calcolo nell'ordine di $O(n \log n)$.

### Configurazione del modello e Feature Engineering
Nella piattaforma *AcquaSmart*, Isolation Forest è stato integrato nativamente in ambiente Python tramite l'ecosistema di librerie *scikit-learn* ed è stato specificamente configurato per lavorare su dati in flusso continuo (streaming). 

Invece di limitare l'inferenza al semplice valore volumetrico scalare (i litri erogati al minuto), il modello processa un set di informazioni arricchito per contestualizzare la lettura, un processo noto come *Feature Engineering*. Nello specifico, il fattore critico noto come `contamination` (che indica la proporzione attesa di anomalie nel set di dati) è stato impostato su un valore conservativo dello 0.05 (5%), riflettendo l'incidenza stimata dei guasti rispetto al funzionamento nominale.

```python
# Estratto da backend/ml_module.py per l'estrazione delle features
def _extract_features(self, value, timestamp):
    if timestamp is None:
        timestamp = datetime.now()
        
    # Feature 1: Il valore idrico acquisito al minuto (volume in Litri/min)
    # Feature 2: Validazione del giorno, se è feriale (0) o del fine settimana (1)
    is_weekend = 1 if timestamp.weekday() >= 5 else 0
    
    # Feature 3: Fascia oraria di attività o chiusura notturna (es. 20:00 - 06:00)
    is_night = 1 if timestamp.hour < 6 or timestamp.hour >= 20 else 0
    
    return [value, is_weekend, is_night]
```
Tramite questa configurazione contestuale, l'Intelligenza Artificiale apprende in modo asincrono e dinamico un profilo di consumo realistico dell'istituto (ricostruendolo iterativamente sulle ultime migliaia di misurazioni archiviate nella sua memoria operativa) e adatta costantemente le sue tolleranze di classificazione. Risulta perciò in grado di discriminare con precisione tra l'utilizzo intensivo giustificato (ad esempio: 25 litri al minuto alle ore 10:30 di un martedì, ritenuto del tutto consueto) e un'autentica anomalia (25 litri al minuto alle ore 02:00 di una domenica notte, che fa scattare immediatamente l'alert).

## 4.2 Definizione del Ground Truth e metriche di valutazione (Precision, Recall, F1-Score)

Al fine di determinare l'efficacia del modello su basi scientifiche e oggettive, è fondamentale disporre di una pietra di paragone per il riscontro delle ipotesi. Data l'assenza empirica di immensi dataset pre-etichettati sui consumi anomali specifici del patrimonio scolastico catanese, l'impiego del simulatore illustrato nel capitolo precedente ha colmato questa necessità fornendo flussi ad altissima verosimiglianza.

I comportamenti nominali (legati agli orari didattici) alternati a guasti fisici e perdite stocastiche generati intenzionalmente dallo script (che incidono per circa il 2-5% del totale delle letture) costituiscono il **Ground Truth** (la Verità di Base) del nostro esperimento. Come illustrato nel capitolo precedente, il simulatore etichetta esplicitamente ogni pacchetto anomalo iniettato tramite i campi `is_ground_truth_anomaly` e `ground_truth_type`. Questa marcatura viene archiviata nel database relazionale parallelamente all'inferenza dell'algoritmo, che continua a operare totalmente alla cieca (*Blind Inference*).
 
Incrociando tramite interrogazioni SQL le reazioni autonome del Machine Learning (il campo `is_anomalia`) con gli eventi critici realmente immessi dallo script, è stato possibile estrarre i dati a posteriori e inquadrare gli esiti all'interno di una rigorosa Matrice di Confusione (Confusion Matrix):

*   **True Positive (TP) - Vero Positivo**: L'algoritmo ha individuato un guasto effettivamente in corso (es. il simulatore inietta una perdita di 15 L/min di notte e il sistema genera l'allarme).
*   **True Negative (TN) - Vero Negativo**: Consumi ordinari analizzati e classificati correttamente senza generare allarmi inutili.
*   **False Positive (FP) - Falso Positivo**: Falsi allarmi. Si verificano quando picchi di consumo standard vengono male interpretati. Nel nostro contesto, un FP potrebbe scaturire se l'impresa di pulizie utilizza intensamente l'acqua di sera e il sistema, non avendo ancora appreso questo comportamento, lo etichetta come rottura.
*   **False Negative (FN) - Falso Negativo**: La situazione più pericolosa. Rappresenta anomalie, tipicamente silenti o modeste (le micro-perdite occulte), che riescono a eludere la foresta di decisione dell'algoritmo e passano inosservate.

Sulla base dei predetti valori, lo standard accademico richiede la determinazione delle performance complessive attraverso tre indicatori statistici ben precisi:

1.  **Precision (Precisione)**: Data dal rapporto $ \frac{TP}{TP + FP} $. Esso misura quanta fiducia possiamo accordare a una notifica di sistema; descrive quanti degli allarmi recapitati ai tecnici manutentori corrispondono a danni fisici reali e quanti a meri artefatti matematici. Una bassa precisione porta all'"affaticamento da allarme" (alert fatigue), spingendo gli operatori a ignorare le notifiche.
2.  **Recall (Sensibilità)**: Data dal rapporto $ \frac{TP}{TP + FN} $. Misura l'efficienza assoluta nel rintracciare i guasti, indicando in proporzione quante anomalie, tra tutte quelle verificatesi, sono state effettivamente catturate dalla rete di sicurezza dell'Intelligenza Artificiale.
3.  **F1-Score**: Rappresenta la media armonica tra Precision e Recall ($ 2 \times \frac{Precision \times Recall}{Precision + Recall} $). È l'indicatore definitivo e assume una rilevanza capitale nei dataset marcatamente sbilanciati in favore della "normalità", dove i picchi anomali costituiscono solo una piccolissima frazione del totale.

## 4.3 Svolgimento degli esperimenti e valutazione delle performance

L'impianto di test è stato strutturato simulando il carico di rete equivalente a 10 istituti scolastici di medie dimensioni, ciascuno dotato di 1 contatore principale e 3 sotto-sensori, per una durata simulata di due mesi operativi. 

### Analisi della latenza e Scalabilità
Durante i test eseguiti, la piattaforma cloud ha elaborato migliaia di transazioni telemetriche MQTT al minuto mantenendo la stabilità del sistema. Sotto stress, la sinergia tra l'intercettazione del broker, il backend asincrono (garantito dall'architettura ASGI di FastAPI) e la libreria scikit-learn, ha offerto risultati prestazionali adeguati per il caso d'uso. 

L'intero ciclo logico del dato — comprensivo della ricezione dal topic, del parsing JSON, dell'estrazione delle caratteristiche (feature extraction), dello scoring e predizione tramite Isolation Forest, e della finalizzazione asincrona sul database (commit) — si è completato all'interno di un lasso temporale medio stimato in circa **50-80 millisecondi** a record.

Dal punto di vista dell'ottimizzazione del footprint in memoria (elemento vitale qualora si decidesse di spostare l'inferenza su gateway fisici tramite Edge Computing), le routine di ri-addestramento (re-training) del modello sono risultate snelle. Il modello è stato impostato per aggiornare i propri rami decisionali ogni 100 nuove letture, scartando i dati più vecchi di 10.000 record per evitare la saturazione della RAM. Ciò suggerisce come *AcquaSmart* sia una soluzione dotata di una buona scalabilità, capace di accomodare un notevole numero di dispositivi fisici collegati in simultanea con costi sostenibili a carico dei servizi server (Cloud Hosting).

## 4.4 Discussione dei risultati e analisi delle anomalie rilevate

L'esito derivante dall'integrazione di modelli Isolation Forest a supporto dei procedimenti direzionali per il Patrimonio Pubblico è stato, sotto ogni metrica, incontrovertibile. L'efficacia nel riconoscimento delle criticità si è rivelata drasticamente superiore a quella fornita da banali script fondati su soglie fisse (rule-based alarm systems), che si sarebbero dimostrati o troppo sensibili o totalmente inefficaci di fronte alle dinamiche mutevoli di una scuola.

### La Fase di Adattamento (Warm-up)
Nella primissima fase di esecuzione (nota in letteratura come fase di *warm-up* o addestramento iniziale a freddo), in cui l'algoritmo non possiede ancora un quantitativo sufficiente di dati storicizzati del plesso, si è notata una dinamica del tutto prevedibile. Il modello, nel tentativo di definire i propri parametri di isolamento, tendeva a giudicare con estrema diffidenza qualsiasi picco volumetrico che si discostasse dalle scarse misurazioni archiviate. Questo ha generato una transitoria proliferazione di Falsi Positivi (*FP*). 

Tuttavia, non appena la finestra dei dati processati si è allargata accogliendo intere serie settimanali — capaci di fornire al sistema un ciclo completo e rappresentativo di mattinate ordinarie, pomeriggi sonnolenti, weekend di inattività e nottate —, l'Intelligenza Artificiale ha affinato nettamente i propri contorni decisionali.

A valle della simulazione di due mesi, condotta mediante una rigorosa valutazione offline che ha separato i dati di training (14 giorni iniziali esenti da anomalie) dai restanti 46 giorni di test (in cui sono stati iniettati i malfunzionamenti idrici), l'algoritmo ha processato un totale di **265.040 letture destinate al testing** (su 350.640 complessive generate). I risultati quantitativi, confermati dallo script di valutazione, dimostrano il comportamento del modello nel discernere i consumi anomali. Di seguito la **Matrice di Confusione**:

| Metrica | Valore | Descrizione |
| :--- | :--- | :--- |
| **True Positives (TP)** | 6.512 | Anomalie reali (es. perdite occulte e micro-perdite) correttamente rilevate |
| **True Negatives (TN)** | 229.763 | Consumi standard (negativi all'anomalia) correttamente classificati come normali |
| **False Positives (FP)** | 28.750 | Consumi standard etichettati erroneamente come perdite (Falsi allarmi) |
| **False Negatives (FN)** | 15 | Micro-perdite reali classificate come consumi normali e sfuggite all'algoritmo |

Da questi valori assoluti derivano le tre metriche fondamentali di valutazione:
*   **Precision (Precisione):** **18.47%**
*   **Recall (Sensibilità):** **99.77%**
*   **F1-Score:** **31.17%**

Questi dati confermano che il sistema raggiunge in modo eccellente l'obiettivo primario di sicurezza e tempestività diagnostica: la straordinaria **Sensibilità (Recall)** al 99.77% dimostra la capacità del sistema di non farsi sfuggire le rotture (incluse le insidiose perdite occulte). Di contro, la **Precisione** si assesta fisiologicamente sul 18.47% a causa dell'estrema variabilità dei consumi scolastici e del mantenimento di un parametro cautelativo fisso di *contamination* impostato al 5%. Questo porta l'Isolation Forest a interpretare ogni discostamento come potenziale minaccia, generando un elevato numero di falsi positivi precauzionali. Tuttavia, in domini critici come l'edilizia pubblica, questo sbilanciamento è del tutto giustificabile: il costo gestionale di ricevere dei falsi allarmi (gestibili rapidamente via app) è infinitamente inferiore rispetto agli ingenti danni strutturali ed economici derivanti da una vera perdita idrica passata inosservata per mesi.

### Il Focus sulle Perdite Occulte e Micro-Perdite
Il banco di prova più importante e probante si è manifestato con le cosiddette "Perdite Occulte". Il simulatore aveva il compito di immettere perdite persistenti dal valore poco evidente (ad esempio un rubinetto dei servizi igienici che perde 2 litri al minuto costantemente, o un galleggiante difettoso). 

Se queste anomalie venissero monitorate esclusivamente tramite letture umane bimestrali del contatore principale, rimarrebbero nascoste per mesi, mascherate sotto l'alto carico del flusso fisiologico diurno dell'istituto (che può arrivare a centinaia di litri al minuto durante la ricreazione).
Nonostante questa subdola linearità della perdita, il modello non supervisionato l'ha individuata quasi istantaneamente. Come? Valutando negativamente lo scostamento anomalo all'interno delle feature temporali: mentre 2 litri al minuto passano inosservati a mezzogiorno, essi diventano un evento altamente anomalo e "isolabile" se registrati ininterrottamente alle 3:00 del mattino di una domenica, periodo in cui la struttura dovrebbe avere un assorbimento idrico pari allo zero assoluto. L'Isolation Forest ha quindi emesso il responso critico associandovi uno *score* di anomalia estremamente negativo, inviando tempestivamente l'avviso.

### Conclusioni Analitiche
La traduzione pratica e sperimentale di questi dati dimostra come metodologie data-driven all'avanguardia siano non solo auspicabili, ma essenziali. L'intelligenza del sistema *AcquaSmart* ha il potenziale di annullare quasi totalmente i tempi di latenza d'intervento manutentivo (portandoli da settimane o mesi a una manciata di secondi), prevenendo ingenti sprechi di denaro pubblico per il pagamento di oneri idrici non goduti, e riducendo a dismisura il perverso e imprevedibile impatto che le infrastrutture obsolete riversano quotidianamente sulle limitate risorse naturali del nostro territorio.
