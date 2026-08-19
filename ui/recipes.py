import customtkinter as ctk
from PIL import Image
from ui.base import card, title, muted, button
from premade_recipes import PREMADE_RECIPES


class RecipesPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.query = ""
        self.render()

    def render(self):
        for w in self.winfo_children():
            w.destroy()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 10))
        header.grid_columnconfigure(0, weight=1)
        title(header, "Recipes").grid(row=0, column=0, sticky="w")

        bar = ctk.CTkFrame(header, fg_color="transparent")
        bar.grid(row=0, column=1, sticky="e")
        self.search = ctk.CTkEntry(bar, width=240, height=38, corner_radius=10, placeholder_text="Search recipes")
        self.search.insert(0, self.query)
        self.search.pack(side="left", padx=(0, 6))
        ctk.CTkButton(bar, text="Search", width=80, height=38, corner_radius=10, command=self.apply).pack(side="left")

        muted(self, "Browse ready-to-cook recipes before generating something new with Gemini.").grid(row=1, column=0, sticky="w", padx=5, pady=(0, 12))
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.grid(row=2, column=0, sticky="nsew")
        for col in range(2):
            scroll.grid_columnconfigure(col, weight=1)

        q = self.query.lower()
        items = [r for r in PREMADE_RECIPES if not q or q in r["recipe_name"].lower() or q in r["cuisine"].lower() or q in r["meal_type"].lower()]
        if not items:
            muted(scroll, "No recipes found.").grid(row=0, column=0, padx=8, pady=15, sticky="w")
            return
        for i, recipe in enumerate(items):
            self.recipe_card(scroll, recipe, i // 2, i % 2)

    def apply(self):
        self.query = self.search.get().strip()
        self.render()

    def recipe_card(self, parent, recipe, row, col):
        c = card(parent)
        c.grid(row=row, column=col, sticky="nsew", padx=7, pady=7)
        c.grid_columnconfigure(0, weight=1)
        path = recipe.get("image_path", "")
        try:
            im = ctk.CTkImage(Image.open(path), size=(320, 185))
            image_label = ctk.CTkLabel(c, image=im, text="")
            image_label.image = im
            image_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 8))
        except Exception:
            pass
        ctk.CTkLabel(c, text=recipe["recipe_name"], wraplength=300, justify="left", anchor="w", font=ctk.CTkFont(size=17, weight="bold")).grid(row=1, column=0, sticky="w", padx=15, pady=(2, 3))
        muted(c, f"{recipe['cuisine']} • {recipe['total_time']} • {recipe['calories']} kcal").grid(row=2, column=0, sticky="w", padx=15, pady=(0, 6))
        button(c, "View Recipe", lambda r=recipe: self.app.show_generated_recipe(r), primary=True, width=135).grid(row=3, column=0, sticky="w", padx=15, pady=(3, 15))
