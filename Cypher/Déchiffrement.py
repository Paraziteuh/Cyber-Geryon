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

def dechiffrement_cesar(texte, decalage):
    return chiffrement_cesar(texte, -decalage)

def evaluer_texte_dechiffre(texte):
    with open('dico.txt', 'r', encoding='utf-8') as f:
        dico = f.read()

    mots_dico = set(mot.strip().lower() for mot in dico.split())

    texte_dechiffre = texte.lower()
    mots = texte_dechiffre.split()

    mots_valides = [mot for mot in mots if mot in mots_dico]
    score = len(mots_valides)

    return score


def dechiffrement_fichier_cesar(fichier_entree, fichier_sortie):
    try:
        with open(fichier_entree, 'r') as f_entree:
            texte_chiffre = f_entree.read()

        meilleur_score = 0
        meilleur_decalage = 0
        meilleur_texte_dechiffre = ""

        for decalage in range(26):
            texte_dechiffre = dechiffrement_cesar(texte_chiffre, decalage)
            score = evaluer_texte_dechiffre(texte_dechiffre)
            if score > meilleur_score:
                meilleur_score = score
                meilleur_decalage = decalage
                meilleur_texte_dechiffre = texte_dechiffre

        with open(fichier_sortie, 'w') as f_sortie:
            f_sortie.write(meilleur_texte_dechiffre)

        print("Le fichier a été déchiffré avec succès et enregistré sur le bureau.")
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

def dechiffrer_fichier():
    fichier_entree = entry_fichier_entree.get()
    fichier_sortie = entry_fichier_sortie.get()

    dechiffrement_fichier_cesar(fichier_entree, fichier_sortie)

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Déchiffrement de César")
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

# Bouton pour déchiffrer le fichier
bouton_dechiffrer = tk.Button(fenetre, text="Déchiffrer", command=dechiffrer_fichier)
bouton_dechiffrer.pack()

fenetre.mainloop()
