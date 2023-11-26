"# PersonalSpace" 

# Time of Flight software for Toronto Metropolitan Aerial Vehicles (TMAV)

# A functional project written in Python which outputs the optimal number of batteries for a multi-rotor drone to maximize the time of flight

This project is a week by week work that was built to help TMAV's drone achieve the maximum time of flight. The project contains 2 mini python programs that extract data from text files and 1 main program which uses the gathered data along with a Time of Flight equation to find the number of batteries that maximizes the flight time. An explaination of the project and how it works in more depth is as follows:

* batteries.py and Propulsion.py are the two mini programs which extract data from Battery and Motor text files respectively. The user will enter the name of these text files and pre-made text files will be provided.
* main.py is the main program that will use data from batteries.py and Propulsion.py as well as a custom-made Time of Flight equation to find the optimal number of batteries to maximize flight time
* When using the program the user will be prompted to enter the following information: name of Motor text file, name of Battery text file, deseried vertical takeoff velocity, desired vertical altitude
* Any text files that are made by the user will have to follow the same format as the pre-made text files. 


## how to install this project on Windows

Below I have provided a rundown of the installation process as well as youtube videos that can guide you through difficult steps:

1. clone this project using github
2. install python and pip [![Watch the video](https://img.youtube.com/vi/dYfKJMPNMDw&ab/default.jpg)](https://youtu.be/dYfKJMPNMDw&ab)
4. install matplotlib --> "pip install matplotlib" in terminal
5. install sympy --> "pip install sympy" in terminal

"# Project" 
