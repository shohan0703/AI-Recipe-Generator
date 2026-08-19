import customtkinter as ctk
from PIL import Image
from ui.base import card, title, muted, button
from recipe_service import recipe_from_row


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.render()

    def render(self):
        for w in self.winfo_children(): w.destroy()
        self.grid_columnconfigure(0, weight=1)
        user = self.app.db.get_user(self.app.user_id)
        stats = self.app.db.stats(self.app.user_id)
        title(self, f"Welcome back, {user['name'].split()[0]} 👋").grid(row=0,column=0,sticky="w",padx=5,pady=(5,3))
        muted(self, "What would you like to cook today?").grid(row=1,column=0,sticky="w",padx=5,pady=(0,20))
        hero = card(self, fg_color=("#FFF7ED", "#35241A")); hero.grid(row=2,column=0,sticky="ew",pady=(0,20)); hero.grid_columnconfigure(0,weight=1); hero.grid_columnconfigure(1,weight=0)
        ctk.CTkLabel(hero,text="✨ AI Recipe Generator",font=ctk.CTkFont(size=25,weight="bold")).grid(row=0,column=0,sticky="w",padx=25,pady=(24,4))
        ctk.CTkLabel(hero,text="Turn the ingredients you already have into a personalized recipe.",text_color=("#57534E", "#D6D3D1")).grid(row=1,column=0,sticky="w",padx=25)
        button(hero,"Generate Recipe",lambda:self.app.show_page("generator"),primary=True,width=190).grid(row=2,column=0,sticky="w",padx=25,pady=20)
        try:
            from config import ASSETS_DIR
            hero_im = ctk.CTkImage(Image.open(ASSETS_DIR / "combo_meal.jpg"), size=(250,150))
            hero_image_label = ctk.CTkLabel(hero, image=hero_im, text="")
            hero_image_label.image = hero_im
            hero_image_label.grid(row=0,column=1,rowspan=3,padx=18,pady=18)
        except Exception:
            pass

        statrow=ctk.CTkFrame(self,fg_color="transparent"); statrow.grid(row=3,column=0,sticky="ew",pady=(0,20));
        for i in range(3): statrow.grid_columnconfigure(i,weight=1)
        for i,(label,val) in enumerate((("Recipes Generated",stats["total"]),("Saved Recipes",stats["saved"]),("Favorites",stats["favorites"]))):
            c=card(statrow); c.grid(row=0,column=i,sticky="ew",padx=6); ctk.CTkLabel(c,text=str(val),font=ctk.CTkFont(size=28,weight="bold")).pack(anchor="w",padx=18,pady=(16,0)); muted(c,label).pack(anchor="w",padx=18,pady=(2,16))
        ctk.CTkLabel(self,text="Recent Recipes",font=ctk.CTkFont(size=20,weight="bold")).grid(row=4,column=0,sticky="w",padx=5,pady=(0,12))
        recent= self.app.db.recent_recipes(self.app.user_id,5)
        if not recent:
            muted(self,"Your latest recipes will appear here after your first generation.").grid(row=5,column=0,sticky="w",padx=5)
        else:
            area=ctk.CTkScrollableFrame(self,fg_color="transparent"); area.grid(row=5,column=0,sticky="nsew"); self.grid_rowconfigure(5,weight=1)
            for row in recent:
                data=recipe_from_row(row); c=card(area); c.pack(fill="x",pady=6); c.grid_columnconfigure(1,weight=1)
                imgp=data.get("image_path");
                if imgp:
                    try: im=ctk.CTkImage(Image.open(imgp),size=(105,70)); lab=ctk.CTkLabel(c,image=im,text=""); lab.grid(row=0,column=0,rowspan=2,padx=12,pady=12)
                    except Exception: pass
                ctk.CTkLabel(c,text=data["recipe_name"],font=ctk.CTkFont(size=16,weight="bold")).grid(row=0,column=1,sticky="w",padx=8,pady=(15,2))
                muted(c,f"{data.get('total_time','')} • {data.get('calories',0)} kcal").grid(row=1,column=1,sticky="w",padx=8,pady=(0,12))
                button(c,"View",lambda rid=data["id"]:self.app.open_recipe(rid),width=100).grid(row=0,column=2,rowspan=2,padx=14)
