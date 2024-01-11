import spacy
import tkinter as tk
from huggingface_hub import HfApi, list_models

HF_API_KEY = "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"

# Charger le modèle de langue français de spaCy
nlp = spacy.load("fr_core_news_sm")

def extraction_mots_cles(phrase):
    doc = nlp(phrase)
    # Extraire les lemmes des noms et des verbes
    mots_cles = [token.lemma_ for token in doc if token.pos_ in ["NOUN", "PROPN", "VERB"]]
    print(f"Mots-clés extraits de la phrase : {mots_cles}")
    return mots_cles

def detecter_tache_specifique(phrase):
    doc = nlp(phrase)
    # Identifier les entités nommées qui peuvent indiquer la tâche spécifique
    entites_nommees = [entite.text.lower() for entite in doc.ents]
    return entites_nommees

def recherche_meilleur_modele(tache_recherchee):
    api = HfApi()
    
    try:
        print(f"Tâche de recherche spécifiée : {tache_recherchee}")
        
        # Récupérer la liste de tous les modèles
        tous_les_modeles = list(list_models())
        print(f"Nombre total de modèles disponibles : {len(tous_les_modeles)}")
        
        # Filtrer les modèles en fonction de la tâche spécifiée
        modeles_appropries = [modele for modele in tous_les_modeles if tache_recherchee.lower() in modele.tags]
        print(f"Nombre de modèles appropriés : {len(modeles_appropries)}")
        
        # Trier les modèles en fonction de la popularité ou d'autres critères pertinents
        modeles_tries = sorted(modeles_appropries, key=lambda x: x.downloads, reverse=True)
        
        # Retourner le meilleur modèle (le plus téléchargé dans cet exemple)
        if modeles_tries:
            meilleur_modele = modeles_tries[0]
            print(f"Meilleur modèle trouvé : {meilleur_modele.modelId}")
            return meilleur_modele
        else:
            print("Aucun modèle approprié trouvé.")
            return None
    
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        return None

def recherche_modele_et_affiche_resultat():
    phrase_utilisateur = entry_phrase.get()
    
    # Extraction des mots-clés importants
    mots_cles = extraction_mots_cles(phrase_utilisateur)
    
    # Détection de la tâche spécifique
    tache_specifique = detecter_tache_specifique(phrase_utilisateur)
    
    if tache_specifique:
        # Utiliser la tâche spécifique comme tâche de recherche
        meilleur_modele = recherche_meilleur_modele(tache_specifique[0])
        if meilleur_modele:
            result_label.config(text=f"Le meilleur modèle pour la tâche '{tache_specifique[0]}' est : {meilleur_modele.modelId}")
        else:
            result_label.config(text=f"Aucun modèle n'a été trouvé pour la tâche '{tache_specifique[0]}'.")
    elif mots_cles:
        # Utiliser les mots-clés comme tâche de recherche
        meilleur_modele = recherche_meilleur_modele(mots_cles)
        if meilleur_modele:
            result_label.config(text=f"Le meilleur modèle pour la tâche '{' '.join(mots_cles)}' est : {meilleur_modele.modelId}")
        else:
            result_label.config(text=f"Aucun modèle n'a été trouvé pour la tâche '{' '.join(mots_cles)}'.")
    else:
        result_label.config(text="Aucun mot-clé important n'a été extrait de la phrase.")

# Créer une fenêtre
fenetre = tk.Tk()
fenetre.title("Recherche de Modèle Hugging Face avec spaCy")

# Créer et placer les widgets
label_phrase = tk.Label(fenetre, text="Quelle tâche souhaitez-vous effectuer ?")
label_phrase.pack(pady=10)

entry_phrase = tk.Entry(fenetre)
entry_phrase.pack(pady=10)

button_rechercher = tk.Button(fenetre, text="Rechercher", command=recherche_modele_et_affiche_resultat)
button_rechercher.pack(pady=10)

result_label = tk.Label(fenetre, text="")
result_label.pack(pady=10)

# Lancer la boucle principale
fenetre.mainloop()
