from flask import Flask, render_template, request
from groq import Groq
import os
import re

# Input your Groq API key securely
os.environ["GROQ_API_KEY"] = "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"

# Set up Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Initialize the Flask app
app = Flask(__name__)

# Route for the homepage (index.html)
@app.route('/')
def home():
    return render_template('index.html')

# Route for the result page (result.html)
@app.route('/result', methods=['POST'])
def result():
    input_data = {
        'age': int(request.form['age']),
        'gender': request.form['gender'],
        'weight': float(request.form['weight']),
        'height': float(request.form['height']),
        'dietary_preferences': request.form['dietary_preferences'],
        'disease': request.form['disease'],
        'region': request.form['region'],
        'allergics': request.form['allergics'],
        'foodtype': request.form['foodtype']
    }

    prompt = f"""
    Suggest 6 restaurant names, 6 breakfast names, 5 dinner names, and 6 workout names based on:
    Age: {input_data['age']}, Gender: {input_data['gender']}, Weight: {input_data['weight']},
    Height: {input_data['height']}, Dietary Preferences: {input_data['dietary_preferences']},
    Disease: {input_data['disease']}, Region: {input_data['region']}, Allergies: {input_data['allergics']},
    Food Type: {input_data['foodtype']}
    Format the response using these headers:
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
            max_tokens=1024
        )

        if not response.choices:
            return "Error: No recommendations found."

        results = response.choices[0].message.content

        restaurant_names = re.findall(r'Restaurants:(.*?)Breakfast:', results, re.DOTALL)
        breakfast_names = re.findall(r'Breakfast:(.*?)Dinner:', results, re.DOTALL)
        dinner_names = re.findall(r'Dinner:(.*?)Workouts:', results, re.DOTALL)
        workout_names = re.findall(r'Workouts:(.*?)$', results, re.DOTALL)

        def clean_response(data):
            return [line.strip('- ').strip() for line in data[0].strip().split('\n') if line.strip()] if data else []

        restaurant_names = clean_response(restaurant_names)
        breakfast_names = clean_response(breakfast_names)
        dinner_names = clean_response(dinner_names)
        workout_names = clean_response(workout_names)

        if not restaurant_names or not breakfast_names or not dinner_names or not workout_names:
            return "Error: Recommendations not generated."

        return render_template('result.html', 
                               restaurant_names=restaurant_names, 
                               breakfast_names=breakfast_names, 
                               dinner_names=dinner_names, 
                               workout_names=workout_names)

    except Exception as e:
        print(f"Error: {e}")
        return "Error: Something went wrong while generating recommendations."

if __name__ == "__main__":
    app.run(debug=True)
