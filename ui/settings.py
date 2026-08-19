import customtkinter as ctk
from tkinter import messagebox
from ui.base import card, title, muted, button


class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.render()

    def render(self):
        for w in self.winfo_children():
            w.destroy()

        self.grid_columnconfigure(0, weight=1)

        title(self, "Settings").grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=(5, 15)
        )

        c = card(self)
        c.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=4
        )

        c.grid_columnconfigure(0, weight=1)

        # =========================
        # AI
        # =========================

        ctk.CTkLabel(
            c,
            text="AI",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 3)
        )

        status = (
            "Connected — API key loaded"
            if self.app.ai.is_configured()
            else "Not configured — add OPENROUTER_API_KEY to .env"
        )

        muted(
            c,
            status
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 25)
        )

        # =========================
        # Account
        # =========================

        ctk.CTkLabel(
            c,
            text="Account",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
            pady=(8, 3)
        )

        button(
            c,
            "Logout",
            self.app.logout,
            width=120
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=20,
            pady=(8, 25)
        )