import json
import os
from uuid import uuid4
from datetime import date

from exceptions import *
from config import FILE


class Filer:
    """CLass for filing applied job adds. It uses files and json for storing objects."""
    filename = FILE

    def __init__(self):
        if self.filename.split("/")[-1] not in os.listdir('files'):
            self.init_file()
        else:
            print("File initialized.")

    def init_file(self) -> None:
        """
        Initialize file for storing records.

        Return: None.
        """
        records = {}
        with open(self.filename, "w") as writer:
            writer.write(json.dumps(records, indent=4))

    def read(self) -> dict:
        """
        Read the file and create dict object using json.

        Return: dict.
        """
        try:
            with open(self.filename) as reader:
                records = json.loads(reader.read())
            return records
        except FileNotFoundError:
            raise InitializeFileError(f"We cannot find file: {self.filename}. Make sure you initialized files.")

    def write(self, records: dict) -> None:
        """
        Write to file, converting dict object to string using json.
        Param records: dict object, representing data from the file.

        Return: None.
        """
        try:
            with open(self.filename, "w") as writer:
                writer.write(json.dumps(records, indent=4))
        except FileNotFoundError:
            raise InitializeFileError(f"We cannot find file: {self.filename}. Make sure you initialized files.")

    def save_ad(self, company, description, link, date_applied=date.today().isoformat()):
        """
        Storing add to the database.

        param company: Name of the company
        param description: Description of the add.
        param link: Link to the add.
        param date_applied: Date when user applied.
        """
        records = self.read()
        new_add_id = str(uuid4())
        records[new_add_id] = {
            "company": company,
            "job_description": description,
            "link": link,
            "date_applied": date_applied
        }
        self.write(records)

