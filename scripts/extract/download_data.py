from app.v1.scripts.extract.gsod import download_gsod_data
from app.v1.scripts.extract.storm_events import get_file_list, filter_files, download_storm_events_data

years = range(2015, 2021)

files = get_file_list()
filtered_files = filter_files(files, years)

if filtered_files:
    print(f"Fichiers filtrés à télécharger : {filtered_files}")
    download_storm_events_data(filtered_files)
else:
    print("Aucun fichier trouvé pour les années spécifiées.")

download_gsod_data(years)
