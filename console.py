#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
#from models.user import User
#from models.state import State
#from models.city import City
#from models.place import Place
#from models.amenity import Amenity
#from models.review import Review


def parse_arguments(argument):
    curly_brace_match = re.search(r"\{(.*?)\}", argument)
    bracket_match = re.search(r"\[(.*?)\]", argument)
    if curly_brace_match is None:
        if bracket_match is None:
            return [item.strip(",") for item in split(argument)]
        else:
            lexer_split = split(argument[:bracket_match.span()[0]])
            result_list = [item.strip(",") for item in lexer_split]
            result_list.append(bracket_match.group())
            return result_list
    else:
        lexer_split = split(argument[:curly_brace_match.span()[0]])
        result_list = [item.strip(",") for item in lexer_split]
        result_list.append(curly_brace_match.group())
        return result_list


class HBNBCommand(cmd.Cmd):
    """HBnB command interpreter Definition.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    supported_classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, argument):
        """Default behavior for cmd module when input is invalid"""
        command_map = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        dot_match = re.search(r"\.", argument)
        if dot_match is not None:
            argument_list = [argument[:dot_match.span()[0]], argument[dot_match.span()[1]:]]
            command_match = re.search(r"\((.*?)\)", argument_list[1])
            if command_match is not None:
                command = [argument_list[1][:command_match.span()[0]], command_match.group()[1:-1]]
                if command[0] in command_map.keys():
                    command_string = "{} {}".format(argument_list[0], command[1])
                    return command_map[command[0]](command_string)
        print("*** Unknown syntax: {}".format(argument))
        return False

    def do_quit(self, argument):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, argument):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, argument):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        argument_list = parse_arguments(argument)
        if len(argument_list) == 0:
            print("** class name missing **")
        elif argument_list[0] not in HBNBCommand.supported_classes:
            print("** class doesn't exist **")
        else:
            print(eval(argument_list[0])().id)
            storage.save()

    def do_show(self, argument):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        argument_list = parse_arguments(argument)
        object_dict = storage.all()
        if len(argument_list) == 0:
            print("** class name missing **")
        elif argument_list[0] not in HBNBCommand.supported_classes:
            print("** class doesn't exist **")
        elif len(argument_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argument_list[0], argument_list[1]) not in object_dict:
            print("** no instance found **")
        else:
            print(object_dict["{}.{}".format(argument_list[0], argument_list[1])])

    def do_destroy(self, argument):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        argument_list = parse_arguments(argument)
        object_dict = storage.all()
        if len(argument_list) == 0:
            print("** class name missing **")
        elif argument_list[0] not in HBNBCommand.supported_classes:
            print("** class doesn't exist **")
        elif len(argument_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argument_list[0], argument_list[1]) not in object_dict.keys():
            print("** no instance found **")
        else:
            del object_dict["{}.{}".format(argument_list[0], argument_list[1])]
            storage.save()

    def do_all(self, argument):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        argument_list = parse_arguments(argument)
        if len(argument_list) > 0 and argument_list[0] not in HBNBCommand.supported_classes:
            print("** class doesn't exist **")
        else:
            object_list = []
            for obj in storage.all().values():
                if len(argument_list) > 0 and argument_list[0] == obj.__class__.__name__:
                    object_list.append(obj.__str__())
                elif len(argument_list) == 0:
                    object_list.append(obj.__str__())
            print(object_list)

    def do_count(self, argument):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argument_list = parse_arguments(argument)
        count = 0
        for obj in storage.all().values():
            if argument_list[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, argument):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argument_list = parse_arguments(argument)
        object_dict = storage.all()

        if len(argument_list) == 0:
            print("** class name missing **")
            return False
        if argument_list[0] not in HBNBCommand.supported_classes:
            print("** class doesn't exist **")
            return False
        if len(argument_list) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argument_list[0], argument_list[1]) not in object_dict.keys():
            print("** no instance found **")
            return False
        if len(argument_list) == 2:
            print("** attribute name missing **")
            return False
        if len(argument_list) == 3:
            try:
                type(eval(argument_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argument_list) == 4:
            obj = object_dict["{}.{}".format(argument_list[0], argument_list[1])]
            if argument_list[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argument_list[2]])
                obj.__dict__[argument_list[2]] = valtype(argument_list[3])
            else:
                obj.__dict__[argument_list[2]] = argument_list[3]
        elif type(eval(argument_list[2])) == dict:
            obj = object_dict["{}.{}".format(argument_list[0], argument_list[1])]
            for key, value in eval(argument_list[2]).items():
                if (key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = valtype(value)
                else:
                    obj.__dict__[key] = value
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
  
