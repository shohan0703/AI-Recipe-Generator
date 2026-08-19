import json
import os
import subprocess
import tempfile
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from ui.base import card, title, muted, button
from recipe_service import recipe_from_row, choose_image


class RecipeDetailsPage(ctk.CTkFrame):
    def __init__(self,parent,app):
        super().__init__(parent,fg_color="transparent"); self.app=app; self.data=None

    def show(self,data,stored=False):
        self.data=data if stored else data.copy()
        if not stored and not self.data.get("image_path"):
            self.data["image_path"]=choose_image(self.data.get("recipe_name",""),self.data.get("cuisine",""))
        for w in self.winfo_children(): w.destroy()
        self.grid_columnconfigure(0,weight=1); self.grid_rowconfigure(1,weight=1)
        top=ctk.CTkFrame(self,fg_color="transparent"); top.grid(row=0,column=0,sticky="ew",pady=(0,10)); top.grid_columnconfigure(0,weight=1)
        button(top,"← Back",self.app.go_back,width=100).grid(row=0,column=0,sticky="w")
        actions=ctk.CTkFrame(top,fg_color="transparent"); actions.grid(row=0,column=1,sticky="e")
        if stored:
            button(actions,"Save" if not self.data.get("is_saved") else "Unsave",self.toggle_save,primary=not bool(self.data.get("is_saved")),width=105).pack(side="left",padx=4)
            button(actions,"★ Favorite" if not self.data.get("is_favorite") else "★ Favorited",self.toggle_favorite,width=125).pack(side="left",padx=4)
        else:
            button(actions,"Save",self.save_new,primary=True,width=105).pack(side="left",padx=4)
            button(actions,"★ Favorite",self.favorite_new,width=125).pack(side="left",padx=4)
        button(actions,"Print",self.print_recipe,width=85).pack(side="left",padx=4)
        scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); scroll.grid(row=1,column=0,sticky="nsew"); scroll.grid_columnconfigure(0,weight=1)
        hero=card(scroll); hero.grid(row=0,column=0,sticky="ew"); hero.grid_columnconfigure(1,weight=1)
        p=self.data.get("image_path","")
        if p:
            try:
                im=ctk.CTkImage(Image.open(p),size=(330,205)); ctk.CTkLabel(hero,image=im,text="").grid(row=0,column=0,rowspan=2,padx=18,pady=18)
            except Exception: pass
        ctk.CTkLabel(hero,text=self.data.get("recipe_name","Recipe"),font=ctk.CTkFont(size=27,weight="bold"),wraplength=520,justify="left").grid(row=0,column=1,sticky="nw",padx=10,pady=(25,6))
        ctk.CTkLabel(hero,text=self.data.get("description",""),wraplength=520,justify="left",text_color=("#57534E","#D6D3D1")).grid(row=1,column=1,sticky="nw",padx=10,pady=(0,18))
        meta=ctk.CTkFrame(hero,fg_color="transparent"); meta.grid(row=2,column=0,columnspan=2,sticky="ew",padx=18,pady=(0,18))
        vals=[("Time",self.data.get("total_time","")),("Servings",self.data.get("servings",1)),("Difficulty",self.data.get("difficulty","")),("Calories",f"{self.data.get('calories',0)} kcal")]
        for i,(a,b) in enumerate(vals): ctk.CTkLabel(meta,text=f"{a}\n{b}",justify="left",font=ctk.CTkFont(size=13,weight="bold")).pack(side="left",expand=True,anchor="w")
        self.section(scroll,"Ingredients",[f"• {x}" for x in self.data.get("ingredients",[])],1)
        self.section(scroll,"Cooking Instructions",[f"{i+1}. {x}" for i,x in enumerate(self.data.get("instructions",[]))],2)
        nutrition=[f"Calories: {self.data.get('calories',0)} kcal",f"Protein: {self.data.get('protein',0)} g",f"Carbs: {self.data.get('carbs',0)} g",f"Fat: {self.data.get('fat',0)} g"]
        self.section(scroll,"Nutrition",nutrition,3,subtitle="Nutrition values are AI-generated estimates.")
        self.section(scroll,"Cooking Tips",[f"• {x}" for x in self.data.get("cooking_tips",[])],4)

    def section(self,parent,heading,lines,row,subtitle=None):
        c=card(parent); c.grid(row=row,column=0,sticky="ew",pady=8); ctk.CTkLabel(c,text=heading,font=ctk.CTkFont(size=20,weight="bold")).pack(anchor="w",padx=22,pady=(18,6))
        if subtitle: muted(c,subtitle).pack(anchor="w",padx=22,pady=(0,5))
        for line in lines: ctk.CTkLabel(c,text=line,wraplength=880,justify="left",anchor="w").pack(fill="x",padx=22,pady=5)
        ctk.CTkLabel(c,text="").pack(pady=4)

    def save_new(self):
        try:
            rid=self.app.db.add_recipe(self.app.user_id,self.data,self.data.get("image_path","")); self.data["id"]=rid; self.data["is_saved"]=1
            messagebox.showinfo("ChefAI","Recipe saved successfully."); self.show(self.data,stored=True)
        except Exception:
            messagebox.showerror("ChefAI","Could not save recipe.")

    def favorite_new(self):
        self.save_new();
        if self.data.get("id"):
            self.app.db.set_favorite(self.data["id"],self.app.user_id,1); self.data["is_favorite"]=1; self.show(self.data,stored=True)

    def toggle_save(self):
        new=0 if self.data.get("is_saved") else 1; self.app.db.set_saved(self.data["id"],self.app.user_id,new); self.data["is_saved"]=new; self.show(self.data,stored=True)

    def toggle_favorite(self):
        new=0 if self.data.get("is_favorite") else 1; self.app.db.set_favorite(self.data["id"],self.app.user_id,new); self.data["is_favorite"]=new; self.show(self.data,stored=True)

    def print_recipe(self):
        text=f"{self.data.get('recipe_name','ChefAI Recipe')}\n\n{self.data.get('description','')}\n\nIngredients:\n"+"\n".join(f"- {x}" for x in self.data.get("ingredients",[]))+"\n\nInstructions:\n"+"\n".join(f"{i+1}. {x}" for i,x in enumerate(self.data.get("instructions",[])))+f"\n\nNutrition: {self.data.get('calories',0)} kcal | Protein {self.data.get('protein',0)} g | Carbs {self.data.get('carbs',0)} g | Fat {self.data.get('fat',0)} g\n"
        try:
            fd,path=tempfile.mkstemp(prefix="chefai_",suffix=".txt"); os.close(fd); open(path,"w",encoding="utf-8").write(text)
            if os.name=="nt": os.startfile(path,"print")
            else: subprocess.run(["lpr",path],check=False)
        except Exception: messagebox.showinfo("Print", "A printable recipe file was prepared, but direct printing is unavailable on this system.")
