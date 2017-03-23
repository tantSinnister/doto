# -*- coding: utf-8 -*-
"""
The command "add" can be used to add a new task to Done!Tools

An example of its use would be
    $ doto apmt add "Document the Add command" "Add still has no doc strings" --difficulty 1

"""
import doto.model
import doto.model.apmt
import doto.cli.parser


COMMAND = "add"
CONF_DEF = {}


def init_parser(subparsers):
    """Initialise the subparser for Add"""
    parser = subparsers.add_parser(COMMAND, help="Add a new appointment.")
    parser.add_argument("title", type=doto.cli.parser.to_unicode, help="The title of the new appointment")
    parser.add_argument("start", type=doto.cli.parser.to_unicode, help="The date when the new appointment will start")
    doto.cli.cmd.apmt.init_apmt_flags(parser)


def print_error(message, exc):
    print(("{}\n\t (Error: {})".format(message, exc)))


def main(store, args, config, _):
    """Add a new appointment with the given args"""
    start = doto.cli.parser.date_parser(args.start)
    new_apmt = doto.model.apmt.Appointment(args.title, start)
    if args.end is not None:
        try:
            new_apmt.schedule.end = doto.cli.parser.date_parser(args.end)
        except ValueError as e:
            print_error("Mhh, looks like the end date is wrong.", e)
            return 5
    if args.description is not None:
        new_apmt.description = args.description
    doto.model.apmt.add_new(store, new_apmt)
    try:
        store.save()
    except Exception as e:
        print_error("It was not possible to save the new appointment", e)
        return 4
    return 0
