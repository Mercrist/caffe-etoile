# Caffè Étoilé- CLI Based Backend
Caffè Étoilé's website utilizes a backend as robust, efficient, and sophisticated as the cafe's service and products. This simple CLI serves not just as a mockup for the backend, but also allows customers and engineers to visualize how the system handles orders. 

## Class UML
![UML][1]

## Dependencies
This project utilizes some external libraries in order for the CLI to run. Install the necessary libraries while in the root folder via: 
```bash
> pip3 install -r requirements.txt
```

## Running the CLI
The CLI program (called cafe_cli.py) handles any and all input for users to order from the cafe. Passing a – help flag will show the users the command options. 
```bash
python3 cafe_cli.py –help
usage: CLI tool used to interact with Caffè Étoilé. [-h] [{interactive,menu,about}]

positional arguments:
  {interactive,menu,about}
                        Main action to take.

optional arguments:
  -h, --help            show this help message and exit
```
When a user starts the program with no arguments, they should be greeted with the default interactive mode. Interactive mode presents the user with options to begin an order, view the menu, and exit the program.

```bash
python3 cafe_cli.py python3 or  cafe_cli.py interactive
Welcome to Cafe Ettoile!
What would you like to do today?
1.Start ordering
2.View menu in browser
3.Exit
:
```
```bash
Python3 cafe_cli.py menu
```
The menu command will open the user’s browser with a new tab containing the menu of the cafe. An important distinction to make is that it will not open the interactive menu and instantly exits. 

```bash
Python3 cafe_cli.py about
```
Like the menu command, opens the user’s browser with a new tab containing the main page of the cafe.


## Design Document
More information on the CLI and class design can be found in the [design document][2] for this project.

[1]: https://i.imgur.com/4paEZ8X.png "UML Diagram"
[2]: https://docs.google.com/document/d/1MGX-FJaVH08It__gCW3-Ja_oFVA535P_7ZlL1mbavcU/edit?usp=sharing&resourcekey=0-Nbmp1yoCrM28XlymrSHyHw "Design Doc"
