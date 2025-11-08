# ============================================================
# AI-Powered Diet and Workout Recommendation App
# Clean, Secure Streamlit Version
# ============================================================

import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import re

# ============================================================
# 🔐 Load Environment Variables
# ============================================================
# This works both locally (using .env) and on Streamlit Cloud (Secrets)
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Handle missing key clearly
if not api_key:
    st.error("⚠️ Missing GROQ_API_KEY — please set it in Streamlit Secrets or a local .env file.")
    st.stop()

# Initialize Groq client
try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error initializing Groq client: {e}")
    st.stop()

# ============================================================
# 🎨 Streamlit App Configuration
# ============================================================
st.set_page_config(page_title="AI Diet & Workout Recommender", page_icon="💪", layout="centered")

st.title("💪 AI-Powered Diet and Workout Recommendation App")
st.write("Get personalized restaurant, meal, and workout recommendations based on your fitness goals.")

st.divider()

# ============================================================
# 🧠 Example Prompts Section
# ============================================================
st.subheader("📝 Example Prompts")

example_prompts = [
    "I want to build lean muscle with a high-protein diet.",
    "I want to lose fat with an Indian vegetarian meal plan.",
    "I want to gain healthy weight with a balanced diet.",
    "I want to maintain my fitness with light workouts.",
    "I have diabetes and want a low-sugar meal plan."
]

st.write("Here are some example prompts you can use 👇")
for prompt in example_prompts:
    st.markdown(f"- {prompt}")

st.divider()

# ============================================================
# 🧍 User Input Section
# ============================================================
st.subheader("⚙️ Customize Your Plan")

goal = st.text_area("💭 Describe your fitness goal:", placeholder="E.g., I want to get lean and improve stamina.")
city = st.text_input("📍 Enter your city:", placeholder="E.g., Hyderabad")
area = st.text_input("🏠 Enter your area/locality:", placeholder="E.g., Himayat Nagar")

age = st.number_input("🎂 Age", min_value=10, max_value=100, value=25)
gender = st.selectbox("🚻 Gender", ["Male", "Female", "Other"])
weight = st.number_input("⚖️ Weight (in kg)", min_value=30.0, max_value=200.0, value=65.0)
height = st.number_input("📏 Height (in meters)", min_value=1.2, max_value=2.2, value=1.7)
diet_pref = st.selectbox("🥗 Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
disease = st.text_input("🩺 Any health conditions (optional)", placeholder="E.g., PCOS, Diabetes, None")
allergies = st.text_input("🚫 Any food allergies (optional)", placeholder="E.g., Peanuts, Gluten, None")

st.divider()

# ============================================================
# ⚡ Generate Recommendations
# ============================================================
if st.button("🚀 Generate My Personalized Plan"):
    if not goal or not city or not area:
        st.warning("Please fill in your goal, city, and area before generating recommendations.")
        st.stop()

    st.info("⏳ Generating your personalized recommendations... please wait.")

    # BMI calculation (for personalized context)
    bmi = weight / (height ** 2)
    if bmi < 18.5:
        bmi_status = "underweight"
    elif bmi < 24.9:
        bmi_status = "normal"
    elif bmi < 29.9:
        bmi_status = "overweight"
    else:
        bmi_status = "obese"

    # Prepare prompt
    prompt = f"""
    Based on the following details:
    - Goal: {goal}
    - Age: {age}
    - Gender: {gender}
    - Weight: {weight} kg
    - Height: {height} m
    - BMI Status: {bmi_status}
    - Dietary Preference: {diet_pref}
    - Health Conditions: {disease}
    - Allergies: {allergies}
    - Location: {city}, {area}

    Suggest:
    1. 6 restaurant names (within 5 km of {area}, {city})
    2. 6 breakfast ideas suitable for the user's goal
    3. 5 dinner meal ideas
    4. 6 workouts suitable for the user's body type and goal

    Use these headers in your response:
    Restaurants:
    Breakfast:
    Dinner:
    Workouts:
    """

    # Call Groq API
    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=1024
        )

        result_text = response.choices[0].message.content

        # Extract content by section
        def extract_section(header1, header2, text):
            pattern = rf"{header1}:(.*?){header2}:"
            section = re.search(pattern, text, re.DOTALL)
            return section.group(1).strip() if section else ""

        def clean_list(section):
            return [item.strip("-• ").strip() for item in section.split("\n") if item.strip()]

        restaurants = clean_list(extract_section("Restaurants", "Breakfast", result_text))
        breakfast = clean_list(extract_section("Breakfast", "Dinner", result_text))
        dinner = clean_list(extract_section("Dinner", "Workouts", result_text))
        workouts = clean_list(result_text.split("Workouts:")[-1])

        # Display results
        st.success("✅ Recommendations Generated Successfully!")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🍽️ Restaurants")
            st.write("\n".join([f"- {r}" for r in restaurants]))

            st.subheader("🌅 Breakfast Ideas")
            st.write("\n".join([f"- {b}" for b in breakfast]))

        with col2:
            st.subheader("🌙 Dinner Ideas")
            st.write("\n".join([f"- {d}" for d in dinner]))

            st.subheader("🏋️ Workouts")
            st.write("\n".join([f"- {w}" for w in workouts]))

    except Exception as e:
        st.error(f"❌ Error generating recommendations: {e}")

# ============================================================
# End of App
# ============================================================
