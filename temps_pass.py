from tkinter import *
from tkinter import simpledialog
from time import time

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
        
    bouton = Checkbutton(fenetre, text="Nouveau fichier ?", command=lambda: )
    bouton.pack()

    bouton_details = Button(fenetre, text="Afficher les détails", command=lambda: )
    bouton_details.pack()

    bouton_fermer = Button(fenetre, text="Fermer", command=fenetre.quit)
    bouton_fermer.pack()

    fenetre.mainloop()

if __name__ == '__main__':
    ma_fenetre()