from colorama import Fore
from colorama import Style
from textwrap import dedent
from sys import exit
import json
import os.path

LABEL = "Label"
START = "Start Day"
T_ID = "ID"
NOTES = "Notes"
STATUS = "Status"

print(f"{Fore.GREEN}Welcome to guy88-todo{Style.RESET_ALL} v1.5.1")
print(f"{Fore.LIGHTBLUE_EX}Made in {Fore.YELLOW}Python{Style.RESET_ALL}")
print("Remember to be careful when writing a command\n")


def tasks_save(tasks, filename="todo-tasks.json"):
    # Save this file
    f = open(filename, "w")
    j_tasks = []
    for task in tasks:
        j_tasks.append({
            "label": task.label,
            "start_day": task.start_day,
            "task_id": task.task_id,
            "notes": task.notes,
            "status": task.status
        })
    f.write(json.dumps(j_tasks))
    f.close()


def tasks_load(tasks, filename="todo-tasks.json"):
    f = open(filename, "r")
    j_tasks = json.load(f)
    for j_task in j_tasks:
        tasks.append(Task(label=j_task["label"],
                          start_day=j_task["start_day"],
                          task_id=j_task["task_id"],
                          notes=j_task["notes"],
                          status=j_task["status"]))


def tasks_exists(filename="todo-tasks.json"):
    return os.path.isfile(filename)


class Task():
    def __init__(self, label=None, start_day=None, task_id=None, notes=None,
                 status=f"{Fore.RED}incomplete{Style.RESET_ALL}"):
        self.label = label
        self.start_day = start_day
        self.task_id = task_id
        self.notes = notes
        self.status = status


class ScreenSwitch():
    def __init__(self, screen):
        self.screen = screen

    def display(self):
        self.screen.display()

    def switch_screen(self, screen):
        self.screen = screen


class Screen():
    def __init__(self):
        pass

    def display(self):
        pass


class WaitCommand(Screen):

    def __init__(self):
        pass

    def display(self):
        while True:
            cmd = input("Input command (h for help): ")

            if "q" in cmd:
                leave()

            elif "n" in cmd:
                screen_change.switch_screen(add_task)
                screen_change.display()

            elif "h" in cmd:
                screen_change.switch_screen(_help)
                screen_change.display()

            elif "s" in cmd:
                screen_change.switch_screen(show_task)
                screen_change.display()

            elif "d" in cmd:
                screen_change.switch_screen(delete_task)
                screen_change.display()

            elif "c" in cmd:
                screen_change.switch_screen(complete_task)
                screen_change.display()

            elif "i" in cmd:
                screen_change.switch_screen(incomplete_task)
                screen_change.display()

            else:
                print(dedent(f"""
                {Fore.RED}Input a command that exists.\n{Style.RESET_ALL}
                """))


def leave():
    print("Exiting\n")
    exit(0)


class TaskHelp(Screen):

    def __init__(self):
        pass

    def display(self):
        print(dedent(
            """
            Command list
            ------------

            h - open this list
            n - new task
            d - delete task
            s - show tasks
            c - mark task as complete
            i - mark task as incomplete
            q / CTRL + C - quit
            """))

        screen_change.switch_screen(await_cmd)


class AddTask(Screen):

    def __init__(self):
        pass

    def display(self):

        print("What is the label of this task?")
        label = input("> ")

        print("When should this task start? (day)")
        start_day = input("> ")

        print("What is the ID for this task?")
        task_id = input("> ")

        print("Any comments to add?")
        comment = input("> ")

        task = Task(label, start_day, int(task_id), comment)
        tasks.append(task)
        tasks_save(tasks)
        print("Well done! Task made.\n")

        screen_change.switch_screen(await_cmd)


class DeleteTask(Screen):
    def __init__(self):
        pass

    def display(self):
        print("What task do you want to delete?")
        print(f"{Fore.RED}Remember to insert an ID.{Style.RESET_ALL}")

        while True:
            task_choice = input("> ")
            task_id = int(task_choice)
            task_index = self.find_index(task_id)

            if task_index == -1:
                print("Task not found\n")
                break

            tasks.pop(task_index)
            tasks_save(tasks)
            print("Task deleted.\n")
            break

        screen_change.switch_screen(await_cmd)

    def find_index(self, task_id):
        i = 0
        for t in tasks:
            if t.task_id == task_id:
                return i
            i += 1
        return -1


class ShowTasks(Screen):

    def __init__(self):
        pass

    def display(self):
        if len(tasks) > 0:
            print(f"{LABEL:15}{START:13}{T_ID:5}{NOTES:10}\n")
            for t in tasks:
                print(f"{t.label:15}{t.start_day:10}{t.task_id:5}{t.notes}")
                print(f"This task is {t.status}")

            print("=" * 10)

            screen_change.switch_screen(await_cmd)

        else:
            print(dedent(f"""{Fore.RED}There seems to be no task registered yet
            {Style.RESET_ALL}"""))
            screen_change.switch_screen(await_cmd)


class CompleteTask(Screen):
    def __init__(self):
        pass

    def display(self):
        print("What task will you mark as complete?")
        print(f"{Fore.RED}Remember to insert an ID.{Style.RESET_ALL}")

        while True:
            task_choice = input("> ")
            task_id = int(task_choice)
            task_index = self.find_index(task_id)

            if task_index == -1:
                print("Task not found\n")
                break

            self.set_as_complete(task_index)
            tasks_save(tasks)
            print("Marked as complete.\n")
            break

    def find_index(self, task_id):
        i = 0
        for t in tasks:
            if t.task_id == task_id:
                return i
            i += 1
        return -1

    def set_as_complete(self, task_index):
        task = tasks[task_index]
        task.status = f"{Fore.GREEN}complete{Style.RESET_ALL}"


class IncompleteTask(Screen):
    def __init__(self):
        pass

    def display(self):
        print("What task will you mark as incomplete?")
        print(f"{Fore.RED}Remember to insert an ID.{Style.RESET_ALL}")

        while True:
            task_choice = input("> ")
            task_id = int(task_choice)
            task_index = self.find_index(task_id)

            if task_index == -1:
                print("Task not found\n")
                break

            self.set_as_incomplete(task_index)
            tasks_save(tasks)
            print("Marked as incomplete.\n")
            break

    def find_index(self, task_id):
        i = 0
        for t in tasks:
            if t.task_id == task_id:
                return i
            i += 1
        return -1

    def set_as_incomplete(self, task_index):
        task = tasks[task_index]
        task.status = f"{Fore.RED}incomplete{Style.RESET_ALL}"


tasks = []

await_cmd = WaitCommand()
add_task = AddTask()
delete_task = DeleteTask()
show_task = ShowTasks()
complete_task = CompleteTask()
incomplete_task = IncompleteTask()
_help = TaskHelp()
task = Task()
screen_change = ScreenSwitch(await_cmd)


def main():
    global tasks
    if tasks_exists():
        tasks_load(tasks)

    screen_change.display()


if __name__ == "__main__":
    main()
