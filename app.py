from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
import json
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

print("Starting Flask application...")

# Load feature mappings
try:
    with open('mappings.json', 'r') as f:
        raw_mappings = json.load(f)
        mappings = {
            'age': raw_mappings['age_map'],
            'gender': raw_mappings['gender_map'],
            'work_hours': raw_mappings['work_hours_map'],
            'screen_time': raw_mappings['screen_time_map'],
            'sleep_time': raw_mappings['sleep_time_map'],
            'exercise_freq': raw_mappings['exercise_freq_map'],
            'mood': raw_mappings['mood_map'],
            'fatigue': raw_mappings['fatigue_map'],
            'headache': raw_mappings['headache_map'],
            'work_life_balance': raw_mappings['work_life_balance_map'],
            'social_support': raw_mappings['social_support_map']
        }
        model_mappings = raw_mappings
    print("Successfully loaded mappings.json")
except Exception as e:
    print(f"Error loading mappings.json: {str(e)}")
    raise

def train_model():
    df = pd.read_csv('stress_dataset.csv')
    df.columns = df.columns.str.strip()
    
    print("="*50)
    print("TRAINING MODEL...")
    print("="*50)
    
    age_map = model_mappings['age_map']
    gender_map = model_mappings['gender_map']
    work_hours_map = model_mappings['work_hours_map']
    screen_time_map = model_mappings['screen_time_map']
    sleep_time_map = model_mappings['sleep_time_map']
    exercise_freq_map = model_mappings['exercise_freq_map']
    mood_map = model_mappings['mood_map']
    fatigue_map = model_mappings['fatigue_map']
    headache_map = model_mappings['headache_map']
    work_life_balance_map = model_mappings['work_life_balance_map']
    social_support_map = model_mappings['social_support_map']
    
    df['Age_Code'] = df['Age'].map(age_map)
    df['Gender_Code'] = df['Gender'].map(gender_map)
    df['Work_Hours_Code'] = df['Work hours'].map(work_hours_map)
    df['Screen_Time_Code'] = df['Screen time'].map(screen_time_map)
    df['Sleep_Time_Code'] = df['Sleep time'].map(sleep_time_map)
    df['Exercise_Freq_Code'] = df['Exercise frequency'].map(exercise_freq_map)
    df['Mood_Code'] = df['Mood Stability'].map(mood_map)
    df['Fatigue_Code'] = df['Fatigue level'].map(fatigue_map)
    df['Headache_Code'] = df['Headache'].map(headache_map)
    df['Work_Life_Balance_Code'] = df['Work_life Balance'].map(work_life_balance_map)
    df['Social_Support_Code'] = df['Social Support'].map(social_support_map)
    
    stress_score = (
        df['Fatigue_Code'] + 
        df['Mood_Code'] + 
        df['Headache_Code'] - 
        df['Work_Life_Balance_Code'] - 
        df['Social_Support_Code']
    )
    
    df['Stress_Level'] = pd.cut(stress_score, bins=3, labels=['Low', 'Medium', 'High'])
    df = df.dropna(subset=['Stress_Level'])
    df['Stress_Level_Code'] = df['Stress_Level'].map({'Low': 0, 'Medium': 1, 'High': 2})
    
    features = ['Age_Code', 'Gender_Code', 'Work_Hours_Code', 'Screen_Time_Code', 
               'Sleep_Time_Code', 'Exercise_Freq_Code', 'Mood_Code', 'Fatigue_Code',
               'Headache_Code', 'Work_Life_Balance_Code', 'Social_Support_Code']
    
    X = df[features]
    y = df['Stress_Level_Code']
    
    model = RandomForestClassifier(random_state=42, n_estimators=100)
    model.fit(X, y)
    
    print("MODEL TRAINING COMPLETE!")
    print("="*50)
    
    return model, features

try:
    model = joblib.load('stress_model.joblib')
    features = list(joblib.load('model_features.joblib'))
    print("Successfully loaded existing model")
except:
    print("Training new model...")
    model, features = train_model()
    joblib.dump(model, 'stress_model.joblib')
    joblib.dump(features, 'model_features.joblib')

def generate_recommendations(input_values, prediction):
    recommendations = []
    
    sleep_time = input_values.get('sleep_time', '')
    exercise_freq = input_values.get('exercise_freq', '')
    
    if prediction == 'Low':
        if sleep_time in ['7 - 8 hours', 'More than 8 hours'] and exercise_freq in ['3 - 4 times per week', '5+ times per week', 'Daily']:
            recommendations.append('Great job! Keep maintaining your current healthy lifestyle')
            recommendations.append('Continue your exercise routine and good sleep habits')
        else:
            recommendations.append('Keep maintaining your current healthy lifestyle')
            recommendations.append('Consider adding stress-relief activities like meditation or yoga')
    else:
        if sleep_time in ['Less than 4 hours', '4 - 6 hours']:
            recommendations.append('Prioritize getting 7-8 hours of sleep per night for optimal stress management')
        if exercise_freq in ['Never', '1 - 2 times per week']:
            recommendations.append('Increase physical activity to at least 3-4 times per week to reduce stress')
        
        if len(recommendations) < 2:
            recommendations.extend([
                'Practice stress-reduction techniques like deep breathing or progressive muscle relaxation',
                'Maintain a consistent daily routine with regular meal times'
            ])
    
    return recommendations[:2]

@app.route('/')
def home():
    return render_template('index.html', mappings=mappings)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json()

        # Create input dictionary with exact feature names used in the model
        input_dict = {
            'Age_Code': mappings['age'][data['age']],
            'Gender_Code': mappings['gender'][data['gender']],
            'Work_Hours_Code': mappings['work_hours'][data['work_hours']],
            'Screen_Time_Code': mappings['screen_time'][data['screen_time']],
            'Sleep_Time_Code': mappings['sleep_time'][data['sleep_time']],
            'Exercise_Freq_Code': mappings['exercise_freq'][data['exercise_freq']],
            'Mood_Code': mappings['mood'][data['mood']],
            'Fatigue_Code': mappings['fatigue'][data['fatigue']],
            'Headache_Code': mappings['headache'][data['headache']],
            'Work_Life_Balance_Code': mappings['work_life_balance'][data['work_life_balance']],
            'Social_Support_Code': mappings['social_support'][data['social_support']]
        }

        # Convert to DataFrame (single row)
        df = pd.DataFrame([input_dict])

        # Make prediction
        prediction_code = model.predict(df)[0]
        stress_map = {0: 'Low', 1: 'Medium', 2: 'High'}
        result = stress_map[prediction_code]

        # Feature importance
        feature_importance = dict(zip(features, model.feature_importances_))

        # Generate recommendations
        recommendations = generate_recommendations(data, result)

        # Build response
        response = {
            'prediction': result,
            'feature_importance': feature_importance,
            'recommendations': recommendations
        }

        return jsonify(response)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)