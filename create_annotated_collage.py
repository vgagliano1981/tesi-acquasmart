from PIL import Image, ImageDraw, ImageFont
import os

def create_annotated_collage():
    # Definisci i file e i relativi testi
    panels = [
        ("c:/Pregetto_tesi_sperimentale/screenshot_1_login.png", "1. Schermata di Accesso (Autenticazione)"),
        ("c:/Pregetto_tesi_sperimentale/screenshot_2_dashboard.png", "2. Panoramica Globale e Dettaglio Plesso"),
        ("c:/Pregetto_tesi_sperimentale/screenshot_3_reali.png", "3. Confronto Consumi (Dati Telemetrici vs Bollette)"),
        ("c:/Pregetto_tesi_sperimentale/screenshot_4_allarmi.png", "4. Storico e Gestione Allarmi")
    ]
    
    processed_images = []
    
    # Prova a caricare un font di sistema, altrimenti usa il default
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()

    label_height = 60  # Altezza della banda bianca per il testo
    padding = 10
    
    for path, text in panels:
        img = Image.open(path)
        # Crea una nuova immagine più alta per contenere il testo
        new_img = Image.new('RGB', (img.width, img.height + label_height), color=(240, 240, 240))
        new_img.paste(img, (0, 0))
        
        draw = ImageDraw.Draw(new_img)
        # Calcola la larghezza del testo per centrarlo
        # (se non supportato textlength per fallback font, usiamo un'approssimazione)
        try:
            text_width = draw.textlength(text, font=font)
        except:
            text_width = len(text) * 20
            
        x = (new_img.width - text_width) // 2
        y = img.height + 10
        draw.text((x, y), text, font=font, fill=(30, 30, 30))
        
        # Aggiungi un piccolo bordo (padding) all'immagine
        bordered = Image.new('RGB', (new_img.width + padding*2, new_img.height + padding*2), color=(255, 255, 255))
        bordered.paste(new_img, (padding, padding))
        
        processed_images.append(bordered)

    # Crea la griglia 2x2
    w, h = processed_images[0].size
    collage_width = w * 2
    collage_height = h * 2
    
    collage = Image.new('RGB', (collage_width, collage_height), color=(255, 255, 255))
    
    collage.paste(processed_images[0], (0, 0))
    collage.paste(processed_images[1], (w, 0))
    collage.paste(processed_images[2], (0, h))
    collage.paste(processed_images[3], (w, h))
    
    output_path = "c:/Pregetto_tesi_sperimentale/acquasmart_collage_annotato.jpg"
    collage.save(output_path, quality=95)
    print(f"Collage annotato salvato in {output_path}")

if __name__ == "__main__":
    create_annotated_collage()
