from pathlib import Path
from config import ASSETS_DIR


def img(name):
    return str(ASSETS_DIR / name)


PREMADE_RECIPES = [

    # ============================================================
    # 1. BANGLADESHI CHICKEN CURRY
    # ============================================================

    {
        "recipe_name": "Bangladeshi Chicken Curry with Rice",
        "description": "A comforting home-style chicken curry served with fragrant rice and fresh herbs.",
        "ingredients": [
            "500 g chicken pieces",
            "2 cups cooked basmati rice",
            "1 onion, sliced",
            "2 tomatoes, chopped",
            "4 cloves garlic, minced",
            "1 tbsp ginger, grated",
            "2 tbsp cooking oil",
            "1 tsp turmeric",
            "1 tsp cumin",
            "Salt to taste"
        ],
        "instructions": [
            "Heat oil in a heavy pan and soften the onion until lightly golden.",
            "Add garlic, ginger, turmeric and cumin; cook for 30 seconds.",
            "Add tomatoes and cook until the mixture becomes thick and glossy.",
            "Add chicken and stir well so every piece is coated.",
            "Add a little water, cover and simmer until the chicken is tender and cooked through.",
            "Season with salt and serve hot with basmati rice."
        ],
        "cuisine": "Bangladeshi",
        "meal_type": "Lunch",
        "dietary_preference": "None",
        "difficulty": "Medium",
        "prep_time": "15 min",
        "cook_time": "35 min",
        "total_time": "50 min",
        "servings": 4,
        "calories": 560,
        "protein": 31,
        "carbs": 58,
        "fat": 22,
        "cooking_tips": [
            "Brown the onion slowly for deeper flavor.",
            "Let the curry rest for 5 minutes before serving.",
            "Add fresh coriander just before serving."
        ],
        "image_path": img("biryani.jpg"),
    },


    # ============================================================
    # 2. CREAMY GARLIC PASTA
    # ============================================================

    {
        "recipe_name": "Creamy Garlic Pasta",
        "description": "A quick Italian-inspired pasta with garlic, herbs and a silky creamy sauce.",
        "ingredients": [
            "250 g pasta",
            "3 cloves garlic, minced",
            "1 tbsp butter",
            "1 cup cooking cream",
            "1/3 cup parmesan cheese",
            "1 tsp Italian herbs",
            "Salt and black pepper",
            "Fresh parsley"
        ],
        "instructions": [
            "Boil the pasta in salted water until al dente; reserve 1/2 cup pasta water.",
            "Melt butter and gently cook the garlic until fragrant.",
            "Pour in the cream and simmer for 2 minutes.",
            "Stir in parmesan, herbs, salt and pepper.",
            "Toss in the pasta and loosen the sauce with reserved pasta water as needed.",
            "Finish with parsley and serve immediately."
        ],
        "cuisine": "Italian",
        "meal_type": "Dinner",
        "dietary_preference": "None",
        "difficulty": "Easy",
        "prep_time": "5 min",
        "cook_time": "15 min",
        "total_time": "20 min",
        "servings": 2,
        "calories": 610,
        "protein": 19,
        "carbs": 74,
        "fat": 27,
        "cooking_tips": [
            "Do not overcook the pasta.",
            "Add cheese off the strongest heat for a smoother sauce.",
            "Use pasta water to control sauce thickness."
        ],
        "image_path": img("combo_meal.jpg"),
    },


    # ============================================================
    # 3. FRESH POWER SALAD
    # ============================================================

    {
        "recipe_name": "Fresh Power Salad",
        "description": "A colorful crunchy salad with greens, vegetables and a simple citrus dressing.",
        "ingredients": [
            "2 cups mixed greens",
            "1 cucumber, sliced",
            "1 tomato, diced",
            "1/2 bell pepper, sliced",
            "1/4 red onion, thinly sliced",
            "2 tbsp olive oil",
            "1 tbsp lemon juice",
            "Salt and black pepper"
        ],
        "instructions": [
            "Wash and dry all vegetables thoroughly.",
            "Combine greens, cucumber, tomato, bell pepper and onion in a large bowl.",
            "Whisk olive oil, lemon juice, salt and black pepper.",
            "Drizzle the dressing over the salad just before serving.",
            "Toss gently and serve fresh."
        ],
        "cuisine": "Any",
        "meal_type": "Lunch",
        "dietary_preference": "Vegan",
        "difficulty": "Easy",
        "prep_time": "10 min",
        "cook_time": "0 min",
        "total_time": "10 min",
        "servings": 2,
        "calories": 190,
        "protein": 5,
        "carbs": 14,
        "fat": 13,
        "cooking_tips": [
            "Dry greens well so the dressing stays flavorful.",
            "Add dressing at the last moment for maximum crunch.",
            "Add roasted chickpeas for more protein."
        ],
        "image_path": img("ingredients.jpg"),
    },


    # ============================================================
    # 4. EASY COMFORT RICE BOWL
    # ============================================================

    {
        "recipe_name": "Easy Comfort Rice Bowl",
        "description": "A flexible rice bowl built around vegetables, protein and a bright savory sauce.",
        "ingredients": [
            "2 cups cooked rice",
            "1 cup mixed vegetables",
            "1 egg or 120 g cooked chicken",
            "1 tbsp soy sauce",
            "1 tsp sesame oil",
            "1 spring onion, sliced",
            "1 tsp sesame seeds"
        ],
        "instructions": [
            "Heat a skillet and warm the vegetables until crisp-tender.",
            "Add the egg or cooked chicken and heat through.",
            "Add rice, soy sauce and sesame oil; toss over medium heat.",
            "Cook for 2–3 minutes until everything is hot and evenly coated.",
            "Top with spring onion and sesame seeds."
        ],
        "cuisine": "Chinese",
        "meal_type": "Lunch",
        "dietary_preference": "None",
        "difficulty": "Easy",
        "prep_time": "10 min",
        "cook_time": "10 min",
        "total_time": "20 min",
        "servings": 2,
        "calories": 430,
        "protein": 20,
        "carbs": 58,
        "fat": 12,
        "cooking_tips": [
            "Use chilled rice for a better texture.",
            "Keep the pan hot so the vegetables stay crisp.",
            "Taste before adding extra soy sauce."
        ],
        "image_path": img("combo_meal.jpg"),
    },


    # ============================================================
    # 5. CHICKEN BIRYANI
    # ============================================================

    {
        "recipe_name": "Classic Chicken Biryani",
        "description": "A fragrant rice dish layered with spiced chicken, aromatic basmati rice and fresh herbs.",
        "ingredients": [
            "500 g chicken",
            "2 cups basmati rice",
            "1 large onion, sliced",
            "1/2 cup plain yogurt",
            "2 tomatoes, chopped",
            "2 tbsp cooking oil",
            "1 tbsp ginger-garlic paste",
            "1 tsp turmeric",
            "1 tsp cumin",
            "1 tsp garam masala",
            "2 green chilies",
            "Fresh coriander",
            "Salt to taste"
        ],
        "instructions": [
            "Wash and soak the basmati rice for 20 minutes.",
            "Marinate chicken with yogurt, turmeric, garam masala, ginger-garlic paste and salt.",
            "Fry sliced onions until golden and set half aside for garnish.",
            "Cook the marinated chicken with tomatoes and green chilies until almost tender.",
            "Boil rice separately until about 70% cooked and drain.",
            "Layer rice over the chicken and cover tightly.",
            "Cook on low heat for 15–20 minutes.",
            "Garnish with fried onions and fresh coriander before serving."
        ],
        "cuisine": "Bangladeshi",
        "meal_type": "Lunch",
        "dietary_preference": "None",
        "difficulty": "Hard",
        "prep_time": "30 min",
        "cook_time": "45 min",
        "total_time": "75 min",
        "servings": 4,
        "calories": 680,
        "protein": 35,
        "carbs": 72,
        "fat": 25,
        "cooking_tips": [
            "Do not fully cook the rice before layering.",
            "Use low heat during the final steaming stage.",
            "Rest the biryani for 5–10 minutes before serving."
        ],
        "image_path": img("biryani.jpg"),
    },


    # ============================================================
    # 6. VEGETABLE FRIED RICE
    # ============================================================

    {
        "recipe_name": "Quick Vegetable Fried Rice",
        "description": "A quick Chinese-style fried rice packed with colorful vegetables and savory flavors.",
        "ingredients": [
            "2 cups cooked cold rice",
            "1 carrot, diced",
            "1/2 cup green peas",
            "1/2 bell pepper, chopped",
            "2 cloves garlic, minced",
            "2 tbsp soy sauce",
            "1 tsp sesame oil",
            "2 spring onions",
            "1 tbsp cooking oil",
            "Black pepper to taste"
        ],
        "instructions": [
            "Heat cooking oil in a large wok or skillet.",
            "Add garlic and cook until fragrant.",
            "Add carrot, peas and bell pepper and stir-fry for 3–4 minutes.",
            "Add the cold cooked rice and break up any large pieces.",
            "Add soy sauce, sesame oil and black pepper.",
            "Stir-fry everything over high heat for 3–4 minutes.",
            "Finish with chopped spring onions and serve hot."
        ],
        "cuisine": "Chinese",
        "meal_type": "Dinner",
        "dietary_preference": "Vegan",
        "difficulty": "Easy",
        "prep_time": "10 min",
        "cook_time": "10 min",
        "total_time": "20 min",
        "servings": 3,
        "calories": 360,
        "protein": 9,
        "carbs": 59,
        "fat": 10,
        "cooking_tips": [
            "Use cold leftover rice for the best texture.",
            "Keep the wok hot while stir-frying.",
            "Avoid adding too much soy sauce."
        ],
        "image_path": img("combo_meal.jpg"),
    },


    # ============================================================
    # 7. CHICKEN TIKKA
    # ============================================================

    {
        "recipe_name": "Indian Chicken Tikka",
        "description": "Juicy pieces of spiced yogurt-marinated chicken cooked until lightly charred and flavorful.",
        "ingredients": [
            "500 g boneless chicken",
            "1/2 cup plain yogurt",
            "1 tbsp lemon juice",
            "1 tsp turmeric",
            "1 tsp cumin powder",
            "1 tsp paprika",
            "1 tsp garam masala",
            "1 tbsp ginger-garlic paste",
            "1 tbsp cooking oil",
            "Salt to taste"
        ],
        "instructions": [
            "Cut chicken into bite-sized pieces.",
            "Mix yogurt, lemon juice, spices, ginger-garlic paste, oil and salt.",
            "Add chicken and coat thoroughly with the marinade.",
            "Marinate for at least 30 minutes.",
            "Thread chicken onto skewers or place directly on a baking tray.",
            "Cook at high heat until the chicken is cooked through and lightly charred.",
            "Serve with lemon wedges and fresh salad."
        ],
        "cuisine": "Indian",
        "meal_type": "Dinner",
        "dietary_preference": "High Protein",
        "difficulty": "Medium",
        "prep_time": "40 min",
        "cook_time": "20 min",
        "total_time": "60 min",
        "servings": 3,
        "calories": 390,
        "protein": 45,
        "carbs": 9,
        "fat": 18,
        "cooking_tips": [
            "Marinate overnight for deeper flavor.",
            "Do not overcrowd the cooking tray.",
            "Cook at high heat to develop a light char."
        ],
        "image_path": img("biryani.jpg"),
    },


    # ============================================================
    # 8. VEGETABLE NOODLES
    # ============================================================

    {
        "recipe_name": "Spicy Vegetable Noodles",
        "description": "Quick stir-fried noodles with crunchy vegetables, garlic and a mildly spicy sauce.",
        "ingredients": [
            "200 g noodles",
            "1 carrot, thinly sliced",
            "1/2 bell pepper, sliced",
            "1 cup cabbage, shredded",
            "2 cloves garlic, minced",
            "1 tbsp soy sauce",
            "1 tbsp chili sauce",
            "1 tsp sesame oil",
            "1 tbsp cooking oil",
            "2 spring onions"
        ],
        "instructions": [
            "Cook noodles according to the package instructions and drain.",
            "Heat cooking oil in a wok.",
            "Add garlic and stir for 20 seconds.",
            "Add carrot, bell pepper and cabbage and stir-fry for 2–3 minutes.",
            "Add cooked noodles, soy sauce and chili sauce.",
            "Toss everything together over high heat.",
            "Finish with sesame oil and spring onions."
        ],
        "cuisine": "Chinese",
        "meal_type": "Dinner",
        "dietary_preference": "Vegan",
        "difficulty": "Easy",
        "prep_time": "10 min",
        "cook_time": "10 min",
        "total_time": "20 min",
        "servings": 2,
        "calories": 410,
        "protein": 10,
        "carbs": 67,
        "fat": 12,
        "cooking_tips": [
            "Do not overcook the vegetables.",
            "Cook noodles slightly firm so they do not become mushy.",
            "Adjust chili sauce according to your preference."
        ],
        "image_path": img("combo_meal.jpg"),
    },


    # ============================================================
    # 9. LENTIL DAL
    # ============================================================

    {
        "recipe_name": "Simple Bangladeshi Masoor Dal",
        "description": "A comforting red lentil dish cooked with turmeric, garlic, onion and aromatic spices.",
        "ingredients": [
            "1 cup red lentils",
            "3 cups water",
            "1/2 onion, chopped",
            "3 cloves garlic, sliced",
            "1 green chili",
            "1/2 tsp turmeric",
            "1 tsp cumin seeds",
            "1 tbsp cooking oil",
            "Fresh coriander",
            "Salt to taste"
        ],
        "instructions": [
            "Wash the red lentils thoroughly.",
            "Add lentils, water, turmeric and salt to a pot.",
            "Cook until the lentils become soft and creamy.",
            "Heat oil in a separate pan.",
            "Add cumin seeds, garlic, onion and green chili.",
            "Cook until the onion becomes lightly golden.",
            "Pour the tempering over the cooked lentils.",
            "Garnish with fresh coriander and serve with rice."
        ],
        "cuisine": "Bangladeshi",
        "meal_type": "Lunch",
        "dietary_preference": "Vegetarian",
        "difficulty": "Easy",
        "prep_time": "5 min",
        "cook_time": "25 min",
        "total_time": "30 min",
        "servings": 4,
        "calories": 270,
        "protein": 15,
        "carbs": 39,
        "fat": 7,
        "cooking_tips": [
            "Wash lentils well before cooking.",
            "Add water gradually if you prefer a thinner dal.",
            "Fresh coriander adds a bright finish."
        ],
        "image_path": img("ingredients.jpg"),
    },


    # ============================================================
    # 10. MEXICAN BEAN TACOS
    # ============================================================

    {
        "recipe_name": "Easy Mexican Bean Tacos",
        "description": "Flavorful soft tacos filled with seasoned beans, fresh vegetables and creamy avocado.",
        "ingredients": [
            "6 small tortillas",
            "1 cup cooked kidney beans",
            "1 tomato, diced",
            "1/2 onion, chopped",
            "1/2 bell pepper, chopped",
            "1/2 avocado, sliced",
            "1 tsp cumin",
            "1/2 tsp paprika",
            "1 tbsp lime juice",
            "Fresh coriander",
            "Salt to taste"
        ],
        "instructions": [
            "Heat the beans in a skillet with cumin, paprika and a pinch of salt.",
            "Cook the chopped onion and bell pepper until slightly softened.",
            "Warm the tortillas in a dry pan.",
            "Fill each tortilla with seasoned beans and vegetables.",
            "Add diced tomato and avocado.",
            "Drizzle with lime juice.",
            "Garnish with fresh coriander and serve immediately."
        ],
        "cuisine": "Mexican",
        "meal_type": "Dinner",
        "dietary_preference": "Vegan",
        "difficulty": "Easy",
        "prep_time": "10 min",
        "cook_time": "10 min",
        "total_time": "20 min",
        "servings": 3,
        "calories": 340,
        "protein": 12,
        "carbs": 51,
        "fat": 11,
        "cooking_tips": [
            "Warm tortillas just before serving.",
            "Add fresh lime juice for extra brightness.",
            "Use fresh avocado for a creamy texture."
        ],
        "image_path": img("ingredients.jpg"),
    },
]