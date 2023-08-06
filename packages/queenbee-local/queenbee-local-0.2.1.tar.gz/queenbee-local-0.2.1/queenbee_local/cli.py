"""Queenbee local command line interface."""
try:
    import click
except ImportError:
    raise ImportError(
        'click module is not installed. Try `pip install click` command.'
    )

import json
import os
import time
import pathlib
import sys
import sysconfig
import subprocess

from queenbee.cli import Context
from .helper import parse_user_recipe_args


@click.group(help='Commands for interacting with Queenbee local recipes.')
@click.version_option()
@click.pass_context
def local(ctx):
    """Queenbee local plugin."""
    ctx.obj = Context()


@local.command('run')
@click.argument(
    'recipe',
    type=click.Path(exists=True, file_okay=False, resolve_path=True, dir_okay='True')
)
@click.argument(
    'project_folder',
    type=click.Path(exists=True, file_okay=False, resolve_path=True, dir_okay=True),
    default='.'
)
@click.option(
    '-i', '--inputs',
    type=click.Path(exists=True, file_okay=True, resolve_path=True, dir_okay=False),
    default=None, show_default=True, help='Path to the JSON file to'
    ' overwrite inputs for this recipe.'
)
@click.option(
    '-w', '--workers', type=int, default=1, show_default=True,
    help='Number of workers to execute tasks in parallel.'
)
@click.option(
    '-e', '--env', multiple=True, help='An option to pass environmental variables to '
    'commands. Use = to separate key and value. RAYPATH=/usr/local/lib/ray'
)
@click.option('-n', '--name', help='Simulation name for this run.')
@click.option(
    '-d', '--debug',
    type=click.Path(exists=False, file_okay=False, resolve_path=True, dir_okay=True),
    help='Optional path to a debug folder. If debug folder is provided all the steps '
    'of the simulation will be executed inside the debug folder which can be used for '
    'furthur inspection.'
)
@click.pass_context
def run_recipe(recipe, project_folder, inputs, workers, env, name, debug):
    """Run a Queenbee local recipe.

    \b
    Args:
        recipe: Path to recipe folder. Recipe folder includes a package.json and a
            run.py file to execute the simulation.
        project_folder: Path to project folder. Project folder includes the input files
            and folders for the recipe.
    """
    # check for run.py to be available
    runner_file = os.path.join(recipe, 'run.py')
    package_info = os.path.join(recipe, 'package.json')
    assert os.path.isfile(runner_file), \
        'Invalid recipe folder. Recipe folder must contain a run.py file.'
    assert os.path.isfile(package_info), \
        'Invalid recipe folder. Recipe folder must contain a package.json file.'

    with open(package_info) as info_file:
        info = json.load(info_file)

    try:
        recipe_name = info['metadata']['name']
    except KeyError:
        raise ValueError('Invalid package.json - missing package metadata.')

    env_vars = {}
    genv = os.environ.copy()
    if env:
        for e in env:
            try:
                key, value = e.split('=')
            except Exception as e:
                raise ValueError(f'env input is not formatted correctly: {e}')
            else:
                env_vars[key.strip()] = pathlib.Path(value.strip()).as_posix()

        for k, v in env_vars.items():
            k = k.strip()
            if k.upper() == 'PATH':
                # extend the new PATH to current PATH
                genv['PATH'] = os.pathsep.join((v, genv['PATH']))
                continue
            elif k.upper() == 'RAYPATH':
                # extend RAYPATH to current RAYPATH
                try:
                    genv['RAYPATH'] = os.pathsep.join((v, genv['RAYPATH']))
                except KeyError:
                    # it will be set below
                    pass
                else:
                    continue
            # overwrite env variable
            genv[k.strip()] = v.strip()

    if inputs:
        # try to load the results
        with open(inputs) as input_file:
            input_data = json.load(input_file)
        input_values = parse_user_recipe_args(input_data)
    else:
        input_values = {}

    # add simulation folder based on simulation name
    if not name:
        name = f'{recipe_name.replace("-", "_")}_{int(round(time.time(), 2) * 100)}'

    simulation_folder = pathlib.Path(project_folder, name)
    input_values['simulation_folder'] = simulation_folder.as_posix()
    simulation_folder.mkdir(exist_ok=True)

    if debug:
        debug_folder = pathlib.Path(debug)
        if not debug_folder.exists():
            debug_folder.mkdir(0o777)
        input_values['__debug__'] = debug_folder.as_posix()

    # write updated inputs to project folder
    inputs_file = pathlib.Path(
        input_values['simulation_folder'], '__inputs__.json'
    ).as_posix()

    with open(inputs_file, 'w') as inpf:
        json.dump(input_values, inpf)

    python_executable_path = sys.executable

    # add path to scripts folder to env
    scripts_path = sysconfig.get_paths()['scripts']
    genv['PATH'] = os.pathsep.join((scripts_path, genv['PATH']))

    # put all the paths in quotes - this should address the issue for paths with
    # white space
    command = f'"{python_executable_path}" "{runner_file}" ' \
        f'"{project_folder}" "{inputs_file}" {workers}'

    try:
        subprocess.call(command, cwd=project_folder, shell=True, env=genv)
    except Exception as e:
        print(f'Failed to run {recipe_name}... :|\n{e}')
        sys.exit(1)
    else:
        sys.exit(0)


# @main.command('inputs')
# @click.argument('recipe', type=click.Path(exists=True, file_okay=True))
# @click.option(
#     '-f', '--filepath', type=click.File(mode='w'), default=None, show_default=True,
#     help='Path to output JSON file.'
#     )
# @click.option(
#     '-r', '--required', is_flag=True, default=False, show_default=True,
#     help='An option to only required inputs.'
# )
# @click.pass_context
# def inputs(ctx, recipe, filepath, required):
#     """Write recipe inputs to a JSON file.

#     This file can be passed to translate command.

#     Use this command to generate a place holder or check the inputs of a recipe.

#     Args:
#         recipe: Path to a backed recipe file or a recipe folder.
#     """

#     rep = Recipe(recipe)
#     values = rep.inputs(required=required)
#     if filepath:
#         json.dump(values, filepath, indent=4)
#     else:
#         click.echo(values)
#     # set permissions
#     os.chmod(filepath, 0o777)

if __name__ == "__main__":
    main()
