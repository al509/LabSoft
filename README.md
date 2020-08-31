# Fiber Lasers Lab soft
It is a collection of all soft in it's actual state used in Fiber Lasers Laboratory of Novosibirsk
State University.

## Installing
1. Download and install [Anaconda](https://www.anaconda.com/) software
2. Download and install [Thorlabs apt software](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control&viewtab=1)
3. Run Anaconda Powershel Prompt (Run->Anaconda) and type following commands
(in *italics*) to install missing modules:
	* *conda install -c anaconda pyserial* - Module for work with serial conections  
	* *pip install thorlabs-apt* - Thorlabs controller module
	* *pip install instrumentkit* - Shutter controller module. 
	As I remember, it should be changed a little to work.
4. Run Spyder and open a program you want to use. Start it.

## Content

### ImpulseMaker
The program to make impulses.

### TaperMaker
 The program to make tapers.