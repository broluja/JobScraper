import json
import os
from uuid import uuid4
from datetime import date

from exceptions import *


class Filer:
    """CLass for filing applied job adds. It uses files and json for storing objects."""
    filename = "applied-adds.txt"

    def __init__(self):
        if self.filename not in os.listdir(os.getcwd()):
            self.init_file(self.filename)
        else:
            print("File initialized.")

    @staticmethod
    def init_file(file: str) -> None:
        """
        Initialize file for storing records.
        :param file: Str, file name
        :return: None.
        """
        records = {}
        with open(file, "w") as writer:
            writer.write(json.dumps(records, indent=4))

    @classmethod
    def read(cls, filename: str) -> dict:
        """
        Read the file and create dict object using json.
        :param filename: Name of the file, str.
        :return: dict.
        """
        try:
            with open(filename) as reader:
                records = json.loads(reader.read())
            return records
        except FileNotFoundError:
            raise InitializeFileError(f"We cannot find file: {cls.filename}. Make sure you initialized files.")

    @classmethod
    def write(cls, records: dict, filename: str) -> None:
        """
        Write to file, converting dict object to string using json.
        :param records: dict object, representing data from the file.
        :param filename: Name of the file, str.
        :return: None.
        """
        try:
            with open(filename, "w") as writer:
                writer.write(json.dumps(records, indent=4))
        except FileNotFoundError:
            raise InitializeFileError(f"We cannot find file: {cls.filename}. Make sure you initialized files.")

    def save_add(self, company, description, link, date_applied=date.today().isoformat()):
        """
        Storing add to the database.

        param company: Name of the company
        param description: Description of the add.
        param link: Link to the add.
        param date_applied: Date when user applied.
        """
        records = self.read(self.filename)
        new_add_id = str(uuid4())
        records[new_add_id] = {
            "company": company,
            "job_description": description,
            "link": link,
            "date_applied": date_applied
        }
        self.write(records, self.filename)

