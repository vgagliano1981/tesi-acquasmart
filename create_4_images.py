from PIL import Image, ImageDraw, ImageFont
import os

def create_individual_images():
    panels = [
        ("c:/Pregetto_tesi_sperimentale/screenshot_1_login.png", "1. Schermata di Accesso (Autenticazione)", "acquasmart_screen_1.jpg"),
        ("c:/Pregetto_tesi_sperimentale/screenshot_2_dashboard.png", "2. Panoramica Globale e Dettaglio Plesso", "acquasmart_screen_2.jpg"),
        ("c:/Pregetto_tesi_sperimentale/screenshot_3_reali.png", "3. Confronto Consumi (Dati Telemetrici vs Bollette)", "acquasmart_screen_3.jpg"),
        ("c:/Pregetto_tesi_sperimentale/screenshot_4_allarmi.png", "4. Storico e Gestione Allarmi", "acquasmart_screen_4.jpg")
    ]
    
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()

    label_height = 60
    padding = 10
    
    for path, text, out_name in panels:
        img = Image.open(path)
        new_img = Image.new('RGB', (img.width, img.height + label_height), color=(240, 240, 240))
        new_img.paste(img, (0, 0))
        
        draw = ImageDraw.Draw(new_img)
        try:
            text_width = draw.textlength(text, font=font)
        except:
            text_width = len(text) * 20
            
        x = (new_img.width - text_width) // 2
        y = img.height + 10
        draw.text((x, y), text, font=font, fill=(30, 30, 30))
        
        bordered = Image.new('RGB', (new_img.width + padding*2, new_img.height + padding*2), color=(255, 255, 255))
        bordered.paste(new_img, (padding, padding))
        
        out_path = f"c:/Pregetto_tesi_sperimentale/{out_name}"
        bordered.save(out_path, quality=95)
        print(f"Salvata immagine {out_name}")

if __name__ == "__main__":
    create_individual_images()
