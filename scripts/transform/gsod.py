import os
import pandas as pd
from tqdm import tqdm

GSOD_RAW_DIR = "data/raw/gsod/"
GSOD_PROCESSED_DIR = "data/processed/gsod/"

def clean_gsod_data(years):
    # Créer le répertoire de base pour les fichiers traités s'il n'existe pas
    os.makedirs(GSOD_PROCESSED_DIR, exist_ok=True)

    # Pour chaque année dans la liste des années
    for year in tqdm(years, desc="Nettoyage des données GSOD", unit="année"):
        # Construire le chemin vers le dossier de l'année dans le répertoire brut
        year_raw_dir = os.path.join(GSOD_RAW_DIR, str(year))
        
        # Vérifie si le dossier de l'année existe
        if not os.path.exists(year_raw_dir):
            print(f"Le répertoire pour l'année {year} n'existe pas.")
            continue
        
        # Créer un sous-dossier pour l'année dans le répertoire traité
        year_processed_dir = os.path.join(GSOD_PROCESSED_DIR, str(year))
        os.makedirs(year_processed_dir, exist_ok=True)

        # Liste les fichiers CSV dans le répertoire de l'année
        files = [f for f in os.listdir(year_raw_dir) if f.endswith(".csv")]
        
        if not files:
            print(f"Aucun fichier CSV trouvé pour l'année {year}.")
            continue
        
        # Traitement de chaque fichier CSV pour l'année
        for file in files:
            input_file = os.path.join(year_raw_dir, file)
            output_file = os.path.join(year_processed_dir, f"{file[:-4]}_cleaned.csv")  # Fichier nettoyé

            print(f"Traitement du fichier : {input_file}")
            
            # Charger les données brutes
            df = pd.read_csv(input_file)
            
            # Supprimer les colonnes inutiles
            columns_to_keep = ["STATION", "DATE", "TEMP", "DEWP", "WDSP", "PRCP"]
            df = df[columns_to_keep]
            
            # Renommer les colonnes pour correspondre au schéma Hive
            df.columns = ["station", "date", "temp", "dew_point", "wind_speed", "precipitation"]
            
            # Nettoyer les valeurs manquantes
            df = df.dropna()
            
            # Sauvegarder le fichier nettoyé dans le dossier de l'année
            df.to_csv(output_file, index=False)
            print(f"Cleaned data saved to: {output_file}")
