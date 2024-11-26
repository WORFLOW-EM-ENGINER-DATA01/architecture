import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm  # Pour afficher une barre de progression

GSOD_BASE_URL = "https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/"
GSOD_RAW_DIR = "data/raw/gsod/"

def download_gsod_data(years, max_files_per_year=5):
    os.makedirs(GSOD_RAW_DIR, exist_ok=True)

    for year in tqdm(years, desc="Téléchargement des données GSOD", unit="année"):
        url = f"{GSOD_BASE_URL}{year}/"
        year_dir = os.path.join(GSOD_RAW_DIR, str(year))
        
        os.makedirs(year_dir, exist_ok=True)

        response = requests.get(url)
        if response.status_code == 200:
            print(f"Page récupérée pour l'année {year}")
        else:
            print(f"Erreur lors du téléchargement de la page pour l'année {year}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        files = [link.get('href') for link in soup.find_all("a") if link.get('href') and link.get('href').endswith(".csv")]

        files_to_download = files[:max_files_per_year]

        for file in tqdm(files_to_download, desc=f"Téléchargement fichiers {year}", unit="fichier"):
            file_url = url + file
            output_file = os.path.join(year_dir, file)

            if not os.path.exists(output_file):
                print(f"Téléchargement de {file}...")
                file_response = requests.get(file_url, stream=True)
                if file_response.ok:
                    with open(output_file, "wb") as f:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Fichier téléchargé : {output_file}")
                else:
                    print(f"Échec du téléchargement pour {file}")
            else:
                print(f"Le fichier {file} existe déjà.")


