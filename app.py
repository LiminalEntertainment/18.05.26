import streamlit as st
import easyocr
from PIL import Image, ImageEnhance
import numpy as np

# Заглавие
st.title("Скенер за хранителни етикети")
st.write("Приложение за разпознаване и анализ на вредни съставки в хранителни продукти.")

# Поддръжка на езици
language = st.selectbox(
    "Изберете език / Choose language",
    ["Български", "English"]
)

# Речник с вредни съставки
harmful_ingredients = {
    "E621": {
        "bg": "Мононатриев глутамат - може да причини главоболие, умора и проблеми с нервната система.",
        "en": "Monosodium glutamate - may cause headaches, fatigue and nervous system problems."
    },
    "палмово масло": {
        "bg": "Палмовото масло съдържа наситени мазнини и може да повиши риска от сърдечни заболявания.",
        "en": "Palm oil contains saturated fats and may increase the risk of heart disease."
    },
    "palm oil": {
        "bg": "Палмовото масло съдържа наситени мазнини и може да повиши риска от сърдечни заболявания.",
        "en": "Palm oil contains saturated fats and may increase the risk of heart disease."
    },
    "E102": {
        "bg": "Тартразин - може да предизвика алергии и хиперактивност при деца.",
        "en": "Tartrazine - may cause allergies and hyperactivity in children."
    },
    "E250": {
        "bg": "Натриев нитрит - свързва се с риск от рак при прекомерна употреба.",
        "en": "Sodium nitrite - linked to cancer risk when consumed excessively."
    }
}

# Алтернативи на пакетирани храни
alternatives = {
    "чипс": "Домашно изпечени картофи",
    "газирани напитки": "Домашна лимонада",
    "шоколад": "Черен шоколад с високо съдържание на какао",
    "колбаси": "Прясно приготвено месо"
}

# Качване на снимка
uploaded_file = st.file_uploader(
    "Качете снимка на етикет / Upload food label image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)

    st.image(image, caption="Качено изображение", use_column_width=True)

    # Подобряване на изображението
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)

    image_np = np.array(image)

    st.write("Разпознаване на текст...")

    # EasyOCR Reader
    reader = easyocr.Reader(['bg', 'en'])

    results = reader.readtext(image_np, detail=0)

    extracted_text = " ".join(results)

    st.subheader("Разпознат текст:")
    st.write(extracted_text)

    found = False

    st.subheader("Открити вредни съставки:")

    for ingredient in harmful_ingredients:
        if ingredient.lower() in extracted_text.lower():
            found = True

            if language == "Български":
                st.error(f"Открито: {ingredient}")
                st.write(harmful_ingredients[ingredient]["bg"])
            else:
                st.error(f"Found: {ingredient}")
                st.write(harmful_ingredients[ingredient]["en"])

    if not found:
        if language == "Български":
            st.success("Не са открити вредни съставки.")
        else:
            st.success("No harmful ingredients found.")

    st.subheader("По-здравословни алтернативи:")

    for food, alt in alternatives.items():
        st.write(f"• {food} → {alt}")