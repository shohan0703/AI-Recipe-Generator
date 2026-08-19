import threading
import customtkinter as ctk
from tkinter import messagebox
from ui.base import card, title, muted


COMMON_INGREDIENTS = [
    "Chicken", "Beef", "Fish", "Egg", "Rice", "Potato", "Tomato", "Onion", "Garlic", "Ginger", "Olive Oil", "Green Chili",
]


class RecipeGeneratorPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.selected = []
        self.build()
    def load_profile_preferences(self):
        user = self.app.db.get_user(self.app.user_id)

        if user:
            preferred_cuisine = user["preferred_cuisine"] or "Any"
            dietary_preference = user["dietary_preference"] or "None"

            self.cuisine.set(preferred_cuisine)
            self.diet.set(dietary_preference)


    def render(self):
        self.load_profile_preferences()
        

    def build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        title(self, "AI Recipe Generator").grid(row=0, column=0, sticky="w", padx=5, pady=(5, 3))
        muted(self, "Select ingredients or type your own, then choose your preferences.").grid(row=1, column=0, sticky="w", padx=5, pady=(0, 12))

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.grid(row=2, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)
        form = card(scroll)
        form.grid(row=0, column=0, sticky="ew", padx=4, pady=4)
        form.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(form, text="Ingredients", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 4))
        muted(form, "Click common ingredients below, or type additional ingredients.").grid(row=1, column=0, columnspan=2, sticky="w", padx=20)
        self.ingredient_grid = ctk.CTkFrame(form, fg_color="transparent")
        self.ingredient_grid.grid(row=2, column=0, columnspan=2, sticky="ew", padx=17, pady=(10, 3))
        for col in range(4):
            self.ingredient_grid.grid_columnconfigure(col, weight=1)
        self.ingredient_buttons = {}
        for i, ingredient in enumerate(COMMON_INGREDIENTS):
            b = ctk.CTkButton(self.ingredient_grid, text=ingredient, height=32, corner_radius=9, fg_color=("#F7F3EE", "#2B2723"), text_color=("#44403C", "#E7E5E4"), hover_color=("#FFE7D2", "#493225"), command=lambda x=ingredient: self.toggle_ingredient(x))
            b.grid(row=i // 4, column=i % 4, padx=4, pady=4, sticky="ew")
            self.ingredient_buttons[ingredient] = b

        self.ingredients = ctk.CTkTextbox(form, height=105, corner_radius=12)
        self.ingredients.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=(8, 20))
        self.ingredients.insert("1.0", "")
        self.cuisine = self.combo(form, "Cuisine", ["Any", "Bangladeshi", "Indian", "Italian", "Chinese", "Mexican"], 4, 0)
        self.meal = self.combo(form, "Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"], 4, 1)
        self.diet = self.combo(form, "Dietary Preference", ["None", "Vegetarian", "Vegan", "High Protein", "Low Carb"], 6, 0)
        self.diff = self.combo(form, "Difficulty", ["Easy", "Medium", "Hard"], 6, 1)
        self.time = self.combo(form, "Cooking Time", ["Under 15 min", "15–30 min", "30–60 min", "60+ min"], 8, 0)
        ctk.CTkLabel(form, text="Servings", font=ctk.CTkFont(size=13, weight="bold")).grid(row=8, column=1, sticky="w", padx=20, pady=(12, 2))
        self.servings = ctk.CTkComboBox(form, values=[str(i) for i in range(1, 13)], height=40, corner_radius=10)
        self.servings.set("2")
        self.servings.grid(row=9, column=1, sticky="ew", padx=20, pady=(0, 3))
        self.generate_btn = ctk.CTkButton(form, text="✨ Generate Recipe", command=self.generate, height=50, corner_radius=14, fg_color="#F97316", hover_color="#EA580C", font=ctk.CTkFont(size=16, weight="bold"))
        self.generate_btn.grid(row=10, column=0, columnspan=2, sticky="ew", padx=20, pady=(14, 8))
        self.status = muted(form, "")
        self.status.grid(row=11, column=0, columnspan=2, padx=20, pady=(0, 15))

    def combo(self, parent, label, values, row, col):
        ctk.CTkLabel(parent, text=label, font=ctk.CTkFont(size=13, weight="bold")).grid(row=row, column=col, sticky="w", padx=20, pady=(12, 2))
        cb = ctk.CTkComboBox(parent, values=values, height=40, corner_radius=10)
        cb.set(values[0])
        cb.grid(row=row + 1, column=col, sticky="ew", padx=20, pady=(0, 3))
        return cb

    def toggle_ingredient(self, ingredient):
        if ingredient in self.selected:
            self.selected.remove(ingredient)
            self.ingredient_buttons[ingredient].configure(fg_color=("#F7F3EE", "#2B2723"), text_color=("#44403C", "#E7E5E4"))
        else:
            self.selected.append(ingredient)
            self.ingredient_buttons[ingredient].configure(fg_color="#F97316", text_color="white")
        self.ingredients.delete("1.0", "end")
        self.ingredients.insert("1.0", ", ".join(self.selected))

    def generate(self):
        ingredients = self.ingredients.get("1.0", "end").strip()
        if not ingredients:
            messagebox.showwarning("Recipe Generator", "Please select or enter at least one ingredient.")
            return
        try:
            servings = int(self.servings.get())
            if servings < 1 or servings > 12:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Recipe Generator", "Please choose a valid serving count.")
            return
        self.generate_btn.configure(state="disabled", text="Creating recipe…")
        self.status.configure(text="ChefAI is creating your recipe...")
        args = (ingredients, self.cuisine.get(), self.meal.get(), self.diet.get(), self.diff.get(), self.time.get(), servings)

        def worker():
            try:
                data = self.app.ai.generate_recipe(*args)
                self.after(0, lambda: self._success(data))
            except Exception as exc:
                self.after(0, lambda: self._failure(str(exc)))
        threading.Thread(target=worker, daemon=True).start()

    def _success(self, data):
        self.generate_btn.configure(state="normal", text="✨ Generate Recipe")
        self.status.configure(text="Recipe generated successfully.")
        self.app.show_generated_recipe(data)

    def _failure(self, msg):
        self.generate_btn.configure(state="normal", text="✨ Generate Recipe")
        self.status.configure(text="")
        messagebox.showerror("ChefAI", msg or "Unable to generate recipe. Please try again.")
