import os
from tqdm import tqdm

GSOD_PROCESSED_DIR = "data/processed/gsod/"

def load_gsod_to_hadoop(hdfs_client):
    for year in tqdm(os.listdir(GSOD_PROCESSED_DIR), desc="Chargement des GSOD dans HDFS", unit="fichier"):
        year_dir = os.path.join(GSOD_PROCESSED_DIR, year)

        if os.path.isdir(year_dir):
            hdfs_year_dir = f"/gsod/{year}"

            try:
                if not hdfs_client.status(hdfs_year_dir, strict=False):
                    hdfs_client.makedirs(hdfs_year_dir)
            except Exception as e:
                print(f"Erreur lors de la création du répertoire {hdfs_year_dir}: {e}")
                continue

            # Charger les fichiers CSV dans HDFS
            for file in os.listdir(year_dir):
                if file.endswith("_cleaned.csv"):
                    local_file_path = os.path.join(year_dir, file)
                    hdfs_file_path = os.path.join(hdfs_year_dir, file)

                    try:
                        hdfs_client.upload(hdfs_file_path, local_file_path)
                        print(f"Fichier {file} chargé vers HDFS sous {hdfs_file_path}")
                    except Exception as e:
                        print(f"Erreur lors du chargement du fichier {file} vers HDFS: {e}")

