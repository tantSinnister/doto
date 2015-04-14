# -*- coding: utf-8 -*-
"""
The command

An example of its use would be
$ doto modify id  [--title <string>] [--description <string>]  [--due <date>]  [--difficulty <int>]

"""
import cli.parser
import cli.util
import cli.cmd.task


COMMAND = "modify"
CONF_DEF = {}

RESET = "RESET"


def init_parser(subparsers):
    """
    Init the parser

    It adds the id argument to the argument parser
    """
    parser = subparsers.add_parser(COMMAND, help="")
    parser.add_argument("id", type=int, help="The id of the task which should be modified.")
    parser.add_argument("--title", type=cli.parser.to_unicode, help="Change the title of the task")
    parser.add_argument("--description", type=cli.parser.to_unicode, help="Change the description of the task")
    cli.cmd.task.init_task_flags(parser)


def set_or_reset(value, fnc=lambda x: x):
    """
    Check if a value is should be set or reset

    If the given value is equal to "RESET" the set the value to None
    else use the function fnc to set it to the return value of fnc.

    @param value the value that schould be tested
    @param fnc a function that can be used to convert the value. Default=identity function
    """
    if value == RESET:
        return None
    return fnc(value)


def main(store, args, config, _):
    """ The Main method of start."""

    modify_task, error = cli.cmd.task.get_cached_task(store, args.id)
    if not modify_task:
        return error
    cli.util.uprint(("Changing task " + cli.util.ID_FORMAT + ":\n\t %s") % (args.id, modify_task.event_id, modify_task.title))
    if args.title is not None:
        modify_task.title = args.title
    if args.description is not None:
        modify_task.description = args.description
    if args.due is not None:
        modify_task.due = set_or_reset(args.due, cli.parser.date_parser)
    if args.difficulty is not None:
        modify_task.difficulty = args.difficulty

    try:
        store.save()
    except:
        cli.util.uprint(("It was not possible to modify the task with id " + cli.util.ID_FORMAT + ":\n\t %r") % (args.id, modify_task.event_id))
        return 4

    cli.util.uprint(("You modified:\n\t(" + cli.util.ID_FORMAT + ") %s") % (args.id, modify_task.event_id, modify_task.title))
    return 0