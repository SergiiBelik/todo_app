import argparse
import json

def sort_argument_checker(v):
    valid_values = ['s', 'p', 'd']
    if v not in valid_values:
        raise argparse.ArgumentTypeError('Wrong value!!! Accepted values: "p" - priority; "s" - status; "d" - due date')
    return v

parser = argparse.ArgumentParser()

parser.add_argument('-l','--list', action="store_true",help='Display todo list')
parser.add_argument('-d','--delete',metavar=' ', help='Delete item from todo list')
parser.add_argument('-a','--add', nargs=4, metavar=' ',help='Add todo item to the list. Accepts 4 arguments: todo,priority,status,due date')
parser.add_argument('-c','--complete', nargs = 1, metavar=' ',help='Comlete todo item')
parser.add_argument('-e','--edit', nargs=1, metavar='', help='Edit todo item')
parser.add_argument('-s','--sort', nargs=1, metavar='', type=sort_argument_checker, help='Sort todo list by a column. Accepts values "p" - priority; "s" - status; "d" - due date')

args = parser.parse_args()

# todo item should have the following attributes:
# - todo
# - due_date
# - status
# - priority
class Todo_List:
    todo_file = '/Users/sergii.biletskyi/Misc/AI/ai_learning_env/todo_app/todos.json'

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
        with open(self.todo_file, mode='w') as f:
            json.dump(sorted_dict, f, indent=2)

    def display_todo_list(self):
        with open(self.todo_file, 'r') as f:
            data = json.load(f)
            count = 1
            for todo in data['resources']:
                print(f"[{count}] \u23f5 {todo['todo']} | {todo['priority']} | {todo['status']} | {todo['due_date']}")
                count += 1


    def delete_item(self, n):
        with open(self.todo_file, mode='r') as f:
            data = json.load(f)
        with open(self.todo_file, mode='w') as f:
            del data['resources'][n-1]
            json.dump(data, f)

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
        data['resources'][n-1]['status'] = "Completed"
        with open(self.todo_file, mode='w') as f:
            json.dump(data, f, indent=2)
    def edit_item(self, n, todo='', priority='', status='', due_date=''):
        with open(self.todo_file, mode='r') as f:
            data = json.load(f)
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

if args.list:
    data = todo_list.display_todo_list()
elif args.delete:
    to_delete = int(args.delete)
    todo_list.delete_item(to_delete)
    todo_list.display_todo_list()
elif args.add:
    todo = args.add[0]
    priority = args.add[1]
    status = args.add[2]
    due_date = args.add[3]
    todo_list.add_item(todo, priority, status, due_date)
    todo_list.display_todo_list()
elif args.complete:
    todo_list.complete_item(int(args.complete[0]))
    todo_list.display_todo_list()
elif args.edit:
    todo = input("Todo: ")
    priority = input("Priority: ")
    status = input("Status: ")
    due_date = input("Due_date: ")

    todo_list.edit_item(int(args.edit[0]), todo, priority, status, due_date)
    todo_list.display_todo_list()
elif args.sort:
    todo_list.sort_todo_list(args.sort)
    todo_list.display_todo_list()


