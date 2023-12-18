"""
- Prompt the user if they want to enter data for a motor+prop combination.
- Ask for the name of the motor
- Take in the thrust and power value pairs.
- Generate the coefficients of the polynomial.
- To accomplish this, please create a class called "PowerSystem" or something along those lines, the class should have attributes for: string motor_name, float propeller_size, int battery_cell_count, 
list thrust_values, list power_values, list poly_coefficients.
- Add a method to the class to take in the thrust power pairs, and add a private method to generate the coefficients of the polynomial
- Make sure to save all the objects created from this class (maybe pickle them) so that the user will NOT have to input the data again each time.
"""
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


class PowerSystem:
    """this class reads a .txt file containing motor information, in specific the values of (power,thrust) and converts that data into a quadratic equation, outputting the coeffecients A, B, C"""

    def __init__(self, file_name):
        self.thrust_values = []  # Holds thrust data points
        self.power_values = []  # Holds inputPower data points
        self.poly_coefficients = []  # Stores calculted coeffecients A, B, C
        self.data_collected = {  # Dictionary for respected info, -1 will be replaced by actual value once program runs
            "FILE NAME": file_name,
            "MOTOR": -1,
            "PROPELLAR NAME": -1,
            "PROPELLAR SIZE": -1,
            "PROPELLAR MASS": -1,
            "BATTERY CELL COUNT": -1,
            "MAX THRUST": -1,
            "A": -1,
            "B": -1,
            "C": -1,
        }

    def thrust_power(self):
        """Reads the file specified by user and replaces values in the dictionary of information with the respected values in the file. If file name is not found exits program"""
        try:
            rotor_file = open(
                "data/propulsion\{}.txt".format(
                    self.data_collected["FILE NAME"]
                ),
                "r",
            )
        except FileNotFoundError:
            print("File not found. Please check the motor file name.")
            exit()
        
        found_motor = False #False initially, becomes true if we found the motor name in the data file
        for line in rotor_file:
            if "end" in line: #end is placed at the end of the data file
                return 0
            if "FINISH" in line: #FINISH is placed at the end of the data points in the data file
                found_motor = False
            if found_motor: #reads the power,thrust data points
                thrust_power_data = line.split(",")
                self.thrust_values.append(float(thrust_power_data[1]))
                self.power_values.append(float(thrust_power_data[0]))
            if "MOTOR" in line: #reads motor name
                motor_name_data = line.split(":")
                self.data_collected["MOTOR"] = motor_name_data[1].rstrip()
                found_motor = True
            if (not found_motor) and ("PROPELLAR NAME" in line): #reads propeller name
                propeller_name_data = line.split(":")
                self.data_collected["PROPELLAR NAME"] = propeller_name_data[
                    1
                ].rstrip()
            if (not found_motor) and ("PROPELLAR SIZE" in line): #reads propellar size
                propeller_size_data = line.split(":")
                self.data_collected["PROPELLAR SIZE"] = propeller_size_data[
                    1
                ].rstrip()
            if (not found_motor) and ("PROPELLAR MASS" in line): #reads propellar mass
                propeller_mass_data = line.split(":")
                self.data_collected["PROPELLAR MASS"] = propeller_mass_data[
                    1
                ].rstrip()
            if (not found_motor) and ("BATTERY CELL COUNT" in line): #reads battery cell count
                battery_cell_count_data = line.split(":")
                self.data_collected[
                    "BATTERY CELL COUNT"
                ] = battery_cell_count_data[1].rstrip()
            if (not found_motor) and ("MAX THRUST" in line): #reads max thrust
                battery_cell_count_data = line.split(":")
                self.data_collected["MAX THRUST"] = battery_cell_count_data[
                    1
                ].rstrip()

    def equation(self, x, a, b, c):
        """takes in paramaters, and returns a quadratic equation using those parameters. This is the equation we will fit the data points into

        Args:
            x variable: inputPower
            a const: A in quadratic standard form
            b const: B in quadratic standard form
            c const: C in quadratic standard form

        Returns:
            equation: Quadratic Form
        """        
        return a * (x**2) + b * x + c

    def get_coefficients(self):
        """sets up the graph of the quadratic equation generated by (inputPower,Thrust) and fills in the A, B, C values of the dictionary of info
        """        
        popt, pcov = curve_fit(
            self.equation, self.power_values, self.thrust_values
        )
        for i in popt:
            self.poly_coefficients.append(i) #coeffecients to poly_coeffecients list
        self.data_collected["A"] = self.poly_coefficients[0] 
        self.data_collected["B"] = self.poly_coefficients[1]
        self.data_collected["C"] = self.poly_coefficients[2]

    def display_graph(self):
        """displays the graph setup by the get_coeffecients function
        """        
        plt.scatter(self.power_values, self.thrust_values)
        plt.show()

    def display_coefficients(self):
        """Displays coeffecients A, B, C to the user
        """        
        print(
            "A: {}, B: {}, C: {}".format(
                self.poly_coefficients[0],
                self.poly_coefficients[1],
                self.poly_coefficients[2],
            )
        )


# Arrays to store PowerSystem objects
power_systems = []
Playing = True
'''while Playing: #Main loop, user enters files and class functions are run    
    new_file = input("Enter motor file name: ")
    ps = PowerSystem(new_file) #Class instance
    ps.thrust_power()
    ps.get_coefficients()
    # ps.display_graph() #This is to display the graph
    ps.display_coefficients()
    power_systems.append(ps.data_collected)
    # print(ps.data_collected) #This is to print the dictionary of info
    Playing = False #Ends loop'''

    
r"""HOW TO USE
    TEXT FILE SETUP
   Make a text file with the first line as the motor name(should be exact), following lines containing the thrust,power pairs(example:1900,2400). One pair per line. When done entering all pairs type "end"
   in the next line. Save your text file and open it in your current working space. You may need to change the text file location at line number 39 depending on how you are running python. 
   Simple way to do this is just to check your current working space(mine is displayed in the terminal as: C:\Users\mehmo\.cursor-tutor), and then checking the location of your text file.
   Mine is in: C:\Users\mehmo\.cursor-tutor\projects\python             
   Therefore my file location specified on line 39 is :"projects\python\{}.txt" --> Ignore the {} its just for coding purposes.

    USING PROGRAM:
        After clicking run, the program will prompt you to choose between 3 options: Enter a new motor/propeller pair, check info on an existing motor/propeller, quit the program. To choose type
        1, 2 or 3, respectively. Entering a motor/propeller pair will allow you to enter info on the motors name, propellars size, and battery cell count. The program will then display info about 
        the quadratic equation(Ax^2 + Bx + C) that can describe the (Thrust,Power) data points. The program will provide estimated values of A, B, and C. Option 2 will allow you to type in the name
        of the motor that already has been inputted into the program, and then the program will show you the information about that motor. Lastly, Option 3 will exit you from the program.
        
    DOWNLOADING scipy AND matplotlib
        https://scipy.org/install/ --> Basically in your cmd type 'python -m pip install scipy' *pip must be installed

        https://matplotlib.org/stable/users/installing/index.html --> Basically in your cmd type 'python -m pip install -U matplotlib' *pip must be installed

        If these commands dont work you can download Anaconda: https://www.anaconda.com/download and follow the guide on  https://scipy.org/install/ and https://matplotlib.org/stable/users/installing/index.html
        """
