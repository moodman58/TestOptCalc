import Propulsion
import batteries
from Propulsion import PowerSystem
from batteries import Batteries
import matplotlib.pyplot as plt
import sympy as s


class flight_time:
    """This class extracts data from a motor text file and a battery text file and outputs the optimal number of batteries needed to maximize the time of flight for the drone
    """    
    def __init__(self):
        # Create instances of Both classes and run the Propulsion.py and batteries.py files
        self.power_system = PowerSystem(Propulsion.new_file)
        self.battery_system = Batteries(batteries.file_name)
        self.battery_system.get_file_values() #
        # Get access to both classes dictionaries of information 
        self.data_collected_Powersystem = self.power_system.data_collected
        self.data_collected_Battery = self.battery_system.data_collected

        self.battery_number = None #hover_phase function gives error if we dont have a battery_number
        

        #User enters velocity(m/s), weight(g) and desired altitude(m) of drone
        self.desired_velocity = input("Enter drone velocity(m/s): ")  # v
        self.desired_altitude = input("Enter drone desired altitude(m): ")  # d
        self.drone_weight = float(input("Enter drone weight (grams): "))
        #Retrieve battery mass
        self.battery_mass = float(
            self.battery_system.data_collected["MASS OF BATTERY"]
        )
        """below variables are for hover_thrust function, uncomment and change them if you want to use it.
        """
        self.battery_number = None #hover_phase function gives error if we dont have a battery_number        
        #self.battery_number = input("Number of batteries: ") #This is used if we want the user to enter a battery number for the hover_phase function
        #Battery weight, if we want to use this, 1 should be replaced with battery number
        #self.battery_weight = self.battery_mass * float(1) 
        #self.hover_thrust = (
            #float(self.drone_weight) + float(self.battery_weight)) / 4
        

        self.motor_number = 4  # M in equation
        #Get the InputPower,Thrust coeffecients
        self.power_system.thrust_power()
        self.power_system.get_coefficients()
        

    def vertical_takeoff(self):
        """Calculates and returns time to reach desired altitude"""

             
        takeoff_time = float(self.desired_altitude) / float(
            self.desired_velocity
        )
        return takeoff_time

    def hover_phase(self):
        """Calculates Hover Time of Flight with ideally a user provided number of batteries
        """        
        discriminant = (self.power_system.data_collected["B"]) ** 2 - 4 * (
            self.power_system.data_collected["A"]
            * (self.power_system.data_collected["C"] - self.hover_thrust)
        )
        power = (
            (
                (-1 * self.power_system.data_collected["B"])
                + ((discriminant) ** 0.5)
            )
        ) / (2 * self.power_system.data_collected["A"])

        time_cruise = 3.6 * (
            (
                (
                    (
                        float(
                            self.battery_system.data_collected[
                                "mAh OF BATTERY"
                            ]
                        )
                        * float(
                            self.battery_system.data_collected[
                                "BATTERY VOLTAGE"
                            ]
                        )
                    )
                    * float(self.battery_number)
                )
                / (power * float(self.motor_number))
            )
            - (
                (
                    2.0
                    * (
                        float(self.desired_altitude)
                        / float(self.desired_velocity)
                    )
                )
                / float(self.motor_number)
            )
        )
        return time_cruise

    def vertical_landing(self):
        """Calculates and returns time to reach ground from desired altitude
        """        
        landing_time = float(self.desired_altitude) / float(
            self.desired_velocity
        )
        return landing_time

    

    def check_cruise_thrust(self):
        """Checks if the hover thrust required for the user inputted number of 
        batteries is within bounds. Used with hover_phase() function, so 
        uncomment hover_thrust variable if you need to use.
        """        
        if float(self.hover_thrust) > float(
            self.power_system.data_collected["MAX THRUST"]
        ):
            return False
        else:
            return True

    def battery_number_finder(self):
        """Calculates and returns highest number of batteries possible so max motor thrust is not exceeded
        """        
        for i in range(1, 100): #Assumes always under 100 batteries will be needed 
            hover_thrust = (float(self.drone_weight) + float(self.battery_mass * i)) / 4 
            if hover_thrust > float(
                self.power_system.data_collected["MAX THRUST"]
            ):
                max_battery_number = int(i) - 1
                print("Max battery number is: " + str(int(i) - 1))
                return max_battery_number

    def optimization(self):
        """Uses Time of Flight equation to optimize number of batteries for highest Time of Flight.
        Uses derivative calculator and solver.
        """      
        #All the variables that go in our time of flight equation
        x = s.symbols("x") #Number of batteries
        mAh = s.symbols("Ah") #Battery mAh
        V = s.symbols("V") #Battery Voltage
        M = s.symbols("M") #Motor Number
        Wb = s.symbols("Wb") #Battery weight
        Wd = s.symbols("Wd") #Drone weight 
        d = s.symbols("d") #Desired altitude
        vel = s.symbols("vel") #Desired Velocity
        A = s.symbols("A") #A in (inputPower, Thrust) equation
        B = s.symbols("B") #B in (inputPower, Thrust) equation
        #Give the variables above numerical values
        values = {
            A: float(self.power_system.data_collected["A"]),
            B: float(self.power_system.data_collected["B"]),
            M: float(self.motor_number),
            V: float(self.battery_system.data_collected["BATTERY VOLTAGE"]),
            mAh: float(self.battery_system.data_collected["mAh OF BATTERY"]),
            Wb: float(self.battery_mass),
        }
        #Just set some variables to simplify writing the equation
        c = self.power_system.data_collected["C"] - self.drone_weight / 4
        a = self.power_system.data_collected["A"] * 4
        #Time of Flight equation
        equation = 3.6 * (((V * mAh) / M) * (2 * A) * x) / (
            -B + s.sqrt((B**2) - a * (c - ((Wb / M) * x)))
        )
        #Take the derivative of the Time of Flight equation and solve it for Number of Batteries
        derivative = s.diff(equation, x).subs(values)
        solutions = s.solve(derivative, x)
        #Array of only real solutions from solving the derivative
        real_solutions = [s.re(sol) for sol in solutions]
        for i in real_solutions: 
            if i > 0: #Since number of batteries positive
                print("Optimal number of batteries: " + str(round(i))) #round the solution since number of batteries is whole number
                substituted_equation = equation.subs(x, round(i))
                
                # Evaluate the Time of Flight equation with optimal number of batteries 
                evaluated_equation = substituted_equation.evalf(subs=values) 

                # Print the Time of flight and the optimal number of batteries
                print(
                    "Time of flight with battery number = {}: {} seconds".format(
                        round(i), evaluated_equation
                    )
                )
                self.optimal_battery = round(i)

        return -1
    
   

# Create an instance of flight_time
flight_time_instance = flight_time()

# Call function
flight_time_instance.battery_number_finder()
#Display takeoff and landing time of flight
print("Takeoff time of flight: ", flight_time_instance.vertical_takeoff())
print("Landing time of flight: ", flight_time_instance.vertical_landing())


#Display hover time of flight and optimal battery number
flight_time_instance.optimization()
