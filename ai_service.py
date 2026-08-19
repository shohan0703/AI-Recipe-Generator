import json
import os
from typing import Any

from google import genai
from google.genai import types

from config import GEMINI_MODEL


RECIPE_SCHEMA = {
    "type": "object",
    "properties": {
        "recipe_name": {"type": "string"},
        "description": {"type": "string"},
        "ingredients": {"type": "array", "items": {"type": "string"}},
        "instructions": {"type": "array", "items": {"type": "string"}},
        "cuisine": {"type": "string"},
        "meal_type": {"type": "string"},
        "dietary_preference": {"type": "string"},
        "difficulty": {"type": "string"},
        "prep_time": {"type": "string"},
        "cook_time": {"type": "string"},
        "total_time": {"type": "string"},
        "servings": {"type": "integer"},
        "calories": {"type": "integer"},
        "protein": {"type": "number"},
        "carbs": {"type": "number"},
        "fat": {"type": "number"},
        "cooking_tips": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "recipe_name", "description", "ingredients", "instructions", "cuisine",
        "meal_type", "dietary_preference", "difficulty", "prep_time", "cook_time",
        "total_time", "servings", "calories", "protein", "carbs", "fat", "cooking_tips"
    ],
}


class AIServiceError(Exception):
    pass


class GeminiRecipeService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.client = (
            genai.Client(
                api_key=self.api_key,
                http_options=types.HttpOptions(timeout=60000),
            )
            if self.api_key else None
        )

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def generate_recipe(self, ingredients: str, cuisine: str, meal_type: str,
                        dietary: str, difficulty: str, cooking_time: str, servings: int) -> dict[str, Any]:
        if not self.client:
            raise AIServiceError(
                "Gemini API key is not configured. Open the ChefAI .env file and set GEMINI_API_KEY=your_key."
            )
        if not ingredients.strip():
            raise AIServiceError("Please enter at least one ingredient.")

        prompt = f"""
You are ChefAI, a recipe generation assistant for a university desktop project.
Create one practical recipe using the user's constraints below.

Ingredients supplied by user: {ingredients.strip()}
Cuisine: {cuisine}
Meal type: {meal_type}
Dietary preference: {dietary}
Difficulty: {difficulty}
Cooking time preference: {cooking_time}
Servings: {servings}

Rules:
- Respect the user's ingredients and preferences as much as reasonably possible.
- You may add normal pantry basics if necessary.
- Give realistic quantities and concise, safe cooking steps.
- Nutrition numbers are estimates per serving.
- Provide exactly 2 or 3 useful cooking tips.
- Return ONLY JSON matching the provided response schema.
"""
        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=RECIPE_SCHEMA,
                    max_output_tokens=1800,
                    thinking_config=types.ThinkingConfig(thinking_level="low"),
                ),
            )
            text = (response.text or "").strip()
            data = json.loads(text)
            self._validate(data)
            return data
        except json.JSONDecodeError as exc:
            raise AIServiceError("Gemini returned an invalid recipe format. Please try again.") from exc
        except AIServiceError:
            raise
        except Exception as exc:
            raise AIServiceError(self._friendly_error(exc)) from exc

    @staticmethod
    def _validate(data):
        required = ["recipe_name", "description", "ingredients", "instructions", "difficulty", "servings"]
        if not isinstance(data, dict) or any(k not in data for k in required):
            raise AIServiceError("Gemini returned incomplete recipe data. Please try again.")
        if not isinstance(data["ingredients"], list) or not data["ingredients"]:
            raise AIServiceError("Gemini returned no ingredients. Please try again.")
        if not isinstance(data["instructions"], list) or not data["instructions"]:
            raise AIServiceError("Gemini returned no instructions. Please try again.")

    @staticmethod
    def _friendly_error(exc: Exception) -> str:
        msg = str(exc).lower()
        if "api key" in msg or "unauthenticated" in msg or "permission" in msg:
            return "Gemini API key is invalid or unavailable. Check GEMINI_API_KEY."
        if "404" in msg or "not found" in msg or "model" in msg and "not found" in msg:
            return "The selected Gemini model is unavailable. Check GEMINI_MODEL in .env."
        if "429" in msg or "resource_exhausted" in msg or "quota" in msg or "rate limit" in msg:
            return "Gemini request limit reached. Please wait a little and try again."
        if "400" in msg or "invalid_argument" in msg:
            return "Gemini rejected the request. Please try again with different recipe preferences."
        if "timeout" in msg or "timed out" in msg:
            return "The request timed out. Please check your internet connection and try again."
        if "connection" in msg or "network" in msg:
            return "Unable to reach Gemini. Please check your internet connection."
        return f"Unable to generate recipe: {str(exc)[:180]}"
