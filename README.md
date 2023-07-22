# Pizza Ordering Website

# Installation Instructions

## Prerequisites

1.	Download and run the Python 3.11.2 installer for your system from [here](https://www.python.org/downloads/release/python-3112/)
2.	During the installation, make sure "Add Python to environmental variables" is selected.
3.	Download the project as a zip file using the green button in the top right of the page
4.	Extract the downloaded “mysite” folder from the zip file to somewhere on your computer.
5.	Open CMD on Windows, or TERMINAL on MacOS/Linux.
6.	Run this command `pip3 install Django==4.2.2`
7.	In your console window, set the current directory to inside the “mysite” folder you placed on your computer.
    - EX command: `cd C:/blah/blah/blah/mysite`
8.	Using the same console window, run the command: `python manage.py migrate`
    - You may need to add a 3 to any commands using python (EX `python3 manage.py migrate`), if on MacOS
    - You only need to run this command once.
  
## Starting the Project

1.	Run this command every time you want to start the Django server: `python manage.py runserver`
    - The current directory for the console window must be inside the “mysite” folder for the command to work
2.	The ordering system webpages will be accessible at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in a browser of your choosing, as long as you keep the server running.
3.	In order to stop the server, make sure the console window running the server is selected/highlighted, and press `L-Ctrl+C`
