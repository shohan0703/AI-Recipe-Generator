import customtkinter as ctk
from pathlib import Path
from PIL import Image
from tkinter import messagebox

from auth import validate_email, verify_password, hash_password, validate_password
from ui.base import button
from config import ASSETS_DIR


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.show_pw = False
        self.build()

    def build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        outer = ctk.CTkFrame(self, corner_radius=28, fg_color=("#FFFDF8", "#201F1C"), width=850, height=540)
        outer.grid(row=0, column=0, padx=30, pady=30)
        outer.grid_propagate(False)
        outer.grid_columnconfigure(0, weight=1)
        outer.grid_columnconfigure(1, weight=1)

        left = ctk.CTkFrame(outer, corner_radius=25, fg_color="#F97316")
        left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        image_path = ASSETS_DIR / "hero_cooking.jpg"
        try:
            self.hero_image = ctk.CTkImage(Image.open(image_path), size=(390, 185))
            ctk.CTkLabel(left, image=self.hero_image, text="", corner_radius=18).pack(fill="x", padx=18, pady=(18, 8))
        except Exception:
            pass
        ctk.CTkLabel(left, text="ChefAI", font=ctk.CTkFont(size=34, weight="bold"), text_color="white").pack(anchor="w", padx=40, pady=(8,4))
        ctk.CTkLabel(left, text="Smart recipes. Simple cooking.", font=ctk.CTkFont(size=16), text_color="white").pack(anchor="w", padx=40)
        ctk.CTkLabel(left, text="Generate personalized recipes with Gemini AI\nand keep your favorites in one place.", justify="left", font=ctk.CTkFont(size=13), text_color="#FFF7ED").pack(anchor="w", padx=40, pady=18)

        form = ctk.CTkFrame(outer, fg_color="transparent")
        form.grid(row=0, column=1, sticky="nsew", padx=45, pady=55)
        ctk.CTkLabel(form, text="Welcome back", font=ctk.CTkFont(size=29, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(form, text="Sign in to continue", text_color=("#71717A", "#A1A1AA")).pack(anchor="w", pady=(3,26))
        self.email = ctk.CTkEntry(form, placeholder_text="Email", height=44, corner_radius=12)
        self.email.pack(fill="x", pady=8)
        pwrow = ctk.CTkFrame(form, fg_color="transparent")
        pwrow.pack(fill="x", pady=8)
        self.password = ctk.CTkEntry(pwrow, placeholder_text="Password", show="•", height=44, corner_radius=12)
        self.password.pack(side="left", fill="x", expand=True)
        self.toggle = ctk.CTkButton(pwrow, text="Show", width=64, height=38, corner_radius=10, command=self.toggle_password)
        self.toggle.pack(side="right", padx=(8,0))
        button(form, "Login", self.login, primary=True, width=220).pack(fill="x", pady=(15,9))
        row = ctk.CTkFrame(form, fg_color="transparent")
        row.pack(fill="x", pady=5)
        ctk.CTkButton(row, text="Create Account", fg_color="transparent", text_color="#F97316", hover_color=("#FFF7ED", "#3A2820"), command=self.app.show_register).pack(side="left")
        ctk.CTkButton(row, text="Forgot Password", fg_color="transparent", hover_color=("#F5F5F4", "#33302C"), command=self.forgot).pack(side="right")

    def toggle_password(self):
        self.show_pw = not self.show_pw
        self.password.configure(show="" if self.show_pw else "•")
        self.toggle.configure(text="Hide" if self.show_pw else "Show")

    def login(self):
        email = self.email.get().strip()
        password = self.password.get()
        if not validate_email(email) or not password:
            messagebox.showerror("Login", "Enter a valid email and password.")
            return
        user = self.app.db.get_user_by_email(email)
        if not user or not verify_password(password, user["password"]):
            messagebox.showerror("Login", "Invalid email or password.")
            return
        self.app.start_session(user["id"])

    def forgot(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Reset Password")
        dialog.geometry("430x330")
        dialog.transient(self)
        dialog.grab_set()
        ctk.CTkLabel(dialog, text="Reset password", font=ctk.CTkFont(size=23, weight="bold")).pack(pady=(30,15))
        email = ctk.CTkEntry(dialog, placeholder_text="Registered email", height=44)
        email.pack(fill="x", padx=35, pady=7)
        pw = ctk.CTkEntry(dialog, placeholder_text="New password", show="•", height=44)
        pw.pack(fill="x", padx=35, pady=7)
        confirm = ctk.CTkEntry(dialog, placeholder_text="Confirm password", show="•", height=44)
        confirm.pack(fill="x", padx=35, pady=7)
        def reset():
            if not validate_email(email.get()) or not validate_password(pw.get()):
                messagebox.showerror("Reset", "Use a valid email and a password of at least 6 characters.", parent=dialog)
                return
            if pw.get() != confirm.get():
                messagebox.showerror("Reset", "Passwords do not match.", parent=dialog)
                return
            if self.app.db.reset_password(email.get(), hash_password(pw.get())):
                messagebox.showinfo("Reset", "Password updated successfully.", parent=dialog)
                dialog.destroy()
            else:
                messagebox.showerror("Reset", "No account was found for that email.", parent=dialog)
        button(dialog, "Reset Password", reset, primary=True, width=180).pack(pady=18)
