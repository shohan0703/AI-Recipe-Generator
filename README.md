# ChefAI — AI Recipe Generator Desktop App

ChefAI is a lightweight university-project desktop application built with **Python + CustomTkinter + SQLite + Gemini API**. It does not train or run a local AI model.

## Features

- Register, login, logout, and local password reset
- Dashboard with recipe statistics and recent recipes
- Gemini-powered structured recipe generation
- Recipe details with ingredients, instructions, nutrition, and tips
- Save / unsave and favorite / unfavorite recipes
- Recipe history with reopen and delete
- Profile editing
- Light / dark mode
- Local recipe image assets with category mapping and fallback
- User-friendly error handling and background Gemini requests so the UI stays responsive

## Project structure

```text
ChefAI/
├── main.py
├── database.py
├── auth.py
├── ai_service.py
├── recipe_service.py
├── config.py
├── ui/
│   ├── __init__.py
│   ├── base.py
│   ├── login.py
│   ├── register.py
│   ├── dashboard.py
│   ├── recipe_generator.py
│   ├── recipe_details.py
│   ├── saved_recipes.py
│   ├── history.py
│   ├── profile.py
│   └── settings.py
├── assets/images/
├── .env.example
├── .gitignore
└── requirements.txt
```

## Setup

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and put your Gemini API key in:

```env
GEMINI_API_KEY=your_key_here
```

The key is never hard-coded and `.env` is ignored by Git.

4. Start the application:

```bash
python main.py
```

## Gemini implementation

ChefAI uses the official `google-genai` Python SDK. The app asks Gemini for JSON that follows a fixed response schema, then validates the decoded result before it is saved. This makes the response easier to parse safely than free-form text.

## Viva-friendly architecture

The app is intentionally small: authentication is separated from database access, Gemini logic is in `ai_service.py`, recipe-specific helpers are in `recipe_service.py`, and each major UI screen has its own module.

## Note on nutrition

Nutrition values are AI-generated estimates and should not be treated as medical or dietary advice.

## UI Photos
ChefAI now ships with a small set of real food/cooking photographs for the login hero, dashboard, and recipe cards. They are stored locally under `assets/images/`, so the UI does not need a second image API. The photographs were sourced from publicly accessible food photography pages; see the project build notes for their original pages.

## Gemini generation troubleshooting

ChefAI uses a 60-second Gemini client timeout so the Generate Recipe screen does not stay on the loading state indefinitely. The current SDK structured-output configuration uses `response_mime_type="application/json"` and `response_schema`.

If generation times out, check that `.env` contains a valid `GEMINI_API_KEY`, that the computer has internet access, and that the selected model is available to the key.
