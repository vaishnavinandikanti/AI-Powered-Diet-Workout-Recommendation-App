# 🥗 AI-Powered Diet & Workout Recommendation Web App

This is a Flask-based web application that generates personalized **diet, workout, and restaurant recommendations** based on user input. It uses the **Groq API with LLaMA 3 model** to generate intelligent and relevant suggestions tailored to users’ lifestyle and health data.

---

## 🚀 Features

- 🧝‍♂️ Personalized suggestions based on:
  - Age, gender, weight, height
  - Diet preferences & food types
  - Health conditions, allergies, and region
- 🥣 Recommendations include:
  - Breakfast & Dinner meals
  - Nearby restaurants
  - Custom workout plans
- ⚡ Powered by **Groq API (LLaMA 3)** for high-performance AI generation
- 💡 Clean and responsive UI using **Bootstrap 4**

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, Bootstrap
- **AI Model:** Groq API with LLaMA 3
- **Templating Engine:** Jinja2

---

## 📁 Project Structure

```
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
└── templates/
    ├── index.html          # Form for user input
    └── result.html         # Displays AI-generated recommendations
```

---

## ⚙️ Installation & Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your Groq API key:**
   ```bash
   export GROQ_API_KEY="your_api_key_here"  # On Windows use `set`
   ```

5. **Run the Flask server:**
   ```bash
   python app.py
   ```

6. **Open in browser:**
   Visit `http://127.0.0.1:5000` in your browser

---

## 📌 Example Prompt Sent to LLaMA 3

> Suggest 6 restaurant names, 6 breakfast names, 5 dinner names, and 6 workout names based on:  
> Age: 25, Gender: Male, Weight: 70, Height: 1.75, Dietary Preferences: Vegan, Disease: None, Region: Asia, Allergies: Nuts, Food Type: Low Carb

---



