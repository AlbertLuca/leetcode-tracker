# LeetCode Tracker CLI

A Python command-line application for tracking LeetCode problems, managing problems in progress, and reviewing previously solved problems.

I built this project to practice Python fundamentals, data structures, file handling, and program state management while creating a tool I could use for my own LeetCode practice.

## Features

- Add and remove solved LeetCode problems.
- Randomly select previously solved problems for review.
- Track the current problem in progress.
- Pause unfinished problems and resume them later.
- Mark problems as completed and add them to the solved list.
- Save and load progress using JSON.
- Validate user input and handle invalid selections.
- Organize program functionality into reusable functions.

## Technologies

- **Python 3** — Application logic and command-line interface.
- **JSON** — Persistent storage for solved problems and practice progress.
- **Git and GitHub** — Version control and project management.

## Getting Started

1. Clone the repository.
2. Navigate to the project directory.
3. Run the application:

```bash
python problemGen.py
```

The application provides an interactive menu for managing problems and reviewing progress.

Progress is stored locally in `tracker.json` and loaded when the program starts.

## What I Learned

### 1. Python Functions and Lambda Expressions

I learned how to use functions as dictionary values to select different operations.

```python
def greet(name):
    print(f"Hello, {name}!")

def goodbye():
    print("Goodbye!")

name = "Lucas"

actions = {
    "1": lambda: greet(name),
    "2": goodbye
}

action = actions.get("1")

if action:
    action()
```

The lambda expression acts as a zero-argument wrapper around `greet(name)`. It delays the function call until the selected action is executed.

I also learned that Python functions can be stored and passed around like other objects.

### 2. JSON Persistence

I learned how to save Python dictionaries to a JSON file and load them again when the application restarts.

```python
import json

# Write data to a JSON file
with open("tracker.json", "w") as fp:
    json.dump(data, fp, indent=4)

# Read data from a JSON file
with open("tracker.json", "r") as fp:
    data = json.load(fp)
```

Saving updated program state to a file allows progress to persist between sessions.

I also learned that JSON object keys are strings, so integer dictionary keys must be converted back to integers after loading when the application expects integer IDs.

### 3. Lists and Dictionaries

This project helped me better understand how to access and modify nested data structures.

For example:

```python
practice["paused"].append(previous_current)
```

This statement:

1. Accesses the `"paused"` key in the `practice` dictionary.
2. Retrieves the list associated with that key.
3. Appends the previous problem to the list.

I also practiced iter