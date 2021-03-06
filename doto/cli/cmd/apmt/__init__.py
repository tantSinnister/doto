"""
The command "add" can be used to add a new task to Done!Tools

An example of its use would be
    $ doto add "Document the Add command" "Add still has no doc strings" --difficulty 1

"""
import functools
import doto.cli.parser
import doto.cli.sub_cmds
import doto.model
import doto.model.apmt


COMMAND = 'apmt'
CONF_DEF = {}
sub_cmds = {}


init_parser = functools.partial(doto.cli.sub_cmds.init_sub_cmd,
                                command=COMMAND,
                                module_name=__name__,
                                help="The appointment command")

main = doto.cli.sub_cmds.main(sub_cmds)


def get_cached_apmt(store, cache_id):
    """
    Get the cached appointment with the cache_id from the given store.

    @param store the store that stores all events
    @param cache_id the id of the cached appointments
    """
    cache_item, cache_error = doto.model.get_cache_item(store, cache_id, doto.model.apmt.Appointment)
    if not cache_item:
        if not cache_error:
            print("There is no appointment with the id %d" % cache_id)
            return None, 1

        if doto.model.apmt.get_count(store) > 0:
            print("I don't know which appointment you want!\nYou should first run:\n\tdoto ls")
            return None, 3
        print("There are no appointments.\nMaybe you would first like to add a new appointment with: \n\t doto apmt add \"title\" \"description\" ")
        return None, 2

    return cache_item, 0


def init_apmt_flags(parser):
    """
    Standard option flags for all apmt commands.
    """
    parser.add_argument("--description", type=str, help="The description of the new appointment")
    parser.add_argument("--end", type=str, help="The date when the new appointment will end")
    parser.add_argument("--repeat", type=str, help="The repeat interval of the appointment.")
