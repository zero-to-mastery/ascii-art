import csv
import os

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists("tasks.csv"):
            with open("tasks.csv", "r") as file:
                csv_reader = csv.reader(file)
                next(csv_reader)
                self.tasks = list(csv_reader)

    def save_tasks(self):
        with open("tasks.csv", "w", newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["Task", "Description", "Due Date"])
            csv_writer.writerows(self.tasks)

    def add_task(self, task, description, due_date):
        self.tasks.append([task, description, due_date])
        self.save_tasks()

    def view_tasks(self):
        if self.tasks:
            print("\nTasks:")
            for index, task in enumerate(self.tasks, 1):
                print(f"{index}. Task: {task[0]}\n   Description: {task[1]}\n   Due Date: {task[2]}")
        else:
            print("\nNo tasks found.")

    def update_task(self, index, task, description, due_date):
        if 1 <= index <= len(self.tasks):
            self.tasks[index - 1] = [task, description, due_date]
            self.save_tasks()
        else:
            print("Invalid task index. No task updated.")

    def delete_task(self, index):
        if 1 <= index <= len(self.tasks):
            deleted_task = self.tasks.pop(index - 1)
            self.save_tasks()
            print(f"Deleted task: {deleted_task}")
        else:
            print("Invalid task index. No task removed.")

if __name__ == "__main__":
    task_manager = TaskManager()

    while True:
        print("\nHacktoberTaskManager")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            task = input("Enter task name: ")
            description = input("Enter task description: ")
            due_date = input("Enter due date: ")
            task_manager.add_task(task, description, due_date)
        elif choice == "2":
            task_manager.view_tasks()
        elif choice == "3":
            index = int(input("Enter the task index to update: "))
            task = input("Enter updated task name: ")
            description = input("Enter updated task description: ")
            due_date = input("Enter updated due date: ")
            task_manager.update_task(index, task, description, due_date)
        elif choice == "4":
            index = int(input("Enter the task index to delete: "))
            task_manager.delete_task(index)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")
