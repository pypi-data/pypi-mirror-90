import click

import dada_settings
import dada_client
import dada_file
from dada_types import T
from dada_utils import etc, path
from dada_log import DadaLogger

log = DadaLogger()


# default context settings (https://click.palletsprojects.com/en/7.x/advanced/#token-normalization)
CONTEXT_SETTINGS = dict(
    token_normalize_func=lambda x: x.lower().replace("_", "-").strip(),
    ignore_unknown_options=True,
)


@click.group("file")
def dada_file_cli():
    pass


# @click.argument('timeit_args', nargs=-1, type=click.UNPROCESSED)


@click.command(context_settings=CONTEXT_SETTINGS)
def setup():
    # TODO
    log.info("Setup configurations for local && global store")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("filepath")
@click.option(
    "-o",
    "--out",
    default=False,
    help="Whether or not to print the results of the put operationn to stdout as json",
    type=bool,
    is_flag=True,
)
def put(filepath, out):
    """"""
    if not path.is_dir(filepath):
        filepath = [filepath]
    else:
        filepath = path.list_files(filepath)

    for fp in filepath:
        log.info(f"Saving file {fp} to local stor")
        df = dada_file.load(fp)
        df.save_locally()
        log.info(f"File is now located at '{df.urls.loc.file.version}'")
        if out:
            log.stdout(df.to_json())


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("filepath")
def share(filepath):
    #
    log.info("Hello %s!" % filepath)


@click.command(context_settings=CONTEXT_SETTINGS)
def get():
    log.info("Fetching a file from local || global store")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-i", "--id", type=str)
@click.option("-k", "--check-sum", type=str)
@click.option("-g", "--slug", type=str)
@click.option("-e", "--entity-type", type=str)
@click.option("-t", "--file-type", type=str)
@click.option("-s", "--file-subtype", type=str)
@click.option("-x", "--ext", type=str)
@click.option("-c", "--created_at", type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"]))
@click.option("-cy", "--created-year2", type=str)
@click.option("-cm", "--created-month", type=str)
@click.option("-cd", "--created-day", type=str)
@click.option("-u", "--updated-at", type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"]))
@click.option("-uy", "--updated-year2", type=str)
@click.option("-um", "--updated-month", type=str)
@click.option("-ud", "--updated-day", type=str)
@click.option("-uh", "--updated-hour", type=str)
@click.option(
    "-o",
    "--out",
    default=False,
    help="Whether or not to print the results of the put operationn to stdout as json",
    type=bool,
    is_flag=True,
)
@click.option(
    "-l",
    "--latest",
    default=False,
    help="Whether or not to only include the latest version of the file",
    type=bool,
    is_flag=True,
)
def find_local(**kwargs):
    kwargs = etc.dict_filter_nulls(kwargs)
    log.info(f"searching for files in local store with kwargs {kwargs}")
    for df in dada_file.find_in_local_store(**kwargs):
        log.info(f"{df.urls.loc.file.version}")
        if kwargs.get("out", False):
            log.stdout(df.to_json())


@click.command(context_settings=CONTEXT_SETTINGS)
def rm():
    log.info("Delete files from local &&|| global store")


dada_file_cli.add_command(setup)
dada_file_cli.add_command(put)
dada_file_cli.add_command(share)
dada_file_cli.add_command(get)
dada_file_cli.add_command(find_local)
dada_file_cli.add_command(rm)


cli = click.CommandCollection(sources=[dada_file_cli])
