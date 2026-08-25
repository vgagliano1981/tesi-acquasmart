import os
from playwright.sync_api import sync_playwright

html_content = """
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>mermaid.initialize({startOnLoad:true});</script>
</head>
<body>
  <div id="diag1" class="mermaid">
graph LR
    subgraph Livello di Campo Edge
    S1[Contatore Principale] -->|Letture Idriche| B(Broker MQTT)
    S2[Sub-Sensore 1] -->|Letture Idriche| B
    S3[Sensore Pressione] -->|Stabilità Impianto| B
    end

    subgraph Livello di Trasporto Middleware
    B{Mosquitto Broker}
    end

    subgraph Livello Applicativo Backend
    B -->|Subscribe Topic| F(FastAPI Backend)
    F -->|Elaborazione e Inferenza| ML[Isolation Forest]
    F -->|Persistenza| DB[(SQLite / PostgreSQL)]
    end
    
    subgraph Frontend Client
    DB --> F
    F -->|REST API JSON| UI[Dashboard Web AcquaSmart]
    end
  </div>
  
  <div id="diag2" class="mermaid">
erDiagram
    SCUOLA {
        int id PK
        string nome
        string indirizzo
        string codice_meccanografico
    }
    SENSORE {
        int id PK
        int scuola_id FK
        string topic_mqtt
        string tipo
        boolean is_main
    }
    LETTURA {
        int id PK
        int sensore_id FK
        datetime timestamp
        float valore_litri
        boolean is_anomalia
        float anomaly_score
        boolean is_ground_truth_anomaly
        string ground_truth_type
    }
    
    SCUOLA ||--o{ SENSORE : "possiede"
    SENSORE ||--o{ LETTURA : "genera"
  </div>
</body>
</html>
"""

def render_diagrams():
    html_path = "c:/Pregetto_tesi_sperimentale/mermaid_temp.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file:///{html_path}")
        
        # Wait for SVG to be rendered
        page.wait_for_selector("#diag1 svg")
        page.wait_for_selector("#diag2 svg")
        
        # Take element screenshots
        diag1 = page.locator("#diag1")
        diag1.screenshot(path="c:/Pregetto_tesi_sperimentale/architettura_sistema.png")
        
        diag2 = page.locator("#diag2")
        diag2.screenshot(path="c:/Pregetto_tesi_sperimentale/schema_er.png")
        
        browser.close()
        
    print("Diagrams rendered and saved.")

if __name__ == "__main__":
    render_diagrams()
