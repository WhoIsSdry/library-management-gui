import customtkinter as ctk
from Students import Student

current_table = None


def open_add_member(table_frame, library):

    window = ctk.CTkToplevel()

    window.title("Add Member")
    window.geometry("400x500")
    window.resizable(False, False)

    title = ctk.CTkLabel(
        master=window,
        text="Add Member",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=20)

    id_label = ctk.CTkLabel(
        master=window,
        text="Member ID"
    )
    id_label.pack(anchor="w", padx=30)

    id_entry = ctk.CTkEntry(
        master=window,
        width=300
    )
    id_entry.pack(pady=(5,15))

    name_label = ctk.CTkLabel(
        master=window,
        text="Name"
    )
    name_label.pack(anchor="w", padx=30)

    name_entry = ctk.CTkEntry(
        master=window,
        width=300
    )
    name_entry.pack(pady=(5,15))

    phone_label = ctk.CTkLabel(
        master=window,
        text="Phone"
    )
    phone_label.pack(anchor="w", padx=30)

    phone_entry = ctk.CTkEntry(
        master=window,
        width=300
    )
    phone_entry.pack(pady=(5,20))

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
        command=lambda: save_member(
            id_entry,
            name_entry,
            phone_entry,
            window,
            table_frame,
            library,
            error_label
        )
    )
    save_btn.pack()


def save_member(id_entry, name_entry, phone_entry, window, table_frame, library, error_label):
    error_label.configure(text="")

    id_text = id_entry.get().strip()
    name = name_entry.get().strip()
    phone_text = phone_entry.get().strip()

    if not id_text.isdigit():
        error_label.configure(text="Member ID must be a number.")
        return

    if not name or not all(c.isalpha() or c.isspace() for c in name):
        error_label.configure(text="Name must contain only letters and spaces.")
        return

    if not phone_text.isdigit():
        error_label.configure(text="Phone number must contain digits only.")
        return

    member_id = int(id_text)

    student = Student(
        books=[],
        name=name,
        Student_ID=member_id,
        Phone_number=phone_text
    )

    library.students.add_student(student)
    library.log(f"Added member '{name}' (ID {member_id})")

    window.destroy()

    show_members_table(table_frame, library)


def show_members_table(table_frame, library, student_list=None):

    for widget in table_frame.winfo_children():
        widget.destroy()

    header = ctk.CTkFrame(
        master=table_frame,
        fg_color="#3A1FA8"
    )
    header.pack(fill="x", padx=10, pady=(10,5))

    ctk.CTkLabel(header, text="ID", width=100, font=("Arial", 14, "bold")).pack(side="left")
    ctk.CTkLabel(header, text="Name", width=220, font=("Arial", 14, "bold")).pack(side="left")
    ctk.CTkLabel(header, text="Phone", width=180, font=("Arial", 14, "bold")).pack(side="left")

    students = student_list if student_list is not None else library.students.Students

    for i, student in enumerate(students):

        row_color = "#26263A" if i % 2 == 0 else "#2F2F46"

        row = ctk.CTkFrame(
            master=table_frame,
            fg_color=row_color
        )
        row.pack(fill="x", padx=10, pady=3)

        ctk.CTkLabel(row, text=student.Student_ID, width=100).pack(side="left")
        ctk.CTkLabel(row, text=student.name, width=220).pack(side="left")
        ctk.CTkLabel(row, text=student.Phone_number, width=180).pack(side="left")


def search_members(query, table_frame, library):

    query = query.strip()
    results = []

    for student in library.students.Students:
        if query.lower() in student.name.lower() or query == str(student.Student_ID):
            results.append(student)

    show_members_table(table_frame, library, results)


def show_members(content, library):

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

    search_entry = ctk.CTkEntry(
        master=search_frame,
        placeholder_text="Search by name or ID...",
        width=280
    )
    search_entry.pack(side="left", padx=(0,10))

    search_btn = ctk.CTkButton(
        master=search_frame,
        text="Search",
        width=90,
        fg_color="#3A1FA8",
        hover_color="#2C1780",
        command=lambda: search_members(search_entry.get(), table_frame, library)
    )
    search_btn.pack(side="left")

    clear_btn = ctk.CTkButton(
        master=search_frame,
        text="Clear",
        width=80,
        fg_color="#4B4B63",
        hover_color="#3B3B4F",
        command=lambda: show_members_table(table_frame, library)
    )
    clear_btn.pack(side="left", padx=(10,0))

    global current_table
    current_table = table_frame

    table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    show_members_table(table_frame, library)

    members_title = ctk.CTkLabel(
        master=header_frame,
        text="Members",
        font=("Arial", 28, "bold")
    )
    members_title.grid(row=0, column=0, sticky="w")

    add_member_btn = ctk.CTkButton(
        master=header_frame,
        text="Add Member",
        width=150,
        fg_color="#3A1FA8",
        hover_color="#2C1780",
        command=lambda: open_add_member(table_frame, library)
    )
    add_member_btn.grid(row=0, column=1)
