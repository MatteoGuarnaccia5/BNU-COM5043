import json
import os
from typing import Any


class Database:
    def __init__(self) -> None:
        self.base_dir = os.path.dirname(__file__) 
        
    def load_data(self, path) -> list[Any]:
        """Load data from database"""
        try:
            # pylint: disable=unspecified-encoding
            with open(os.path.join(self.base_dir, path), "r") as file:
                return json.load(file)
            file.close()
        except FileNotFoundError as e:
            print(e)
            return []

    def save_data(self, data, path) -> None:
        """Save database"""
        try:
        # pylint: disable=unspecified-encoding
            with open(os.path.join(self.base_dir, path), "w") as file:
                json.dump([d.to_json() for d in data], file)
            file.close()
        except Exception as e:
            print(e)