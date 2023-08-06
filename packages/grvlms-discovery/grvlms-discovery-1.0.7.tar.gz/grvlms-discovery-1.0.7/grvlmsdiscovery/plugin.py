from glob import glob
import os
import click

from grvlms.commands import config as config_cli
from grvlms import config as grvlms_config
from grvlms import env
from grvlms import interactive

from .__about__ import __version__

HERE = os.path.abspath(os.path.dirname(__file__))

templates = os.path.join(HERE, "templates")

config = {
    "add": {
        "VERSION": __version__,
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 20|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "HOST": "discovery.{{ WILDCARD_DOMAIN }}",
        "INDEX_NAME": "catalog",
        "MYSQL_DATABASE": "discovery",
        "MYSQL_USERNAME": "discovery",
        "OAUTH2_KEY": "discovery",
        "OAUTH2_KEY_DEV": "discovery-dev",
    },
    "defaults": {
        "DOCKER_IMAGE": "groovetech/openedx-discovery:{{ DISCOVERY_VERSION }}",
    },
}

hooks = {
    "build-image": {"discovery": "{{ DISCOVERY_DOCKER_IMAGE }}"},
    "remote-image": {"discovery": "{{ DISCOVERY_DOCKER_IMAGE }}"},
    "init": ["mysql", "lms", "discovery"],
}


def patches():
    all_patches = {}
    for path in glob(os.path.join(HERE, "patches", "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches

@click.group(help="Extra Command for Discovery")
def command():
    pass

def ask_questions_discovery(config, defaults):
    interactive.ask(
        "Discovery host:", 
        "DISCOVERY_HOST",
        config, 
        {"DISCOVERY_HOST": ""})
    interactive.ask(
        "Index name:", 
        "DISCOVERY_INDEX_NAME",
        config, 
        {"DISCOVERY_INDEX_NAME": ""})
    interactive.ask(
        "Database name:", 
        "DISCOVERY_MYSQL_DATABASE",
        config, 
        {"DISCOVERY_MYSQL_DATABASE": ""})
    interactive.ask(
        "Username:", 
        "DISCOVERY_MYSQL_USERNAME",
        config, 
        {"DISCOVERY_MYSQL_USERNAME": ""})
    interactive.ask(
        "Partner name:", 
        "DISCOVERY_OAUTH2_KEY",
        config, 
        {"DISCOVERY_OAUTH2_KEY": ""})
    interactive.ask(
        "Development Partner name:", 
        "DISCOVERY_OAUTH2_KEY_DEV",
        config, 
        {"DISCOVERY_OAUTH2_KEY_DEV": ""})
    

def load_config_discovery(root, interactive=True):
    defaults = grvlms_config.load_defaults()
    config = grvlms_config.load_current(root, defaults)
    if interactive:
        ask_questions_discovery(config, defaults)
    return config, defaults

@click.command(help="Config discovery variables", name="config")
@click.option("-i", "--interactive", is_flag=True, help="Run interactively")
@click.option("-s", "--set", "set_",
    type=config_cli.YamlParamType(),
    multiple=True,
    metavar="KEY=VAL", 
    help="Set a configuration value")
@click.pass_obj
def config_discovery(context, interactive, set_):
    config, defaults = load_config_discovery(
        context.root, interactive=interactive
    )
    if set_:
        grvlms_config.merge(config, dict(set_), force=True)
    grvlms_config.save_config_file(context.root, config)
    grvlms_config.merge(config, defaults)
    env.save(context.root, config)

command.add_command(config_discovery)
