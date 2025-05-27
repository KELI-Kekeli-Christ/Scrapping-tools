import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
EXCEL_FILE = "liens.xlsx"
LINKEDIN_EMAIL = "hisciences331@gmail.com"
LINKEDIN_PASSWORD = "58590303#christ972"
echecs=0
success=0
# --- SETUP SELENIUM ---
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)

# --- ETAPE 1 : Connexion LinkedIn ---
driver.get("https://www.linkedin.com/checkpoint/lg/sign-in-another-account")

# Saisie de l'identifiant
email_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
email_input.send_keys(LINKEDIN_EMAIL)

# Saisie du mot de passe
password_input = driver.find_element(By.ID, "password")
password_input.send_keys(LINKEDIN_PASSWORD)

# Soumettre le formulaire
submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
submit_btn.click()

# --- ETAPE 2 : Lecture des liens depuis Excel ---
df = pd.read_excel(EXCEL_FILE)
liens = df.iloc[:, 1].dropna().tolist()

# --- ETAPE 3 : Visiter les liens et cliquer sur le bouton ember ---
for lien in liens:
    print(f"Ouverture de : {lien}")
    driver.get(lien)
    time.sleep(3)

    try:
        bouton = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@aria-label, 'Invite') and contains(@aria-label, 'connect')]")
        ))
        bouton.click()
        print("Bouton cliqué avec succès.")
        success += 1
        print(f"Succès : {success}")

    except Exception as e:
        echecs += 1
        print(f"Échec pour le lien {lien}. Erreur : {e}")
        print(f"Erreur lors du clic : {e} ")
        print(f"Échecs : {echecs}")

# --- FIN ---
print("Tous les liens ont été traités.")
print(f"Succès : {success} | Erreurs : {echecs}")

# driver.quit()
