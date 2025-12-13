from datetime import datetime
import sqlite3
import random
import pandas as pd

from PasswordStrengthChecker import PasswordStrengthChecker
from PasswordDictionary import ALL_CHARS
from PasswordGenerator import PasswordGenerator, GeneratorPolicy

class PasswordManager:
    """
    Manages password entries using SQLite for storage
    Uses pandas for viewing, importing, and exporting password data
    """

    def __init__(self, db_name="passwords.db", min_strength="Medium"):
        """
        Initialize the PasswordManager
        Store the database file name
        Create the passwords table
        Load existing data into a pandas dataframe
        """
        self.db_name = db_name
        self.min_strength = min_strength
        self.checker = PasswordStrengthChecker()
        self.generator = PasswordGenerator(GeneratorPolicy(min_length=15, max_length=32))
        self._create_table()
        self.df = self._load_from_db()
        

    def _connect(self):
        """
        Create and return a connection to the sqlite database.
        """
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        """
        Create the passwords table
        """
        with self._connect() as conn:
            cur = conn.cursor()

            # defines the structure of the passwords table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

            #saves the changes
            conn.commit()

    def _load_from_db(self):
        """
        Load all password records from sqlite into a pandas DataFrame
        """
        with self._connect() as conn:
            # executes the sql and returns a dataframe
            return pd.read_sql_query(
                "SELECT id, site, username, password, created_at FROM passwords ORDER BY id ASC",
                conn
            )

    def _refresh_df(self):
        """
        Refresh the DataFrame
        """
        self.df = self._load_from_db()

    def _enforce_strength(self, password: str) -> str:
        label = self.checker.get_strength_label(password)
        if not self.checker.meets_min_strength(password, self.min_strength):
            raise ValueError(f"Password too weak ({label}). Minimum required: {self.min_strength}")
        return label

    def generate_password(self, length=15):
        """
        Generate a random password using ALL_CHARS
        Password length must be between 15 and 32 characters
        """
        if length < 15 or length > 32:
            raise ValueError("Password length must be between 15 and 32 characters.")

        # Randomly select characters and join them into one string
        return "".join(random.choice(ALL_CHARS) for _ in range(length))

    def add_password(self, site, username, password):
        """
        Add a new password entry to the database
        and returns the password strength label
        """
        # Use passwordstrengthchecker
        strength_label = self._enforce_strength(password)

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("""
                        INSERT INTO passwords (site, username, password, created_at)
                        VALUES (?, ?, ?, ?)
                        """, (site, username, password, created_at))
            conn.commit()

        # Reload dataframe
        self._refresh_df()
        return strength_label

    def get_all_passwords(self):
        """
        Return all password entries as a list of dictionaries
        """
        self._refresh_df()
        return self.df.to_dict(orient="records")

    def get_passwords_for_site(self, site):
        """
        Return all password entries that match a given site name
        """
        self._refresh_df()

        # If the database is empty it returns an empty list
        if self.df.empty:
            return []

        # Convert both values to lowercase to avoid it being case sensitive
        mask = self.df["site"].astype(str).str.lower() == site.lower()

        # Convert rows back into a list of dictionaries
        return self.df[mask].to_dict(orient="records")

    def update_password(self, entry_id, new_password):
        """
        Update the password for a specific entry ID
        Returns the new password strength label
        """
        strength_label = self._enforce_strength(new_password)

        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE passwords SET password = ? WHERE id = ?", (new_password, entry_id))
            conn.commit()

        self._refresh_df()
        return strength_label

    def remove_password(self, entry_id):
        """
        Remove a password entry by its database ID
        """
        with self._connect() as conn:
            cur = conn.cursor()

            # Delete the row with the matching id
            cur.execute("DELETE FROM passwords WHERE id = ?", (entry_id,))
            conn.commit()

        self._refresh_df()

    def export_csv(self, csv_path):
        """
        Export all password entries to a csv file using pandas
        """
        self._refresh_df()

        # donesnt let pandas from adding an extra index column
        self.df.to_csv(csv_path, index=False)

    def import_csv(self, csv_path):
        df_in = pd.read_csv(csv_path)
        required = {"site", "username", "password"}
        if not required.issubset(df_in.columns):
            raise ValueError("CSV must include: site, username, password")

        imported = 0
        skipped = 0

        with self._connect() as conn:
            cur = conn.cursor()
            for _, row in df_in.iterrows():
                pwd = str(row["password"])
                try:
                    self._enforce_strength(pwd)
                except ValueError:
                    skipped += 1
                    continue

                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cur.execute("""
                    INSERT INTO passwords (site, username, password, created_at)
                    VALUES (?, ?, ?, ?)
                """, (row["site"], row["username"], pwd, created_at))
                imported += 1
            conn.commit()

        self._refresh_df()
        return imported, skipped