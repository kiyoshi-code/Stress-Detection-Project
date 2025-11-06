document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Get form values
    const data = {
        age: document.getElementById('age').value,
        gender: document.getElementById('gender').value,
        work_hours: document.getElementById('work_hours').value,
        screen_time: document.getElementById('screen_time').value,
        sleep_time: document.getElementById('sleep_time').value,
        exercise_freq: document.getElementById('exercise_freq').value,
        mood: document.getElementById('mood').value,
        fatigue: document.getElementById('fatigue').value,
        headache: document.getElementById('headache').value,
        work_life_balance: document.getElementById('work_life_balance').value,
        social_support: document.getElementById('social_support').value
    };

    try {
        // Send prediction request
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            // Show result section
            document.getElementById('result').style.display = 'block';

            // Display prediction with color coding
            const predictionDiv = document.getElementById('predictionResult');
            predictionDiv.innerHTML = `<h2 class="prediction-${result.prediction.toLowerCase()}">
                Predicted Stress Level: ${result.prediction}
            </h2>`;

            // Create feature importance chart
            const featureImportanceDiv = document.getElementById('featureImportance');
            const profileImpactDiv = document.getElementById('profileImpact');
            
            // Remove existing charts if they exist
            if (window.featureChart) {
                window.featureChart.destroy();
            }
            if (window.profileChart) {
                window.profileChart.destroy();
            }

            // Feature Importance Chart
            const ctxFeature = document.createElement('canvas');
            featureImportanceDiv.innerHTML = '';
            featureImportanceDiv.appendChild(ctxFeature);

            const features = Object.keys(result.feature_importance);
            const importance = Object.values(result.feature_importance);

            window.featureChart = new Chart(ctxFeature, {
                type: 'bar',
                data: {
                    labels: features.map(f => f.replace('_Code', '').replace('_', ' ')),
                    datasets: [{
                        label: 'Feature Importance',
                        data: importance,
                        backgroundColor: 'rgba(54, 162, 235, 0.6)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'General Feature Importance'
                        }
                    }
                }
            });

            // Profile Impact Chart
            const ctxProfile = document.createElement('canvas');
            profileImpactDiv.innerHTML = '';
            profileImpactDiv.appendChild(ctxProfile);

            const profileFeatures = Object.keys(result.importance_by_value);
            const profileImpact = Object.values(result.importance_by_value);

            window.profileChart = new Chart(ctxProfile, {
                type: 'bar',
                data: {
                    labels: profileFeatures.map(f => f.replace('_', ' ')),
                    datasets: [{
                        label: 'Impact on Your Stress',
                        data: profileImpact,
                        backgroundColor: 'rgba(255, 99, 132, 0.6)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Your Profile Impact'
                        }
                    }
                }
            });

            // Generate recommendations
            const recommendationsDiv = document.getElementById('recommendations');
            let recommendations = [];

            // Sort features by impact
            const sortedImpacts = Object.entries(result.importance_by_value)
                .sort((a, b) => b[1] - a[1]);

            // Generate recommendations based on top contributing factors
            for (const [feature, impact] of sortedImpacts.slice(0, 3)) {
                const value = result.input_values[feature];
                switch (feature) {
                    case 'sleep_time':
                        if (value === 'Less than 4 hours' || value === '4 - 6 hours') {
                            recommendations.push('Try to get more sleep (aim for 7-8 hours per night)');
                        }
                        break;
                    case 'work_hours':
                        if (value === 'More than 10 hours' || value === '9 - 10 hours') {
                            recommendations.push('Consider reducing work hours or taking regular breaks');
                        }
                        break;
                    case 'exercise_freq':
                        if (value === 'Never' || value === '1 - 2 times per week') {
                            recommendations.push('Increase physical activity (aim for at least 3-4 times per week)');
                        }
                        break;
                    case 'screen_time':
                        if (value === 'More than 6 hours' || value === '4 - 6 hours') {
                            recommendations.push('Take regular breaks from screen time and practice the 20-20-20 rule');
                        }
                        break;
                    case 'work_life_balance':
                        if (value === 'Not Balanced' || value === 'Somewhat Balanced') {
                            recommendations.push('Work on improving work-life balance through better time management');
                        }
                        break;
                    case 'social_support':
                        if (value === 'None' || value === 'Weak') {
                            recommendations.push('Build stronger social connections and seek support when needed');
                        }
                        break;
                }
            }

            // Add general recommendations if needed
            if (recommendations.length < 3) {
                recommendations.push(
                    'Practice stress management techniques like meditation or deep breathing',
                    'Maintain a regular sleep schedule',
                    'Take regular breaks during work hours'
                );
            }

            // Display recommendations
            recommendationsDiv.innerHTML = recommendations
                .slice(0, 5)
                .map(rec => `<p class="mb-2">• ${rec}</p>`)
                .join('');

        } else {
            throw new Error(result.error || 'Prediction failed');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});