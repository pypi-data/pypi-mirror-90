import json

import click

from freeldep.modules.utils import file_exists
from freeldep.modules.utils import isdir
from freeldep.modules.utils import list_files
from freeldep.modules.utils import read_json


@click.group()
@click.pass_obj
def show(ctx):
    """show Freeldep variables"""
    pass


@show.command()
@click.argument("name")
@click.pass_context
def config(ctx, name):
    """Display resources used by a deployer"""
    home_folder = ctx.obj.config.get("cli", "home_folder", "~/.freeldep")
    config_file = home_folder + "/" + name + ".json"
    if file_exists(config_file):
        config = read_json(config_file)
        click.echo(json.dumps(config, indent=4))
    else:
        raise click.BadParameter(f"This deployer {name} does not exist")


@show.command()
@click.pass_context
def configs(ctx):
    """List all deployers already initialized"""
    home_folder = ctx.obj.config.get("cli", "home_folder", "~/.freeldep")
    if isdir(home_folder):
        config_files = list_files(home_folder)
        click.echo("\n".join([x.split(".")[0] for x in config_files]))
