# Capitolo 5 – Conclusioni e Sviluppi Futuri

## 5.1 Raggiungimento degli obiettivi del progetto

Il presente elaborato di tesi si è posto l'obiettivo di progettare, sviluppare e validare un ecosistema IoT completo, denominato *AcquaSmart*, per il monitoraggio intelligente delle risorse idriche nel patrimonio scolastico della Città Metropolitana di Catania. L'architettura realizzata, basata su un'infrastruttura Cloud/Edge e supportata da algoritmi di Machine Learning (Isolation Forest), ha dimostrato la fattibilità tecnica ed economica del passaggio da una manutenzione reattiva e periodica a una diagnostica predittiva e in tempo reale.

I risultati sperimentali esposti nel Capitolo 4 hanno evidenziato come l'implementazione tecnologica riesca a garantire standard diagnostici elevati. In particolare, con una **Recall (Sensibilità) del 91.15%**, il sistema si è dimostrato straordinariamente capace di intercettare e notificare quasi la totalità delle perdite d'acqua, comprese quelle occulte e le micro-perdite notturne, eventi storicamente sfuggenti ai tradizionali controlli bimestrali e responsabili dei maggiori danni strutturali e aggravi economici. Il modello non supervisionato ha superato i limiti degli allarmi basati su soglie fisse, bilanciando efficacia predittiva ed oneri computazionali. 

Nonostante una fisiologica percentuale di falsi allarmi, derivante dall'intrinseca aleatorietà del fattore umano all'interno delle scuole (pulizie straordinarie, attività extra-curriculari), la scalabilità del backend ASGI e del broker MQTT ha assicurato tempi di latenza irrisori (50-80 millisecondi per pacchetto), dimostrando che il prototipo è pronto a sostenere scenari su vasta scala, abbracciando centinaia di istituti.

## 5.2 Limiti della soluzione proposta

Ogni approccio di ricerca porta con sé margini di perfettibilità. Attualmente, la limitazione principale dell'infrastruttura di *AcquaSmart* risiede proprio nella fase di "warm-up" dell'algoritmo Isolation Forest: nei primi giorni di attività presso un nuovo plesso scolastico, l'assenza di uno storico dati sufficientemente stratificato porta l'algoritmo a una momentanea iper-sensibilità, incrementando la generazione di falsi positivi (la cosiddetta *alert fatigue* per gli operatori). 
Inoltre, la dipendenza esclusiva da connettività Wi-Fi/Cloud in alcuni nodi IoT potrebbe rappresentare un collo di bottiglia in plessi dove l'infrastruttura di rete è precaria o soggetta a blackout energetici. 

## 5.3 Roadmap per sviluppi futuri

Il potenziale tracciato da *AcquaSmart* apre a scenari di estensione e integrazione decisamente ambiziosi. Le direttrici principali per l'evoluzione del progetto si articolano su tre livelli:

1. **Integrazione con i sistemi BMS (Building Management Systems)**: La piattaforma dovrà essere integrata a livello API con i software di automazione degli edifici già eventualmente in uso presso l'ente pubblico. Ciò consentirebbe di incrociare i flussi di consumo idrico con altre variabili ambientali (presenza umana nelle aule, riscaldamento, sistemi antincendio), trasformando il dato vettoriale in un approccio olistico al risparmio delle risorse (Smart Building).

2. **Edge AI ed elaborazione distribuita**: Per ovviare alla dipendenza dalla connettività Cloud, le logiche di Machine Learning potranno essere "miniaturizzate" e trasferite direttamente a bordo del microcontrollore (Edge Computing o TinyML). Questo ridurrebbe i costi di invio dati su reti a consumo, permettendo al sensore di trasmettere esclusivamente il segnale di "anomalia rilevata" piuttosto che il flusso continuo dei consumi (telemetria aggregata).

3. **Espansione Multi-Utility**: Il paradigma analitico fondato in questo lavoro è facilmente esportabile. Adottando l'architettura già collaudata, il sistema potrà essere dotato di sensori per il monitoraggio dei quadri elettrici (assorbimenti anomali, power quality) e del gas metano, centralizzando la diagnostica energetica di ogni edificio all'interno di un'unica dashboard unificata per i gestori del patrimonio immobiliare.

## 5.4 Considerazioni finali

Il percorso di ricerca condotto ha dimostrato che l'innovazione tecnologica, se applicata con pragmatismo alle infrastrutture pubbliche, può generare un impatto tangibile. *AcquaSmart* non è solo un esercizio accademico o un prototipo isolato, ma rappresenta un *proof of concept* concreto per la transizione digitale della Pubblica Amministrazione. 
L'adozione di paradigmi Open Source (Python, MQTT, SQLite) e architetture leggere (FastAPI) dimostra che la sostenibilità ambientale (risparmio idrico) e la sostenibilità economica (basso costo di implementazione) possono procedere di pari passo. Il monitoraggio idrico intelligente è, in definitiva, il primo passo essenziale verso la realizzazione di una vera *Smart City*, in cui i dati guidano le decisioni per preservare i beni più preziosi della comunità.
L'impiego sinergico di sensori a basso costo e di Intelligenze Artificiali adattive rappresenta, ad oggi, l'unica risposta concreta e sostenibile alle sfide poste dal decadimento delle infrastrutture civili e dalla transizione ecologica. *AcquaSmart* dimostra che la digitalizzazione del settore idrico pubblico non è più solo una remota speculazione ingegneristica, ma uno strumento immediatamente implementabile, capace di generare un rapido ritorno sull'investimento (ROI) salvaguardando il bene primario più prezioso per la collettività: l'acqua.
