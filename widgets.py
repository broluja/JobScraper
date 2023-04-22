import webbrowser

import customtkinter as ctk


class APPLabel(ctk.CTkLabel):
    """Custom APP label with custom font size and weight."""
    def __init__(self, size: int = 25, **kwargs):
        super().__init__(**kwargs, font=ctk.CTkFont(size=size, weight="bold"))


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

    def add_item(self, desc=None, comp=None, date=None, link=None, date_form="Valid till") -> None:
        self.remove_items()
        text1 = f"Job description: {desc}" if desc != "End of queue." else desc
        text2 = f"Company: {comp}" if comp else ""
        text3 = f"{date_form}: {date}" if date else ""
        text4 = "Click for more info" if link else ""
        description = ctk.CTkLabel(self, text=text1, compound="left", padx=5, anchor="w")
        company = ctk.CTkLabel(self, text=text2, compound="left", padx=5, anchor="w")
        deadline = ctk.CTkLabel(self, text=text3, compound="left", padx=5, anchor="w")
        more_info = APPLabel(master=self, text=text4, size=18, padx=5, anchor="w")
        description.grid(row=0, column=1, pady=(10, 5), sticky="w")
        company.grid(row=1, column=1, pady=(0, 5), sticky="w")
        deadline.grid(row=2, column=1, pady=(0, 5), sticky="w")
        more_info.grid(row=3, column=1, pady=(0, 10), sticky="w")
        if link:
            more_info.bind("<Button-1>", lambda e: self.open_browser(link))
            more_info.bind("<Enter>", lambda e: more_info.configure(text_color="blue"))
            more_info.bind("<Leave>", lambda e: more_info.configure(text_color="white"))
        self.label_list.extend([description, company, deadline, more_info])
        if text1 != "End of queue.":
            self.button = ctk.CTkButton(
                self,
                text="Mark as applied",
                command=lambda x=comp, y=desc, z=link: self.command_one(x, y, z),
                width=100)
            self.button.grid(row=5, column=1, padx=10, pady=20)

    def remove_items(self) -> None:
        for label in self.label_list:
            label.destroy()
        self.label_list.clear()
        if self.button:
            self.button.destroy()
            self.button = None

    def switch(self):
        self.button.destroy()
        self.button = None
        self.checker = ctk.CTkCheckBox(self, text="Applied for this one")
        self.checker.grid(row=5, column=1)
        self.checker.select()
        self.checker.configure(state="disabled")

    @staticmethod
    def open_browser(link: str):
        webbrowser.open(link)
