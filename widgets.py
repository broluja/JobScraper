import webbrowser
from tktooltip import ToolTip

import customtkinter as ctk


class APPLabel(ctk.CTkLabel):
    """Custom APP label with custom font size and weight."""
    def __init__(self, size: int = 18, **kwargs):
        super().__init__(**kwargs, font=ctk.CTkFont(size=size, weight="bold"))


class LinkLabel(ctk.CTkLabel):
    """Custom APP Label representing a link."""
    def __init__(self, link: str, command=None, size: int = 18, **kwargs):
        super().__init__(**kwargs, font=ctk.CTkFont(size=size, weight="bold"))
        self.link = link
        self.command = command
        if self.link:
            self.bind("<Button-1>", lambda e=self.link: self.command(link))
            self.bind("<Enter>", lambda e: self.configure(text_color="#1f538d"))
            self.bind("<Leave>", lambda e: self.configure(text_color="gray"))
        ToolTip(self, msg=self.link, delay=0.2, fg="#ffffff", bg="#1c1c1c", padx=8, pady=3, width=1000)


class JobsFrame(ctk.CTkScrollableFrame):
    """Class inherits tkinter frame widget customized to be scrollable with labels and buttons."""
    def __init__(self, command_1=None, command_2=None, **kwargs):
        super().__init__(**kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.command_one = command_1
        self.command_two = command_2
        self.label_list = []
        self.button = None
        self.checker = None
        self.applied_ads_labels = []

    def add_item(self, desc=None, comp=None, date=None, link=None, date_form="Valid till") -> None:
        self.remove_items()
        text1 = f"Job description: {desc}" if desc != "End of queue." else desc
        text2 = f"Company: {comp}" if comp else ""
        text3 = f"{date_form}: {date}" if date else ""
        text4 = "Click for more info" if link else ""
        description = APPLabel(master=self, text=text1, compound="left", padx=5, anchor="w")
        company = APPLabel(master=self, text=text2, compound="left", padx=5, anchor="w")
        deadline = ctk.CTkLabel(self, text=text3, compound="left", padx=5, anchor="w")
        more_info = LinkLabel(master=self, command=lambda e: self.open_browser(e), link=link, text=text4, padx=5)
        description.grid(row=0, column=1, pady=(10, 5), sticky="w")
        company.grid(row=1, column=1, pady=(0, 5), sticky="w")
        deadline.grid(row=2, column=1, pady=(0, 5), sticky="w")
        more_info.grid(row=3, column=1, pady=(0, 10), sticky="w")
        self.label_list.extend([description, company, deadline, more_info])
        if text1 != "End of queue.":
            self.button = ctk.CTkButton(
                self,
                text="Mark as applied",
                command=lambda x=comp, y=desc, z=link: self.command_one(x, y, z),
                width=100)
            self.button.grid(row=5, column=1, padx=10, pady=20)

    def add_applied_ads(self, company: str, position: str, date, link: str, index) -> None:
        text1 = f"{company} - {position} - Date applied: {date}"
        text2 = "Click here to open ad link."
        ad_label = APPLabel(master=self, text=text1, compound="left", padx=5, anchor="w", size=17, text_color="#1f538d")
        link_label = LinkLabel(master=self,
                               command=lambda e: self.open_browser(e),
                               link=link,
                               text=text2,
                               padx=5,
                               size=14,
                               text_color="gray")
        ad_label.grid(row=index-1, column=1, sticky="w")
        link_label.grid(row=index, column=1, pady=(0, 25), sticky="w")
        self.applied_ads_labels.extend([ad_label, link_label])

    def remove_items(self) -> None:
        for label in self.label_list:
            label.destroy()
        self.label_list.clear()
        if self.button:
            self.button.destroy()
            self.button = None
        if self.checker:
            self.checker.destroy()
            self.checker = None

    def remove_applied_ads_labels(self) -> None:
        for label in self.applied_ads_labels:
            label.destroy()
        self.applied_ads_labels.clear()

    def populate_applied_ads_labels(self, iterable) -> None:
        self.remove_applied_ads_labels()
        for index, ad in enumerate(iterable, start=1):
            self.add_applied_ads(ad["company"], ad["job_description"], ad["date_applied"], ad["link"], index + index)

    def switch(self) -> None:
        self.button.destroy()
        self.button = None
        self.checker = ctk.CTkCheckBox(self, text="Applied for this one")
        self.checker.grid(row=5, column=1)
        self.checker.select()
        self.checker.configure(state="disabled")

    @staticmethod
    def open_browser(link: str) -> None:
        webbrowser.open(link)
