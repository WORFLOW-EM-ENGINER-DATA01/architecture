import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm 

STORM_EVENTS_URL = "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/"
STORM_EVENTS_OUTPUT_DIR = "data/raw/storm_events/"

def get_file_list():
    response = requests.get(STORM_EVENTS_URL)
    
    if response.status_code == 200:
        print("Page récupérée avec succès.")
    else:
        print(f"Erreur lors du téléchargement de la page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    files = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.startswith("StormEvents_details-ftp_v1.0_") and href.endswith(".csv.gz"):
            files.append(href)

    return files

def filter_files(files, years):
    filtered_files = [file for file in files if any(str(year) in file for year in years)]
    
    return filtered_files

def download_storm_events_data(files):
    os.makedirs(STORM_EVENTS_OUTPUT_DIR, exist_ok=True)
    
    for file in tqdm(files, desc="Téléchargement des Storm Events", unit="fichier"):
        url = STORM_EVENTS_URL + file
        output_file = os.path.join(STORM_EVENTS_OUTPUT_DIR, file)
        
        if not os.path.exists(output_file):
            response = requests.get(url, stream=True)
            
            if response.ok:
                with open(output_file, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            else:
                print(f"Échec du téléchargement pour : {file}")
        else:
            print(f"Fichier déjà présent : {file}")
