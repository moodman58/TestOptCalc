"""
Should have the following values from data files:
Mass of battery.
mAh of battery.
Battery voltage.
C (discharge) of battery
Use those values to compute the energy per battery 
and have these values as attributes in a class, similar to motors.

"""
import os
class Batteries:
    def __init__(self, file_name):
        self.data_collected: dict = {
            "FILE NAME": file_name,
            "MASS OF BATTERY": -1,
            "mAh OF BATTERY": -1,
            "BATTERY VOLTAGE": -1,
            "BATTERY DISCHARGE": -1,
            "MAX CURRENT DRAW": -1,
            "BATTERY ENERGY": -1,
        }
        
    def battery_energy(self):
        return (float(self.data_collected["mAh OF BATTERY"]) / 1000) * float(
            self.data_collected["BATTERY VOLTAGE"]
        )

    def max_current(self):
        return float(self.data_collected["BATTERY DISCHARGE"]) * float(
            self.data_collected["mAh OF BATTERY"]
        )

    def change_data_values(self):
        self.data_collected["MAX CURRENT DRAW"] = self.max_current()
        self.data_collected["BATTERY ENERGY"] = self.battery_energy()

    def get_file_values(self):
        try: 
            print("Current Working Directory:", os.getcwd())
            battery_file = open(
                "data/batteries\{}.txt".format(self.data_collected["FILE NAME"]),
                "r",
            )
        except FileNotFoundError:
            print("File not found. Please check the battery file name.")
            print("Current Working Directory:", os.getcwd())
            exit()
            

        for line in battery_file:
            if "MASS OF BATTERY" in line:
                mass_split = line.split(":")
                mass = mass_split[1]
                self.data_collected["MASS OF BATTERY"] = mass.strip()
            if "mAh OF BATTERY" in line:
                current_split = line.split(":")
                current = current_split[1]
                self.data_collected["mAh OF BATTERY"] = current.strip()
            if "BATTERY VOLTAGE" in line:
                voltage_split = line.split(":")
                voltage = voltage_split[1]
                self.data_collected["BATTERY VOLTAGE"] = voltage.strip()
            if "BATTERY DISCHARGE" in line:
                discharge_split = line.split(":")
                discharge = discharge_split[1]
                self.data_collected["BATTERY DISCHARGE"] = discharge.strip()


entering_data = True
batteries = []

'''while entering_data:
    
    battery = Batteries("Battery")
    
    file_name = input("Battery file name: ")
    battery.data_collected["FILE NAME"] = file_name
    battery.get_file_values()
    battery.max_current()
    battery.battery_energy()
    battery.change_data_values()
    batteries.append(battery)
    entering_data = False
'''
