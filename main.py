import tkinter as tk
from tkinter import messagebox
from ticket_system import TicketSystem

system = TicketSystem()

root = tk.Tk()
root.title("🎬 Movie Ticket Booking System")
root.geometry("500x650")
root.configure(bg="#1c1c1c")

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def add_movie():
    clear_window()
    tk.Label(root, text="🎬 Add Movie", fg="white", bg="#1c1c1c", font=("Arial", 16)).pack(pady=10)

    tk.Label(root, text="Movie Name:", fg="white", bg="#1c1c1c").pack()
    name_entry = tk.Entry(root)
    name_entry.pack(pady=5)

    tk.Label(root, text="Genre:", fg="white", bg="#1c1c1c").pack()
    genre_entry = tk.Entry(root)
    genre_entry.pack(pady=5)

    tk.Label(root, text="Language:", fg="white", bg="#1c1c1c").pack()
    lang_entry = tk.Entry(root)
    lang_entry.pack(pady=5)

    tk.Label(root, text="Type (2D/3D):", fg="white", bg="#1c1c1c").pack()
    type_var = tk.StringVar(value="2D")
    tk.OptionMenu(root, type_var, "2D", "3D").pack(pady=5)

    def save_movie():
        name = name_entry.get().strip()
        genre = genre_entry.get().strip()
        language = lang_entry.get().strip()
        mov_type = type_var.get()

        if name and genre and language and mov_type:
            if system.movie_exists(name, language, mov_type):
                messagebox.showwarning("Duplicate", "Movie with same name, language and type already exists.")
            else:
                system.add_movie(name, genre, language, mov_type)
                messagebox.showinfo("Success", f"Movie '{name}' added successfully.")
                show_main_interface("admin")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    tk.Button(root, text="Save", command=save_movie).pack(pady=10)
    tk.Button(root, text="🔙 Back", command=lambda: show_main_interface("admin")).pack()

def add_show():
    clear_window()
    tk.Label(root, text="📅 Add Show", fg="white", bg="#1c1c1c", font=("Arial", 16)).pack(pady=10)

    tk.Label(root, text="Movie ID:", fg="white", bg="#1c1c1c").pack()
    movie_id_entry = tk.Entry(root)
    movie_id_entry.pack(pady=5)

    tk.Label(root, text="Start Time (YYYY-MM-DD HH:MM):", fg="white", bg="#1c1c1c").pack()
    start_time_entry = tk.Entry(root)
    start_time_entry.pack(pady=5)

    tk.Label(root, text="End Time (YYYY-MM-DD HH:MM):", fg="white", bg="#1c1c1c").pack()
    end_time_entry = tk.Entry(root)
    end_time_entry.pack(pady=5)

    tk.Label(root, text="Seats:", fg="white", bg="#1c1c1c").pack()
    seats_entry = tk.Entry(root)
    seats_entry.pack(pady=5)

    def save_show():
        try:
            movie_id = int(movie_id_entry.get())
            start_time = start_time_entry.get()
            end_time = end_time_entry.get()
            seats = int(seats_entry.get())

            if start_time and end_time:
                system.add_show(movie_id, start_time, end_time, seats)
                messagebox.showinfo("Success", "Show added successfully.")
                show_main_interface("admin")
            else:
                messagebox.showwarning("Input Error", "Enter valid start and end time.")
        except ValueError:
            messagebox.showerror("Input Error", "Invalid input. IDs and seats must be integers.")

    tk.Button(root, text="Add Show", command=save_show).pack(pady=10)
    tk.Button(root, text="🔙 Back", command=lambda: show_main_interface("admin")).pack()


def show_all_movies():
    window = tk.Toplevel(root)
    window.title("🎬 Current and Upcoming Movies")
    window.geometry("900x400")  # Wider to fit more columns

    from tkinter import ttk
    cols = ("Show ID", "Movie ID", "Name", "Genre", "Language", "Type", "Start Time", "End Time", "Seats")
    tree = ttk.Treeview(window, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(expand=True, fill='both')

    movies = system.get_all_movie_shows()  # This method must return dicts with required keys
    for m in movies:
        seats_info = f"{m['seats_available']}/{m['total_seats']}"
        tree.insert("", "end", values=(
            m['show_id'], m['movie_id'], m['title'], m['genre'],
            m['language'], m['format'], m['start_time'], m['end_time'], seats_info
        ))

def view_movies():
    movies = system.get_movies()
    if not movies:
        messagebox.showinfo("Movies", "No movies found.")
        return
    movie_text = "\n".join(
        f"ID: {m['id']}, Title: {m['name']}, Genre: {m['genre']}"
        for m in movies
    )
    messagebox.showinfo("Movies", movie_text)


def view_shows():
    clear_window()
    tk.Label(root, text="🎞 View Shows for Movie", fg="white", bg="#1c1c1c", font=("Arial", 16)).pack(pady=10)
    tk.Label(root, text="Enter Movie ID:", fg="white", bg="#1c1c1c").pack()
    movie_id_entry = tk.Entry(root)
    movie_id_entry.pack(pady=5)

    def fetch_shows():
        try:
            movie_id = int(movie_id_entry.get())

            # Fetch movie details
            movie = system.get_movie_by_id(movie_id)
            if not movie:
                messagebox.showwarning("Not Found", f"No movie found with ID {movie_id}")
                return

            # Fetch shows
            shows = system.get_shows(movie_id)
            if not shows:
                messagebox.showinfo("No Shows", "No shows available for this movie.")
                return

            # Safe dictionary access with .get()
            movie_info = (
                f"Movie ID: {movie.get('id', 'N/A')}\n"
                f"Name: {movie.get('name', 'N/A')}\n"
                f"Genre: {movie.get('genre', 'N/A')}\n"
                f"Language: {movie.get('language', 'N/A')}\n"
                f"Type: {movie.get('type', 'N/A')}\n"
                f"Release Date: {movie.get('release_date', 'N/A')}\n\n"
            )

            show_text = "\n".join(
                f"Show ID: {s.get('id', 'N/A')}, Start: {s.get('start_time', 'N/A')}, End: {s.get('end_time', 'N/A')}, Seats: {s.get('seats', 'N/A')}"
                for s in shows
            )

            messagebox.showinfo("Show Details", movie_info + show_text)

        except ValueError:
            messagebox.showerror("Input Error", "Movie ID must be an integer.")

    # Buttons section for smoother layout
    button_frame = tk.Frame(root, bg="#1c1c1c")
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="View Shows", width=20, bg="#0066cc", fg="white", command=fetch_shows).pack(side="left", padx=10)
    tk.Button(button_frame, text="🔙 Back", width=20, bg="#888", fg="white", command=lambda: show_main_interface("admin")).pack(side="left", padx=10)




def book_ticket():
    clear_window()
    tk.Label(root, text="🎟️ Book Ticket", fg="white", bg="#1c1c1c", font=("Arial", 16)).pack(pady=10)

    tk.Label(root, text="Show ID:", fg="white", bg="#1c1c1c").pack()
    show_id_entry = tk.Entry(root)
    show_id_entry.pack(pady=5)

    tk.Label(root, text="Customer Name:", fg="white", bg="#1c1c1c").pack()
    customer_entry = tk.Entry(root)
    customer_entry.pack(pady=5)

    tk.Label(root, text="Seats:", fg="white", bg="#1c1c1c").pack()
    seats_entry = tk.Entry(root)
    seats_entry.pack(pady=5)

    def confirm_booking():
        try:
            show_id = int(show_id_entry.get())
            customer = customer_entry.get()
            seats = int(seats_entry.get())
            if customer:
                ticket_id = system.book_ticket(show_id, customer, seats)
                if ticket_id:
                    messagebox.showinfo("Booked", f"Ticket booked! ID: {ticket_id}")
                else:
                    messagebox.showwarning("Unavailable", "Booking failed. Not enough seats or invalid show.")
                show_main_interface("clerk")
            else:
                messagebox.showwarning("Input Error", "Enter customer name.")
        except ValueError:
            messagebox.showerror("Input Error", "Show ID and seats must be integers.")

    tk.Button(root, text="Book", command=confirm_booking).pack(pady=10)
    tk.Button(root, text="🔙 Back", command=lambda: show_main_interface("clerk")).pack()

def cancel_booking():
    clear_window()
    tk.Label(root, text="❌ Cancel Booking", fg="white", bg="#1c1c1c", font=("Arial", 16)).pack(pady=10)
    tk.Label(root, text="Ticket ID:", fg="white", bg="#1c1c1c").pack()
    ticket_id_entry = tk.Entry(root)
    ticket_id_entry.pack(pady=5)

    def confirm_cancel():
        try:
            ticket_id = int(ticket_id_entry.get())
            success = system.cancel_ticket(ticket_id)
            if success:
                messagebox.showinfo("Cancelled", f"Ticket ID {ticket_id} canceled.")
            else:
                messagebox.showwarning("Not Found", "Ticket ID not found.")
            show_main_interface("clerk")
        except ValueError:
            messagebox.showerror("Input Error", "Ticket ID must be an integer.")

    tk.Button(root, text="Cancel Ticket", command=confirm_cancel).pack(pady=10)
    tk.Button(root, text="🔙 Back", command=lambda: show_main_interface("clerk")).pack()

from datetime import datetime

def view_bookings():
    bookings = system.get_all_bookings()
    if not bookings:
        messagebox.showinfo("Bookings", "No bookings found.")
    else:
        now = datetime.now()
        upcoming = [
            b for b in bookings
            if datetime.strptime(b['show_time'], "%Y-%m-%d %H:%M") >= now
        ]
        if not upcoming:
            messagebox.showinfo("Bookings", "No upcoming bookings.")
            return
        booking_text = "\n".join(
            f"ID: {b['id']}, Customer: {b['customer']}, Show ID: {b['show_id']}, Seats: {b['seats']}, Time: {b['show_time']}"
            for b in upcoming
        )
        messagebox.showinfo("Bookings", booking_text)

def show_main_interface(role):
    clear_window()
    tk.Label(root, text="🎬 Ticket Booking Dashboard", fg="white", bg="#1c1c1c", font=("Arial", 18)).pack(pady=20)

    if role == "admin":
        tk.Label(root, text="👨‍💼 Admin Actions", fg="white", bg="#1c1c1c", font=("Arial", 14, "bold")).pack(pady=(10, 5))
        admin_buttons = [
            ("1. Add Movie", add_movie),
            ("2. View Movies", view_movies),  # moved here
            ("3. Add Show", add_show),
            ("4. View Shows for a Movie", view_shows),
            ("5. View All Movies (Today & Upcoming)", show_all_movies)
        ]

        for text, command in admin_buttons:
            tk.Button(root, text=text, width=35, height=2, bg="#444", fg="white", command=command).pack(pady=3)

    elif role == "clerk":
        tk.Label(root, text="🎫 Booking Clerk Actions", fg="white", bg="#1c1c1c", font=("Arial", 14, "bold")).pack(pady=(10, 5))
        clerk_buttons = [
            ("1. Book Ticket", book_ticket),
            ("2. Cancel Booking", cancel_booking),
            ("3. View All Bookings", view_bookings),
            ("4. View All Movies (Today & Upcoming)", show_all_movies)
        ]
        for text, command in clerk_buttons:
            tk.Button(root, text=text, width=35, height=2, bg="#444", fg="white", command=command).pack(pady=3)

    tk.Button(root, text="🔙 Logout", width=35, height=2, bg="#555555", fg="white", command=show_role_selection).pack(pady=10)
    tk.Button(root, text="❌ Exit", width=35, height=2, bg="#880000", fg="white", command=root.destroy).pack(pady=10)

def show_role_selection():
    clear_window()
    tk.Label(root, text="🎟️ Select Role to Login", fg="white", bg="#1c1c1c", font=("Arial", 18)).pack(pady=50)
    tk.Button(root, text="👨‍💼 Admin Login", width=25, height=2, bg="#2c3e50", fg="white", command=lambda: show_login("admin")).pack(pady=15)
    tk.Button(root, text="🎫 Booking Clerk Login", width=25, height=2, bg="#16a085", fg="white", command=lambda: show_login("clerk")).pack(pady=15)
    tk.Button(root, text="❌ Exit", width=25, height=2, bg="#880000", fg="white", command=root.destroy).pack(pady=40)

def show_login(role):
    clear_window()
    role_name = "Admin" if role == "admin" else "Booking Clerk"
    tk.Label(root, text=f"🔐 {role_name} Login", fg="white", bg="#1c1c1c", font=("Arial", 18)).pack(pady=30)

    tk.Label(root, text="Username:", fg="white", bg="#1c1c1c").pack()
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password:", fg="white", bg="#1c1c1c").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if role == "admin" and username == "admin" and password == "admin123":
            show_main_interface("admin")
        elif role == "clerk" and username == "clerk" and password == "clerk123":
            show_main_interface("clerk")
        else:
            messagebox.showerror("Login Failed", f"Invalid credentials for {role_name}!")

    tk.Button(root, text="Login", width=20, height=2, bg="#0066cc", fg="white", command=login).pack(pady=20)
    tk.Button(root, text="🔙 Back", width=20, height=2, bg="#888", fg="white", command=show_role_selection).pack()

# Launch the app
show_role_selection()
root.mainloop()
