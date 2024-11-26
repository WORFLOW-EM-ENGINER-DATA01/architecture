import os
from tqdm import tqdm


STORM_EVENTS_PROCESSED_DIR = "data/processed/storm_events/"

from tqdm import tqdm
import os

def load_storm_events_to_hadoop(hdfs_client):
    for file in tqdm(os.listdir(STORM_EVENTS_PROCESSED_DIR), desc="Chargement des Storm Events dans HDFS", unit="fichier"):

        if file.endswith("_cleaned.csv"):

            year = file.split("_")[0]
            local_file_path = os.path.join(STORM_EVENTS_PROCESSED_DIR, file)
            hdfs_year_dir = f"/storm_events/{year}"
            hdfs_file_path = f"{hdfs_year_dir}/{file}"

            try:

                if not hdfs_client.status(hdfs_year_dir, strict=False):
                    hdfs_client.makedirs(hdfs_year_dir)

                # Charge le fichier dans HDFS
                hdfs_client.upload(hdfs_file_path, local_file_path)
                print(f"Fichier {file} chargé vers HDFS sous {hdfs_file_path}")
            except Exception as e:
                print(f"Erreur lors du chargement du fichier {file} vers HDFS: {e}")
