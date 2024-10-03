import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
import os

# Lista klientów
clients = {}

# Funkcja aktualizująca Listbox klientów
def update_client_listbox():
    client_listbox.delete(0, tk.END)
    for client in clients.keys():
        client_listbox.insert(tk.END, client)

# Funkcja dodająca klienta
def add_client():
    client_name = client_name_entry.get()
    if client_name:
        clients[client_name] = []
        update_client_listbox()  # Zaktualizowanie listy klientów w Listbox
        client_name_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Błąd", "Nazwa klienta nie może być pusta.")

# Funkcja generująca raport
def generate_report(client_name):
    if client_name not in clients:
        messagebox.showerror("Błąd", "Wybierz poprawnego klienta.")
        return

    pdf_filename = f"SEO_Report_{client_name}_{datetime.now().strftime('%Y%m%d')}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Rejestracja czcionki Noto Sans
    pdfmetrics.registerFont(TTFont('NotoSans', os.path.join("fonts", "NotoSans-VariableFont_wdth,wght.ttf")))
    pdfmetrics.registerFont(TTFont('NotoSansBold', os.path.join("fonts", "NotoSans_Condensed-Bold.ttf")))

    # Ustawienia czcionki
    c.setFont("NotoSansBold", 24)
    c.drawString(100, 750, f"Raport SEO dla: {client_name}")
    # Dodanie daty utworzenia raportu
    c.setFont("NotoSans", 12)
    creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.drawString(100, 730, f"Data utworzenia: {creation_date}")

    y_position = 680
    for change in clients[client_name]:
        # Ustaw czcionkę na NotoSansBold dla nagłówków
        c.setFont("NotoSansBold", 12)
        c.drawString(100, y_position, "Data:")

        # Ustaw czcionkę na NotoSans dla wartości
        c.setFont("NotoSans", 12)
        c.drawString(130, y_position, change['date'])  # Wartość daty obok nagłówka
        y_position -= 20  # Przejdź do następnej linii

        # Nagłówek dla wpływu na SEO
        c.setFont("NotoSansBold", 12)
        c.drawString(100, y_position, "Wpływ na SEO:")

        # Wartość wpływu obok nagłówka
        c.setFont("NotoSans", 12)
        if change['impact'] == "Inne":
            impact_text = f"Inne: {change['description']}"  # Dodanie opisu, jeśli zaznaczone "Inne"
        else:
            impact_text = change['impact']
        c.drawString(180, y_position, impact_text)  # Wartość wpływu obok nagłówka
        y_position -= 20  # Przejdź do następnej linii

        # Nagłówek dla opisu
        c.setFont("NotoSansBold", 12)
        c.drawString(100, y_position, "Opis:")

        # Wartość opisu obok nagłówka
        c.setFont("NotoSans", 12)
        c.drawString(130, y_position, change['description'])  # Wartość opisu obok nagłówka
        y_position -= 30  # Odstęp między zmianami

    c.save()
    messagebox.showinfo("Sukces", f"Raport został wygenerowany: {pdf_filename}")

# Funkcja dodająca zmianę dla klienta
def add_change():
    client_name = client_listbox.get(tk.ACTIVE)
    if not client_name:
        messagebox.showerror("Błąd", "Wybierz klienta z listy.")
        return

    change_date = change_date_entry.get()
    impact = selected_impact.get()
    description = description_entry.get("1.0", tk.END).strip()  # Pobranie tekstu z Text

    # Sprawdzenie, czy pole opisu jest wymagane, gdy wybrano "Inne"
    if impact == "Inne" and not description:
        messagebox.showerror("Błąd", "Proszę podać opis wpływu na SEO.")
        return

    if not change_date or not impact:
        messagebox.showerror("Błąd", "Data i wpływ na SEO muszą być wypełnione.")
        return

    clients[client_name].append({
        'date': change_date,
        'impact': impact,
        'description': description
    })

    # Utrzymanie daty po dodaniu zmiany
    change_date_entry.delete(0, tk.END)
    change_date_entry.insert(0, change_date)  # Przywrócenie daty
    description_entry.delete("1.0", tk.END)  # Wyczyść pole tekstowe dla opisu
    selected_impact.set(None)  # Resetowanie wyboru checkboxów
    other_impact_entry.grid_remove()  # Ukryj pole tekstowe "Inne"
    show_changes(client_name)  # Zaktualizuj podgląd zmian

# Funkcja wyświetlająca zmiany dla wybranego klienta
def show_changes(client_name):
    changes_text.delete(1.0, tk.END)  # Wyczyść poprzedni tekst
    for change in clients[client_name]:
        changes_text.insert(tk.END, f"Data: {change['date']}\n")
        changes_text.insert(tk.END, f"Wpływ na SEO: {change['impact']}\n")
        changes_text.insert(tk.END, f"Opis: {change['description']}\n\n")

# Funkcja do wyświetlania pola tekstowego dla "Inne"
def update_impact_selection(*args):
    if selected_impact.get() == "Inne":
        other_impact_entry.grid(row=8, column=1, padx=5, pady=5)  # Pokaż dodatkowe pole
    else:
        other_impact_entry.grid_remove()  # Ukryj pole, jeśli nie jest wybrane "Inne"

# Funkcja do obsługi wyboru klienta
def on_client_select(event):
    client_name = client_listbox.get(tk.ACTIVE)
    if client_name:
        show_changes(client_name)  # Zaktualizuj zmiany dla wybranego klienta

# Tworzenie GUI
root = tk.Tk()
root.title("Generator raportów SEO")

# Dodawanie klienta
tk.Label(root, text="Nazwa klienta:").grid(row=0, column=0, padx=5, pady=5)
client_name_entry = tk.Entry(root)
client_name_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Dodaj klienta", command=add_client).grid(row=0, column=2, padx=5, pady=5)

# Lista klientów
client_listbox = tk.Listbox(root, width=50)
client_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
client_listbox.bind('<<ListboxSelect>>', on_client_select)  # Dodaj obsługę wyboru

# Dodawanie zmiany
tk.Label(root, text="Data zmiany:").grid(row=2, column=0, padx=5, pady=5)
change_date_entry = tk.Entry(root)
change_date_entry.grid(row=2, column=1, padx=5, pady=5)
change_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))  # Ustawienie dzisiejszej daty

tk.Label(root, text="Wpływ na SEO:").grid(row=3, column=0, padx=5, pady=5)
selected_impact = tk.StringVar()
selected_impact.trace_add('write', update_impact_selection)  # Dodaj śledzenie zmian wyboru

# Checkboxy dla wpływu na SEO
tk.Radiobutton(root, text="Niski", variable=selected_impact, value="Niski").grid(row=3, column=1, sticky=tk.W)
tk.Radiobutton(root, text="Średni", variable=selected_impact, value="Średni").grid(row=4, column=1, sticky=tk.W)
tk.Radiobutton(root, text="Wysoki", variable=selected_impact, value="Wysoki").grid(row=5, column=1, sticky=tk.W)
tk.Radiobutton(root, text="Inne", variable=selected_impact, value="Inne").grid(row=6, column=1, sticky=tk.W)

other_impact_entry = tk.Entry(root)
other_impact_entry.grid(row=7, column=1, padx=5, pady=5)
other_impact_entry.grid_remove()  # Ukryj pole tekstowe "Inne"

tk.Label(root, text="Opis:").grid(row=8, column=0, padx=5, pady=5)
description_entry = tk.Text(root, height=5, width=40)
description_entry.grid(row=8, column=1, padx=5, pady=5)

tk.Button(root, text="Dodaj zmianę", command=add_change).grid(row=9, column=1, padx=5, pady=5)

# Wyświetlanie zmian
tk.Label(root, text="Zmiany:").grid(row=10, column=0, padx=5, pady=5)
changes_text = tk.Text(root, height=10, width=50)
changes_text.grid(row=11, column=0, columnspan=3, padx=5, pady=5)

tk.Button(root, text="Generuj raport", command=lambda: generate_report(client_listbox.get(tk.ACTIVE))).grid(row=12, column=1, padx=5, pady=5)

root.mainloop()
