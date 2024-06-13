## Noah’s Art Program (Stained Glass)
# Introduction
The Noah’s Art Program is a unique application that allows a wide range of species to create art using a touchscreen-based digital paint program. This project involves a control panel for selecting pigeon subjects and a painting interface where the art is created. The program supports two modes: one for use in an operant box and another for a regular desktop environment. The software is built with minimal dependencies, making it easy to implement across various systems. However, the hardware aspect could be challenging, particularly with setting up the touchscreen. We use an infrared touchscreen frame mounted over our monitor, which is connected to our main computer via USB.

# Instructions
1.	Setup:
•	Ensure all dependencies are installed (see the Requirements section).
•	Place the Box_number.txt file in the appropriate directory if running in operant box mode.
2.	Running the Program:
•	Launch the program by running the script. This will open the control panel.
•	Select a subject name from the dropdown menu.
•	Click the "Start program" button to begin the painting session.
•	The painting interface will open, where the subject can create art using the touchscreen.
3.	Controls:
•	(l) Toggle lines on the canvas.
•	(spacebar) Toggle labels on the canvas.
•	Left mouse button Draw on the canvas.
•	Right mouse button Cancel drawing.
•	Escape Save the current artwork and exit the program.

# Requirements
The following dependencies are required to run the program:
•	Python 3.x
•	tkinter (included with standard Python installations)
•	functools (included with standard Python installations)
•	time (included with standard Python installations)
•	datetime (included with standard Python installations)
•	random (included with standard Python installations)
•	os (included with standard Python installations)
•	csv (included with standard Python installations)
•	math (included with standard Python installations)
•	Pillow (Python Imaging Library)
You can install Pillow using pip:
pip install pillow

# Contact Information
Contributions are welcome! If you would like to contribute to this project, or if you have any questions, suggestions, or issues, please feel free to contact:
•	Corresponding Author : Aaron P. Blaisdell
•	Email : DrAaronBlaisdell@gmail.com

# Acknowledgements
•	Thanks to the Python community for their contributions to open-source libraries that made this project possible.

# Credits
The Noah’s Art Program was developed through the collaborative efforts of Paul Gan, Robert Tsai, Cameron Guo, and Cyrus Kirkman. Their combined expertise and dedication have made this project possible.

# License
Copyright (c) [2024] [Aaron Blaisdell] 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
