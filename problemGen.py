import time
import sys
import json

# "dont repeat yourself" (DRY) violation
TRACKER_FILE = "tracker.json"

def displayMenu(solved):
    print("+-----------------------------------------------+")
    print("                    Menu")
    print("+-----------------------------------------------+")
    displayList(solved)

    print("\n1. Randomly pick a solved Leetcode problem")
    print("2. Add a Leetcode problem")
    print("3. Remove a Leetcode problem")
    print("4. Display Leetcode problems in progress")
    print("5. Update Leetcode currently in progress")
    print("6. Exit program\n")

"""
displayList(): Displays list of previously solved problems
"""
def displayList(problems):

    print("* Solved Problems *")
    for num, problem in problems.items():
        print(f"{num}. {problem}")

"""
pick(): Randomly selects a Leetcode problem from the list of solved problem
"""
def pick():
    print("Randomly picking previously solved problem...")
    input("Press Enter to continue...")

"""
add(): Allows user to add a problem to the list 
"""
def add(solved):
    print(">> ADD")

    # .strip() removes accident leading/trailing spaces
    ID = input("What is the problem ID? ").strip()
    problem = input("What is the problem name? ").strip()

    # Prevents empty inputs from ruining tracker file
    if not ID or not problem:
        print("Error: ID and problem cannot be empty!")
        time.sleep(2)
        return

    # Secure duplicate check (Works great with JSON keys!)
    if ID in solved:
        print(f"ID: {ID} Problem: {solved[ID]} already tracker")
        time.sleep(2)
        return
    
    solved[ID] = problem
    save_problems(solved)

    print(f"Adding {problem}!")
    time.sleep(2)
"""
remove(): Allows user to remove a problem from the list
"""
def remove(solved):
    print(">> REMOVE")

    # .strip() removes accident leading/trailing spaces 
    ID = input("What is the problem ID? ").strip()

    # Prevents empty inputs from ruining tracker file
    if not ID: 
        print("Error: ID and problem cannot be empty!")
        time.sleep(2)
        return  

    # Safely pop first without printing solved[ID] directly (avoids KeyError)
    # Use raw object None (no quotes) as fallback safety net
    removed = solved.pop(ID, None)

    # Correct comparison using the Python keyword 'is None' or '== None'
    if removed is None:
        return print(f"{ID} not found!")

    # Safe to print the name since we verified it existed
    print(f"Removing {removed}")

    # Commit the clean dictionary back to JSON file
    save_problems(solved)
    time.sleep(2)

"""
displayWIP() function displays most recently generate leetcode problem, the most recent problem solved that was added to the
list of problems, AND the leetcode problem that the user is progressing on. 
This is supposed to help the practice 1 random previous solved problem, the most recent problem the user completed and the 
problem the user is currently trying to solve to add to the list of solved problems. 
So 3 problems in total are to be displayed!
Note: Repractice problem is not yet added to main list of problems until current problem is solved
Example:
Random selected problem: Valid Anagram
Repractice: Group Anagrams
Currently working on: Top K Frequent Elements
"""
def displayWIP():
    print("Displaying Leetcode problems in progress: ")
    print("Randomly picked problem: ")
    print("Practice previously solved problem: ")
    print("Currently solving: ")
    input("Press Enter to continue...")

"""
updateWIP(): Allows the user to tell the program that the user completed the current Leetcode problem in progression.
The repractice problem is added to the main list of problems and the current problem is moved to the repractice problem.
Then the user tells the program which problem they're currently solving.
"""
def updateWIP():
    print("What problem are you currently working on?")
    input("Press Enter to continue...")
    
def exit_program():
    print("Exiting program...")
    time.sleep(3)
    sys.exit(0)

def load_problems():
    try:
        with open(TRACKER_FILE, "r") as fp:
            return json.load(fp)
    except FileNotFoundError:
        return {}

def save_problems(solved):
    with open(TRACKER_FILE, "w") as fp:
        json.dump(solved, fp, indent= 4)


def main():

    solved = load_problems()

    while True:
        displayMenu(solved)

        menu = {
            "1": pick,
            "2": lambda: add(solved),
            "3": lambda: remove(solved),
            "4": displayWIP,
            "5": updateWIP,
            "6": exit_program,
        }

        choice = input("Select an option: ")

        action = menu.get(choice)

        if action:
            action()
        else:
            print("Invalid selection")
            time.sleep(2)

        


if __name__ == "__main__":

    main()