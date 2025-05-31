from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Load models and vectorizers
sarcasm_model = joblib.load('models/sarcasm_model.pkl')
sarcasm_vectorizer = joblib.load('vectorizers/sarcasm_vectorizer.pkl')

cyber_model = joblib.load('models/cyberbullying_model.pkl')
cyber_vectorizer = joblib.load('vectorizers/cyberbullying_vectorizer.pkl')

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    input_text = None
    selected_task = None
    error_message = None

    if request.method == 'POST':
        input_text = request.form.get('comment')
        selected_task = request.form.get('task')

        if not input_text:
            error_message = "Please enter a comment."
        elif not selected_task:
            error_message = "Please select a task."
        else:
            if selected_task == 'sarcasm':
                vec = sarcasm_vectorizer.transform([input_text])
                result = sarcasm_model.predict(vec)[0]
                prediction = "Sarcastic" if result == 1 else "Not Sarcastic"
            elif selected_task == 'cyber':
                vec = cyber_vectorizer.transform([input_text])
                result = cyber_model.predict(vec)[0]
                prediction = f"Cyberbullying Intent: {result}"
            else:
                error_message = "Invalid task."

    return render_template('index.html', prediction=prediction, input_text=input_text,
                           error=error_message, selected_task=selected_task)

if __name__ == '__main__':
    app.run(debug=True)
