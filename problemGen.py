import time
import sys
import json
import random

# "dont repeat yourself" (DRY) violation
TRACKER_FILE = "tracker.json"

def displayMenu(solved, practice):
    print("+-----------------------------------------------+")
    print("                    Menu")
    print("+-----------------------------------------------+")
    displayList(solved)
    displayWIP(solved, practice)

    print("\n1. Randomly pick a solved Leetcode problem")
    print("2. Add a Leetcode problem")
    print("3. Remove a Leetcode problem")
    print("4. Update Leetcode currently in progress")
    print("5. Exit program\n")



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
def pick(solved, practice):
    print("Randomly picking solved problem...")
    input("Press Enter to continue...")

    if not solved:
        print("Solved dictionary is empty!")
        return


    problem_ID = random.choice(list(solved.keys()))

    print(f"Picked Problem {problem_ID}: {solved[problem_ID]}")

    practice["random"] = problem_ID

    save_problems(solved, practice)

    time.sleep(2)
    return


"""
add(): Allows user to add a problem to the list 
"""
def add(solved,practice):
    print(">> ADD")

    ID = get_problem_id()

    if ID is None:
        return

    problem = input("What is the problem name? ").strip()

    # Prevents empty inputs from ruining tracker file
    if not problem:
        print("Error: ID and problem cannot be empty!")
        time.sleep(2)
        return
    
    # Secure duplicate check (Works great with JSON keys!)
    if ID in solved:
        print(f"ID: {ID} Problem: {solved[ID]} already tracker")
        time.sleep(2)
        return
    
    solved[ID] = problem
    save_problems(solved,practice)

    print(f"Adding {problem}!")
    time.sleep(2)
"""
remove(): Allows user to remove a problem from the list
"""
def remove(solved, practice):
    print(">> REMOVE")

    ID = get_problem_id()

    if ID is None:
        return


    # Safely pop first without printing solved[ID] directly (avoids KeyError)
    # Use raw object None (no quotes) as fallback safety net
    removed = solved.pop(ID, None)

    # Checks if ID matches practice "random"
    if ID == practice.get("random"):
        practice["random"] = None

    # Checks if ID matches practice "repractice"
    if ID == practice.get("repractice"):
        practice["repractice"] = None

    # Correct comparison using the Python keyword 'is None' or '== None'
    if removed is None:
        print(f"Problem ID: {ID} not found!")
        time.sleep(2)
        return

    # Safe to print the name since we verified it existed
    print(f"Removing {removed}")

    # Commit the clean dictionary back to JSON file
    save_problems(solved, practice)
    time.sleep(2)
"""
get_problem_id(): Prompts user for problem ID and returns it as an integer. 
If the input is invalid, it returns None.
Enforce the DRY principle by using this function in both add() and remove() functions
to avoid code duplication.
"""
def get_problem_id():

    try: 
        ID = int(input("What is the problem ID? ").strip())
    except ValueError:
        print("Error: Invalid problem ID!")
        time.sleep(2)
        return None

        # Prevent negative problem ID's
    if ID <= 0:
        print("Error: Problem ID must be greater than zero!")
        time.sleep(2)
        return None

    return ID
    

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
def displayWIP(solved, practice):


    print("\nLeetcode problems in progress: ")

    if not solved:
        print("No problems in solved list!")
        time.sleep(2)
        return

    if practice["random"] is None:
        print("No random problem selected!")
    else:
        print(f"Random Selected Problem: {practice['random']}. {solved[practice['random']]}")

    repractice_id = practice.get("repractice")
    repractice_problem = solved.get(repractice_id)

    if repractice_id is None:
        print("No repractice problem selected!")
    else:
        print(f"Repractice: {repractice_id}. {repractice_problem}")

    current_problem = practice.get("current")

    if current_problem is None:
        print("No problem currently in progress, must update by selecting " \
        "'4. Update Leetcode currently in progress'\n")
    else:
        # Remember that json.load() loads tuples to lists
        print(f"Current: {current_problem[0]}. {current_problem[1]}\n")

    print("Paused:")
    if not practice["paused"]:
        print("No paused problems")
    else:
        for ID, problem_name in practice["paused"]:
            print(f"{ID}. {problem_name}")


def switch_problem(solved, practice):
    ID = get_problem_id()

    if ID is None:
        return

    problem = input("What is the problem name? ").strip()

    # Prevents empty inputs from ruining tracker file
    if not problem:
        print("Error: Problem name cannot be empty!")
        time.sleep(2)
        return

    previous_current = practice.get("current")

    if previous_current is not None and ID == previous_current[0]:
        print("Error: This problem is already in progress!")
        return

    # Adds previus_current to practice["paused"] if previous_current is not None and 
    # The problem isn't already in the paused list
    if previous_current is not None and previous_current not in practice["paused"]:
        practice["paused"].append(previous_current)

    practice["current"] = [ID, problem]

    save_problems(solved, practice)

def complete_problem(solved, practice):
    current = practice.get("current")

    if current is None:
        print("Error: No current problem to complete!")
        time.sleep(2)
        return

    ID, problem_name = current

    solved[ID] = problem_name

    practice["repractice"] = ID

    practice["current"] = None

    save_problems(solved, practice)

    print(f"Completed {ID}. {problem_name}! This problem is now repractice")
    time.sleep(2)
    return

def resume_problem(solved, practice):
    if not practice["paused"]:
        print("No paused problems to resume!")
        time.sleep(2)
        return

    ID = get_problem_id()

    if ID is None:
        return

    resumed_problem = None

    for problem_id, problem_name in practice["paused"]:
        if ID == problem_id:
            resumed_problem = [problem_id, problem_name]
            break

    if resumed_problem is None:
        print("Error: Problem not found in paused list!")
        time.sleep(2)
        return

    previous_current = practice.get("current")

    if previous_current is not None and previous_current not in practice["paused"]:
        practice["paused"].append(previous_current)

    practice["paused"].remove(resumed_problem)

    practice["current"] = resumed_problem

    save_problems(solved, practice)

    print(f"Resuming: {resumed_problem[0]}. {resumed_problem[1]}")
    time.sleep(2)
    return

"""
Display the WIP submenu and delegate switching,
completing, or resuming problems to helper functions.
"""
def updateWIP(solved, practice):

    print("\nUpdate WIP")
    print("1. Switch to a new problem")
    print("2. Complete current problem")
    print("3. Resume a paused problem")
    print("4. Return to a main menu")

    choice = input("Select an option: ")

    if choice == "1":
        switch_problem(solved, practice)
        return
        
    elif choice == "2":
        complete_problem(solved, practice)
        return

    # resume a paused problem
    elif choice == "3":
        resume_problem(solved, practice)
        return
        
    elif choice == "4":
        time.sleep(2)
        return
    else:
        print("Invalid selection!")



"""

def exit_program(): Exits the program
"""
def exit_program():
    print("Exiting program...")
    time.sleep(3)
    sys.exit(0)

def load_problems():

    try:
        with open(TRACKER_FILE, "r") as fp:
            data = json.load(fp)

            practice = data.get("practice", {
                "random": None,
                "repractice": None,
                "current": None,
                "paused": []
            })

            practice.setdefault("paused", [])

            solved = data.get("solved", {})

            converted = {}

            for ID, problem in solved.items():
                converted[int(ID)] = problem

            return converted, practice

    except FileNotFoundError:
        return {}, {
            "random": None,
            "repractice": None,
            "current": None,
            "paused": []
        }

def save_problems(solved, practice):

    data = {
        "solved": solved,
        "practice": practice
    }

    with open(TRACKER_FILE, "w") as fp:
        json.dump(data, fp, indent= 4)


def main():

    # tuple unpacking
    solved, practice = load_problems()

    while True:
        displayMenu(solved, practice)

        menu = {
            "1": lambda: pick(solved, practice),
            "2": lambda: add(solved, practice),
            "3": lambda: remove(solved, practice),
            "4": lambda: updateWIP(solved, practice),
            "5": exit_program,
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