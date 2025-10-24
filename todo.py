import argparse
import json
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
config_data = config['DEFAULT']

def sort_argument_checker(v):
    valid_values = ['s', 'p', 'd']
    if v not in valid_values:
        raise argparse.ArgumentTypeError('Wrong value!!! Accepted values: "p" - priority; "s" - status; "d" - due date')
    return v

class Todo_List:
    
    def __init__(self):
        self.todo_file = config_data['file_path'] + '/' + config_data['file_name']

    def sort_todo_list(self, field):
        fields = {
            'p': 'priority',
            's': 'status',
            'd': 'due_date'
        }
        with open(self.todo_file, mode='r') as f:
            data = json.load(f)
            sorted_list = sorted(data['resources'], key=lambda r: r[fields[field[0]]], reverse=False)
            sorted_dict = {
                'resources' : sorted_list
            }
        for count, todo in enumerate(sorted_dict['resources']):
            print(f"[{count}] \u23f5 {todo['todo']} | {todo['priority']} | {todo['status']} | {todo['due_date']}")

    def display_todo_list(self):
        with open(self.todo_file, 'r') as f:
            data = json.load(f)
            for count, todo in enumerate(data['resources']):
                print(f"[{count}] \u23f5 {todo['todo']} | {todo['priority']} | {todo['status']} | {todo['due_date']}")


    def delete_item(self, n):
        with open(self.todo_file, mode='r') as f:
            data = json.load(f)
        try:
            del data['resources'][n-1]
            with open(self.todo_file, mode='w') as f:              
                json.dump(data, f, indent=2)
        except(IndexError):
            print("There's no such todo item")

    def add_item(self, todo, priority, status, due_date):
        data = {
            'todo': todo,
            'priority': priority,
            'status': status,
            'due_date': due_date
        }
        with open(self.todo_file, mode='r') as f:
            existing_json = json.load(f)
            existing_json['resources'].append(data)
        with open(self.todo_file, mode='w') as f:
            json.dump(existing_json, f, indent=2)

    def complete_item(self, n):
        with open(self.todo_file, mode='r') as f:
            data = json.load(f)
            if n > len(data['resources']):
                print("You are trying to complete non-existing todo item. Enter valid number: \n")
                self.display_todo_list()
            else:
                with open(self.todo_file, mode='w') as f:
                    data['resources'][n-1]['status'] = "Completed"
                    json.dump(data, f, indent=2)

    def edit_item(self, n, data, todo='', priority='', status='', due_date=''):       
                if len(todo) > 0:
                    data['resources'][n-1]['todo'] = todo
                if len(priority) > 0:
                    data['resources'][n-1]['priority'] = priority
                if len(status) > 0:
                    data['resources'][n-1]['status'] = status
                if len(due_date) > 0:
                    data['resources'][n-1]['due_date'] = due_date
                
                with open(self.todo_file, mode='w') as f:
                    json.dump(data, f, indent=2)
        

todo_list = Todo_List()

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-l','--list', action="store_true",help='Display todo list')
    parser.add_argument('-d','--delete',metavar=' ', help='Delete item from todo list')
    parser.add_argument('-a','--add', action='store_true',help='Add todo item to the list')
    parser.add_argument('-c','--complete', nargs = 1, metavar=' ',help='Comlete todo item')
    parser.add_argument('-e','--edit', nargs=1, metavar='', type=int, help='Edit todo item. Enter the list number you want to edit')
    parser.add_argument('-s','--sort', nargs=1, metavar='', type=sort_argument_checker, help='Sort todo list by a column. Accepts values "p" - priority; "s" - status; "d" - due date')

    args = parser.parse_args()

    if args.list:
        data = todo_list.display_todo_list()
    elif args.delete:
        to_delete = int(args.delete)
        todo_list.delete_item(to_delete)
        todo_list.display_todo_list()
    elif args.add:
        todo = input("Todo: ")
        priority = input("Priority: ")
        status = input("Status: ")
        due_date = input("Due Date: ")
        todo_list.add_item(todo, priority, status, due_date)
        todo_list.display_todo_list()
    elif args.complete:
        todo_list.complete_item(int(args.complete[0]))
        todo_list.display_todo_list()
    elif args.edit:
        with open(todo_list.todo_file, mode='r') as f:
            data = json.load(f)
            if args.edit[0] > len(data['resources']):
                print("There's no such todo item. Please enter valid number: \n")
                todo_list.display_todo_list()
            else:
                todo = input("Todo: ")
                priority = input("Priority: ")
                status = input("Status: ")
                due_date = input("Due_date: ")
                todo_list.edit_item(int(args.edit[0]), data, todo, priority, status, due_date)
                todo_list.display_todo_list()        
    elif args.sort:
        todo_list.sort_todo_list(args.sort)

if __name__ == '__main__':
    main()
