from PIL import Image, ImageDraw, ImageFont
import os

def create_split_collages():
    panels = [
        ("c:/Pregetto_tesi_sperimentale/screenshot_1_login.png", "1. Schermata di Accesso (Autenticazione)"),
        ("c:/Pregetto_tesi_sperimentale/screenshot_2_dashboard.png", "2. Panoramica Globale e Dettaglio Plesso"),
        ("c:/Pregetto_tesi_sperimentale/screenshot_3_reali.png", "3. Confronto Consumi (Dati Telemetrici vs Bollette)"),
        ("c:/Pregetto_tesi_sperimentale/screenshot_4_allarmi.png", "4. Storico e Gestione Allarmi")
    ]
    
    processed_images = []
    
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()

    label_height = 60
    padding = 10
    
    for path, text in panels:
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
        
        processed_images.append(bordered)

    # Immagine 1 (1 e 2)
    w, h = processed_images[0].size
    img1 = Image.new('RGB', (w * 2, h), color=(255, 255, 255))
    img1.paste(processed_images[0], (0, 0))
    img1.paste(processed_images[1], (w, 0))
    path1 = "c:/Pregetto_tesi_sperimentale/acquasmart_collage_1_2.jpg"
    img1.save(path1, quality=95)
    print(f"Salvata prima parte in {path1}")

    # Immagine 2 (3 e 4)
    img2 = Image.new('RGB', (w * 2, h), color=(255, 255, 255))
    img2.paste(processed_images[2], (0, 0))
    img2.paste(processed_images[3], (w, 0))
    path2 = "c:/Pregetto_tesi_sperimentale/acquasmart_collage_3_4.jpg"
    img2.save(path2, quality=95)
    print(f"Salvata seconda parte in {path2}")

if __name__ == "__main__":
    create_split_collages()
