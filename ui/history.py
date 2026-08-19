import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from ui.base import card,title,muted,button
from recipe_service import recipe_from_row

class HistoryPage(ctk.CTkFrame):
    def __init__(self,parent,app): super().__init__(parent,fg_color="transparent"); self.app=app; self.render()
    def render(self):
        for w in self.winfo_children(): w.destroy()
        self.grid_columnconfigure(0,weight=1); self.grid_rowconfigure(1,weight=1)
        title(self,"Recipe History").grid(row=0,column=0,sticky="w",padx=5,pady=(5,15))
        scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); scroll.grid(row=1,column=0,sticky="nsew"); scroll.grid_columnconfigure(0,weight=1)
        rows=self.app.db.list_recipes(self.app.user_id)
        if not rows: muted(scroll,"Generate a recipe and it will appear here.").pack(anchor="w",padx=5,pady=10)
        for row in rows:
            d=recipe_from_row(row); c=card(scroll); c.pack(fill="x",pady=6); c.grid_columnconfigure(1,weight=1)
            try: im=ctk.CTkImage(Image.open(d["image_path"]),size=(120,80)); ctk.CTkLabel(c,image=im,text="").grid(row=0,column=0,rowspan=2,padx=12,pady=12)
            except Exception: pass
            ctk.CTkLabel(c,text=d["recipe_name"],font=ctk.CTkFont(size=16,weight="bold")).grid(row=0,column=1,sticky="w",padx=7,pady=(15,3))
            muted(c,f"Generated {d.get('created_at','')}").grid(row=1,column=1,sticky="w",padx=7,pady=(0,14))
            button(c,"View",lambda rid=d["id"]:self.app.open_recipe(rid),width=90).grid(row=0,column=2,rowspan=2,padx=8)
            button(c,"Delete",lambda rid=d["id"]:self.delete(rid),width=90).grid(row=0,column=3,rowspan=2,padx=8)
    def delete(self,rid):
        if messagebox.askyesno("Delete Recipe","Remove this recipe from history?"): self.app.db.delete_recipe(rid,self.app.user_id); self.render()
