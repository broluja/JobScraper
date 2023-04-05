import tkinter
import customtkinter as ctk

from scraper import JobScraper
from config import *
from widgets import APPLabel, JobsFrame


class JobScraperApp(ctk.CTk):
    """Job Scraper APP for scraping Python developer positions on biggest job market sites."""

    def __init__(self):
        super().__init__()
        self._scraper = JobScraper()
        self.configure_window()
        self.hello_world_adds = None
        self.infostud_adds = None
        self.linked_in_adds = None

        # Create sidebar frame with widgets
        self.side_frame = ctk.CTkFrame(self, width=WIDTH // 10, corner_radius=0, border_width=1)
        self.side_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.side_frame.grid_rowconfigure(7, weight=1)

        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = APPLabel(master=self.side_frame, text="Select Job Adds Site", size=18)
        self.label_radio_group.grid(row=1, column=0, padx=10, pady=(20, 10))
        self.radio_button_1 = ctk.CTkRadioButton(self.side_frame, variable=self.radio_var, value=0, text="Hello World")
        self.radio_button_1.grid(row=2, column=0, pady=8, padx=20, sticky="n")
        self.radio_button_2 = ctk.CTkRadioButton(self.side_frame, variable=self.radio_var, value=1, text="Infostud")
        self.radio_button_2.grid(row=3, column=0, pady=8, padx=20, sticky="n")
        self.radio_button_3 = ctk.CTkRadioButton(self.side_frame, variable=self.radio_var, value=2, text="LinkedIn")
        self.radio_button_3.grid(row=4, column=0, pady=8, padx=20, sticky="n")

        self.btn_one = ctk.CTkButton(self.side_frame, text="Scrape Site", command=self.yield_jobs)
        self.btn_one.grid(row=5, column=0, padx=25, pady=(10, 10), sticky="nsew")

        self.appearance_mode_label = ctk.CTkLabel(self.side_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(20, 10))
        self.appearance_menu = ctk.CTkOptionMenu(self.side_frame, values=THEMES, command=self.change_appearance)
        self.appearance_menu.grid(row=9, column=0, padx=20, pady=(10, 30))
        self.scaling_label = ctk.CTkLabel(self.side_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=10, column=0, padx=20, pady=10)
        self.scaling_menu = ctk.CTkOptionMenu(self.side_frame, values=SCALES, command=self.change_scaling_event)
        self.scaling_menu.grid(row=11, column=0, padx=20, pady=(10, 30))

        # Create Tabview
        self.tabview = ctk.CTkTabview(self, height=HEIGHT)
        self.tabview.grid(row=0, column=1, padx=(10, 0), pady=(5, 0), sticky="nsew", rowspan=2)
        self.tabview.add("Job Adds")
        self.tabview.add("My Applications")
        self.tabview.tab("Job Adds").grid_columnconfigure(0, weight=1)
        self.tabview.tab("My Applications").grid_columnconfigure(0, weight=1)

        self.job_frame = JobsFrame(master=self.tabview.tab("Job Adds"), width=WIDTH, height=HEIGHT)
        self.job_frame.grid(row=1, column=0, pady=(10, 0))

    @property
    def scraper(self):
        return self._scraper

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
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.wm_iconbitmap(r"C:\Users\Branko\PycharmProjects\JobScraper\spider.ico")

    def yield_jobs(self):
        site = self.radio_var.get()
        match site:
            case 0:
                if self.hello_world_adds is None:
                    self.hello_world_adds = self.scraper.scrape_hello_world()
                try:
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
                    self.job_frame.add_item(title, company, date=None, link=link)
                except StopIteration:
                    self.job_frame.add_item("End of queue.")
                    self.infostud_adds = None
            case 2:
                if self.linked_in_adds is None:
                    self.linked_in_adds = self.scraper.scrape_linkedin()
                try:
                    company_name, description, link = next(self.linked_in_adds)
                    self.job_frame.add_item(description, company_name, date=None, link=link)
                except StopIteration:
                    self.job_frame.add_item("End of queue.")
                    self.infostud_adds = None


if __name__ == "__main__":
    app = JobScraperApp()
    app.mainloop()
