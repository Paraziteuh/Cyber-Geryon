import os
import Crypto
from tkinter import *
from tkinter import messagebox, filedialog
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
import base64
import sqlite3

# Définition des répertoires de travail
encrypted_dir = os.path.join(os.path.expanduser("~"), "Desktop", "fichiers_chiffres")
decrypted_dir = os.path.join(os.path.expanduser("~"), "Desktop", "fichiers_dechiffres")
os.makedirs(encrypted_dir, exist_ok=True)
os.makedirs(decrypted_dir, exist_ok=True)

# Création de la fenêtre principale
root = Tk()
root.title("Application de chiffrement")
root.geometry("800x600")

# Connexion à la base de données
conn = sqlite3.connect("C:\\Users\\Anto\\Desktop\\projet Cyber\\MaBaseDeDonnées.db") # chemin vers la base de données
cursor = conn.cursor()

# Création de la table AESKeys si elle n'existe pas
cursor.execute("CREATE TABLE IF NOT EXISTS AESKeys (id INTEGER PRIMARY KEY, aes_key TEXT)")



# Fonction pour générer une clé AES
def generate_aes_key():
    aes_key = get_random_bytes(32)  # Génère une clé AES de 32 octets
    aes_key_base64 = base64.b64encode(aes_key).decode()  # Encode la clé en base64
    save_aes_key(aes_key)  # Enregistre la clé dans la base de données
    return aes_key_base64


# Fonction pour enregistrer la clé AES dans la base de données
def save_aes_key(aes_key):
    cursor.execute("INSERT INTO AESKeys (aes_key) VALUES (?)", (base64.b64encode(aes_key).decode(),))
    conn.commit()
    cursor.execute("SELECT last_insert_rowid()")
    key_id = cursor.fetchone()[0]
    print("Clé AES enregistrée avec l'ID", key_id)

# Fonction pour chiffrer un fichier avec la clé AES
def encrypt_file():
    # Sélectionner les fichiers source à chiffrer
    file_paths = file_listbox.get(0, "end")
    if not file_paths:
        return
    
    try:
        # Générer une clé AES
        aes_key_base64 = generate_aes_key()
        aes_key = base64.b64decode(aes_key_base64)

        for file_path in file_paths:
            # Créer un objet AES avec le mode CBC et un vecteur d'initialisation aléatoire pour chaque fichier
            cipher_aes = AES.new(aes_key, AES.MODE_CBC)
            
            # Générer un vecteur d'initialisation aléatoire
            iv = get_random_bytes(AES.block_size)

            # Lire les données du fichier source
            with open(file_path, 'rb') as source_file:
                file_data = source_file.read()

            # Ajouter un padding aux données du fichier
            padded_data = pad(file_data, AES.block_size)

            # Chiffrer les données
            encrypted_data = cipher_aes.encrypt(padded_data)

            # Obtenir le nom du fichier source
            source_file_name = os.path.basename(file_path)

            # Ajouter le préfixe "chiffré_" au nom du fichier chiffré
            encrypted_file_name = "chiffré_" + source_file_name

            # Construire le chemin du répertoire "Fichiers Chiffrés"
            encrypted_file_path = os.path.join(encrypted_dir, encrypted_file_name)

            # Créer un fichier chiffré contenant le vecteur d'initialisation, les données chiffrées et la clé AES
            with open(encrypted_file_path, 'wb') as encrypted_file:
                encrypted_file.write(iv)
                encrypted_file.write(encrypted_data)


        # Afficher un message de succès
        messagebox.showinfo('Succès', 'Fichiers chiffrés avec succès.')

        # Afficher la clé AES générée dans l'encart
        aes_key_entry.delete(0, 'end')
        aes_key_entry.insert(0, aes_key_base64)

        # Mettre à jour la liste des fichiers sélectionnés
        update_file_listbox()

    except Exception as e:
        messagebox.showerror('Erreur', 'Erreur lors du chiffrement des fichiers:\n' + str(e))








# Fonction pour déchiffrer un fichier avec la clé AES

def decrypt_file():
    # Sélectionner les fichiers chiffrés à déchiffrer
    file_paths = file_listbox.get(0, "end")
    if not file_paths:
        return

    try:
        # Récupérer la clé AES à partir de l'encart
        aes_key_base64 = aes_key_entry.get()
        aes_key = base64.b64decode(aes_key_base64)

        for file_path in file_paths:
            # Lire les données du fichier chiffré
            with open(file_path, 'rb') as encrypted_file:
                encrypted_data = encrypted_file.read()

            # Extraire le vecteur d'initialisation du fichier chiffré
            iv = encrypted_data[:AES.block_size]

            # Créer un objet AES avec la clé et le mode CBC
            cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)

            # Récupérer les données chiffrées (après le vecteur d'initialisation)
            encrypted_data = encrypted_data[AES.block_size:]

            # Déchiffrer les données
            decrypted_data = cipher_aes.decrypt(encrypted_data)

            # Supprimer le padding des données déchiffrées
            unpadded_data = unpad(decrypted_data, AES.block_size, style='pkcs7')

            # Obtenir le nom du fichier chiffré
            encrypted_file_name = os.path.basename(file_path)

            # Supprimer le préfixe "chiffré_" du nom du fichier pour obtenir le nom du fichier déchiffré
            decrypted_file_name = encrypted_file_name.replace("chiffré_", "")

            # Construire le chemin du répertoire "Fichiers Déchiffrés"
            decrypted_file_path = os.path.join(decrypted_dir, decrypted_file_name)

            # Écrire les données déchiffrées dans le fichier déchiffré
            with open(decrypted_file_path, 'wb') as decrypted_file:
                decrypted_file.write(unpadded_data)

        # Afficher un message de succès
        messagebox.showinfo('Succès', 'Fichiers déchiffrés avec succès.')

        # Mettre à jour la liste des fichiers sélectionnés
        update_file_listbox()

    except Exception as e:
        messagebox.showerror('Erreur', 'Erreur lors du déchiffrement des fichiers:\n' + str(e))













# Fonction pour sélectionner des fichiers à chiffrer/déchiffrer
def select_files():
    files = filedialog.askopenfilenames(filetypes=[("Fichiers", "*.*")])
    if files:
        for file in files:
            file_listbox.insert(END, file)

# Fonction pour supprimer un fichier sélectionné
def delete_file():
    selection = file_listbox.curselection()
    if selection:
        file_listbox.delete(selection)

# Fonction pour supprimer tous les fichiers sélectionnés
def clear_files():
    file_listbox.delete(0, END)

# Fonction pour mettre à jour la liste des fichiers sélectionnés
def update_file_listbox():
    files = file_listbox.get(0, END)
    file_listbox.delete(0, END)
    for file in files:
        file_listbox.insert(END, file)

# Encart pour afficher la clé AES générée
aes_key_frame = LabelFrame(root, text="Clé AES générée")
aes_key_frame.place(x=10, y=10, width=560, height=60)

aes_key_label = Label(aes_key_frame, text="Clé AES:")
aes_key_label.place(x=10, y=10)

aes_key_entry = Entry(aes_key_frame, width=50, show="*")
aes_key_entry.place(x=80, y=10)

# Bouton de chiffrement
encrypt_button = Button(root, text="Chiffrer", command=encrypt_file)
encrypt_button.place(x=10, y=80, width=100)

# Bouton de déchiffrement
decrypt_button = Button(root, text="Déchiffrer", command=decrypt_file)
decrypt_button.place(x=120, y=80, width=100)

# Bouton de sélection des fichiers
select_button = Button(root, text="Sélectionner", command=select_files)
select_button.place(x=230, y=80, width=100)

# Bouton de suppression des fichiers sélectionnés
delete_button = Button(root, text="Supprimer", command=delete_file)
delete_button.place(x=340, y=80, width=100)

# Bouton de suppression de tous les fichiers sélectionnés
clear_button = Button(root, text="Clear", command=clear_files)
clear_button.place(x=450, y=80, width=100)

# Encart pour afficher la liste des fichiers sélectionnés
file_listbox_frame = LabelFrame(root, text="Fichiers sélectionnés")
file_listbox_frame.place(x=10, y=120, width=560, height=360)

file_listbox = Listbox(file_listbox_frame, width=70, height=15)
file_listbox.pack(side="left", fill="y")

scrollbar = Scrollbar(file_listbox_frame, orient="vertical")
scrollbar.config(command=file_listbox.yview)
scrollbar.pack(side="right", fill="y")

file_listbox.config(yscrollcommand=scrollbar.set)

# Barre de progression
progress_bar = Progressbar(root, orient=HORIZONTAL, length=560, mode='determinate')
progress_bar.place(x=10, y=490)

# Mettre à jour la liste des fichiers sélectionnés
update_file_listbox()

# Logo
logo_path = "logo.png"  # Chemin vers votre logo
try:
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((200, 200), Image.ANTIALIAS)  # Redimensionner le logo
    logo_photo = ImageTk.PhotoImage(logo_image)

    logo_label = Label(root, image=logo_photo)
    logo_label.image = logo_photo
    logo_label.place(x=590, y=10)

except Exception as e:
    print("Erreur lors du chargement du logo:", str(e))

# Exécution de la boucle principale de l'interface utilisateur
root.mainloop()
