# Installation

This project was built on python 3.9.12. To run this project you must have python 3.9.12 installed on your system to avoid compatibility issues. Note: The python version that comes with mac is not compatible with this project and must therefore be updated. To download or update your python version follow this link (`https://www.python.org/downloads/`). Several python library were also used in the development of this project all of which are within the requirements.txt file. The following steps below will guide with installation, running and visualising the project. Also Test Driven Development was adopted in this project.

# Steps

1. Open the project folder in terminal or command prompt. Check your python version using `python -v` if the version of your python is below 3 you need to update it follow this link to do so (`https://www.python.org/downloads/`)
2. Open the project folder in terminal or command prompt. Install all packages used in this project by pasting the following command in command prompt `python -m pip install -r requirements.txt` or terminal for Mac users `python3 -m pip install -r requirements.txt`
3. Run (`python -m phase_1` and `python -m phase_2`) on windows and (`python3 -m phase_1` and `python3 -m phase_2`)on Mac for console based interaction of phase_1 and phase_2 of the application
4. Run (`python -m phase_3`) on windows and (`python -m phase_3`) on Mac for GUI based interaction of all phases of the project. phase 4 has also been included in phase_3 and can be accessed using the GUI


# Visualisation

The following graphs and plots have been included in this project

1. ![Show Average Annual Temperature of Cities](img/Figure_1.png) 
2. ![Show Average Annual Precipitation of Countries](img/Figure_2.png)
3. ![Show 7-Day Precipitation by City](img/Figure_3.png)
4. ![Show Average Annual Temperature and Precipitation](img/Figure_4.png)
5. ![Show Daily Temperature](img/Figure_5.png)


# Test

Open the project folder in Command Prompt or Terminal (Mac)

1. Run `python -m test_main` on Windows and `python3 -m test_main` on Mac to generate the result of the test cases.
2. To run test coverage paste the following command into command prompt or terminal `python -m coverage run -m unittest discover`. For Mac - `python3 -m coverage run -m unittest discover` 
(attach image here).
3. To report the coverage enter the following command into command propmt or terminal `python -m coverage report -m`. For Mac enter `python3 -m coverage report -m`. (attach image here)


The report contains the full details about the Blackbox testing.
