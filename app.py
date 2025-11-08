import streamlit as st
from groq import Groq
import re

# Page setup
st.set_page_config(page_title="AI Fitness & Diet Coach 🥗", page_icon="💪", layout="wide")

st.title("🥗 AI Fitness & Diet Coach")
st.markdown("### Your personalized health assistant powered by Groq LLaMA 3")

st.write("👋 Tell me your fitness goal — or pick one of the example goals below to get started!")

# Example fitness goal prompts
example_goals = [
    "I want to gain lean muscle.",
    "I want to lose fat and tone my body.",
    "I want to maintain a balanced and healthy lifestyle.",
    "I want to improve my stamina and strength.",
    "I want to manage stress and eat healthier meals.",
]

# Sidebar for structured inputs
with st.sidebar:
    st.header("🧾 Your Information")
    age = st.number_input("Age", min_value=10, max_value=100, value=25)
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, step=0.01, value=1.70)
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, step=0.1, value=70.0)
    diet = st.selectbox("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    city = st.selectbox(
        "City", [
            "Hyderabad", "Bengaluru", "Chennai", "Delhi",
            "Mumbai", "Pune", "Kolkata", "Ahmedabad"
        ]
    )
    area = st.text_input("Enter your locality or area (e.g., Miyapur, Indiranagar, T. Nagar)")

# Main goal selection section
st.subheader("🎯 Choose Your Goal")
selected_goal = st.radio("Select from examples:", example_goals, index=None)
custom_goal = st.text_area("Or write your own goal:", placeholder="e.g., I want a high-protein vegetarian diet with home workouts.")

final_goal = selected_goal if selected_goal else custom_goal

if st.button("Generate My Personalized Plan 🚀"):
    if not final_goal:
        st.warning("Please select or enter a goal first!")
    else:
        st.info("Generating your personalized recommendations... please wait ⏳")

        # Calculate BMI
        bmi = weight / (height ** 2)
        if bmi < 18.5:
            bmi_status = "underweight"
        elif bmi < 24.9:
            bmi_status = "normal"
        elif bmi < 29.9:
            bmi_status = "overweight"
        else:
            bmi_status = "obese"

        # Prepare the Groq client
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        # Construct the AI prompt
        prompt = f"""
        You are a certified nutritionist and fitness coach. Based on the following information, generate:
        - 5 healthy restaurant recommendations within 5 km radius of the user's area (assume India).
        - 6 personalized breakfast ideas.
        - 5 personalized dinner ideas.
        - 6 workouts based on the user's goal, BMI, and health condition.

        User Goal: {final_goal}
        Age: {age}, Gender: {gender}, Height: {height}m, Weight: {weight}kg, BMI: {bmi:.1f} ({bmi_status})
        Dietary Preference: {diet}
        Region: {city} — {area}

        Format the response as:
        Restaurants:
        Breakfast:
        Dinner:
        Workouts:
        """

        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=1000
            )

            text = response.choices[0].message.content

            # Helper function to extract sections
            def extract(section):
                pattern = rf"{section}:(.*?)(?=\n[A-Z]|$)"
                match = re.search(pattern, text, re.DOTALL)
                return [i.strip('- ').strip() for i in match.group(1).split('\n') if i.strip()] if match else []

            restaurants = extract("Restaurants")
            breakfasts = extract("Breakfast")
            dinners = extract("Dinner")
            workouts = extract("Workouts")

            st.success("✅ Personalized plan generated!")

            if restaurants:
                st.subheader("🍽️ Recommended Restaurants (within 5 km)")
                for r in restaurants:
                    st.write(f"- {r}")

            if breakfasts:
                st.subheader("🥣 Breakfast Suggestions")
                for b in breakfasts:
                    st.write(f"- {b}")

            if dinners:
                st.subheader("🌙 Dinner Suggestions")
                for d in dinners:
                    st.write(f"- {d}")

            if workouts:
                st.subheader("🏋️ Workout Plan")
                for w in workouts:
                    st.write(f"- {w}")

        except Exception as e:
            st.error(f"An error occurred: {e}")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit and Groq LLaMA 3.")
