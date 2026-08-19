import customtkinter as ctk
from tkinter import messagebox
from auth import hash_password, validate_email, validate_password
from ui.base import button


class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.build()

    def build(self):
        self.grid_rowconfigure(0, weight=1); self.grid_columnconfigure(0, weight=1)
        box = ctk.CTkFrame(self, corner_radius=25, fg_color=("#FFFDF8", "#201F1C"), width=600, height=620)
        box.grid(row=0, column=0, padx=30, pady=25); box.grid_propagate(False)
        ctk.CTkLabel(box, text="Create your ChefAI account", font=ctk.CTkFont(size=28, weight="bold")).pack(anchor="w", padx=55, pady=(45,6))
        ctk.CTkLabel(box, text="Save recipes, favorites, and history securely.", text_color=("#71717A", "#A1A1AA")).pack(anchor="w", padx=55, pady=(0,20))
        self.name = ctk.CTkEntry(box, placeholder_text="Full Name", height=46, corner_radius=12)
        self.email = ctk.CTkEntry(box, placeholder_text="Email", height=46, corner_radius=12)
        self.pw = ctk.CTkEntry(box, placeholder_text="Password (6+ characters)", show="•", height=46, corner_radius=12)
        self.confirm = ctk.CTkEntry(box, placeholder_text="Confirm Password", show="•", height=46, corner_radius=12)
        for w in (self.name,self.email,self.pw,self.confirm): w.pack(fill="x", padx=55, pady=7)
        button(box, "Create Account", self.register, primary=True, width=220).pack(fill="x", padx=55, pady=(18,8))
        ctk.CTkButton(box, text="Back to Login", fg_color="transparent", text_color="#F97316", command=self.app.show_login).pack()

    def register(self):
        name, email, pw, conf = self.name.get().strip(), self.email.get().strip(), self.pw.get(), self.confirm.get()
        if not name or not email or not pw or not conf:
            messagebox.showerror("Register", "Please fill in every field."); return
        if not validate_email(email):
            messagebox.showerror("Register", "Enter a valid email address."); return
        if not validate_password(pw):
            messagebox.showerror("Register", "Password must be at least 6 characters."); return
        if pw != conf:
            messagebox.showerror("Register", "Passwords do not match."); return
        if self.app.db.get_user_by_email(email):
            messagebox.showerror("Register", "That email is already registered."); return
        try:
            self.app.db.create_user(name, email, hash_password(pw))
            messagebox.showinfo("Register", "Account created. You can now log in.")
            self.app.show_login()
        except Exception:
            messagebox.showerror("Register", "Could not create account. Please try again.")
