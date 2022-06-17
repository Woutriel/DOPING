'''
Decimals Of Pi In Neighbour Grid (DOPING)
VERSION 1.1
Author: Wouter Trieling
Last edited: 12 June 2022

This program called DOPING solves and generates DoPing puzzles. Below you can find basic information on how to use DOPING, what the game DoPing is and a (probably incomplete) list of DOPING's functionalities.

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
-> For further explanation and DoPing's origins, contact Wouter Trieling at woutertrieling@gmail.com.

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
- Check that the input field is not the unsolvable [5,5], [4,4] or [7,7] (these fields have no solutions). Please contact w.m.trieling@student.utwente.nl if you find any other unsolvable field dimensions.

POSSIBLE FUTURE ADDITIONS IN THE COMING MONTHS:
- Hint option (shows only the next field or a random yet unsolved field)
- Structural starting positions (goes through all possible starting positions instead of choosing random ones with the possibility of double testing some while missing others).
- Storage for puzzles
- Prettier user interface

For further information, contact woutertrieling@gmail.com
'''

import numpy as np
import random
import time
from time import perf_counter
pi = "314159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808653282306647"
field = []
n = 0 #current progress quantifier
r = [] #row
c = [] #column
position = [] #[row, column in field matrix]
moves = [] #keeps track of route and tried options from that position. List items: [position, count, order, digit]
unsolved_field = [] #list to store unsolved field
display_field = [] #field with string items instead of integers
coordinates = [] #list to store locations with pre-set digits
failed_sp = 0 #counter for unsuccesful starting positions

def reset_variables():
    """
    Reset global variables
    """
    global field
    global n
    global r
    global r
    global c
    global position
    global moves
    global unsolved_field
    global display_field
    global coordinates
    global failed_sp
    field = []
    n = 0  # current progress quantifier
    r = []  # row
    c = []  # column
    position = []  # [row, column in field matrix]
    moves = []  # keeps track of route and tried options from that position. List items: [position, count, order, digit]
    unsolved_field = []  # list to store unsolved field
    display_field = []  # field with string items instead of integers
    coordinates = []  # list to store locations with pre-set digits
    failed_sp = 0  # counter for unsuccesful starting positions

def field_check(field_dimensions, number_of_prefilled):
    """
    Initial check of whether the field can be created
    :param field_dimension: [r,c]
    :param number_of_prefilled: number of digits, or number of preset digits
    :return: True or False
    """
    if field_dimensions == [5,5] or field_dimensions == [4,4] or field_dimensions == [7,7]: #fields without solutions (update if necessary)
        print(f"There are no solutions for a {field_dimensions} field.")
        return False
    if number_of_prefilled > field_dimensions[0]*field_dimensions[1]: #check if number of (pre-set) digits exceeds the number of locations in field.
        print("You have more pre-filled digits than the number of positions in the field.")
        return False
    return True

def create_field(field_dimensions, pre_set):
    """
    Create the field, display_field and unsolved_field with, if applicable, the pre_set digits set
    :param field_dimensions: (number of rows, number of columns)
    :param pre_set: list coordinates and corresponding digits of pre_set fields
    :return: "fields made" when succesful, "impossible" when pre-set positions are out of bounds
    """
    global field
    global unsolved_field
    global coordinates
    global display_field
    field = -1 * np.ones((field_dimensions[0], field_dimensions[1]), dtype=int) #create field
    display_field = np.full((field_dimensions[0], field_dimensions[1]), '_', str) #create display field
    if pre_set == [0]: #no pre-set
        unsolved_field = field.copy() #store the unsolved field
    else:
        coordinates = [x[0] for x in pre_set] #split preset lists for coordinates and digits
        digits = [x[1] for x in pre_set]
        pi_int_list = ([int(y) for y in pi])
        j = 0
        while j < len(digits): #if the preset digits are not in the possible digits for this size of field, let solve() know it's impossible to solve.
            if digits[j] not in pi_int_list[0: field.size]:
                return "impossible"
            j += 1
        i = 0
        while i < len(pre_set): #put the pre-set digits in the field and display field
            field[coordinates[i][0], coordinates[i][1]] = digits[i]
            display_field[coordinates[i][0], coordinates[i][1]] = digits[i]
            i += 1
        unsolved_field = field.copy() #store the unsolved field
    return "fields made"

def new_position(count):
    """
    Create the coordinates of new positions to check for validity.
    Follows the standard order right -> down -> left -> up
    Input moves[n][1] to know which option needs to be checked.
    :return: proposed position in [r,c] or False if all possible positions have been tried without succes.
    """
    r = position[0]
    c = position[1]
    order = [[r, c + 1], [r + 1, c], [r, c - 1], [r - 1, c]]  # move options [right, down, left, up]
    if count == 0:
        proposed_position = order[moves[n][2][0]]
    elif count == 1:
        proposed_position = order[moves[n][2][1]]
    elif count == 2:
        proposed_position = order[moves[n][2][2]]
    elif count == 3:
        proposed_position = order[moves[n][2][3]]
    else: #count == 4
        return False
    return proposed_position

def legal_position (proposed_position):
    """
    Checking mechanism for legality of new position.
    Checking for (in order):
    - if position is within the field;
    - if position is not already taken;
    - if the input value won't be the same as that of any of the directly surrounding 8 fields.
    If legal, the function returns True
    If not legal, function returns False
    """
    if proposed_position == False:
        return False
#Q: is there any reason to use 'else:' like I did here when the if statement includes a return?
    else:
        r = proposed_position[0]
        c = proposed_position[1]
        try: # test whether position is in the field. If not, except will return False
            if r < 0 or c < 0: #check if the position is not already taken by another digit and that the row or column isn't negative (would mean the solver would jump across the field)
                return False
            if field[r,c] != -1:
                return match_init_digits(r,c)
        except:
            return False
        #checking mechanism value
        next_number = int(pi[n+1])
        #nb = neighbouring fields including field being checked
        nb = field[ max(0,r-1) : min(r+1,field.shape[0]-1)+1, max(0,c-1) : min(c+1,field.shape[1]-1)+1 ] #from one row above to one row below the column on the left to the column on the right, excluding any positions outside of the matrix
        if np.count_nonzero(nb == next_number) == 0 or np.count_nonzero(nb == next_number) == 1 and next_number == int(pi[n]): #if digit not present in surrounding positions, or if it's the preceeding digit, the position is valid.
            return True
        else: #if digit present in surrounding positions once and the preceeding digit is not the same, or if present more than once in surrounding fields, the position is invalid.
            return False

def match_init_digits(r,c):
    """
    Checks when encountering a filled position whether this is a previously solved positition, or an pre-set position.
    :param r: row
    :param c: column
    :return: True if pre-set digit, False if previously solved position
    """
    global moves
    global field
    global pi
    global n
    if [r,c] in list(zip(*moves))[0]: #previously solved position
        return False
    elif field[r,c] == unsolved_field[r,c]: #pre-filled position and correct digit
        return True
    elif field[r,c] != unsolved_field[r,c]: #pre-filled position and incorrect digit
        return False
    else: #shouldn't happen. Might be an artifact. Was added in VERSION 0.2 for bug-fixing purposes.
        print("ERROR 1 potentially at match_init_digits (remove print and add comment if legit)")
        return False

def remove():
    """"
    remove the positions and numbers if it leads to a dead end. Go back as far as needed, then update position.
    """
    global n
    global field
    global moves
    global position
    if moves[n][1] >= 4:
        if n == 0: #when the starting position yields no solutions
            return False
        else:
            if [moves[n][0][0], moves[n][0][1]] not in coordinates:
                field[moves[n][0][0], moves[n][0][1]] = -1
            moves.remove(moves[n])
            n += -1
            moves[n][1] += 1
            if moves[n][1] == 4:
                remove() #call remove() again if all options have already been tried for the new current position (prevents the count succeeding 4)
        position = moves[n][0] #update position

def solver(bugfix_type):
    """
    Solves the puzzle. Input bugfix_type for bugfixing options.
    Prints the solution + taken route in coordinates and directions (0=right, 1=down, 2=left, 3=up)
    """
    global field
    global n
    global moves
    global position
    global r
    global c
    global failed_sp
    #starting spot needs to be added
    while n+1 != field.size: #or -1 in field: #contintue as long as there are no 'empty' fields and all fields have been 'visited'
        while legal_position(new_position(moves[n][1])) != True:
            moves[n][1] += 1 #log that a new move has been tried
            if bugfix_type != 0:
                if bugfix_type == 1:
                    print("moves:", moves)
                    print(field)
                if bugfix_type == 2:
                    print("moves:", moves)
                if bugfix_type == 3:
                    print(field)
            if remove() == False: #check if removal is needed and remove log items if needed
                return False
        position = new_position(moves[n][1]) #make position the proposed position
        r = position [0]
        c = position [1]
        n += 1 #keep track of progress
        field[r, c] = int(pi[n]) #change field value to the corresponding digit of pi
        try: #if moves[n] exists, update with new position, else create moves[n]
            moves[n] = [position, 0, random.sample(list(range(4)), k=4), int(pi[n])]
        except:
            moves.append([position, 0, random.sample(list(range(4)), k=4), int(pi[n])])
    return True

def start_solver (start_position , bugfix_type):
    """
    Puts the initial starting position in the field and calls solver(). Also checks for validity of bugfix_type input.
    :param start_position: position of n(0) digit of pi (so 3)
    :param bugfix_type: see solve(). If create_puzzle was called, this function is disabled (input 0).
    :return: "solved" or "no solution"
    """
    global field
    global r
    global c
    global moves
    global position
    global failed_sp
    # initial value
    r = start_position[0]
    c = start_position [1]
    field[r, c] = 3
    moves = [[[r, c], 0, random.sample(list(range(4)), k=4), 3]]
    position = [r, c]  # [row, column in field matrix]
    if bugfix_type not in [0,1,2,3]:
        print("Invalid input for bugfix type. Accepted inputs are 0, 1, 2, or 3. Program will run with bugfix disabled (input 0).")
    if solver(bugfix_type) == True:
        return "solved"
    else:
        failed_sp += 1
        return "no solution"
    print("ERROR start_solver: There is no solution")

def solve(field_dimensions, pre_set = [0], start_position = 0, max_process_time = 30, bugfix_type = 0):
    """
    Checks whether 'a' solution exists for a certain field with a given starting position, or for random starting positions.
    :param field_dimensions: 2 item list [rows, columns] to define the dimensions of the field you want to solve
    :param pre_set: input initial digits. pre_set = [ [[row,column], digit], [[row,column], digit], ... ]
    :param start_position: 0 (default) for random start position. For custom start position, enter a 2 item list [row, column] to define the starting positions (where the 3 before the decimal point is placed)
    :param max_process_time: max time in seconds for which the program will START searching for a solution with a new position. Default is 30s.
    :param bugfix_type: 0 (default) bufix off; 1 for both field and moves; 2 for moves only; 3 for field only.
    :return only the first solution found, or returns that no solution has been found, if none exists.
    """
    t1_start = perf_counter()
    if field_check(field_dimensions, len(pre_set)) == True:
        if create_field(field_dimensions, pre_set) == "impossible":  # create field and check for validity
            print(
                f"At least one of your pre-filled digits is not present in the first {field_dimensions[0] * field_dimensions[1]} digits of pi, therefor this puzzle is impossible to solve.")
            return "Not succesful"
    else:
        return "Not succesful"
    global field
    global display_field
    print("Busy finding you a solution...")
    if start_position == 0: #default is random start position
        print("Trying out multiple starting positions for max", max_process_time, "seconds...\n")
        while perf_counter() - t1_start < max_process_time:
            start_position = [random.randint(0, field_dimensions[0]-1), random.randint(0, field_dimensions[1]-1)]
            if start_solver(start_position, bugfix_type) == "solved":
                print("\nSolution found!")
                print(f"For the field \n{display_field}\n with starting position {start_position}, a solution is:\n\n {field}\n\nThe path taken is: {list(zip(*moves))[0]}")
                return "Succesful"
            create_field(field_dimensions, pre_set) #reset field
            if bugfix_type == 1:
                print("time elapsed", perf_counter()-t1_start)
        print(f"\nNo solution found for field \n{display_field}\nwith random starting positions in {max_process_time} seconds.")
        print(failed_sp, "starting positions were analysed in this run.")
    else:
        if start_solver(start_position , bugfix_type) == "solved":
            print(f"For the field \n{display_field}\n with starting position {start_position}, a solution is:\n\n {field}\n\nThe path taken is: {list(zip(*moves))[0]}")
            return "Succesful"
        else:
            print(f"No solution exists for the field {display_field} with starting position {start_position}")
            print("Sorry, I'm afraid your puzzle is unsolvable :(")
    return "Not succesful"

def create_puzzle(field_dimensions, number_of_digits = 1, max_process_time = 30):
    """
    Creates solvable puzzles with the option to see the corresponding solutions.
    :param field_dimensions: dimensions of the playing field [number of rows, number of columns]
    :param number_of_digits: number of digits you want to be pre-filled in the field. Default is 1 digit.
    :param max_process_time: maximum time in seconds to try new random starting positions for the field before giving up on finding a new starting position with a solution. Default is half a minute.
    :return: User gets to see the puzzle(s) and optionally the solution(s). The return values are arbitrary and exist merely to end the program.
    """
    if field_check(field_dimensions, number_of_digits) == True:
        play_again = "Y" #default start the program
    else:
        return "Fail. End of program"
    while play_again in ["Y","y","yes","Yes"]: #continue for as long as the user wants
        reset_variables() #start with clean slate
        t1_start = perf_counter()
        create_field(field_dimensions, [0])
        global field
        global display_field
        print("Construction a DoPing puzzle for you...")
        puzzle_made = False
        while perf_counter() - t1_start < max_process_time and puzzle_made == False:
            start_position = [random.randint(0, field_dimensions[0] - 1), random.randint(0, field_dimensions[1] - 1)]
            if start_solver(start_position, 0) == "solved":
                i=0
                while np.count_nonzero(display_field != "_") < number_of_digits: #put number_of_digits digits in the unsolved field.
                    r = random.randint(0, field_dimensions[0] - 1) #select random row
                    c = random.randint(0, field_dimensions[1] - 1) #select random column
                    display_field[r,c] = field[r,c] #insert the selected digits in the display field
                print("Your puzzle:\n\n", display_field) #give the user the puzzle
                show_solution = "" #to show solution
                while show_solution not in ["Y","y","yes","Yes", "N", "n", "no", "No"]: #show solution when user wants it. In a loop to force a correct (yes/no) input
                    show_solution = input("Do you want to see the solution? Y/N")
                    if show_solution in ["Y","y","yes","Yes"]:
                        print(field, "\n\nmoves:\n", list(zip(*moves))[0])
                        puzzle_made = True
                    elif show_solution in ["N", "n", "no", "No"]:
                        print("Good luck solving the puzzle! I won't spoil the fun by showing you a solution.")
                        puzzle_made = True
                    else:
                        print("Didn't understand that input, please input only 'Y' or 'N'.")
            create_field(field_dimensions, [0])  #reset field
        if puzzle_made == False:
            print(f"Couldn't find a solution for a {field_dimensions} field within {max_process_time} seconds to create a puzzle from.")
            print("Please run create_puzzle again with different dimensions.")
            return "Failed to make puzzle within time limit."
        play_again = input(f"\nDo you want another {field_dimensions} puzzle with {number_of_digits} pre-filled digits? Y/N")
    print("Thank you for playing DoPing, hope to see you back for another puzzle soon!")
    return "End of program"

# measure start and end time when executing code
start_time = time.process_time()

#call solve to solve puzzle
#solve([5,4])
#call create_puzzle to create puzzle
create_puzzle([4,5],4)

end_time = time.process_time()
result_time = (end_time - start_time)
print(f"\nCode took {result_time}s to execute.")




