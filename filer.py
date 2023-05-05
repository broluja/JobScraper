import json
import os
from uuid import uuid4
from datetime import date

from exceptions import *
from config import FILE, GARBAGE


class Filer:
    """CLass for filing applied job adds. It uses files and json for storing objects."""
    filename = FILE
    ignored = GARBAGE

    def __init__(self):
        files = os.listdir('files')
        if self.filename.split("/")[-1] not in files or self.ignored.split("/")[-1] not in files:
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
        with open(self.ignored, "w") as writer:
            writer.write(json.dumps(records, indent=4))

    def read(self, ignoring=False) -> dict:
        """
        Read the file and create dict object using json.

        Return: dict.
        """
        if ignoring:
            try:
                with open(self.ignored) as reader:
                    records = json.loads(reader.read())
                return records
            except FileNotFoundError as exc:
                raise InitializeFileError(f"We cannot find file: {self.ignored}. Please, initialize files.") from exc
        else:
            try:
                with open(self.filename) as reader:
                    records = json.loads(reader.read())
                return records
            except FileNotFoundError as exc:
                raise InitializeFileError(f"We cannot find file: {self.filename}. Please, initialize files.") from exc

    def write(self, records: dict, ignoring=False) -> None:
        """
        Write to file, converting dict object to string using json.
        Param records: dict object, representing data from the file.

        Return: None.
        """
        if ignoring:
            try:
                with open(self.ignored, "w") as writer:
                    writer.write(json.dumps(records, indent=4))
            except FileNotFoundError as exc:
                raise InitializeFileError(f"We cannot find file: {self.ignored}. Please, initialize files.") from exc
        else:
            try:
                with open(self.filename, "w") as writer:
                    writer.write(json.dumps(records, indent=4))
            except FileNotFoundError as exc:
                raise InitializeFileError(f"We cannot find file: {self.filename}. Please, initialize files.") from exc

    def save_ad(self, company, description, link, date_applied=date.today().isoformat()) -> None:
        """
        Storing ad to the database.

        Param company: Name of the company
        Param description: Description of the add.
        Param link: Link to the add.
        Param date_applied: Date when user applied.
        Return: None.
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

    def ignore_ad(self, company: str, description: str, link: str) -> None:
        """
        Ignoring ad by storing iy in ignored-adds.txt file

        Param company: Name of the company
        Param description: Description of the add.
        Param link: Link to the add.
        Return: None.
        """
        records = self.read(ignoring=True)
        ignored_ad_id = str(uuid4())
        records[ignored_ad_id] = {
            "company": company,
            "job_description": description,
            "link": link
        }
        self.write(records, ignoring=True)
