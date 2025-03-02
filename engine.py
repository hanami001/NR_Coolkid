import pandas as pd
import os
import hashlib
from pathlib import Path

class UserManager:
    def __init__(self, csv_path="data/users.csv"):
        """
        Initialize UserManager - creates CSV if it doesn't exist
        
        Parameters:
        csv_path (str): Path to the CSV file for storing user data
        """
        self.csv_path = csv_path
        
        # Create data directory if it doesn't exist
        Path(os.path.dirname(csv_path)).mkdir(parents=True, exist_ok=True)
        
        # Create CSV file with headers if it doesn't exist
        if not os.path.exists(csv_path):
            headers = ['username', 'password', 'bank', 'card_type', 'lifestyle']
            pd.DataFrame(columns=headers).to_csv(csv_path, index=False)
    
    def _hash_password(self, password):
        """
        Hash password for security
        
        Parameters:
        password (str): Plain password
        
        Returns:
        str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password, bank, card_type, lifestyle):
        """
        Register a new user
        
        Parameters:
        username (str): Username
        password (str): Password
        bank (str): Bank name
        card_type (str): Credit card type
        lifestyle (str): User lifestyle
        
        Returns:
        bool: True if registration successful, False otherwise
        str: Message about the result
        """
        # Load current users
        df = pd.read_csv(self.csv_path)
        
        # Check if username already exists
        if username in df['username'].values:
            return False, "Username already exists"
        
        # Hash the password
        hashed_password = self._hash_password(password)
        
        # Add new user
        new_user = pd.DataFrame({
            'username': [username],
            'password': [hashed_password],
            'bank': [bank],
            'card_type': [card_type],
            'lifestyle': [lifestyle]
        })
        
        # Append to CSV
        df = pd.concat([df, new_user], ignore_index=True)
        df.to_csv(self.csv_path, index=False)
        
        return True, "Registration successful"
    
    def authenticate_user(self, username, password):
        """
        Authenticate a user
        
        Parameters:
        username (str): Username
        password (str): Password
        
        Returns:
        bool: True if authentication successful, False otherwise
        """
        if not os.path.exists(self.csv_path):
            return False
        
        df = pd.read_csv(self.csv_path)
        
        if username not in df['username'].values:
            return False
        
        hashed_password = self._hash_password(password)
        user_data = df[df['username'] == username]
        
        return user_data['password'].values[0] == hashed_password
    
    def get_user_data(self, username):
        """
        Get user data
        
        Parameters:
        username (str): Username
        
        Returns:
        dict: User data as dictionary
        """
        df = pd.read_csv(self.csv_path)
        user_row = df[df['username'] == username]
        
        if len(user_row) == 0:
            return None
        
        # Convert to dictionary
        user_data = user_row.iloc[0].to_dict()
        # Remove password from returned data
        user_data.pop('password', None)
        
        return user_data

# Constants for dropdowns
BANKS = [
    "กสิกรไทย (KBANK)", 
    "ไทยพาณิชย์ (SCB)", 
    "กรุงเทพ (BBL)", 
    "กรุงไทย (KTB)", 
    "กรุงศรี (BAY)", 
    "ทหารไทยธนชาต (TTB)",
    "อื่นๆ"
]

CARD_TYPES = [
    "บัตรเครดิตทั่วไป",
    "บัตรเครดิตแคชแบ็ค",
    "บัตรเครดิตสะสมไมล์",
    "บัตรเครดิตเพื่อผู้ประกอบการ",
    "บัตรเครดิตเพื่อการเดินทาง",
    "อื่นๆ"
]

LIFESTYLES = [
    "นักช้อป",
    "นักเดินทาง",
    "คนรักอาหาร",
    "ประหยัดและออม",
    "นักกีฬา",
    "คนทำงาน",
    "อื่นๆ"
]
