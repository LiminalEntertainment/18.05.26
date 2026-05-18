# =========================================
# AI СКЕНЕР ЗА ХРАНИТЕЛНИ ЕТИКЕТИ
# OCR + AI PRODUCT DETECTION
# =========================================

import streamlit as st
import easyocr
from PIL import Image, ImageEnhance
import numpy as np

# =========================================
# STREAMLIT SETTINGS
# =========================================

st.set_page_config(
    page_title="Food Label Scanner",
    layout="centered"
)

st.title("Скенер за хранителни етикети")

# =========================================
# LANGUAGE SELECTION
# =========================================

language = st.selectbox(
    "Изберете език / Choose language",
    ["Български", "English"]
)

# =========================================
# BULGARIAN MODE
# =========================================

if language == "Български":

    OCR_LANG = ['bg']

    harmful_ingredients = {

        "e102": "Тартразин – може да причини алергии и хиперактивност.",
        "e104": "Жълто хинолиново – свързва се с хиперактивност.",
        "e110": "Сънсет жълто – възможни алергии.",
        "e122": "Кармоизин – може да причини алергии.",
        "e124": "Понсо 4R – възможна хиперактивност.",
        "e129": "Алура червено – свързва се с хиперактивност.",
        "e211": "Натриев бензоат – възможни проблеми с нервната система.",
        "e220": "Серен диоксид – може да причини астма.",
        "e250": "Натриев нитрит – свързва се с риск от рак.",
        "e251": "Натриев нитрат – вреден при прекомерна консумация.",
        "e320": "BHA – възможен канцероген.",
        "e321": "BHT – възможни проблеми с черния дроб.",
        "e407": "Карагенан – може да раздразни стомаха.",
        "e621": "Мононатриев глутамат – може да причини главоболие.",
        "e627": "Динатриев гуанилат – усилвател на вкуса.",
        "e631": "Динатриев инозинат – усилвател на вкуса.",
        "палмово масло": "Съдържа много наситени мазнини.",
        "аспартам": "Изкуствен подсладител.",
        "глюкозо-фруктозен сироп": "Може да доведе до диабет.",
        "транс мазнини": "Повишават риска от сърдечни заболявания."
    }

    # =========================================
    # HEALTH PROBLEMS
    # =========================================

    health_problems = {

        "e621": [
            "Главоболие",
            "Умора",
            "Проблеми с нервната система"
        ],

        "e250": [
            "Риск от рак",
            "Проблеми със сърцето"
        ],

        "e102": [
            "Алергии",
            "Хиперактивност"
        ],

        "палмово масло": [
            "Висок холестерол",
            "Сърдечни заболявания"
        ],

        "аспартам": [
            "Главоболие",
            "Замайване"
        ],

        "глюкозо-фруктозен сироп": [
            "Диабет",
            "Затлъстяване"
        ],

        "транс мазнини": [
            "Сърдечни заболявания",
            "Висок холестерол"
        ]
    }

    # =========================================
    # PRODUCT DETECTION
    # =========================================

    product_patterns = {

        "Чипс": {
            "ingredients": [
                "картофи",
                "палмово масло",
                "e621",
                "сол"
            ],

            "alternatives": [
                "Домашно изпечени картофи",
                "Зеленчуков чипс",
                "Пуканки без масло"
            ]
        },

        "Газирана напитка": {
            "ingredients": [
                "захар",
                "аспартам",
                "карамел",
                "кофеин"
            ],

            "alternatives": [
                "Домашна лимонада",
                "Минерална вода с лимон",
                "Студен чай без захар"
            ]
        },

        "Шоколад": {
            "ingredients": [
                "какао",
                "палмово масло",
                "мляко",
                "захар"
            ],

            "alternatives": [
                "Черен шоколад 85%",
                "Плодове",
                "Домашни десерти"
            ]
        },

        "Бисквити": {
            "ingredients": [
                "брашно",
                "захар",
                "палмово масло",
                "глюкозо-фруктозен сироп"
            ],

            "alternatives": [
                "Овесени бисквити",
                "Домашни сладки",
                "Ядки и плодове"
            ]
        },

        "Колбас": {
            "ingredients": [
                "e250",
                "e251",
                "нитрит",
                "нитрат",
                "месо"
            ],

            "alternatives": [
                "Печено месо",
                "Пилешко филе",
                "Домашно месо"
            ]
        }
    }

# =========================================
# ENGLISH MODE
# =========================================

else:

    OCR_LANG = ['en']

    harmful_ingredients = {

        "e102": "Tartrazine – may cause allergies and hyperactivity.",
        "e104": "Quinoline Yellow – linked to hyperactivity.",
        "e110": "Sunset Yellow – may cause allergic reactions.",
        "e122": "Carmoisine – possible allergies.",
        "e124": "Ponceau 4R – linked to hyperactivity.",
        "e129": "Allura Red – may affect children.",
        "e211": "Sodium benzoate – may affect the nervous system.",
        "e220": "Sulfur dioxide – may trigger asthma.",
        "e250": "Sodium nitrite – linked to cancer risk.",
        "e251": "Sodium nitrate – harmful in excess.",
        "e320": "BHA – possible carcinogen.",
        "e321": "BHT – may affect the liver.",
        "e407": "Carrageenan – may irritate the stomach.",
        "e621": "MSG – may cause headaches.",
        "e627": "Disodium guanylate – flavor enhancer.",
        "e631": "Disodium inosinate – flavor enhancer.",
        "palm oil": "Contains high saturated fats.",
        "aspartame": "Artificial sweetener.",
        "high fructose corn syrup": "May lead to diabetes.",
        "trans fats": "Increase heart disease risk."
    }

    # =========================================
    # HEALTH PROBLEMS
    # =========================================

    health_problems = {

        "e621": [
            "Headaches",
            "Fatigue",
            "Nervous system problems"
        ],

        "e250": [
            "Cancer risk",
            "Heart problems"
        ],

        "e102": [
            "Allergies",
            "Hyperactivity"
        ],

        "palm oil": [
            "High cholesterol",
            "Heart disease"
        ],

        "aspartame": [
            "Headaches",
            "Dizziness"
        ],

        "high fructose corn syrup": [
            "Diabetes",
            "Obesity"
        ],

        "trans fats": [
            "Heart disease",
            "High cholesterol"
        ]
    }

    # =========================================
    # PRODUCT DETECTION
    # =========================================

    product_patterns = {

        "Chips": {
            "ingredients": [
                "potatoes",
                "palm oil",
                "e621",
                "salt"
            ],

            "alternatives": [
                "Baked potatoes",
                "Vegetable chips",
                "Air popcorn"
            ]
        },

        "Soft Drink": {
            "ingredients": [
                "sugar",
                "aspartame",
                "caramel",
                "caffeine"
            ],

            "alternatives": [
                "Homemade lemonade",
                "Sparkling water with lemon",
                "Unsweetened iced tea"
            ]
        },

        "Chocolate": {
            "ingredients": [
                "cocoa",
                "palm oil",
                "milk",
                "sugar"
            ],

            "alternatives": [
                "Dark chocolate 85%",
                "Fruit",
                "Homemade desserts"
            ]
        },

        "Cookies": {
            "ingredients": [
                "flour",
                "sugar",
                "palm oil",
                "high fructose corn syrup"
            ],

            "alternatives": [
                "Oat cookies",
                "Homemade cookies",
                "Nuts and fruits"
            ]
        },

        "Processed Meat": {
            "ingredients": [
                "e250",
                "e251",
                "nitrite",
                "nitrate",
                "meat"
            ],

            "alternatives": [
                "Roasted meat",
                "Chicken fillet",
                "Homemade meat"
            ]
        }
    }

# =========================================
# FILE UPLOAD
# =========================================

uploaded_file = st.file_uploader(
    "Качете снимка / Upload image",
    type=["jpg", "jpeg", "png"]
)

# =========================================
# OCR ANALYSIS
# =========================================

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Качено изображение" if language == "Български" else "Uploaded image",
        use_column_width=True
    )

    # IMAGE ENHANCEMENT
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)

    image_np = np.array(image)

    if language == "Български":
        st.write("Разпознаване на текст...")
    else:
        st.write("Reading text...")

    # OCR
    reader = easyocr.Reader(OCR_LANG)

    results = reader.readtext(image_np, detail=0)

    extracted_text = " ".join(results).lower()

    # =========================================
    # SHOW OCR TEXT
    # =========================================

    if language == "Български":
        st.subheader("Разпознат текст:")
    else:
        st.subheader("Recognized text:")

    st.write(extracted_text)

    # =========================================
    # HARMFUL INGREDIENTS
    # =========================================

    if language == "Български":
        st.subheader("Вредни съставки:")
    else:
        st.subheader("Harmful ingredients:")

    found = False

    for ingredient, info in harmful_ingredients.items():

        if ingredient in extracted_text:

            found = True

            st.error(f"{ingredient.upper()}")

            st.write(info)

            # =========================================
            # HEALTH PROBLEMS
            # =========================================

            if ingredient in health_problems:

                if language == "Български":
                    st.warning("Възможни здравословни проблеми:")
                else:
                    st.warning("Possible health problems:")

                for problem in health_problems[ingredient]:
                    st.write(f"• {problem}")

    if not found:

        if language == "Български":
            st.success("Не са открити вредни съставки.")
        else:
            st.success("No harmful ingredients found.")

    # =========================================
    # PRODUCT DETECTION
    # =========================================

    best_match = None
    best_score = 0

    for product, data in product_patterns.items():

        score = 0

        for keyword in data["ingredients"]:

            if keyword in extracted_text:
                score += 1

        if score > best_score:
            best_score = score
            best_match = product

    # =========================================
    # RESULTS
    # =========================================

    if language == "Български":
        st.subheader("Разпознат продукт:")
    else:
        st.subheader("Detected product:")

    if best_match:

        st.success(best_match)

        if language == "Български":
            st.subheader("По-здравословни алтернативи:")
        else:
            st.subheader("Healthier alternatives:")

        for alt in product_patterns[best_match]["alternatives"]:
            st.write(f"• {alt}")

    else:

        if language == "Български":
            st.warning("Продуктът не можа да бъде разпознат.")
        else:
            st.warning("Could not recognize the product.")
