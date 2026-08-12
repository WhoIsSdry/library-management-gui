import customtkinter as ctk
from book import Books
from Students import Students
from Library import Library
from books import show_books
from members import show_members
from dashboard import show_dashboard

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

library = Library(Books(), Students())

app = ctk.CTk()

app.resizable(False, False)
app.title("Library Management System")
app.geometry("1200x700")

sidebar = ctk.CTkFrame(
    fg_color="#241468",
    master=app,
    width=250,
    corner_radius=0
)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

title = ctk.CTkLabel(
    master=sidebar,
    text="Library",
    font=("Arial", 22, "bold"),
    text_color="#F5F5F5"
)
title.pack(pady=(20, 40))


def clear_content():
    for widget in content.winfo_children():
        widget.destroy()


def open_dashboard():
    clear_content()
    show_dashboard(content, library)


def open_books():
    clear_content()
    show_books(content, library)


def open_members():
    clear_content()
    show_members(content, library)


buttons = [
    ("Dashboard", open_dashboard),
    ("Books", open_books),
    ("Members", open_members),
]

for text, command in buttons:

    button = ctk.CTkButton(
        master=sidebar,
        text=text,
        command=command,
        height=45,
        fg_color="#3A1FA8",
        hover_color="#2C1780"
    )
    button.pack(fill="x", padx=15, pady=5)

main_frame = ctk.CTkFrame(
    master=app,
    corner_radius=0
)
main_frame.pack(side="right", fill="both", expand=True)

topbar = ctk.CTkFrame(
    fg_color="#3A1FA8",
    master=main_frame,
    height=70,
    corner_radius=8
)
topbar.pack(side="top", fill="x", padx=25, pady=(20, 10))
topbar.pack_propagate(False)

ctk.CTkLabel(
    master=topbar,
    text="Library Management System",
    font=("Arial", 18, "bold"),
    text_color="#F5F5F5"
).pack(side="left", padx=20)

content = ctk.CTkFrame(
    master=main_frame,
    corner_radius=0
)
content.pack(fill="both", expand=True)

open_dashboard()

app.mainloop()
