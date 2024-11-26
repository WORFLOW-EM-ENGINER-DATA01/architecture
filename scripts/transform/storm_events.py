import pandas as pd
import gzip
import shutil
import os
from tqdm import tqdm
import re 

STORM_EVENTS_RAW_DIR = "data/raw/storm_events/"
STORM_EVENTS_DIR = "data/processed/storm_events/"

def decompress_storm_events_files():
    os.makedirs(STORM_EVENTS_RAW_DIR, exist_ok=True)
    
    for file in tqdm(os.listdir(STORM_EVENTS_RAW_DIR), desc="Décompression des fichiers Storm Events", unit="fichier"):
        if file.endswith(".gz"):
            input_file = os.path.join(STORM_EVENTS_RAW_DIR, file)
            output_file = os.path.join(STORM_EVENTS_RAW_DIR, "csv/",file[:-3]) 
            
            print(f"Décompression de {input_file} vers {output_file}...")
            with gzip.open(input_file, "rb") as f_in:
                with open(output_file, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(f"Fichier décompressé : {output_file}")

def preprocess_storm_events():
    STORM_EVENTS_CSV_DIR = os.path.join(STORM_EVENTS_RAW_DIR, "csv/")
    os.makedirs(STORM_EVENTS_DIR, exist_ok=True)
    
    for file in tqdm(os.listdir(STORM_EVENTS_CSV_DIR), desc="Traitement des fichiers Storm Events", unit="fichier"):
        if file.endswith(".csv"):
            input_file = os.path.join(STORM_EVENTS_CSV_DIR, file)
            
            # Utilisation d'une expression régulière pour extraire l'année
            match = re.search(r'd(\d{4})', file)  # Cherche un 'd' suivi de 4 chiffres
            if match:
                year = match.group(1)  # L'année extraite
            else:
                print(f"Erreur : Année non trouvée dans le fichier {file}")
                continue
            
            # Définir le fichier de sortie
            output_file = os.path.join(STORM_EVENTS_DIR, f"{year}_cleaned.csv")
            
            # Charger les données
            df = pd.read_csv(input_file)
            
            # Garder uniquement les colonnes nécessaires
            df = df[["BEGIN_DATE_TIME", "END_DATE_TIME", "EVENT_TYPE", "STATE", "CZ_NAME", "INJURIES_DIRECT", "DEATHS_DIRECT"]]
            
            # Renommer les colonnes
            df.columns = ["start_time", "end_time", "event_type", "state", "county", "injuries", "deaths"]
            
            # Sauvegarder le fichier nettoyé
            df.to_csv(output_file, index=False)
            print(f"Cleaned Storm Events saved to: {output_file}")