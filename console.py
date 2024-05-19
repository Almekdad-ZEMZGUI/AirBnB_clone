#!/usr/bin/python3
"""
Entry to CMD
"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """
    Entry to command interpreter
    """
    prompt = "(hbnb) "
    classes = {"BaseModel", "State", "City",
               "Amenity", "Place", "Review", "User"}

    def do_EOF(self, line):
        """
        Exit on Ctrl-D
        """
        print()
        return True

    def do_quit(self, line):
        """
        Exit on quit
        """
        return True

    def emptyline(self):
        """
        Overwrite default behavior
        """
        pass

    def do_create(self, line):
        """
        Create instance
        """
        if len(line) == 0:
            print("** class name missing **")
        elif line not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            instance = eval(line)()
            instance.save()
            print(instance.id)

    def do_show(self, line):
        """
        Print string representation
        """
        if len(line) == 0:
            print("** class name missing **")
            return
        args = parse(line)
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        try:
            if args[1]:
                name = "{}.{}".format(args[0], args[1])
                if name not in storage.all().keys():
                    print("** no instance found **")
                else:
                    print(storage.all()[name])
        except IndexError:
            print("** instance id missing **")

    def do_destroy(self, line):
        """
        Destroy instance
        """
        if len(line) == 0:
            print("** class name missing **")
            return
        args = parse(line)
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        try:
            if args[1]:
                name = "{}.{}".format(args[0], args[1])
                if name not in storage.all().keys():
                    print("** no instance found **")
                else:
                    del storage.all()[name]
                    storage.save()
        except IndexError:
            print("** instance id missing **")

    def do_all(self, line):
        """
        Print all objects
        """
        args = parse(line)
        obj_list = []
        if len(line) == 0:
            for objs in storage.all().values():
                obj_list.append(objs)
            print(obj_list)
        elif args[0] in HBNBCommand.classes:
            for k, objs in storage.all().items():
                if args[0] in k:
                    obj_list.append(objs)
            print(obj_list)
        else:
            print("** class doesn't exist **")

    def do_update(self, line):
        """Updates an instance based on the class name and id by adding or updating attribute"""
        args = parse(line)
        try:
            if not args:
                raise ValueError("** class name missing **")
            args_list = args.split()
            if len(args_list) < 2:
                raise ValueError("** instance id missing **")
            if len(args_list) < 3:
                raise ValueError("** attribute name missing **")
            if len(args_list) < 4:
                raise ValueError("** value missing **")

            class_name = args_list[0]
            instance_id = args_list[1]
            attribute_name = args_list[2]
            attribute_value = args_list[3].strip('"')

            if class_name not in self.classes:
                raise ValueError("** class doesn't exist **")

            key = "{}.{}".format(class_name, instance_id)
            instance = storage.all().get(key)
            if not instance:
                raise ValueError("** no instance found **")

            if attribute_name in ['id', 'created_at', 'updated_at']:
                return

            attr_type = type(getattr(instance, attribute_name, str))
            try:
                attribute_value = attr_type(attribute_value)
            except ValueError:
                print("** wrong value type **")
                return

            setattr(instance, attribute_name, attribute_value)
            instance.save()

        except ValueError as e:
            print(e)

    def do_count(self, line):
        """
        Display
        """
        if line in HBNBCommand.classes:
            count = 0
            for key, objs in storage.all().items():
                if line in key:
                    count += 1
            print(count)
        else:
            print("** class doesn't exist **")

    def default(self, line):
        """
        Accepts class name followed by args
        """
        args = line.split('.')
        class_arg = args[0]
        if len(args) == 1:
            print("*** Unknown syntax: {}".format(line))
            return
        try:
            args = args[1].split('(')
            command = args[0]
            if command == 'all':
                HBNBCommand.do_all(self, class_arg)
            elif command == 'count':
                HBNBCommand.do_count(self, class_arg)
            elif command == 'show':
                args = args[1].split(')')
                id_arg = args[0]
                id_arg = id_arg.strip("'")
                id_arg = id_arg.strip('"')
                arg = class_arg + ' ' + id_arg
                HBNBCommand.do_show(self, arg)
            elif command == 'destroy':
                args = args[1].split(')')
                id_arg = args[0]
                id_arg = id_arg.strip('"')
                id_arg = id_arg.strip("'")
                arg = class_arg + ' ' + id_arg
                HBNBCommand.do_destroy(self, arg)
            elif command == 'update':
                args = args[1].split(',')
                id_arg = args[0].strip("'")
                id_arg = id_arg.strip('"')
                name_arg = args[1].strip(',')
                val_arg = args[2]
                name_arg = name_arg.strip(' ')
                name_arg = name_arg.strip("'")
                name_arg = name_arg.strip('"')
                val_arg = val_arg.strip(' ')
                val_arg = val_arg.strip(')')
                arg = class_arg + ' ' + id_arg + ' ' + name_arg + ' ' + val_arg
                HBNBCommand.do_update(self, arg)
            else:
                print("*** Unknown syntax: {}".format(line))
        except IndexError:
            print("*** Unknown syntax: {}".format(line))


def parse(line):
    """
    Helper method
    """
    return tuple(line.split())


if __name__ == "__main__":
    HBNBCommand().cmdloop()
