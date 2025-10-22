import pytest
import argparse
import json
from unittest import mock
from todo import Todo_List, sort_argument_checker

@pytest.fixture
def todo_list():
    todo_list = Todo_List()
    yield todo_list
    with open(todo_list.todo_file, mode='r') as f:
        data = json.load(f)
    todo_list.delete_item(len(data['resources']))

@pytest.mark.parametrize("invalid_input", ['a','b','K','',1,[],None,{}])
def test_invalid_arguments_in_sort_function_checker(invalid_input):
    with pytest.raises(argparse.ArgumentTypeError):
        sort_argument_checker(invalid_input)

@pytest.mark.parametrize("valid_input",['s','p','d'])
def test_valid_arguments_in_sort_function_checker(valid_input):
    assert sort_argument_checker(valid_input) == valid_input

def test_add_item(todo_list):
    with open(todo_list.todo_file, mode='r') as f:
        data = json.load(f)
    assert len(list(filter(lambda item: item['todo'] == 'test', data['resources']))) == 0

    todo_list.add_item('test', 'test', 'test', '0000-00-00')

    with open(todo_list.todo_file, mode='r') as f:
        data = json.load(f)
    assert len(list(filter(lambda item: item['todo'] == 'test', data['resources']))) > 0

@mock.patch("builtins.open", new_callable=mock.mock_open, read_data='{"resources": [{"todo": "TEST", "due_date": "0000-00-00", "status": "Completed", "priority": "High"}]}')
@mock.patch("todo.json.dump")
def test_delete_item(mock_dump, mock_open, capsys):
    todo_list = Todo_List()
    todo_list.delete_item(1)

    expected_data = {"resources": []}

    mock_dump.assert_called_once_with(expected_data, mock.ANY, indent=2)

@mock.patch("builtins.open", new_callable=mock.mock_open, read_data='{"resources":[]}')
def test_deletion_error_handling(mock_open,capsys):
    todo_list = Todo_List()
    todo_list.delete_item(1)

    out = capsys.readouterr()
    assert out.out == "There's no such todo item\n"

