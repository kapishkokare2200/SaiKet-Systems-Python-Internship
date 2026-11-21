
import json
import os

DATA_FILE = "tasks.json"


class Task:
    def __init__(self, description, completed=False):
        self.description = description
        self.completed = completed

    def to_dict(self):
        return {
            "description": self.description,
            "completed": self.completed
        }

    def __str__(self):
        mark = "[x]" if self.completed else "[ ]"
        return f"{mark} {self.description}"


class TodoList:
    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.tasks = []
        self.load()

    def add(self, description):
        self.tasks.append(Task(description))

    def complete(self, number):
        if 1 <= number <= len(self.tasks):
            self.tasks[number - 1].completed = True
            return True
        return False

    def delete(self, number):
        if 1 <= number <= len(self.tasks):
            self.tasks.pop(number - 1)
            return True
        return False

    def show(self):
        if not self.tasks:
            print("\nYour to-do list is empty")
            return

        print("\n--- Your Tasks ---")

        for i, task in enumerate(self.tasks, start=1):
            print(f"{i}. {task}")

        done = sum(task.completed for task in self.tasks)
        print(f"({done}/{len(self.tasks)} completed)")

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(
                [task.to_dict() for task in self.tasks],
                file,
                indent=2
            )

    def load(self):
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.tasks = [
                Task(item["description"], item["completed"])
                for item in data
            ]

        except (json.JSONDecodeError, KeyError, OSError):
            print("Warning: Unable to load saved tasks")


def ask_number(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        return -1


def main():
    todo = TodoList()

    menu = """
===== TO-DO LIST =====
1. Add task
2. View tasks
3. Mark task as completed
4. Delete task
5. Exit
"""

    while True:
        print(menu)
        choice = input("Choose an option (1-5):- ").strip()

        if choice == "1":
            description = input("Task description:- ").strip()

            if description:
                todo.add(description)
                todo.save()
                print("Task added successfully")
            else:
                print("Description cannot be empty")

        elif choice == "2":
            todo.show()

        elif choice == "3":
            todo.show()

            if todo.tasks:
                number = ask_number("Task number to complete ")

                if todo.complete(number):
                    todo.save()
                    print("Task marked as completed")
                else:
                    print("Invalid task number")

        elif choice == "4":
            todo.show()

            if todo.tasks:
                number = ask_number("Task number to delete:- ")

                if todo.delete(number):
                    todo.save()
                    print("Task deleted successfully")
                else:
                    print("Invalid task number")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Please enter a number from 1 to 5")


if __name__ == "__main__":
    main()
