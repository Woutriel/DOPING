# DOPING
DoPing generator and solver
VERSION 1.1
Decimals Of Pi In Neighbour Grid (DOPING)
by Wouter Trieling
Last edit: 12 June 2022

This program called DOPING solves and generates DoPing puzzles. Below you can find basic information on how to use DOPING, what the game DoPing is, a (probably incomplete) list of DOPING's functionalities, and some comments on how the program was tested.

HOW TO USE (basics):
PREREQUISITES: This program should be ran with the newest versions that were available at the date of last edit of numpy, random, and time. These packages should be installed by the user prior to running DOPING. This program was made to work in Python 3.10.
SOLVE: Use by calling solve([number_of_rows, number_of_columns]) on line 389. For other options and details, use help(solve).
CREATE: Use by calling create_puzzle([[number_of_rows, number_of_columns]) on line 391. For other options and details, use help(create_puzzle).
I advise to create puzzles with a maxiumum number of 42 positions as it takes very long to solve bigger fields.


HOW THE PUZZLE GAME WORKS
DoPing (pronounce: do pie'ing) is a game where your goal is to fill the playing field with a string of the digits of π (31415926...) starting at 3, then going to 1 in one of the surrounding four fields,then to 4, to 1, to 5, etc. 
The catch is that no two equal digits are allowed to touch, also not diagonally.
This means that the 8 squares surrounding a certain square in the field can not contain the same number as that square.
There is, logically, an exception for consecutive occurences of decimals of pi, such as in the 933832. Here the two three's surrounded by the 9 and 8 have to touch eachother.
If the puzzle comes with digits pre-filled, your string must include these digits at their pre-filled location (just like with pre-filled numbers in a sudoku puzzle).
To get an example of what a solution looks like, create a puzzle (e.g. with create_puzzle([4,5],4) and type 'Y' when asked whether you want to see the solution.
-> For further explanation and DoPing's origins, contact Wouter Trieling at woutertrieling@gmail .com.

FUNCTIONALITY:
- Solves DoPing puzzles (if possible :)
- DoPing puzzle maker (creates puzzles for user to solve)
- (User adjustable) time limit to prevent infinite tries
- Shows starting field and position together with the solution when having found the solution
- Shows how long code took to run
- Debugging options: printed log of all moves and/or field after each step
- Support for fields with up to 115 squares (although this might take very much to (not) solve)
- Start position can be either user input or automatic
- Support for pre-set digits to solve puzzles with initial digits given. This also allows for users to input semi-solved puzzles when they get stuck solving it by themselves.
- Ability to show field when puzzle is created
- Option to create another puzzle with the same dimensions and number of pre-filled digits
- Check that the input field is not the unsolvable [5,5], [4,4] or [7,7] (these fields have no solutions). Please contact woutertrieling@gmail .com if you find any other unsolvable field dimensions.

TESTING
For other students or hobbyists (or however is interested) attempting to make a puzzle generator themselves, it might be interesting to see how one could go about testing the program. So as reference I summarized how I went about testing this program (note this is not based on any established testing frameworks).

To test the programme, I tested each function individually. For every bifurcation (if statements and certain loops), I tweaked my inputs to create all the different possible options to test if the code at every track worked. This is important as when you don't test all sections of the code but instead just tear a few possible user inputs with the final code, it is easy to miss the exception cases.
I also tested the two functions the user might call (solve() and create_puzzle()) by calling them many times with different inputs, including inputs that should activate code aimed at exceptions, such as debugging options, cases were the user inputs more pre-filles digits than there are locations in the field.
I furthermore also checked and tackled a few faulty user inputs to make sure they are either interpreted correctly (e.g. with slightly off answers in yes/no questions), or to make sure the user is asked to correct their input or gets served an error (so the code doesn't output a weird field).
I did this testing while I worked on the program (after finishing a new function I would test it rigourously) as to not forget testing any sections of the code. I would redo this testing after improving or bugfixing a function.
As a further check, I loaded the final version of DoPing on my phone and ran it a multitude of times, trying to give inputs that would test all functions of the program. 
Additionally, I solved a number of the puzzles that the program generated as an additional check of whether they were actually humanly solvable (they were, which was to be expected as the generator creates puzzles from solutions, so they always have at least one solution).


For further information, woutertrieling@gmail .com
