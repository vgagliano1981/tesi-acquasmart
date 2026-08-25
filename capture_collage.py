import time
from playwright.sync_api import sync_playwright
from PIL import Image

def capture_screenshots():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        
        # 1. Login
        print("Navigating to login...")
        page.goto("https://tesi-acquasmart.onrender.com/login.html", wait_until="networkidle")
        time.sleep(2)
        page.screenshot(path="c:/Pregetto_tesi_sperimentale/screenshot_1_login.png")
        
        # Effettua il login
        print("Logging in...")
        page.fill("#username", "amministratore")
        page.fill("#password", "amministratore")
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")
        time.sleep(3) # Wait for animations and data fetch
        
        # 2. Dashboard (Overview & Details)
        print("Capturing Dashboard...")
        page.screenshot(path="c:/Pregetto_tesi_sperimentale/screenshot_2_dashboard.png")
        
        # 3. Confronto Dati Reali
        print("Navigating to Dati Reali...")
        page.click("[data-view='dati-reali']")
        time.sleep(2)
        page.screenshot(path="c:/Pregetto_tesi_sperimentale/screenshot_3_reali.png")
        
        # 4. Gestione Alert (Allarmi)
        print("Navigating to Allarmi...")
        page.click("#nav-btn-allarmi")
        time.sleep(2)
        page.screenshot(path="c:/Pregetto_tesi_sperimentale/screenshot_4_allarmi.png")
        
        browser.close()

def create_collage():
    print("Creating collage...")
    images = [
        Image.open(f"c:/Pregetto_tesi_sperimentale/screenshot_{i}_{name}.png") 
        for i, name in [(1, 'login'), (2, 'dashboard'), (3, 'reali'), (4, 'allarmi')]
    ]
    
    # Calcola le dimensioni (griglia 2x2)
    widths, heights = zip(*(i.size for i in images))
    total_width = max(widths[0] + widths[1], widths[2] + widths[3])
    max_height = max(heights[0] + heights[2], heights[1] + heights[3])
    
    collage = Image.new('RGB', (total_width, max_height), color=(255, 255, 255))
    
    collage.paste(images[0], (0, 0))
    collage.paste(images[1], (widths[0], 0))
    collage.paste(images[2], (0, heights[0]))
    collage.paste(images[3], (widths[2], max(heights[0], heights[1])))
    
    collage_path = "c:/Pregetto_tesi_sperimentale/acquasmart_collage_reale.jpg"
    collage.save(collage_path, quality=90)
    print(f"Collage saved to {collage_path}")

if __name__ == "__main__":
    capture_screenshots()
    create_collage()
