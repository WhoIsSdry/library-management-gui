import customtkinter as ctk


def show_dashboard(content, library):

    header_frame = ctk.CTkFrame(
        master=content,
        fg_color="transparent",
        height=60
    )
    header_frame.pack(fill="x", padx=20, pady=(20,10))
    header_frame.pack_propagate(False)

    ctk.CTkLabel(
        master=header_frame,
        text="Dashboard",
        font=("Arial", 28, "bold")
    ).pack(anchor="w")

    stats_frame = ctk.CTkFrame(
        master=content,
        fg_color="transparent"
    )
    stats_frame.pack(fill="x", padx=20, pady=(0,10))

    stats = [
        ("Total Books", len(library.All_Books.books), "#3B82F6"),
        ("Available", len(library.SHELF.books), "#22C55E"),
        ("Borrowed", len(library.lend), "#F59E0B"),
        ("Members", len(library.students.Students), "#A855F7"),
    ]

    for i, (label_text, value, color) in enumerate(stats):

        stats_frame.grid_columnconfigure(i, weight=1)

        card = ctk.CTkFrame(
            master=stats_frame,
            corner_radius=10,
            fg_color="#2B2B40",
            border_width=2,
            border_color=color
        )
        card.grid(row=0, column=i, padx=(0 if i == 0 else 10, 0), sticky="nsew")

        ctk.CTkLabel(
            master=card,
            text=str(value),
            font=("Arial", 26, "bold"),
            text_color=color
        ).pack(pady=(15,0))

        ctk.CTkLabel(
            master=card,
            text=label_text,
            font=("Arial", 13),
            text_color="#9A9AB0"
        ).pack(pady=(0,15))

    body_frame = ctk.CTkFrame(
        master=content,
        fg_color="transparent"
    )
    body_frame.pack(fill="both", expand=True, padx=20, pady=(10,20))
    body_frame.grid_columnconfigure(0, weight=1)
    body_frame.grid_columnconfigure(1, weight=1)
    body_frame.grid_rowconfigure(0, weight=1)

    borrowed_frame = ctk.CTkFrame(
        master=body_frame,
        corner_radius=10,
        fg_color="#2B2B40"
    )
    borrowed_frame.grid(row=0, column=0, sticky="nsew", padx=(0,10))

    ctk.CTkLabel(
        master=borrowed_frame,
        text="Currently Borrowed",
        font=("Arial", 16, "bold")
    ).pack(anchor="w", padx=15, pady=(15,5))

    borrowed_list = ctk.CTkScrollableFrame(
        master=borrowed_frame,
        fg_color="transparent"
    )
    borrowed_list.pack(fill="both", expand=True, padx=10, pady=(0,10))

    if library.lend:
        for book in library.lend:
            who = book.borrowed_by.name if book.borrowed_by else "Unknown"
            ctk.CTkLabel(
                master=borrowed_list,
                text=f"{book.name} \u2014 {who}",
                anchor="w",
                text_color="#F59E0B"
            ).pack(fill="x", pady=2)
    else:
        ctk.CTkLabel(
            master=borrowed_list,
            text="No books currently borrowed.",
            text_color="#9A9AB0"
        ).pack(pady=10)

    activity_frame = ctk.CTkFrame(
        master=body_frame,
        corner_radius=10,
        fg_color="#2B2B40"
    )
    activity_frame.grid(row=0, column=1, sticky="nsew", padx=(10,0))

    ctk.CTkLabel(
        master=activity_frame,
        text="Recent Activity",
        font=("Arial", 16, "bold")
    ).pack(anchor="w", padx=15, pady=(15,5))

    activity_list = ctk.CTkScrollableFrame(
        master=activity_frame,
        fg_color="transparent"
    )
    activity_list.pack(fill="both", expand=True, padx=10, pady=(0,10))

    if library.activity_log:
        for entry in library.activity_log:
            ctk.CTkLabel(
                master=activity_list,
                text=entry,
                anchor="w",
                text_color="#F5F5F5"
            ).pack(fill="x", pady=2)
    else:
        ctk.CTkLabel(
            master=activity_list,
            text="No activity yet.",
            text_color="#9A9AB0"
        ).pack(pady=10)
