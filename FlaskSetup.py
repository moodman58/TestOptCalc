from flask import Flask, request, render_template, url_for, redirect, session, jsonify
from src.main import flight_time  # Adjust import according to your project structure
import os
app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        motor_file = request.form['motor_file']
        battery_file = request.form['battery_file']
        drone_weight = request.form['drone_weight']
        desired_velocity = request.form['desired_velocity']
        desired_altitude = request.form['desired_altitude']

        # Create an instance of flight_time and call optimization
        flight_time_instance = flight_time(motor_file, battery_file, drone_weight, desired_velocity, desired_altitude)
        optimal_batteries = flight_time_instance.optimization()
        time_of_flight = flight_time_instance.hover_phase(flight_time_instance.optimization())

        session["optimal_batteries"] = float(optimal_batteries)
        session["time_of_flight"] = float(time_of_flight)
        # Pass the results to the template
        return render_template('results.html', optimal_batteries=optimal_batteries, time_of_flight=time_of_flight)
    else:
        return render_template('index.html')


if __name__ == '__main__':
      if 'SECRET_KEY' in os.environ:
        app.config['SECRET_KEY'] = os.urandom(12)
      else:
        # Set a default secret key if the environment variable is not set
        app.config['SECRET_KEY'] = 'your_default_secret_key_here'
    app.run(debug=False)

    
