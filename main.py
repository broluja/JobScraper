import tkinter
import customtkinter as ctk

from scraper import JobScraper
from config import *
from widgets import APPLabel, JobsFrame
from filer import Filer


class JobScraperApp(ctk.CTk):
    """Job Scraper APP for scraping Python developer positions on biggest job market sites."""

    def __init__(self):
        super().__init__()
        self._scraper = JobScraper()
        self._filer = Filer()
        self.configure_window()
        self.hello_world_adds = None
        self.infostud_adds = None
        self.linked_in_adds = None
        self.teamcubate_adds = None
        self.jooble = None
        self.joberty = None
        self.applied_adds = self.filer.read()

        # Create sidebar frame with widgets
        self.side_frame = ctk.CTkFrame(self, width=WIDTH // 10, corner_radius=0, border_width=1)
        self.side_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.side_frame.grid_rowconfigure(9, weight=1)

        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = APPLabel(master=self.side_frame, text="Select Job Ads Site", size=18)
        self.label_radio_group.grid(row=1, column=0, padx=10, pady=(20, 10))
        self.radio_button_1 = ctk.CTkRadioButton(self.side_frame, variable=self.radio_var, value=0, text="Hello World")
        self.radio_button_1.grid(row=2, column=0, pady=8, padx=20, sticky="n")
        self.radio_button_2 = ctk.CTkRadioButton(self.side_frame, variable=self.radio_var, value=1, text="Infostud")
        self.radio_button_2.grid(row=3, column=0, pady=8, padx=20, sticky="n")
        self.radio_button_3 = ctk.CTkRadioButton(self.side_frame, variable=self.radio_var, value=2, text="LinkedIn")
        self.radio_button_3.grid(row=4, column=0, pady=8, padx=20, sticky="n")
        self.radio_button_4 = ctk.CTkRadioButton(self.side_frame, variable=self.radio_var, value=3, text="Teamcubate")
        self.radio_button_4.grid(row=5, column=0, pady=8, padx=20, sticky="n")
        self.radio_button_5 = ctk.CTkRadioButton(self.side_frame, variable=self.radio_var, value=4, text="Jooble")
        self.radio_button_5.grid(row=6, column=0, pady=8, padx=20, sticky="n")
        self.radio_button_6 = ctk.CTkRadioButton(self.side_frame, variable=self.radio_var, value=5, text="Joberty")
        self.radio_button_6.grid(row=7, column=0, pady=8, padx=20, sticky="n")

        self.btn_one = ctk.CTkButton(self.side_frame, text="Scrape Site", command=self.yield_jobs)
        self.btn_one.grid(row=8, column=0, padx=35, pady=(10, 10), sticky="nsew")

        self.appearance_mode_label = ctk.CTkLabel(self.side_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=10, column=0, padx=20, pady=(10, 5))
        self.appearance_menu = ctk.CTkOptionMenu(self.side_frame, values=THEMES, command=self.change_appearance)
        self.appearance_menu.grid(row=11, column=0, padx=20, pady=5)
        self.scaling_label = ctk.CTkLabel(self.side_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=12, column=0, padx=20, pady=5)
        self.scaling_menu = ctk.CTkOptionMenu(self.side_frame, values=SCALES, command=self.change_scaling_event)
        self.scaling_menu.grid(row=13, column=0, padx=20, pady=(5, 10))
        self.version_label = ctk.CTkLabel(self.side_frame, text="Software version 0.1.0", anchor="w")
        self.version_label.grid(row=14, column=0, padx=20, pady=5)

        # Create Tabview
        self.tabview = ctk.CTkTabview(self, height=HEIGHT)
        self.tabview.grid(row=0, column=1, padx=(10, 0), pady=(5, 0), sticky="nsew", rowspan=2)
        self.tabview.add("Job Adds")
        self.tabview.add("My Applications")
        self.tabview.tab("Job Adds").grid_columnconfigure(0, weight=1)
        self.tabview.tab("My Applications").grid_columnconfigure(0, weight=1)

        # Jobs Frame
        self.job_frame = JobsFrame(
            master=self.tabview.tab("Job Adds"),
            width=WIDTH,
            height=HEIGHT,
            command_1=self.save_applied_ad
        )
        self.job_frame.grid(row=1, column=0, pady=(10, 0))

        # Applications Frame
        self.applications_frame = JobsFrame(
            master=self.tabview.tab("My Applications"),
            width=WIDTH,
            height=HEIGHT,
            command_1=None
        )
        self.applications_frame.grid(row=1, column=0, pady=(10, 0))
        self.applications_frame.populate_applied_ads_labels(self.applied_adds.values())

    @property
    def scraper(self):
        return self._scraper

    @property
    def filer(self):
        return self._filer

    @staticmethod
    def change_scaling_event(new_scaling: str) -> None:
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    @staticmethod
    def change_appearance(new_appearance_mode: str) -> None:
        ctk.set_appearance_mode(new_appearance_mode)

    def configure_window(self):
        """Configure window size, name and grid layout (4×4)"""
        self.title("Scrape Jobs APP")
        self.geometry(f"{WIDTH}x{HEIGHT}+600+200")
        ctk.set_appearance_mode("Dark")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.wm_iconbitmap("files/spider.ico")

    def yield_jobs(self):
        if self.tabview.tab != "Job Adds":
            self.tabview.set("Job Adds")
        site = self.radio_var.get()
        match site:
            case 0:
                if self.hello_world_adds is None:
                    self.hello_world_adds = self.scraper.scrape_hello_world()
                try:
                    company, description, date, link = next(self.hello_world_adds)
                    while self.is_already_applied(company=company, description=description, link=link):
                        company, description, date, link = next(self.hello_world_adds)
                    self.job_frame.add_item(description, company, date, link)
                except StopIteration:
                    self.job_frame.add_item("End of queue.")
                    self.hello_world_adds = None
            case 1:
                if self.infostud_adds is None:
                    self.infostud_adds = self.scraper.scrape_infostud()
                try:
                    title, company, link = next(self.infostud_adds)
                    while self.is_already_applied(company=company, description=title, link=link):
                        title, company, link = next(self.infostud_adds)
                    self.job_frame.add_item(title, company, date=None, link=link)
                except StopIteration:
                    self.job_frame.add_item("End of queue.")
                    self.infostud_adds = None
            case 2:
                if self.linked_in_adds is None:
                    self.linked_in_adds = self.scraper.scrape_linkedin()
                try:
                    company_name, description, link = next(self.linked_in_adds)
                    while self.is_already_applied(company=company_name, description=description, link=link):
                        company_name, description, link = next(self.linked_in_adds)
                    self.job_frame.add_item(description, company_name, date=None, link=link)
                except StopIteration:
                    self.job_frame.add_item("End of queue.")
                    self.linked_in_adds = None
            case 3:
                if self.teamcubate_adds is None:
                    self.teamcubate_adds = self.scraper.scrape_teamcubate()
                try:
                    description, link = next(self.teamcubate_adds)
                    while self.is_already_applied(company=None, description=description, link=link):
                        description, link = next(self.teamcubate_adds)
                    self.job_frame.add_item(desc=description, link=link)
                except StopIteration:
                    self.job_frame.add_item("End of queue.")
                    self.teamcubate_adds = None
            case 4:
                if self.jooble is None:
                    self.jooble = self.scraper.scrape_jooble()
                try:
                    company, description, link, date = next(self.jooble)
                    while self.is_already_applied(company=company, description=description, link=link):
                        company, description, link, date = next(self.jooble)
                    self.job_frame.add_item(description, company, date, link, date_form="Published on")
                except StopIteration:
                    self.job_frame.add_item("End of queue.")
                    self.jooble = None
            case 5:
                if self.joberty is None:
                    self.joberty = self.scraper.scrape_joberty()
                try:
                    company, description, link, date = next(self.joberty)
                    while self.is_already_applied(company=company, description=description, link=link):
                        company, description, link, date = next(self.joberty)
                    self.job_frame.add_item(description, company, date, link, date_form="Expires on")
                except StopIteration:
                    self.job_frame.add_item("End of queue.")
                    self.joberty = None

    def is_already_applied(self, company: str | None, description: str | None, link: str | None):
        applied_adds = list(self.applied_adds.values())
        for add in applied_adds:
            if add["company"] == company and add["job_description"] == description and add["link"] == link:
                return True
        return False

    def save_applied_ad(self, *args):
        company, description, link = args
        self.filer.save_ad(company, description, link)
        self.job_frame.switch()
        self.applied_adds = self.filer.read()
        self.applications_frame.populate_applied_ads_labels(self.applied_adds.values())


if __name__ == "__main__":
    app = JobScraperApp()
    app.mainloop()
