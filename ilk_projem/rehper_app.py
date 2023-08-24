import pyodbc
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, END, SINGLE

# SQL Server'a Windows kimlik doğrulaması ile bağlanmak için gerekli bağlantı bilgileri
server = 'DESKTOP-TUPJNM2'
database = 'ders'
trusted_connection = 'yes'  # Windows kimlik doğrulamasını kullanacağımızı belirtiyoruz

connection_string = f'DRIVER=SQL Server;SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection}'

def add_person():
    ad = ad_entry.get()
    soyad = soyad_entry.get()
    telefon = telefon_entry.get()

    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    insert_query = "INSERT INTO Kisi (Ad, Soyad, Telefon) VALUES (?, ?, ?)"
    cursor.execute(insert_query, (ad, soyad, telefon))
    connection.commit()

    messagebox.showinfo("Başarılı", "Kişi veritabanına kaydedildi.")

    cursor.close()
    connection.close()

    list_people()

def list_people():
    people_listbox.delete(0, END)  # Listeyi temizle

    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    select_query = "SELECT Ad, Soyad FROM Kisi"
    cursor.execute(select_query)

    for row in cursor.fetchall():
        people_listbox.insert(END, f"{row.Ad} {row.Soyad}")

    cursor.close()
    connection.close()

def select_person(event):
    selected_person = people_listbox.get(people_listbox.curselection()[0])  # Seçilen kişiyi al
    ad, soyad = selected_person.split()  # İsmi ve soyismi ayır

    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    select_query = "SELECT Ad, Soyad, Telefon FROM Kisi WHERE Ad = ? AND Soyad = ?"
    cursor.execute(select_query, (ad, soyad))

    person_data = cursor.fetchone()
    if person_data:
        messagebox.showinfo("Kişi Bilgileri", f"Ad: {person_data.Ad}\nSoyad: {person_data.Soyad}\nTelefon: {person_data.Telefon}")
    else:
        messagebox.showerror("Hata", "Kişi bilgileri bulunamadı.")

    cursor.close()
    connection.close()

def delete_person():
    selected_person = people_listbox.get(people_listbox.curselection()[0])  # Seçilen kişiyi al
    ad, soyad = selected_person.split()  # İsmi ve soyismi ayır

    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    delete_query = "DELETE FROM Kisi WHERE Ad = ? AND Soyad = ?"
    cursor.execute(delete_query, (ad, soyad))
    connection.commit()

    messagebox.showinfo("Başarılı", "Kişi veritabanından silindi.")

    cursor.close()
    connection.close()

    list_people()  # Listeyi güncelle

root = tk.Tk()
root.title("Kişi Veritabanı İşlemleri")

ad_label = tk.Label(root, text="Kişinin adı:")
ad_label.pack()

ad_entry = tk.Entry(root)
ad_entry.pack()

soyad_label = tk.Label(root, text="Kişinin soyadı:")
soyad_label.pack()

soyad_entry = tk.Entry(root)
soyad_entry.pack()

telefon_label = tk.Label(root, text="Telefon numarası:")
telefon_label.pack()

telefon_entry = tk.Entry(root)
telefon_entry.pack()

ekle_button = tk.Button(root, text="Kişi Ekle", command=add_person)
ekle_button.pack()

list_button = tk.Button(root, text="Kişileri Listele", command=list_people)
list_button.pack()

# Kişi listesi
people_listbox = Listbox(root, selectmode=SINGLE, width=40)
people_listbox.pack()

# Liste için kaydırma çubuğu
scrollbar = Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
people_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=people_listbox.yview)

people_listbox.bind("<<ListboxSelect>>", select_person)

# Kişi Sil butonu
sil_button = tk.Button(root, text="Kişi Sil", command=delete_person)
sil_button.pack()

root.mainloop()

