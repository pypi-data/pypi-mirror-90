# -*- coding: utf-8 -*-

"""Console script for pymklist."""
import sys
import click
import os

import re

from mklist.generate import generate_parts_lst

ldraw = re.compile(r'ldraw', flags=re.IGNORECASE)
yes = re.compile(r'[y](?:es)?', flags=re.IGNORECASE)


@click.command(name='mklist')
@click.argument('input_directory', required=False)
@click.option('--description', default=False, is_flag=True)
@click.option('--number', default=False, is_flag=True)
def main(input_directory, description, number, ):
    """Console script for pymklist."""
    if input_directory is None:
        input_directory = os.getcwd()
    if re.match(ldraw, input_directory) and os.path.exists('parts'):
        print('operating from a LDraw folder, continuing...')
    elif not (
        re.match(ldraw, input_directory)
        and
        os.path.exists(os.path.join(input_directory, 'parts'))
    ):
        print('LDraw parts directory not found')
        print('Please specify a LDraw parts library directory'
              'location in the arguments of the mklist call')
        raise click.Abort()

    parts_lst_path = os.path.join(input_directory, 'parts.lst')
    parts_folder_path = os.path.join(input_directory, 'parts')
    if description:
        generate_parts_lst('description', parts_folder_path, parts_lst_path)
    if number:
        generate_parts_lst('number', parts_folder_path, parts_lst_path)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
