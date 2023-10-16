from tkinter import *
from datetime import *
from tkinter import simpledialog
import pickle

def nouvelle_boite_dialogue(liste):
    fichier = simpledialog.askstring("Nouveau fichier", "Entrez le nom du fichier ou du dossier :")
    if fichier:
        liste.insert(END, fichier)
        sauvegarder_liste(liste)

def sauvegarder_liste(liste):
    fichiers = liste.get(0, END)  # Obtenez tous les éléments de la liste
    with open('liste_fichiers.pickle', 'wb') as fichier:
        pickle.dump(fichiers, fichier)

def charger_liste(liste):
    try:
        with open('liste_fichiers.pickle', 'rb') as fichier:
            fichiers = pickle.load(fichier)
            for fichier in fichiers:
                liste.insert(END, fichier)
    except FileNotFoundError:
        pass

def ma_fenetre():
    fenetre = Tk()
    fenetre.geometry('500x500')
    fenetre.title('Temps passé à programmer')

    choix_label = Label(fenetre, text="Quel fichier voulez-vous choisir ?")
    choix_label.pack()

    liste = Listbox(fenetre)
    liste.pack()

    charger_liste(liste)

    bouton = Checkbutton(fenetre, text="Nouveau fichier ?", command=lambda: nouvelle_boite_dialogue(liste))
    bouton.pack()

    bouton=Button(fenetre, text="Fermer", command=fenetre.quit)
    bouton.pack()

    fenetre.protocol("WM_DELETE_WINDOW", lambda: sauvegarder_liste(liste))
    fenetre.mainloop()

if __name__ == '__main__':
    ma_fenetre()