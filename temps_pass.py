import json
import os
import time
from tkinter import *
from tkinter import simpledialog

# Créez un dictionnaire pour stocker les chronomètres
chronometres = {}

def charger_donnees():
    if os.path.exists('donnees.json'):
        with open('donnees.json', 'r') as fichier_json:
            contenu = fichier_json.read()
            if contenu:  # Vérifie si le fichier n'est pas vide
                return json.loads(contenu)
    return {}  # Si le fichier est vide ou n'existe pas, retourne un dictionnaire vide

def sauvegarder_donnees():
    with open("donnees.json", 'w') as f:
        json.dump(chronometres, f)

def ajouter_element(liste):
    nouveau_nom = simpledialog.askstring("Nouvel élément", "Entrez le nom du nouvel élément:")
    if nouveau_nom:
        chronometres[nouveau_nom] = {'start_time': 0, 'temps_passer': 0}
        sauvegarder_donnees()
        liste.insert(END, nouveau_nom)

def supprimer_element(liste):
    selection = liste.curselection()
    if selection:
        nom = liste.get(selection[0])
        if nom in chronometres:
            del chronometres[nom]  # Supprime l'élément du dictionnaire de chronomètres
            sauvegarder_donnees()  # Enregistrez les données mises à jour dans le fichier JSON
        liste.delete(selection)  # Supprime l'élément de la liste

def afficher_details(liste):
    selection = liste.curselection()
    if selection:
        nom = liste.get(selection[0])
        chrono = chronometres.get(nom)
        if chrono:
            global fenetre_detail
            fenetre_detail = Toplevel()
            fenetre_detail.geometry('400x300')
            fenetre_detail.title(f"Détails de l'élément : {nom}")

            Label(fenetre_detail, text=f"Nom de l'élément : {nom}").pack()
            
            if 'temps_passer' in chrono:
                temps_ecoule = chrono['temps_passer']
                heures = int(temps_ecoule / 3600)
                minutes = int((temps_ecoule % 3600) / 60)
                secondes = int(temps_ecoule % 60)
                label_chronometre = Label(fenetre_detail, text=f"Temps total : {heures:02d}:{minutes:02d}:{secondes:02d}")
            else:
                label_chronometre = Label(fenetre_detail, text="Temps total : 00:00:00")

            label_chronometre.pack()

            bouton_demarrer = Button(fenetre_detail, text="Démarrer le chronomètre", command=lambda nom=nom: demarrer_chronometre(nom, bouton_demarrer, bouton_arreter, label_chronometre))
            bouton_demarrer.pack()

            bouton_arreter = Button(fenetre_detail, text="Arrêter le chronomètre", state=DISABLED, command=lambda nom=nom: arreter_chronometre(nom, bouton_demarrer, bouton_arreter))
            bouton_arreter.pack()

            bouton_retour = Button(fenetre_detail, text="Retour", command=fenetre_detail.destroy)
            bouton_retour.pack()


def demarrer_chronometre(nom, bouton_demarrer, bouton_arreter, label_chronometre):
    bouton_demarrer.config(state=DISABLED)
    bouton_arreter.config(state=NORMAL)

    if nom in chronometres:
        if 'start_time' in chronometres[nom]:
            chronometres[nom]['start_time'] = time.time() - chronometres[nom]['temps_passer']  # Redémarrage avec le temps passé précédent
    else:
        chronometres[nom] = {'start_time': time.time(), 'temps_passer': 0}

    def mise_a_jour_chronometre():
        if nom in chronometres:
            temps_ecoule = int(chronometres[nom]['temps_passer'])
            heures = temps_ecoule // 3600
            minutes = (temps_ecoule % 3600) // 60
            secondes = temps_ecoule % 60
            label_chronometre.config(text=f"Temps total : {heures:02d}:{minutes:02d}:{secondes:02d}")
            chronometres[nom]['temps_passer'] += 1  # Incrémentez le temps passé d'une seconde
            chronometres[nom]['update_id'] = fenetre_detail.after(1000, mise_a_jour_chronometre)  # Mise à jour toutes les 1000 ms (1 seconde)

    chronometres[nom]['update_id'] = fenetre_detail.after(1000, mise_a_jour_chronometre)  # Initialiser la boucle de mise à jour

def arreter_chronometre(nom, bouton_demarrer, bouton_arreter):
    bouton_demarrer.config(state=NORMAL)
    bouton_arreter.config(state=DISABLED)

    if nom in chronometres:
        fenetre_detail.after_cancel(chronometres[nom]['update_id'])  # Arrête la boucle de mise à jour du chronomètre
        chronometres[nom]['start_time'] = time.time()  # Mettez à jour le temps de départ pour éviter de continuer le comptage
        sauvegarder_donnees()

def ma_fenetre():
    global chronometres
    chronometres = charger_donnees()

    fenetre = Tk()
    fenetre.geometry('400x300')
    fenetre.title('Chronomètres personnels')

    choix_label = Label(fenetre, text="Quel fichier voulez-vous choisir ?")
    choix_label.pack()

    liste = Listbox(fenetre)
    liste.pack()

    for nom in chronometres:
        liste.insert(END, nom)

    bouton = Checkbutton(fenetre, text="Nouveau fichier ?", command=lambda: ajouter_element(liste))
    bouton.pack()

    bouton_details = Button(fenetre, text="Afficher les détails", command=lambda: afficher_details(liste))
    bouton_details.pack()

    bouton_supprimer = Button(fenetre, text="Supprimer", command=lambda: supprimer_element(liste))
    bouton_supprimer.pack()

    bouton_fermer = Button(fenetre, text="Fermer", command=fenetre.quit)
    bouton_fermer.pack()

    fenetre.mainloop()

if __name__ == '__main__':
    ma_fenetre()