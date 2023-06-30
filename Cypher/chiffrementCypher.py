import os
import tkinter as tk
from tkinter import filedialog

def chiffrement_cesar(texte, decalage):
    texte_chiffre = ""
    for caractere in texte:
        if caractere.isalpha():
            ascii_debut = ord('a') if caractere.islower() else ord('A')
            index = (ord(caractere) - ascii_debut + decalage) % 26
            texte_chiffre += chr(index + ascii_debut)
        else:
            texte_chiffre += caractere
    return texte_chiffre

def chiffrement_fichier_cesar(fichier_entree, fichier_sortie, decalage):
    try:
        with open(fichier_entree, 'r') as f_entree:
            texte = f_entree.read()
            texte_chiffre = chiffrement_cesar(texte, decalage)

        with open(fichier_sortie, 'w') as f_sortie:
            f_sortie.write(texte_chiffre)

        print("Le fichier a été chiffré avec succès et enregistré sur le bureau.")
    except IOError:
        print("Erreur lors de la lecture/écriture du fichier.")

def choisir_fichier_entree():
    fichier_entree = filedialog.askopenfilename(title="Sélectionner le fichier d'entrée")
    entry_fichier_entree.delete(0, tk.END)
    entry_fichier_entree.insert(tk.END, fichier_entree)

def choisir_fichier_sortie():
    fichier_sortie = filedialog.asksaveasfilename(title="Sélectionner le fichier de sortie", defaultextension=".txt",
                                                  filetypes=(("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")))
    entry_fichier_sortie.delete(0, tk.END)
    entry_fichier_sortie.insert(tk.END, fichier_sortie)

def chiffrer_fichier():
    fichier_entree = entry_fichier_entree.get()
    fichier_sortie = entry_fichier_sortie.get()
    decalage = int(entry_decalage.get())

    chiffrement_fichier_cesar(fichier_entree, fichier_sortie, decalage)

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Chiffrement de César")
fenetre.geometry("400x200")

# Étiquette et champ de saisie pour le fichier d'entrée
label_fichier_entree = tk.Label(fenetre, text="Fichier d'entrée :")
label_fichier_entree.pack()
entry_fichier_entree = tk.Entry(fenetre, width=40)
entry_fichier_entree.pack()
bouton_fichier_entree = tk.Button(fenetre, text="Parcourir", command=choisir_fichier_entree)
bouton_fichier_entree.pack()

# Étiquette et champ de saisie pour le fichier de sortie
label_fichier_sortie = tk.Label(fenetre, text="Fichier de sortie :")
label_fichier_sortie.pack()
entry_fichier_sortie = tk.Entry(fenetre, width=40)
entry_fichier_sortie.pack()
bouton_fichier_sortie = tk.Button(fenetre, text="Parcourir", command=choisir_fichier_sortie)
bouton_fichier_sortie.pack()

# Étiquette et champ de saisie pour le décalage
label_decalage = tk.Label(fenetre, text="Décalage :")
label_decalage.pack()
entry_decalage = tk.Entry(fenetre, width=10)
entry_decalage.pack()

# Bouton pour chiffrer le fichier
bouton_chiffrer = tk.Button(fenetre, text="Chiffrer", command=chiffrer_fichier)
bouton_chiffrer.pack()

fenetre.mainloop()
