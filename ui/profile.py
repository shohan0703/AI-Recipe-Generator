import customtkinter as ctk
from tkinter import messagebox
from ui.base import card,title,muted,button

class ProfilePage(ctk.CTkFrame):
    def __init__(self,parent,app): super().__init__(parent,fg_color="transparent"); self.app=app; self.render()
    def render(self):
        for w in self.winfo_children(): w.destroy()
        self.grid_columnconfigure(0,weight=1)
        title(self,"Profile").grid(row=0,column=0,sticky="w",padx=5,pady=(5,15))
        user=self.app.db.get_user(self.app.user_id); c=card(self); c.grid(row=1,column=0,sticky="ew",padx=4); c.grid_columnconfigure(1,weight=1)
        labels=[("Full Name",user["name"]),("Email",user["email"])]
        for r,(lab,val) in enumerate(labels): ctk.CTkLabel(c,text=lab,font=ctk.CTkFont(size=13,weight="bold")).grid(row=r*2,column=0,sticky="w",padx=20,pady=(20,3)); e=ctk.CTkEntry(c,height=42,corner_radius=10); e.insert(0,val); e.configure(state="disabled" if lab=="Email" else "normal"); e.grid(row=r*2+1,column=0,columnspan=2,sticky="ew",padx=20,pady=(0,6)); setattr(self,lab.lower().replace(" ","_"),e)
        r=4
        ctk.CTkLabel(c,text="Preferred Cuisine",font=ctk.CTkFont(size=13,weight="bold")).grid(row=r,column=0,sticky="w",padx=20,pady=(18,3)); self.cuisine=ctk.CTkComboBox(c,values=["Any","Bangladeshi","Indian","Italian","Chinese","Mexican"],height=42); self.cuisine.set(user["preferred_cuisine"] or "Any"); self.cuisine.grid(row=r+1,column=0,columnspan=2,sticky="ew",padx=20)
        r=6
        ctk.CTkLabel(c,text="Dietary Preference",font=ctk.CTkFont(size=13,weight="bold")).grid(row=r,column=0,sticky="w",padx=20,pady=(18,3)); self.diet=ctk.CTkComboBox(c,values=["None","Vegetarian","Vegan","High Protein","Low Carb"],height=42); self.diet.set(user["dietary_preference"] or "None"); self.diet.grid(row=r+1,column=0,columnspan=2,sticky="ew",padx=20,pady=(0,10))
        button(c,"Save Changes",self.save,primary=True,width=170).grid(row=8,column=0,columnspan=2,pady=25)
    def save(self):
        try:
            self.app.db.update_user(self.app.user_id,self.full_name.get().strip(),self.cuisine.get(),self.diet.get()); messagebox.showinfo("Profile","Profile updated successfully.")
        except Exception: messagebox.showerror("Profile","Could not save profile.")
