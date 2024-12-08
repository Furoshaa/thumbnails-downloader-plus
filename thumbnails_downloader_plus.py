import os
import json
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote

# Chemins de répertoire
dossier_script = os.path.dirname(os.path.abspath(__file__))
dossier_lpl = os.path.join(dossier_script, '..', 'playlists')
dossier_thumbnails = dossier_script
base_url = "https://thumbnails.libretro.com"

# Extraction du nom de jeu en supprimant les parenthèses et autres caractères inutiles
def extract_game_name(rom_label):
    game_name = rom_label.replace("&", "_")
    if "-" in game_name:
        game_name = game_name.split("-")[0].strip()
    return re.sub(r'\(.*?\)', '', game_name).strip()

# Fonction principale pour vérifier les thumbnails
def verifier_thumbnails():
    resultats = {}

    for nom_fichier in os.listdir(dossier_lpl):
        if nom_fichier.endswith('.lpl'):
            chemin_fichier = os.path.join(dossier_lpl, nom_fichier)
            console = os.path.splitext(nom_fichier)[0]
            
            # Charger le fichier .lpl
            try:
                with open(chemin_fichier, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except UnicodeDecodeError:
                with open(chemin_fichier, 'r', encoding='latin-1') as f:
                    data = json.load(f)

            total_jeux = 0
            jeux_avec_thumbnail = 0

            for item in data.get('items', []):
                total_jeux += 1
                nom_jeu = item['label']
                thumbnail_local = os.path.join(dossier_thumbnails, console, 'Named_Boxarts', f"{nom_jeu}.png")

                if os.path.isfile(thumbnail_local):
                    jeux_avec_thumbnail += 1
                else:
                    print(f"Le jeu '{nom_jeu}' dans '{console}' n'a pas de thumbnail en local.")
                    
                    # Si manquant, récupérer les thumbnails en ligne
                    selected_thumbnail = fetch_possible_thumbnails(console, nom_jeu)
                    if selected_thumbnail:
                        print(f"Thumbnail choisi pour '{nom_jeu}' : {selected_thumbnail}")
                    else:
                        print(f"Aucun thumbnail trouvé pour '{nom_jeu}'.")

            pourcentage = (jeux_avec_thumbnail / total_jeux) * 100 if total_jeux > 0 else 0
            resultats[console] = pourcentage
            print(f"\nPourcentage de jeux avec thumbnail pour {console}: {pourcentage:.2f}%\n")

    return resultats

# Fonction pour récupérer les options de thumbnails pour toutes les catégories
def fetch_possible_thumbnails(console_dir, rom_label):
    game_name = extract_game_name(rom_label).replace(" ", "%20")
    categories = ["Named_Boxarts", "Named_Snaps", "Named_Titles"]
    thumbnails = set()  # Utiliser un set pour éviter les doublons

    for category in categories:
        search_url = f"{base_url}/{console_dir}/{category}/"
        response = requests.get(search_url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            for link in soup.find_all('a'):
                file_name = link.get('href')
                if file_name and game_name.lower() in file_name.lower():
                    thumbnails.add(file_name)  # Ajouter uniquement le nom du fichier, sans catégorie

    if thumbnails:
        return prompt_user_choice(list(thumbnails), console_dir, rom_label)
    else:
        print(f"Aucun thumbnail trouvé pour '{rom_label}'.")
        return None

# Fonction pour afficher les options et demander un choix
def prompt_user_choice(thumbnails, console_dir, rom_label):
    print(f"\nThumbnails possibles pour '{rom_label}':\n")
    
    for index, thumb in enumerate(thumbnails):
        readable_name = unquote(thumb)
        print(f"{index + 1}. {readable_name}")
    
    try:
        choice = int(input("\nEntrez le numéro de votre choix : ")) - 1
        if 0 <= choice < len(thumbnails):
            selected_thumbnail = thumbnails[choice]
            print(f"\nVous avez choisi : {selected_thumbnail}")
            
            # Téléchargement pour toutes les catégories
            download_thumbnails(console_dir, selected_thumbnail, rom_label)
            return selected_thumbnail
        else:
            print("Choix invalide.")
            return None
    except ValueError:
        print("Entrée non valide.")
        return None

# Fonction pour télécharger un thumbnail dans toutes les catégories
def download_thumbnails(console_dir, thumbnail, rom_label):
    categories = ["Named_Boxarts", "Named_Snaps", "Named_Titles"]
    for category in categories:
        search_url = f"{base_url}/{console_dir}/{category}/"
        file_url = f"{search_url}{thumbnail}"
        response = requests.get(file_url, stream=True)

        if response.status_code == 200:
            filename = f"{rom_label}.png"
            category_dir = os.path.join(dossier_thumbnails, console_dir, category)

            if not os.path.exists(category_dir):
                os.makedirs(category_dir)

            with open(os.path.join(category_dir, filename), 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            print(f"Thumbnail téléchargé et sauvegardé dans '{category}': {filename}")
        else:
            print(f"Erreur lors du téléchargement du thumbnail dans {category}.")

# Exécuter la fonction
resultats = verifier_thumbnails()

# Afficher les résultats finaux
print("\nRésumé du pourcentage de jeux avec thumbnails par console:")
for console, pourcentage in resultats.items():
    print(f"{console}: {pourcentage:.2f}%")
