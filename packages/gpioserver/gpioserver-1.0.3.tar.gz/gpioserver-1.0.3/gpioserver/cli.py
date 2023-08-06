from gpioserver.app import run_app

import argparse
import sys, os

def add_argument(parser, argv, name, split_by = False, **opts):
    parser.add_argument("--" + name, **opts)

    try:
        value = os.environ['GPIOSERVER_%s' % name.replace('-', '_').upper()]
    except KeyError:
        value = None

    if value:
        argv.append("--" + name)
        argv.append(value)

def make_mode_validator(mode):
    def gpio(v):
        return (
            tuple(map(int, v.split(','))),
            mode
        )
    return gpio

def get_parser_with_env():

    parser = argparse.ArgumentParser(prog="Run a rest api to control GPIO")

    args = []

    add_argument(parser, args, "port", default=None, help="Insert the port.")
    add_argument(parser, args, "host", default=None, help="Insert the host.")
    add_argument(
        parser, args, "mode", default=None, type=int, help="Insert board mode, defaults to BCM"
    )
    add_argument(
        parser, args, "debug", action="store_true", help="Run in debug mode, all operations are faked."
    )
    add_argument(
        parser, args, "max-wait", dest="max_wait", type=int, help="Insert the maximum time for the wait command, defaults to 2000."
    )
    for mode in (
        "input",
        "input-pull-up",
        "input-pull-down",
        "output",
        "output-low",
        "output-high",
    ):
        add_argument(
            parser, args, mode, dest='gpio_modes', action='append', type=make_mode_validator(mode), nargs="*", default=None
        )

    return parser, args 

def main(argv=sys.argv[1:], **opts):

    parser, args = get_parser_with_env()

    cmd_options = vars(parser.parse_args(args + argv))

    #unpacking gpio_modes

    cmd_options['gpio_modes'] = dict((c, mode.replace('-', '_')) for a in (cmd_options['gpio_modes'] or ()) for b, mode in a for c in b)

    return run_app(**cmd_options)