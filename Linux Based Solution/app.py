import os
import tkinter
from tkinter import Tk, filedialog, messagebox, Label, Entry, Button, Listbox, Scrollbar
from tkinter import LabelFrame, StringVar, IntVar, BooleanVar, HORIZONTAL, VERTICAL, END
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64


# Fonction de génération d'une clé AES
def generate_aes_key():
    return os.urandom(32)

# Fonction de chiffrement d'un fichier avec AES
def encrypt_file():
    # Sélectionner les fichiers source à chiffrer
    file_paths = file_listbox.get(0, "end")
    if not file_paths:
        return

    try:
        # Générer une clé AES
        aes_key = generate_aes_key()

        for file_path in file_paths:
            # Créer un objet AES avec le mode CBC et un vecteur d'initialisation aléatoire pour chaque fichier
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

            # Obtenir le nom du fichier source
            source_file_name = os.path.basename(file_path)

            # Ajouter le préfixe "chiffré_" au nom du fichier chiffré
            encrypted_file_name = "chiffré_" + source_file_name

            # Construire le chemin du répertoire "Fichiers Chiffrés"
            encrypted_file_path = os.path.join(encrypted_dir, encrypted_file_name)

            # Créer un fichier chiffré contenant le vecteur d'initialisation et les données chiffrées
            with open(encrypted_file_path, 'wb') as encrypted_file:
                encrypted_file.write(iv + encrypted_data)

        # Afficher un message de succès
        messagebox.showinfo('Succès', 'Fichiers chiffrés avec succès.')

        # Mettre à jour la barre de progression
        progress_bar.stop()
        progress_bar['value'] = 100

        # Attendre quelques secondes avant de réinitialiser la barre de progression
        root.after(5000, reset_progress_bar)

        # Afficher la clé AES générée dans l'encart
        aes_key_entry.delete(0, 'end')
        aes_key_entry.insert(0, base64.b64encode(aes_key).decode())

        # Mettre à jour la liste des fichiers sélectionnés
        update_file_listbox()

    except Exception as e:
        messagebox.showerror('Erreur', 'Erreur lors du chiffrement des fichiers:\n' + str(e))
        

# Fonction de déchiffrement d'un fichier avec AES
def decrypt_file():
    # Sélectionner les fichiers chiffrés à déchiffrer
    file_paths = file_listbox.get(0, "end")
    if not file_paths:
        return

    try:
        # Obtenir la clé AES à partir de l'encart
        aes_key = base64.b64decode(aes_key_entry.get())

        for file_path in file_paths:
            # Créer un objet AES avec le mode CBC et le vecteur d'initialisation extrait du fichier chiffré
            with open(file_path, 'rb') as encrypted_file:
                iv = encrypted_file.read(16)
                cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)

                # Lire les données chiffrées à partir du fichier
                encrypted_data = encrypted_file.read()

            # Fonction d'enregistrement de la clé AES
            def save_aes_key(aes_key):

            # Créer le répertoire "Fichiers Chiffrés" s'il n'existe pas
                os.makedirs(encrypted_dir, exist_ok=True)

            # Enregistrer la clé AES dans le fichier "aes_key.txt" dans le répertoire "Fichiers Chiffrés"
            aes_key_file_path = os.path.join(encrypted_dir, 'aes_key.txt')
            with open(aes_key_file_path, 'wb') as aes_key_file:
                aes_key_file.write(aes_key)    

            # Déchiffrer les données
            decrypted_data = cipher_aes.decrypt(encrypted_data)

            # Supprimer le padding des données déchiffrées
            unpadded_data = unpad(decrypted_data, AES.block_size)

            # Obtenir le nom du fichier chiffré
            encrypted_file_name = os.path.basename(file_path)

            # Supprimer le préfixe "chiffré_" du nom du fichier pour obtenir le nom du fichier déchiffré
            decrypted_file_name = encrypted_file_name.replace('chiffré_', '', 1)

            # Construire le chemin du répertoire "Fichiers Déchiffrés"
            decrypted_file_path = os.path.join(decrypted_dir, decrypted_file_name)

            # Créer un fichier déchiffré contenant les données déchiffrées
            with open(decrypted_file_path, 'wb') as decrypted_file:
                decrypted_file.write(unpadded_data)

        # Afficher un message de succès
        messagebox.showinfo('Succès', 'Fichiers déchiffrés avec succès.')

        # Mettre à jour la barre de progression
        progress_bar.stop()
        progress_bar['value'] = 100

        # Attendre quelques secondes avant de réinitialiser la barre de progression
        root.after(5000, reset_progress_bar)

        # Mettre à jour la liste des fichiers sélectionnés
        update_file_listbox()

    except Exception as e:
        messagebox.showerror('Erreur', 'Erreur lors du déchiffrement des fichiers:\n' + str(e))

# Fonction de sélection des fichiers à chiffrer/déchiffrer
def select_files():
    # Ouvrir une boîte de dialogue pour sélectionner les fichiers
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        # Ajouter les fichiers sélectionnés à la liste des fichiers
        for file_path in file_paths:
            file_listbox.insert(END, file_path)

# Fonction de suppression d'un fichier de la liste
def delete_file():
    selected_indices = file_listbox.curselection()
    if selected_indices:
        for index in selected_indices:
            file_listbox.delete(index)

# Fonction de suppression de tous les fichiers sélectionnés
def clear_files():
    file_listbox.delete(0, END)

# Fonction de mise à jour de la liste des fichiers sélectionnés
def update_file_listbox():
    file_listbox.delete(0, END)
    for file_name in os.listdir(selected_dir):
        file_listbox.insert(END, file_name)

# Fonction de réinitialisation de la barre de progression
def reset_progress_bar():
    progress_bar['value'] = 0

# Fonction d'enregistrement de la clé AES
def save_aes_key(aes_key):
    # Créer le répertoire "Fichiers Chiffrés" s'il n'existe pas
    os.makedirs(encrypted_dir, exist_ok=True)

    # Enregistrer la clé AES dans le fichier "aes_key.txt" dans le répertoire "Fichiers Chiffrés"
    aes_key_file_path = os.path.join(encrypted_dir, 'aes_key.txt')
    with open(aes_key_file_path, 'wb') as aes_key_file:
        aes_key_file.write(aes_key)


# Configuration de la fenêtre principale
root = Tk()
root.title("Application de chiffrement AES")
root.geometry("800x500")

# Répertoire initial pour la sélection des fichiers
selected_dir = os.path.join(os.path.expanduser("~"), "Desktop")

# Répertoires de stockage des fichiers chiffrés et déchiffrés
encrypted_dir = os.path.join(selected_dir, "Fichiers Chiffrés")
decrypted_dir = os.path.join(selected_dir, "Fichiers Déchiffrés")

# Vérifier si les répertoires de stockage existent, sinon les créer
if not os.path.exists(encrypted_dir):
    os.makedirs(encrypted_dir)

if not os.path.exists(decrypted_dir):
    os.makedirs(decrypted_dir)

# Encart pour afficher la clé AES générée
aes_key_frame = LabelFrame(root, text="Clé AES")
aes_key_frame.place(x=10, y=10, width=560, height=60)

aes_key_label = Label(aes_key_frame, text="Clé AES:")
aes_key_label.place(x=10, y=10)

aes_key_entry = Entry(aes_key_frame, width=50)
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
