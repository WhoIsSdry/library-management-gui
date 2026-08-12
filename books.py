import customtkinter as ctk
from book import Book

current_table = None


def open_add_book(table_frame, library):

    window = ctk.CTkToplevel()

    window.title("Add Book")
    window.geometry("400x480")
    window.resizable(False, False)

    title = ctk.CTkLabel(
        master=window,
        text="Add Book",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=20)

    name_label = ctk.CTkLabel(
        master=window,
        text="Book Name"
    )
    name_label.pack(anchor="w", padx=30)

    name_entry = ctk.CTkEntry(
        master=window,
        width=300
    )
    name_entry.pack(pady=(5,15))

    author_label = ctk.CTkLabel(
        master=window,
        text="Author"
    )
    author_label.pack(anchor="w", padx=30)

    author_entry = ctk.CTkEntry(
        master=window,
        width=300
    )
    author_entry.pack(pady=(5,15))

    year_label = ctk.CTkLabel(
        master=window,
        text="Year"
    )
    year_label.pack(anchor="w", padx=30)

    year_entry = ctk.CTkEntry(
        master=window,
        width=300
    )
    year_entry.pack(pady=(5,15))

    error_label = ctk.CTkLabel(
        master=window,
        text="",
        text_color="#F87171"
    )
    error_label.pack(pady=(0,10))

    save_btn = ctk.CTkButton(
        master=window,
        text="Save",
        fg_color="#22C55E",
        hover_color="#16A34A",
        command=lambda: save_book(
            name_entry,
            author_entry,
            year_entry,
            window,
            table_frame,
            library,
            error_label
        )
    )
    save_btn.pack()


def save_book(name_entry, author_entry, year_entry, window, table_frame, library, error_label):
    error_label.configure(text="")

    name = name_entry.get().strip()
    author = author_entry.get().strip()
    year_text = year_entry.get().strip()

    if not name:
        error_label.configure(text="Book Name is required.")
        return

    if not author or not all(c.isalpha() or c.isspace() for c in author):
        error_label.configure(text="Author must contain only letters and spaces.")
        return

    if not year_text.isdigit():
        error_label.configure(text="Year must be a number.")
        return

    year = int(year_text)
    if year < 0 or year > 2100:
        error_label.configure(text="Year must be between 0 and 2100.")
        return

    new_book = Book(
        name=name,
        author=author,
        year=year
    )

    library.All_Books.add_book(new_book)
    library.SHELF.add_book(new_book)
    library.log(f"Added book '{name}' (ID {new_book.Book_ID})")

    show_books_table(table_frame, library.All_Books.books, library)

    window.destroy()


def show_books_table(table_frame, book_list, library):

    for widget in table_frame.winfo_children():
        widget.destroy()

    header = ctk.CTkFrame(
        master=table_frame,
        fg_color="#3A1FA8"
    )
    header.pack(fill="x", padx=10, pady=10)

    ctk.CTkLabel(master=header, text="ID", width=80, font=("Arial", 15, "bold")).pack(side="left")
    ctk.CTkLabel(master=header, text="Name", width=220, font=("Arial", 15, "bold")).pack(side="left")
    ctk.CTkLabel(master=header, text="Author", width=180, font=("Arial", 15, "bold")).pack(side="left")
    ctk.CTkLabel(master=header, text="Year", width=100, font=("Arial", 15, "bold")).pack(side="left")
    ctk.CTkLabel(master=header, text="Status", width=120, font=("Arial", 15, "bold")).pack(side="left")

    for i, book in enumerate(book_list):

        row_color = "#26263A" if i % 2 == 0 else "#2F2F46"

        row = ctk.CTkFrame(
            master=table_frame,
            fg_color=row_color
        )
        row.pack(fill="x", padx=10, pady=3)

        ctk.CTkLabel(master=row, text=book.Book_ID, width=80).pack(side="left")
        ctk.CTkLabel(master=row, text=book.name, width=220).pack(side="left")
        ctk.CTkLabel(master=row, text=book.author, width=180).pack(side="left")
        ctk.CTkLabel(master=row, text=book.year, width=100).pack(side="left")

        status = "Taken" if book.borrowed else "Ok"
        status_color = "#F59E0B" if book.borrowed else "#22C55E"

        ctk.CTkLabel(master=row, text=status, width=120, text_color=status_color).pack(side="left")

        if not book.borrowed:
            action_btn = ctk.CTkButton(
                master=row,
                text="Borrow",
                width=90,
                fg_color="#22C55E",
                hover_color="#16A34A",
                command=lambda b=book: open_borrow_window(b, table_frame, library)
            )
        else:
            action_btn = ctk.CTkButton(
                master=row,
                text="Return",
                width=90,
                fg_color="#F59E0B",
                hover_color="#D97706",
                command=lambda b=book: return_book(b, table_frame, library)
            )

        action_btn.pack(side="left", padx=5)


def open_borrow_window(book, table_frame, library):

    window = ctk.CTkToplevel()

    window.title("Borrow Book")
    window.geometry("350x220")
    window.resizable(False, False)

    title = ctk.CTkLabel(
        master=window,
        text="Borrow Book",
        font=("Arial", 20, "bold")
    )
    title.pack(pady=20)

    member_label = ctk.CTkLabel(
        master=window,
        text="Member ID"
    )
    member_label.pack(anchor="w", padx=25)

    member_entry = ctk.CTkEntry(
        master=window,
        width=250
    )
    member_entry.pack(pady=(5,15))

    error_label = ctk.CTkLabel(
        master=window,
        text="",
        text_color="#F87171"
    )
    error_label.pack(pady=(0,10))

    borrow_btn = ctk.CTkButton(
        master=window,
        text="Borrow",
        fg_color="#22C55E",
        hover_color="#16A34A",
        command=lambda: borrow_book(
            book,
            member_entry,
            window,
            table_frame,
            library,
            error_label
        )
    )
    borrow_btn.pack()


def borrow_book(book, member_entry, window, table_frame, library, error_label):

    member_id_text = member_entry.get().strip()

    if not member_id_text.isdigit():
        error_label.configure(text="Member ID must be a number.")
        return

    member_id = int(member_id_text)

    student = None
    for s in library.students.Students:
        if s.Student_ID == member_id:
            student = s
            break

    if student is None:
        error_label.configure(text="Member ID not found.")
        return

    try:
        library.lend_book(student, book)
    except ValueError as e:
        error_label.configure(text=str(e))
        return

    library.log(f"'{book.name}' borrowed by {student.name}")
    show_books_table(table_frame, library.All_Books.books, library)
    window.destroy()


def return_book(book, table_frame, library):

    student = book.borrowed_by

    if student is None:
        return

    try:
        library.Return_book(student, book)
    except ValueError as e:
        print(e)
        return

    library.log(f"'{book.name}' returned by {student.name}")
    show_books_table(table_frame, library.All_Books.books, library)


def search_books(search_type, query, table_frame, library):

    results = []
    query = query.strip()

    for book in library.All_Books.books:

        if search_type == "Book ID":
            if str(book.Book_ID) == query:
                results.append(book)

        elif search_type == "Book Name":
            if query.lower() in book.name.lower():
                results.append(book)

        elif search_type == "Author":
            if query.lower() in book.author.lower():
                results.append(book)

    show_books_table(table_frame, results, library)


def show_books(content, library):

    header_frame = ctk.CTkFrame(
        master=content,
        fg_color="transparent",
        height=60
    )
    header_frame.pack(fill="x", padx=20, pady=(20,10))
    header_frame.pack_propagate(False)
    header_frame.grid_columnconfigure(0, weight=1)
    header_frame.grid_columnconfigure(1, weight=0)

    table_frame = ctk.CTkFrame(
        master=content,
        corner_radius=10,
        fg_color="#2B2B40"
    )

    search_frame = ctk.CTkFrame(
        master=content,
        fg_color="transparent"
    )
    search_frame.pack(fill="x", padx=20, pady=(0,10))

    search_type_box = ctk.CTkComboBox(
        master=search_frame,
        values=["Book Name","Author","Book ID"],
        width=150
    )
    search_type_box.set("Book Name")
    search_type_box.pack(side="left", padx=(0,10))

    search_entry = ctk.CTkEntry(
        master=search_frame,
        placeholder_text="Search books...",
        width=280
    )
    search_entry.pack(side="left", padx=(0,10))

    search_btn = ctk.CTkButton(
        master=search_frame,
        text="Search",
        width=90,
        fg_color="#3A1FA8",
        hover_color="#2C1780",
        command=lambda: search_books(
            search_type_box.get(),
            search_entry.get(),
            table_frame,
            library
        )
    )
    search_btn.pack(side="left")

    clear_btn = ctk.CTkButton(
        master=search_frame,
        text="Clear",
        width=80,
        fg_color="#4B4B63",
        hover_color="#3B3B4F",
        command=lambda: show_books_table(table_frame, library.All_Books.books, library)
    )
    clear_btn.pack(side="left", padx=(10,0))

    global current_table
    current_table = table_frame

    table_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))
    show_books_table(table_frame, library.All_Books.books, library)

    books_title = ctk.CTkLabel(
        master=header_frame,
        text="Books",
        font=("Arial", 28, "bold")
    )
    books_title.grid(row=0, column=0, sticky="w")

    add_book_btn = ctk.CTkButton(
        master=header_frame,
        text="Add Book",
        width=150,
        fg_color="#3A1FA8",
        hover_color="#2C1780",
        command=lambda: open_add_book(table_frame, library)
    )
    add_book_btn.grid(row=0, column=1)
