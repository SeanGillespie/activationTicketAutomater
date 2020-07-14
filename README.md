## activationTicketAutomater.py

Script that automates the tedious filling out of Ethernet port activation tickets

**Prerequisites (there is a little setup involved, but the time will be gained back later!):**


1) Install Python3 if not installed
2) Install selenium and argparse. (install pip package manager if you have not, and do pip install [selenium or argparse] in powershell or CMD)
3) Install ChromeDriver from https://chromedriver.chromium.org/downloads for your version of Chrome, check verison in chrome settings > about chrome
4) Put the chromedriver.exe file anywhere, but add its location to PATH variable on Windows
5) While editing the System and Environment Variables on your dedicated vm, (not the best idea on a shared machine) in step 4, add a variable 'SECRET' that has your password as its value
6) Create a file called settings.py in the same directory that activationTicketAutomater.py is located
7) Fill the settings.py file with the following, but change to your specifics:

        import os
    	EMAIL = 'email@up.edu'
    	PASSWORD = os.environ['SECRET']
    	NAME = 'FirstName LastName'


**Example Usage**

The program takes one required argument and can add up to 3 additional optional arguments with flags.

Required arguments:
| The url of the activation ticket |
 
Optional arguments:
___________________________________________________________
| **-h, --help**    | show this help message and exit  |
_____________________________________________________________
| **-j [JACK_LABEL], --jack_label [JACK_LABEL]** | optional jack label and/or description in double quotes, e.g. "CR-2A-J-041 (left side)" |
____________________________________________________________________
| **-w [WORKNOTES], --worknotes [WORKNOTES]**  |  optional worknotes in double quotes, e.g. "Activated to HH-4A-2960-01 Gi1/0/34" |
__________________________________________________________________
| **-l, --logging**    |  Show logging info if you want to see what is going on during execution |
____________________________________________________________________________


           
    
   
       
**Use case 1: you do not want/need to put any specific info into the ticket**

In this case all you need is the url of the activation ticket as an argument after the file argument.
a message will be written in the comments addressed to the caller, from your name, state changed if needed, and changes saved. 
If the caller is a student, a student specific message is added as well.
```
python activiationTicketAutomater.py https://rest_of_url
```

**Use case 2: you want to be specific as to what jack was activated**

Same as above, but add the optional -j or --jack_label argument to add a specific string (use double quotes around the string).
```
python activationTicketAutomater.py https://rest_of_url -j "CR-2A-J-41 left side"
```

**Use case 3: you want to add worknotes because you like to be thorough**

Same as use case 1, but use the -w or --worknotes flag with a following string in double quotes.
```
python activationTicketAutomater.py https://rest_of_url -w "Activated to switch 1 port Gi1/0/23 on VLAN 888"
```
**Use case 4: example with multiple flags and arguments**
```
python activationTicketAutomater.py https://rest_of_url -j "BB-9C-J-01" -w "Activated to switch 1 port Gi1/0/23 on VLAN 888" -l
```

**Authors**
Sean Gillespie

