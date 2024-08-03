from flask import Flask, request, render_template, url_for, redirect, session, jsonify
from src.main import flight_time  # Adjust import according to your project structure
import os
import numpy as np
import sympy as s
import json
app = Flask(__name__)
app.secret_key = 'f435gg364h45h5h5df'
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
        graph_data = flight_time_instance.ReturnData()
        battery_weight = flight_time_instance.BatteryWeight()
        battery_voltage = flight_time_instance.BatteryVoltage()
        battery_capacity = flight_time_instance.BatteryCapacity()
        battery_energy = flight_time_instance.BatteryEnergy()
        prop_name = flight_time_instance.MotorPropellar()
        prop_mass = flight_time_instance.MotorPropellarMass()
        max_thrust = flight_time_instance.MotorMaxThrust()
        battery_cell_count = flight_time_instance.MotorPropellarBatteryCellCount()
        drone_total_weight = flight_time_instance.DroneWeight() + float(drone_weight)


        session["optimal_batteries"] = float(optimal_batteries)
        session["time_of_flight"] = float(time_of_flight)
        session["graph_data"] = graph_data
        session["battery_weight"] = float(battery_weight)
        session["battery_voltage"] = float(battery_voltage)
        session["battery_capacity"] = float(battery_capacity)
        session["battery_energy"] = float(battery_energy)
        session["prop_name"] = str(prop_name)
        session["prop_mass"] = float(prop_mass)
        session["max_thrust"] = float(max_thrust)
        session["battery_cell_count"] =  float(battery_cell_count)
        session["drone_total_weight"] =  float(drone_total_weight)
        
        # Pass the results to the template
        return render_template('results.html', optimal_batteries=optimal_batteries, time_of_flight=time_of_flight, graph_data = json.dumps(graph_data), battery_weight = battery_weight, 
                               battery_voltage = battery_voltage, battery_capacity = battery_capacity, battery_energy = battery_energy, prop_name = prop_name, prop_mass = prop_mass, 
                               max_thrust = max_thrust, battery_cell_count = battery_cell_count, drone_total_weight =  drone_total_weight)
    else:
        return render_template('index.html')
@app.route('/')
def Home():
    return render_template('index.html')
@app.route('/About')
def About():
    return render_template('About.html')
@app.route('/Contact')
def Contact():
    return render_template('Contact.html')


if __name__ == '__main__':
    app.run(debug=False)

    
