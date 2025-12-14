from db_config import connect_db
import datetime  # Use only this import for datetime operations

class TicketSystem:
    def __init__(self):
        self.conn = connect_db()
        self.cursor = self.conn.cursor()

    def add_movie(self, title, genre, language, mov_format, release_date=None):
        if release_date is None:
            release_date = datetime.date.today()
        self.cursor.execute(
            "INSERT INTO movies (title, genre, language, format, release_date) VALUES (%s, %s, %s, %s, %s)",
            (title, genre, language, mov_format, release_date)
        )
        self.conn.commit()

    def movie_exists(self, title, language, mov_format):
        self.cursor.execute(
            "SELECT * FROM movies WHERE title = %s AND language = %s AND format = %s",
            (title, language, mov_format)
        )
        return self.cursor.fetchone() is not None

    def get_movies(self):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("SELECT * FROM movies WHERE release_date >= %s", (current_date,))
        rows = self.cursor.fetchall()
        return [
            {
                'id': row[0],
                'name': row[1],
                'genre': row[2],
                'language': row[3],
                'type': row[4],
                'release_date': row[5].strftime("%Y-%m-%d")
            } for row in rows
        ]

    def add_show(self, movie_id, start_time, end_time, seats):
        self.cursor.execute(
            "INSERT INTO shows (movie_id, start_time, end_time, seats_available) VALUES (%s, %s, %s, %s)",
            (movie_id, start_time, end_time, seats)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_shows(self, movie_id):
        self.cursor.execute("SELECT * FROM shows WHERE movie_id = %s", (movie_id,))
        rows = self.cursor.fetchall()
        return [
            {'id': row[0], 'movie_id': row[1], 'start_time': row[2], 'end_time': row[3], 'seats': row[4]}
            for row in rows
        ]

    def get_movie_by_id(self, movie_id):
        self.cursor.execute("SELECT * FROM movies WHERE movie_id = %s", (movie_id,))
        result = self.cursor.fetchone()
        if result:
            return {
                'id': result[0],
                'name': result[1],
                'genre': result[2],
                'language': result[3],
                'type': result[4],
                'release_date': result[5]
            }
        return None

    def book_ticket(self, show_id, customer_name, seats):
        self.cursor.execute("SELECT seats_available FROM shows WHERE show_id = %s", (show_id,))
        result = self.cursor.fetchone()

        if result is None:
            raise ValueError(f"No show found with ID {show_id}.")

        available_seats = result[0]

        if available_seats is None:
            raise ValueError(f"Seat information not available for show ID {show_id}.")

        if available_seats >= seats:
            self.cursor.execute(
                "INSERT INTO bookings (show_id, customer_name, seats_booked) VALUES (%s, %s, %s)",
                (show_id, customer_name, seats)
            )
            self.cursor.execute(
                "UPDATE shows SET seats_available = seats_available - %s WHERE show_id = %s",
                (seats, show_id)
            )
            self.conn.commit()
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            booking_id = self.cursor.fetchone()[0]
            return booking_id
        else:
            raise ValueError(f"Only {available_seats} seats are available. Cannot book {seats} seats.")

    def cancel_ticket(self, ticket_id):
        self.cursor.execute("SELECT show_id, seats_booked FROM bookings WHERE booking_id = %s", (ticket_id,))
        result = self.cursor.fetchone()
        if result:
            show_id, seats = result
            self.cursor.execute("DELETE FROM bookings WHERE booking_id = %s", (ticket_id,))
            self.cursor.execute("UPDATE shows SET seats_available = seats_available + %s WHERE show_id = %s", (seats, show_id))
            self.conn.commit()
            return True
        return False

    def get_all_bookings(self):
        import datetime
        now = datetime.datetime.now()

        self.cursor.execute("""
            SELECT b.booking_id, b.customer_name, b.seats_booked, s.show_id, s.start_time 
            FROM bookings b
            JOIN shows s ON b.show_id = s.show_id
            WHERE s.start_time >= %s
            ORDER BY s.start_time
        """, (now,))

        rows = self.cursor.fetchall()
        return [
            {
                'id': row[0],
                'customer': row[1],
                'seats': row[2],
                'show_id': row[3],
                'show_time': row[4].strftime("%Y-%m-%d %H:%M")
            }
            for row in rows
        ]

    def show_all_movies():
        window = tk.Toplevel(root)
        window.title("🎬 All Movies with Movie ID and Show ID")
        window.geometry("900x400")  # Wider to fit more columns

        from tkinter import ttk
        cols = ("Show ID", "Movie ID", "Name", "Genre", "Language", "Type", "Start Time", "End Time", "Seats")
        tree = ttk.Treeview(window, columns=cols, show='headings')
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(expand=True, fill='both')

        movies = system.get_all_movie_shows()  # This must return the necessary info
        for m in movies:
            seats_info = f"{m['seats_available']}/{m['total_seats']}"
            tree.insert("", "end", values=(
                m['show_id'], m['movie_id'], m['name'], m['genre'],
                m['language'], m['type'], m['start_time'], m['end_time'], seats_info
            ))

    from datetime import datetime

    def get_all_movie_shows(self):
        self.cursor.execute("""
            SELECT m.movie_id, m.title, m.genre, m.language, m.format, m.release_date, 
                   s.show_id, s.start_time, s.end_time, s.seats_available,
                   s.seats_available + COALESCE(
                       (SELECT SUM(b.seats_booked) FROM bookings b WHERE b.show_id = s.show_id), 0
                   ) AS total_seats
            FROM movies m
            JOIN shows s ON m.movie_id = s.movie_id
            ORDER BY s.start_time
        """)
        rows = self.cursor.fetchall()
        result = []
        for row in rows:
            start_time = row[7]
            end_time = row[8]

            # Convert to readable format if not None
            formatted_start = start_time.strftime("%Y-%m-%d %H:%M") if start_time else "N/A"
            formatted_end = end_time.strftime("%Y-%m-%d %H:%M") if end_time else "N/A"

            result.append({
                'movie_id': row[0],
                'title': row[1],
                'genre': row[2],
                'language': row[3],
                'format': row[4],
                'release_date': row[5],
                'show_id': row[6],
                'start_time': formatted_start,
                'end_time': formatted_end,
                'seats_available': row[9],
                'total_seats': row[10]
            })
        return result

