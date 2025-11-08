# app.py
# AI-Powered Diet & Workout Recommender (Streamlit)
# - Safe env handling (dotenv optional)
# - Groq model call with fallback
# - Robust parsing + debug output
# - No hard-coded API keys

import os
import re
import json
import streamlit as st

# Try to load dotenv for local development (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv is optional; continue if not installed
    pass

# Try importing Groq and show a helpful message if it's missing
try:
    from groq import Groq
except Exception as e:
    st.error(f"Missing or failing import: groq library not available. Install dependencies (`pip install -r requirements.txt`).\nDetails: {e}")
    st.stop()

# ------------------------
# Configuration & page UI
# ------------------------
st.set_page_config(page_title="AI Diet & Workout Recommender", page_icon="💪", layout="wide")
st.title("💪 AI-Powered Diet & Workout Recommender")
st.write("Personalized restaurants, meals, and workouts — tell the assistant your goal and location.")

st.markdown("---")

# Example prompts
st.subheader("Example prompts (choose or write your own)")
example_prompts = [
    "I want to build lean muscle with a high-protein diet.",
    "I want to lose fat and tone up with vegetarian meals.",
    "I want to maintain my weight with weekly home workouts.",
    "I want low-carb, diabetes-friendly meals and light cardio.",
    "I want short 30-minute daily workouts and easy-to-find meals."
]
cols = st.columns(2)
for i, p in enumerate(example_prompts):
    with cols[i % 2]:
        st.write(f"- {p}")

st.markdown("---")

# ------------------------
# User inputs (sidebar)
# ------------------------
with st.sidebar:
    st.header("Your profile")
    age = st.number_input("Age", min_value=10, max_value=100, value=25)
    gender = st.selectbox("Gender", ["Female", "Male", "Other"])
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=65.0, step=0.1)
    height = st.number_input("Height (m)", min_value=1.2, max_value=2.2, value=1.7, step=0.01)
    diet_pref = st.selectbox("Dietary preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    allergies = st.text_input("Allergies (optional)", placeholder="e.g., Peanuts, Gluten, None")
    disease = st.text_input("Health conditions (optional)", placeholder="e.g., Diabetes, None")
    st.markdown("---")
    st.caption("Note: Keep sensitive info minimal. Use the main form for goal & location.")

# ------------------------
# Main form
# ------------------------
st.subheader("Tell your AI Coach")
goal_col1, goal_col2 = st.columns([3, 1])
with goal_col1:
    chosen_example = st.selectbox("Select an example prompt (optional)", [""] + example_prompts)
    custom_goal = st.text_area("Or describe your goal (required)", placeholder="E.g., I want to gain lean muscle with vegetarian meals.")
with goal_col2:
    st.write("Location (for local restaurant suggestions)")
    city = st.selectbox("City (for context)", ["", "Hyderabad", "Bengaluru", "Chennai", "Delhi", "Mumbai", "Pune", "Kolkata", "Ahmedabad"])
    area = st.text_input("Area/locality (type your exact area)", placeholder="e.g., Miyapur, Indiranagar, T. Nagar")

final_goal = custom_goal.strip() if custom_goal.strip() else (chosen_example if chosen_example else "")

st.markdown("---")

# ------------------------
# Environment & Groq client setup
# ------------------------
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.warning(
        "GROQ_API_KEY not found. For local testing, create a `.env` with `GROQ_API_KEY=gsk_xxx`. "
        "On Streamlit Cloud, add a secret: `GROQ_API_KEY = \"gsk_xxx\"`."
    )

# delayed client creation — only create when needed (after button click) to avoid errors on page load

# ------------------------
# Helper functions
# ------------------------
def calculate_bmi(w, h):
    try:
        bmi = w / (h ** 2)
        return round(bmi, 1)
    except Exception:
        return None

def clean_list_block(text):
    """Convert a block of text into list items using heuristics."""
    if not text:
        return []
    items = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # remove common bullets/numbers
        line = re.sub(r'^[\-\*\u2022\s\d\.\)\:]+', '', line).strip()
        if line:
            items.append(line)
    # If single-line comma-separated, split by comma
    if len(items) == 1 and ',' in items[0]:
        return [x.strip() for x in items[0].split(',') if x.strip()]
    return items

def parse_by_headers(text):
    """Try to extract Restaurants / Breakfast / Dinner / Workouts sections (case-insensitive)."""
    out = {"restaurants": "", "breakfast": "", "dinner": "", "workouts": ""}
    if not text:
        return out
    lower = text.lower()
    # find header positions
    headers = ["restaurants", "breakfast", "dinner", "workouts"]
    positions = {}
    for h in headers:
        idx = lower.find(h + ":")
        positions[h] = idx

    found = [h for h in headers if positions[h] != -1]
    if not found:
        return out

    # sort found headers
    sorted_found = sorted(found, key=lambda x: positions[x])
    for i, h in enumerate(sorted_found):
        start = positions[h] + len(h) + 1
        end = None
        if i + 1 < len(sorted_found):
            end = positions[sorted_found[i + 1]]
        out[h] = text[start:end].strip() if end else text[start:].strip()
    return out

def show_list(title, items):
    if not items:
        st.write(f"No items found for **{title}**.")
        return
    st.markdown(f"**{title}**")
    for it in items:
        st.write(f"- {it}")

# ------------------------
# Model call & parsing logic
# ------------------------
preferred_models = [
    # safe options — pick ones known to be supported; update if Groq deprecates
    "llama-3.3-70b-versatile",
    "llama-3.3-8b-instant",
    "llama-3.2-70b"
]

# Button triggers the AI call
if st.button("🚀 Generate My Personalized Plan"):
    if not final_goal:
        st.warning("Please provide a goal (either select an example or type your goal).")
        st.stop()
    if not city or not area:
        st.warning("Please provide both City and Area/locality to get localized restaurant suggestions.")
        st.stop()
    if not api_key:
        st.error("GROQ_API_KEY is not set. Add it to a .env file (local) or Streamlit Secrets (cloud).")
        st.stop()

    st.info("Generating personalized recommendations — this may take a few seconds...")

    # compute BMI
    bmi = calculate_bmi(weight, height)
    bmi_status = "unknown"
    if bmi is not None:
        if bmi < 18.5:
            bmi_status = "underweight"
        elif bmi < 25:
            bmi_status = "normal"
        elif bmi < 30:
            bmi_status = "overweight"
        else:
            bmi_status = "obese"

    # build prompt for the model
    prompt = f"""
You are a certified nutrition and fitness coach. Based on the details below, produce:
- 6 restaurant names (within ~5 km of {area}, {city}) suitable for the user's dietary preference,
- 6 breakfast ideas tailored to the goal,
- 5 dinner ideas,
- 6 workout suggestions tailored to the user's BMI and goal.

User details:
Goal: {final_goal}
Age: {age}
Gender: {gender}
Weight (kg): {weight}
Height (m): {height}
BMI: {bmi} ({bmi_status})
Dietary preference: {diet_pref}
Allergies: {allergies}
Health conditions: {disease}
Location: {city}, {area}

Return the response using clear headers exactly like:
Restaurants:
Breakfast:
Dinner:
Workouts:
Use bullet points or numbered lists under each header.
"""

    # create Groq client
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize Groq client: {e}")
        st.stop()

    # attempt model calls with fallback
    response_obj = None
    last_exception = None
    with st.spinner("Contacting model..."):
        for model_name in preferred_models:
            try:
                response_obj = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.6,
                    max_tokens=1200
                )
                # success
                break
            except Exception as e:
                last_exception = e
                # try next model
                continue

    if response_obj is None:
        st.error(f"All model attempts failed. Last error: {last_exception}")
        st.stop()

    # extract text from response (defensive)
    result_text = ""
    try:
        # common response shapes:
        # response.choices[0].message.content
        choices = getattr(response_obj, "choices", None)
        if choices and len(choices) > 0:
            choice0 = choices[0]
            # SDK may expose message.content or text
            msg = getattr(choice0, "message", None)
            if msg and hasattr(msg, "content"):
                result_text = msg.content
            elif hasattr(choice0, "text"):
                result_text = choice0.text
            else:
                result_text = str(choice0)
        else:
            # fallback: stringify the response object
            result_text = str(response_obj)
    except Exception:
        result_text = str(response_obj)

    # Show raw output inside an expander for debugging
    with st.expander("🔎 Raw model output (expand to inspect)"):
        # limit size to avoid huge dumps, but show plenty
        try:
            safe_preview = result_text if len(result_text) < 20000 else result_text[:20000] + "\n\n... (truncated)"
            st.code(safe_preview)
        except Exception as e:
            st.write("Unable to preview raw output:", e)

    # First, try header-based parsing
    sections = parse_by_headers(result_text)
    restaurants_block = sections.get("restaurants", "")
    breakfast_block = sections.get("breakfast", "")
    dinner_block = sections.get("dinner", "")
    workouts_block = sections.get("workouts", "")

    # Convert to lists
    restaurants = clean_list_block(restaurants_block)
    breakfasts = clean_list_block(breakfast_block)
    dinners = clean_list_block(dinner_block)
    workouts = clean_list_block(workouts_block)

    # Fallback heuristics if header parsing yielded nothing
    if not any([restaurants, breakfasts, dinners, workouts]):
        st.info("Header parsing returned no content — trying fallback heuristics.")
        # Split by blank lines and try to assign
        chunks = [c.strip() for c in re.split(r"\n\s*\n", result_text) if c.strip()]
        if len(chunks) >= 4:
            restaurants = clean_list_block(chunks[0])
            breakfasts = clean_list_block(chunks[1])
            dinners = clean_list_block(chunks[2])
            workouts = clean_list_block("\n".join(chunks[3:]))
        elif len(chunks) > 0:
            # best-effort slicing
            n = max(1, len(chunks) // 4)
            restaurants = clean_list_block("\n".join(chunks[0:n]))
            breakfasts = clean_list_block("\n".join(chunks[n:2*n]))
            dinners = clean_list_block("\n".join(chunks[2*n:3*n]))
            workouts = clean_list_block("\n".join(chunks[3*n:]))

    # Display the parsed results in two columns
    st.markdown("### ✅ Personalized Recommendations")
    left, right = st.columns(2)
    with left:
        show_list("🍽️ Restaurants (within ~5 km)", restaurants)
        st.markdown("---")
        show_list("🥣 Breakfast Ideas", breakfasts)
    with right:
        show_list("🌙 Dinner Ideas", dinners)
        st.markdown("---")
        show_list("🏋️ Workouts", workouts)

    # If everything is empty, show helpful message
    if not any([restaurants, breakfasts, dinners, workouts]):
        st.error("No recommendations could be parsed from the model output. Please check the Raw model output (expand above) and consider editing the prompt to request a clearer headered response.")

st.markdown("---")
st.caption("Built with ❤️ — keep your API key secure (use .env locally or Streamlit Secrets).")