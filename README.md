# AI-Powered Diet & Workout Recommendation App

An intelligent Streamlit web app that generates personalized meal plans, restaurant suggestions, and workout routines using the Groq API (Llama 3 models).

This application combines AI reasoning with user data (age, weight, goals, diet type, and location) to create practical, localized fitness and nutrition recommendations.

---

## Features

- Personalized recommendations based on:
  - Age, gender, height, and weight
  - Dietary preferences (Vegetarian / Non-Vegetarian / Vegan)
  - Allergies and medical conditions
  - Fitness goals (e.g., lean muscle, fat loss, maintenance)
  - Location (city and area for local restaurants)

- Interactive user interface:
  - Example prompts for quick start
  - Manual text prompt support
  - Raw model output expander for debugging
  - Clean Streamlit layout with form-based input

- Secure API key management:
  - `.env` for local development
  - Streamlit Secrets for production deployments

---

## File Structure
AI-Powered-Diet-Workout-Recommendation-App/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Project dependencies
├── .gitignore              # Ignores .env and temporary files
├── .env (local only)       # Stores GROQ_API_KEY (not pushed)
└── README.md               # Documentation

---

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/AI-Powered-Diet-Workout-Recommendation-App.git
cd AI-Powered-Diet-Workout-Recommendation-App
```

### 2. Install dependencies
pip install -r requirements.txt

### 3. Add your Groq API key
Create a .env file in the root folder and add:
GROQ_API_KEY=gsk_your_api_key_here
Note: .env is already listed in .gitignore, so it will not be pushed to GitHub.

### 4. Run the Streamlit app
streamlit run app.py

The app will start locally at:
http://localhost:8501
---
Deployment on Streamlit Cloud
1. Push your latest code to GitHub.

2. Go to https://share.streamlit.io and create a new app.

3. Choose your repository and set the main file to app.py.

4. Add your Groq API key in Settings → Secrets:

GROQ_API_KEY = "gsk_your_api_key_here"
Click Deploy.

5. After deployment, your app will be available at:

https://<your-username>-ai-powered-diet-workout-recommendation-app.streamlit.app
---
Example Prompts
Try entering:

- I want to build lean muscle with a high-protein diet.

- I want to lose fat and tone up with vegetarian meals.

- I want low-carb meals and short daily workouts.

- I want diabetic-friendly Indian meal options.

- I want a high-protein bulking plan with nearby restaurants.
  
---

Requirements

streamlit==1.39.0
groq==0.22.0
python-dotenv==1.0.1
requests==2.32.3

---

Future Enhancements
- Add calorie and macronutrient analysis

- Integrate Google Maps API for real restaurant locations

- Include a downloadable PDF plan

- Improve mobile responsiveness

---
Tech Stack
- Python

- Streamlit

- Groq API (Llama 3 models)

- dotenv

- Requests
---
Author
Vaishnavi Nandikanti
GitHub: https://github.com/vaishnavinandikanti








