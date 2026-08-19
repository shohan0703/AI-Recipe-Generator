import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from ui.base import card, title, muted, button
from recipe_service import recipe_from_row


class SavedRecipesPage(ctk.CTkFrame):
    def __init__(self,parent,app):
        super().__init__(parent,fg_color="transparent"); self.app=app; self.filter="All"; self.search=""; self.render()
    def render(self):
        for w in self.winfo_children(): w.destroy()
        self.grid_columnconfigure(0,weight=1); self.grid_rowconfigure(2,weight=1)
        title(self,"Saved Recipes").grid(row=0,column=0,sticky="w",padx=5,pady=(5,15))
        bar=ctk.CTkFrame(self,fg_color="transparent"); bar.grid(row=1,column=0,sticky="ew",pady=(0,12)); bar.grid_columnconfigure(0,weight=1)
        self.search_entry=ctk.CTkEntry(bar,placeholder_text="Search saved recipes",height=42,corner_radius=11); self.search_entry.grid(row=0,column=0,sticky="ew",padx=(0,8)); self.search_entry.bind("<Return>",lambda e:self.apply())
        ctk.CTkButton(bar,text="Search",width=90,command=self.apply).grid(row=0,column=1,padx=4)
        ctk.CTkButton(bar,text="All",width=75,command=lambda:self.set_filter("All")).grid(row=0,column=2,padx=4)
        ctk.CTkButton(bar,text="Favorites",width=95,command=lambda:self.set_filter("Favorites")).grid(row=0,column=3,padx=4)
        scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); scroll.grid(row=2,column=0,sticky="nsew"); scroll.grid_columnconfigure(0,weight=1)
        rows=self.app.db.list_recipes(self.app.user_id,saved_only=True,favorites_only=self.filter=="Favorites",search=self.search)
        if not rows: muted(scroll,"No saved recipes match your filter.").pack(anchor="w",padx=5,pady=10)
        for row in rows: self.item(scroll,recipe_from_row(row))
    def set_filter(self,v): self.filter=v; self.render()
    def apply(self): self.search=self.search_entry.get().strip(); self.render()
    def item(self,parent,d):
        c=card(parent); c.pack(fill="x",pady=6); c.grid_columnconfigure(1,weight=1)
        try: im=ctk.CTkImage(Image.open(d["image_path"]),size=(135,90)); ctk.CTkLabel(c,image=im,text="").grid(row=0,column=0,rowspan=2,padx=12,pady=12)
        except Exception: pass
        ctk.CTkLabel(c,text=d["recipe_name"],font=ctk.CTkFont(size=17,weight="bold")).grid(row=0,column=1,sticky="w",padx=5,pady=(14,3))
        muted(c,f"{d.get('total_time','')} • {d.get('calories',0)} kcal • {'★ Favorite' if d.get('is_favorite') else 'Not favorite'}").grid(row=1,column=1,sticky="w",padx=5)
        acts=ctk.CTkFrame(c,fg_color="transparent"); acts.grid(row=0,column=2,rowspan=2,padx=12)
        button(acts,"View",lambda:self.app.open_recipe(d["id"]),width=75).pack(pady=3)
        button(acts,"★" if not d.get("is_favorite") else "★✓",lambda:self.favorite(d["id"],not d.get("is_favorite")),width=50).pack(pady=3)
        button(acts,"Delete",lambda:self.delete(d["id"]),width=75).pack(pady=3)
    def favorite(self,rid,v): self.app.db.set_favorite(rid,self.app.user_id,v); self.render()
    def delete(self,rid):
        if messagebox.askyesno("Delete Recipe","Delete this saved recipe?"): self.app.db.delete_recipe(rid,self.app.user_id); self.render()
