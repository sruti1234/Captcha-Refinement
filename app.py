from flask import Flask, request, render_template
import h2o

app = Flask(__name__)

# Initialize the H2O model
h2o.init()
model = h2o.load_model(r"C:\Users\deepi\Desktop\captcha\DRF_1_AutoML_1_20240905_180337")

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the form data (username and password)
    username = request.form['username']
    password = request.form['password']
    
    # Get the user interaction metrics
    try:
        time_taken = float(request.form['time_taken'])
        typing_speed = float(request.form['typing_speed'])
        mouse_movement = int(request.form['mouse_movement'])
    except (ValueError, KeyError) as e:
        return "Error: Missing or invalid input metrics!"

    # Log the values for verification
    print(f"Username: {username}, Password: {password}")
    print(f"Time Taken: {time_taken}, Typing Speed: {typing_speed}, Mouse Movement: {mouse_movement}")

    # Prepare the input data for the model
    input_data = h2o.H2OFrame({
        'Time_Taken': [time_taken],
        'Typing_Speed': [typing_speed],
        'Mouse_Movement': [mouse_movement]
    })
    
    # Make the prediction using the model
    try:
        prediction = model.predict(input_data)
        pred_class = prediction['predict'][0, 0]  # Get the predicted class

        # Determine if it's a bot or human
        if pred_class == 1:
            result = "Access Denied. You are a bot!"
        else:
            result = "Access Granted. You are a human!"
    except Exception as e:
        result = f"Prediction failed: {str(e)}"

    # Render the result page with the prediction outcome
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
