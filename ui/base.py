import customtkinter as ctk
from PIL import Image, ImageDraw

from config import (
    CARD_DARK, CARD_LIGHT, DARK_BG, LIGHT_BG, MUTED_DARK, MUTED_LIGHT,
    PRIMARY, PRIMARY_HOVER, SECONDARY, TEXT_DARK, TEXT_LIGHT,
)


def card(parent, **kwargs):
    return ctk.CTkFrame(parent, corner_radius=18, fg_color=kwargs.pop("fg_color", None), **kwargs)


def title(parent, text, size=28):
    return ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=size, weight="bold"), anchor="w")


def muted(parent, text, size=13):
    return ctk.CTkLabel(parent, text=text, text_color=(MUTED_LIGHT, MUTED_DARK), font=ctk.CTkFont(size=size), anchor="w")


def button(parent, text, command, primary=False, width=150):
    return ctk.CTkButton(
        parent, text=text, command=command, width=width, height=40,
        corner_radius=12, fg_color=PRIMARY if primary else ("#EDE7DF", "#33302C"),
        hover_color=PRIMARY_HOVER if primary else ("#DDD6CC", "#403C37"),
        text_color="#FFFFFF" if primary else (TEXT_LIGHT, TEXT_DARK),
        font=ctk.CTkFont(size=14, weight="bold" if primary else "normal")
    )


def make_placeholder_image(path, theme="food", size=(900, 550)):
    img = Image.new("RGB", size, "#F8F5EF")
    d = ImageDraw.Draw(img)
    cx, cy = size[0]//2, size[1]//2 + 15
    colors = {
        "chicken": (218, 134, 75), "rice": (248, 232, 180), "pasta": (224, 173, 75),
        "salad": (111, 164, 79), "soup": (193, 112, 59), "dessert": (188, 118, 162),
        "curry": (213, 125, 50), "food": (237, 175, 93)
    }
    main = colors.get(theme, colors["food"])
    d.ellipse((cx-250, cy-170, cx+250, cy+140), fill=(230, 224, 214), outline=(190,185,177), width=4)
    d.ellipse((cx-210, cy-125, cx+210, cy+105), fill=main)
    # simple ingredient accents
    for dx, dy, r, col in [(-110,-35,24,(96,125,55)), (40,-45,28,(178,56,44)), (125,5,18,(246,214,100)), (-35,45,20,(255,245,220)), (65,55,20,(96,70,45))]:
        d.ellipse((cx+dx-r, cy+dy-r, cx+dx+r, cy+dy+r), fill=col)
    d.rounded_rectangle((40, 35, size[0]-40, 115), radius=24, fill=(34,34,34), outline=(34,34,34))
    d.text((65, 57), "ChefAI • Recipe", fill="white")
    img.save(path)
