import pandas as pd
import os

class UserDatabase:
    def __init__(self, filename="users.csv"):
        self.filename = filename
        self.fields = ["username", "password", "bank", "card_type", "lifestyle"]
        if not os.path.exists(self.filename):
            pd.DataFrame(columns=self.fields).to_csv(self.filename, index=False)

    def register_user(self, username, password, bank, card_type, lifestyle):
        df = pd.read_csv(self.filename)
        if username in df["username"].values:
            return False, "Username already exists."
        new_user = pd.DataFrame([[username, password, bank, card_type, lifestyle]], columns=self.fields)
        df = pd.concat([df, new_user], ignore_index=True)
        df.to_csv(self.filename, index=False)
        return True, "User registered successfully."

    def authenticate_user(self, username, password):
        df = pd.read_csv(self.filename)
        user = df[(df["username"] == username) & (df["password"] == password)]
        return not user.empty
