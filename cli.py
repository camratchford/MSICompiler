import logging
import sys

import click

from msi_compiler.config import Config
from msi_compiler.__main__ import main
from msi_compiler.exceptions import MsiCompilerException

stderr_handler = logging.StreamHandler()
stderr_handler.setLevel(logging.ERROR)
stderr_formatter = logging.Formatter('%(levelname)s - %(message)s')
stderr_handler.setFormatter(stderr_formatter)
logging.basicConfig(
    level="INFO",
    format='%(levelname)s - %(message)s',
    datefmt="[%X]",
    handlers=[stderr_handler],
)
logger = logging.getLogger(__name__)

@click.command
@click.option(
    "-c",
    "--config-file",
    type=click.Path(file_okay=True, dir_okay=False, resolve_path=True),
    help="The location of the yaml configuration file",
    required=False,
)
def run(config_file: str):
    config = Config.from_file(config_file)
    main(config)


if getattr(sys, 'frozen', False):
    run.invoke(run.make_context(info_name="MsiCompiler", args=sys.argv[1:]))
    # try:
    #
    #
    # except click.exceptions.Exit as code:
    #     if code == 0:
    #         pass

    # except MsiCompilerException as e:
    #     logger.log(e.level, e.message)
    #     if e.exit_code:
    #         sys.exit(e.exit_code)
