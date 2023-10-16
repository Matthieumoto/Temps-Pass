from tkinter import *
from tkinter import simpledialog
from time import time
import pickle
import threading

# Crée un dictionnaire pour stocker les chronomètres par nom
chronometres = {}

def nouvelle_boite_dialogue(liste):
    fichier = simpledialog.askstring("Nouveau fichier", "Entrez le nom du fichier ou du dossier :")
    if fichier:
        liste.insert(END, fichier)
        chronometres[fichier] = {'temps_debut': None, 'temps_total': 0}
        sauvegarder_liste(liste)

def sauvegarder_liste(liste):
    fichiers = liste.get(0, END)
    with open('liste_fichiers.pickle', 'wb') as fichier:
        pickle.dump(fichiers, fichier)

def charger_liste(liste):
    try:
        with open('liste_fichiers.pickle', 'rb') as fichier:
            fichiers = pickle.load(fichier)
            for fichier in fichiers:
                liste.insert(END, fichier)
                chronometres[fichier] = {'temps_debut': None, 'temps_total': 0}
    except FileNotFoundError:
        pass

def actualiser_chronometre(nom, label_chronometre):
    if chronometres[nom]['temps_debut'] is not None:
        temps_actuel = time()
        temps_passe = temps_actuel - chronometres[nom]['temps_debut']
        temps_total = chronometres[nom]['temps_total'] + temps_passe
        heures, secondes = divmod(int(temps_total), 3600)
        minutes, secondes = divmod(secondes, 60)
        label_chronometre.config(text=f"Temps écoulé : {heures:02d}:{minutes:02d}:{secondes:02d}")
        fenetre_detail.after(1000, actualiser_chronometre, nom, label_chronometre)

def demarrer_chronometre(nom, bouton_demarrer, bouton_arreter, label_chronometre):
    if nom in chronometres and chronometres[nom]['temps_debut'] is None:
        chronometres[nom]['temps_debut'] = time()
        bouton_demarrer.config(state=DISABLED)
        bouton_arreter.config(state=NORMAL)
        actualiser_chronometre(nom, label_chronometre)

def arreter_chronometre(nom, bouton_demarrer, bouton_arreter):
    if nom in chronometres and chronometres[nom]['temps_debut'] is not None:
        temps_actuel = time()
        temps_passe = temps_actuel - chronometres[nom]['temps_debut']
        chronometres[nom]['temps_total'] += temps_passe
        chronometres[nom]['temps_debut'] = None
        bouton_demarrer.config(state=NORMAL)
        bouton_arreter.config(state=DISABLED)

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
            label_chronometre = Label(fenetre_detail, text="Temps écoulé : 00:00:00")
            label_chronometre.pack()

            bouton_demarrer = Button(fenetre_detail, text="Démarrer le chronomètre", command=lambda nom=nom: demarrer_chronometre(nom, bouton_demarrer, bouton_arreter, label_chronometre))
            bouton_demarrer.pack()

            bouton_arreter = Button(fenetre_detail, text="Arrêter le chronomètre", state=DISABLED, command=lambda nom=nom: arreter_chronometre(nom, bouton_demarrer, bouton_arreter))
            bouton_arreter.pack()

            bouton_retour = Button(fenetre_detail, text="Retour", command=fenetre_detail.quit)
            bouton_retour.pack()
            
            actualiser_chronometre(nom, label_chronometre)

def ma_fenetre():
    fenetre = Tk()
    fenetre.geometry('400x300')
    fenetre.title('Chronomètres personnels')

    choix_label = Label(fenetre, text="Quel fichier voulez-vous choisir ?")
    choix_label.pack()

    liste = Listbox(fenetre)
    liste.pack()

    charger_liste(liste)

    bouton = Checkbutton(fenetre, text="Nouveau fichier ?", command=lambda: nouvelle_boite_dialogue(liste))
    bouton.pack()

    bouton_details = Button(fenetre, text="Afficher les détails", command=lambda: afficher_details(liste))
    bouton_details.pack()

    bouton_fermer = Button(fenetre, text="Fermer", command=fenetre.quit)
    bouton_fermer.pack()

    fenetre.protocol("WM_DELETE_WINDOW", lambda: sauvegarder_liste(liste))
    fenetre.mainloop()

if __name__ == '__main__':
    ma_fenetre()