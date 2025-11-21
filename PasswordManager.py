from datetime import datetime
import pandas as pd
#from Password_dictionary import Password_dictionary

class PasswordManager:
    """
    Manages password entries using a pandas.

    Each password entry includes:
    - site
    - username
    - password
    - notes
    - created_at
    """

    def __init__(self, storage_file="passwords.csv"):
        """
        Initialize the PasswordManager.

        Attempts to load existing passwords from the storage file.
        If the file does not exist, starts with an empty set of entries.
        """
        self.storage_file = storage_file
        try:
            self.df = pd.read_csv(self.storage_file)
        except FileNotFoundError:
            self.df = pd.DataFrame(
                columns=["site", "username", "password", "notes", "created_at"]
            )
    
    def add_password(self, site, username, password, notes=""):
        """
        Add a new password entry.
        """
        new_entry = {
            "site": site,
            "username": username,
            "password": password,
            "notes": notes,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        self.df = pd.concat(
            [self.df, pd.DataFrame([new_entry])],
            ignore_index=True
        )

    def list_passwords(self):
        """
        Return all password entries as a list of dictionaries.
        """
        return self.df.to_dict(orient="records")

    def find_by_site(self, site):
        """
        Return all password entries for a given site name.
        Matching is case-insensitive.
        """
        if "site" not in self.df.columns:
            return []
        mask = self.df["site"].astype(str).str.lower() == site.lower()
        return self.df[mask].to_dict(orient="records")

    def remove_password(self, site, username):
        """
        Remove password entries that match the given site and username.
        Matching is case-insensitive.
        """
        pass
    