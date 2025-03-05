# app.py
from flask import Flask, jsonify, request, send_from_directory
import pandas as pd
import random
import os

app = Flask(__name__, static_folder='static')

# Load the dataset
df = pd.read_csv('dataset.tsv', sep='\t')

def recommend_meal(meal_time):
    meals = df[df['MEAL_TIME'] == meal_time]
    recommended_meal = meals.sample(n=1)
    return recommended_meal.to_dict(orient='records')[0]

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    meal_time = request.args.get('meal_time')
    if meal_time not in ['Breakfast', 'Lunch', 'Dinner']:
        return jsonify({'error': 'Invalid meal time'}), 400
    meal = recommend_meal(meal_time)
    return jsonify(meal)

if __name__ == '__main__':
    app.run(debug=True)