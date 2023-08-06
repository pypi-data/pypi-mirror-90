"""State Command."""
from .common import create_ebus, disable_stdout_buffering


def parse_args(subparsers):
    """Parse Arguments."""
    parser = subparsers.add_parser("state", help="Show EBUSD state")
    parser.set_defaults(main=_main)


async def _main(args):
    disable_stdout_buffering()
    ebus = create_ebus(args)
    print(await ebus.get_state())
