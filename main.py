import os
from pathlib import Path

import customtkinter as ctk
from dotenv import load_dotenv
from tkinter import messagebox

from config import APP_NAME, DARK_BG, LIGHT_BG, CARD_DARK, CARD_LIGHT, PRIMARY
from database import Database
from ai_service import GeminiRecipeService
from ui.login import LoginPage
from ui.register import RegisterPage
from ui.dashboard import DashboardPage
from ui.recipe_generator import RecipeGeneratorPage
from ui.recipe_details import RecipeDetailsPage
from ui.saved_recipes import SavedRecipesPage
from ui.history import HistoryPage
from ui.profile import ProfilePage
from ui.settings import SettingsPage
from ui.recipes import RecipesPage


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class ChefAIApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1200x760")
        self.minsize(1050, 680)
        self.user_id = None
        self.last_page = "dashboard"
        self.current_page = "dashboard"
        self.db = Database()
        self.ai = GeminiRecipeService()
        self.pages = {}
        self.build_auth_pages()

    def build_auth_pages(self):
        self.root = ctk.CTkFrame(self, fg_color=(LIGHT_BG, DARK_BG))
        self.root.pack(fill="both", expand=True)
        self.login_page = LoginPage(self.root, self)
        self.register_page = RegisterPage(self.root, self)
        self.show_login()

    def clear_root(self):
        for w in self.root.winfo_children(): w.pack_forget(); w.grid_forget()

    def show_login(self):
        self.clear_root(); self.login_page = LoginPage(self.root, self); self.login_page.pack(fill="both", expand=True)

    def show_register(self):
        self.clear_root(); self.register_page = RegisterPage(self.root, self); self.register_page.pack(fill="both", expand=True)

    def start_session(self, user_id):
        self.user_id = user_id
        self.build_main_shell()
        self.show_page("dashboard")

    def build_main_shell(self):
        self.clear_root()
        self.shell = ctk.CTkFrame(self.root, fg_color=(LIGHT_BG, DARK_BG), corner_radius=0)
        self.shell.pack(fill="both", expand=True)
        self.shell.grid_columnconfigure(1, weight=1); self.shell.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self.shell, width=225, corner_radius=0, fg_color=("#FFFCF7", "#1C1B18"))
        self.sidebar.grid(row=0,column=0,sticky="nsew"); self.sidebar.grid_propagate(False)
        ctk.CTkLabel(self.sidebar,text="ChefAI",font=ctk.CTkFont(size=28,weight="bold"),text_color=PRIMARY).pack(anchor="w",padx=24,pady=(28,2))
        ctk.CTkLabel(self.sidebar,text="AI Recipe Studio",font=ctk.CTkFont(size=12),text_color=("#78716C","#A8A29E")).pack(anchor="w",padx=25,pady=(0,22))
        self.nav_buttons=[]
        nav=[("⌂  Dashboard","dashboard"),("✨  Generate Recipe","generator"),("▣  Recipes","recipes"),("♡  Saved Recipes","saved"),("◷  History","history"),("◯  Profile","profile"),("⚙  Settings","settings")]
        for label,key in nav:
            b=ctk.CTkButton(self.sidebar,text=label,anchor="w",height=43,corner_radius=11,fg_color="transparent",hover_color=("#F4EFE8","#302B26"),text_color=("#44403C","#E7E5E4"),command=lambda k=key:self.show_page(k))
            b.pack(fill="x",padx=14,pady=4); self.nav_buttons.append((key,b))
        ctk.CTkFrame(self.sidebar,fg_color="transparent",height=1).pack(expand=True,fill="both")
        user=self.db.get_user(self.user_id)
        ctk.CTkLabel(self.sidebar,text=user["name"],anchor="w",font=ctk.CTkFont(size=14,weight="bold")).pack(fill="x",padx=22,pady=(5,2))
        ctk.CTkLabel(self.sidebar,text=user["email"],anchor="w",font=ctk.CTkFont(size=11),text_color=("#78716C","#A8A29E")).pack(fill="x",padx=22)
        ctk.CTkButton(self.sidebar,text="Logout",height=38,corner_radius=10,command=self.logout,fg_color=("#F4EFE8","#302B26"),hover_color=("#E7E5E4","#403A34"),text_color=("#44403C","#F5F5F4")).pack(fill="x",padx=14,pady=18)

        self.content=ctk.CTkFrame(self.shell,fg_color="transparent"); self.content.grid(row=0,column=1,sticky="nsew",padx=27,pady=25); self.content.grid_columnconfigure(0,weight=1); self.content.grid_rowconfigure(0,weight=1)
        self.pages={
            "dashboard":DashboardPage(self.content,self),
            "generator":RecipeGeneratorPage(self.content,self),
            "recipes":RecipesPage(self.content,self),
            "details":RecipeDetailsPage(self.content,self),
            "saved":SavedRecipesPage(self.content,self),
            "history":HistoryPage(self.content,self),
            "profile":ProfilePage(self.content,self),
            "settings":SettingsPage(self.content,self),
        }

    def hide_pages(self):
        for p in self.pages.values(): p.grid_forget()

    def show_page(self,key):
        if not self.user_id: return
        if key not in self.pages: return
        if key != "details": self.last_page=key
        self.current_page=key
        self.hide_pages()
        page=self.pages[key]
        if hasattr(page,"render") and key in {"dashboard","generator","recipes","saved","history","profile","settings"}: page.render()
        page.grid(row=0,column=0,sticky="nsew")
        for k,b in self.nav_buttons:
            b.configure(fg_color=("#FFF0E5","#39261B") if k==key else "transparent", text_color=(PRIMARY,"#FDBA74") if k==key else (("#44403C","#E7E5E4")))

    def show_generated_recipe(self,data):
        self.hide_pages(); self.current_page="details"; self.pages["details"].show(data,stored=False); self.pages["details"].grid(row=0,column=0,sticky="nsew")

    def open_recipe(self,recipe_id):
        row=self.db.get_recipe(recipe_id,self.user_id)
        if not row: messagebox.showerror("ChefAI","Recipe not found."); return
        self.last_page=self.current_page if self.current_page!="details" else self.last_page
        self.hide_pages(); self.current_page="details"; self.pages["details"].show(__import__("recipe_service").recipe_from_row(row),stored=True); self.pages["details"].grid(row=0,column=0,sticky="nsew")

    def go_back(self): self.show_page(self.last_page if self.last_page!="details" else "dashboard")

    def set_theme(self, mode):
        ctk.set_appearance_mode("Dark" if mode.lower()=="dark" else "Light")
        if self.user_id:
            self.build_main_shell(); self.show_page(self.current_page if self.current_page!="details" else "dashboard")

    def logout(self):
        self.user_id=None
        for w in self.root.winfo_children(): w.destroy()
        self.show_login()


if __name__ == "__main__":
    ctk.set_default_color_theme("blue")
    ctk.set_appearance_mode("System")
    app=ChefAIApp()
    app.mainloop()
