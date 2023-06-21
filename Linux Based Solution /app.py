import os
from tkinter import Tk, filedialog, messagebox, Label, Entry, Button
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Fonction de génération d'une clé AES
def generate_aes_key():
    return os.urandom(32)

# Fonction de chiffrement d'un fichier avec AES
def encrypt_file():
    # Sélectionner le fichier source à chiffrer
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    try:
        # Générer une clé AES
        aes_key = generate_aes_key()

        # Créer un objet AES avec le mode CBC et le vecteur d'initialisation aléatoire
        cipher_aes = AES.new(aes_key, AES.MODE_CBC)

        # Lire les données du fichier source
        with open(file_path, 'rb') as source_file:
            file_data = source_file.read()

        # Ajouter un padding aux données du fichier
        padded_data = pad(file_data, AES.block_size)

        # Chiffrer les données
        encrypted_data = cipher_aes.encrypt(padded_data)

        # Obtenir le vecteur d'initialisation utilisé pour le chiffrement
        iv = cipher_aes.iv

        # Demander un emplacement pour enregistrer le fichier chiffré
        encrypted_file_path = filedialog.asksaveasfilename()

        if encrypted_file_path:
            # Créer un fichier chiffré contenant le vecteur d'initialisation et les données chiffrées
            with open(encrypted_file_path, 'wb') as encrypted_file:
                encrypted_file.write(iv + encrypted_data)

            # Afficher un message de succès
            messagebox.showinfo('Succès', 'Fichier chiffré avec succès.')

            # Afficher la clé AES générée dans l'encart
            aes_key_entry.delete(0, 'end')
            aes_key_entry.insert(0, base64.b64encode(aes_key).decode())

    except Exception as e:
        messagebox.showerror('Erreur', 'Erreur lors du chiffrement du fichier:\n' + str(e))
