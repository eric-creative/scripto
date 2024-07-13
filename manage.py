import os
import pathlib
import shutil
import sys
import argparse
import time
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

pageDir = os.path.join(BASE_DIR, 'page')
templateDir = os.path.join(BASE_DIR, 'templates')
wsgiDir = os.path.join(BASE_DIR, './', 'wsgi.py')


def register_new_blueprint(pagename):
    try:
        bps = os.listdir(pageDir)
        for bp_name in bps:
            if bp_name == pagename:
                with open(wsgiDir, 'r+') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        imported = line.startswith(f"from .page.{bp_name}.page import {bp_name}")
                        if imported:
                            print("Page already registered")
                            return
                        else:
                            if line.startswith("from .page.page import page"):
                                lines[i] = line.strip() + f"\nfrom .page.{bp_name}.page import {bp_name}\n"
                            if line.startswith("app.register_blueprint(page)"):
                                lines[i] = line.strip() + f"\napp.register_blueprint({bp_name})\n"

                    f.seek(0)
                    for line in lines:
                        f.write(line)
                    print(f'Page {bp_name} registered.')
    except OSError:
        raise OSError("Can not find page")


def delete_file(filename):
    try:
        os.remove(filename)
        print(f"File '{filename}' deleted successfully!")
    except OSError as e:
        print(f"Error deleting file: {e}")


def list_files(directory_path):
    try:
        path = Path(directory_path)
        files = [file.name for file in path.iterdir() if file.is_file()]
        for file in files:
            if file:
                return file
            else:
                raise FileNotFoundError(f'No file found')
    except OSError as e:
        print(f"Error listing files: {e}")


def generate_files(pagename):
    if pagename is not None:
        f = [list_files(os.path.join(pageDir, pagename)), list_files(os.path.join(templateDir, pagename))]
        for a in f:
            if a is None:
                try:
                    with open(os.path.join(pageDir, pagename, '__init__.py'), 'w+') as f:
                        f.write(
                            f'######################################################################## \n'
                            f'# __INIT__ INITIALIZES THIS PAGE........................................ \n'
                            f'######################################################################## \n'
                        )
                    with open(os.path.join(pageDir, pagename, 'page.py'), 'w+') as f:
                        f.write(
                            f'######################################################################## \n'
                            f'# IMPORTS HERE.......................................................... \n'
                            f'######################################################################## \n'
                            f'from flask import Blueprint, render_template \n\n'
                            f'########################################################################\n'
                            f'# CREATING A BLUEPRINT HERE.............................................\n'
                            f'########################################################################\n'
                            f"{pagename} = Blueprint('{pagename}', __name__, template_folder='templates', "
                            f"url_prefix='/{pagename}') \n"
                            f"\n"
                            f'########################################################################\n'
                            f'# BLUEPRINT ROUTES HERE.................................................\n'
                            f'######################################################################## \n'
                            f"@{pagename}.route('/', methods=['GET'])\n"
                            f'def page():\n\n'
                            f"\treturn render_template('{pagename}/page.jinja2') \n"
                            f'\n'
                        )
                    try:
                        with open(os.path.join(templateDir, pagename, 'page.jinja2'), 'w+') as f:
                            f.write(
                                "{% extends 'layout.jinja2' %} \n\n"
                                "{% block title %} \n"
                                f"\t{str(pagename).capitalize()} - page \n"
                                "{% endblock %} \n\n"
                                "{% block content %} \n"
                                f"\t<h1>{str(pagename).capitalize()} page</h1> \n"
                                "{% endblock %} \n"
                            )
                    except FileNotFoundError:
                        raise FileNotFoundError(f'Unable to write template file: {pagename}')

                except FileNotFoundError:
                    raise FileNotFoundError(f'Unable to write page file: {pagename}')
            else:
                delete_file(str(a))
        print(f'Page {pagename} has been added to your project')
        time.sleep(2)
        register_new_blueprint(pagename)


def generate(pagename):
    if os.path.exists(os.path.join(pageDir, pagename)):
        raise FileExistsError(
            f'\n Page with pagename: {pagename} already exist \n ---->> delete any directory with '
            f'same name in {os.path.join(pageDir)} before running this command'
        )
    else:
        try:
            os.makedirs(os.path.join(pageDir, pagename), exist_ok=True)
            os.makedirs(os.path.join(templateDir, pagename), exist_ok=True)
            # print(f"Directory created successfully!")

            # check if the directory is created
            if os.path.exists(os.path.join(pageDir, pagename)):
                if os.path.exists(os.path.join(templateDir, pagename)):

                    # check if the directory created is a directory
                    if os.path.isdir(os.path.join(pageDir, pagename)):
                        if os.path.isdir(os.path.join(templateDir, pagename)):
                            print('Check performed successful.')
                            generate_files(pagename)
                        else:
                            raise FileExistsError(
                                f'\n Template with name: {pagename} is not a directory '
                                f'in {os.path.join(templateDir)} '
                            )
                    else:
                        raise FileExistsError(
                            f'\n Page with name: {pagename} is not a directory '
                            f'in {os.path.join(pageDir)} '
                        )

                else:
                    raise FileExistsError(
                        f'\n Template with name: {pagename} does not exist '
                        f'in {os.path.join(templateDir)}'
                    )
            else:
                raise FileExistsError(
                    f'\n Page with name: {pagename} does not exist '
                    f'in {os.path.join(pageDir)}'
                )
        except OSError as e:
            print(f"Error creating directory: {e}")


def remove_page(pagename):
    if os.path.exists(os.path.join(pageDir, pagename)):
        if os.path.exists(os.path.join(templateDir, pagename)):
            p = pathlib.Path(os.path.join(pageDir, pagename))
            t = pathlib.Path(os.path.join(templateDir, pagename))
            try:
                shutil.rmtree(t)
                shutil.rmtree(p)
                new_lines = []
                with open(wsgiDir, 'r+') as c:
                    lines = c.readlines()
                    for i, line in enumerate(lines):
                        imported = line.startswith(f"from .page.{pagename}.page import {pagename}")
                        registered = line.startswith(f"app.register_blueprint({pagename}")
                        if not (imported or registered):
                            # Include other lines in the new_lines list
                            new_lines.append(line)
                    c.seek(0)
                    # Convert the list of lines to a single string
                    updated_content = "".join(new_lines)
                    c.write(updated_content)
                    c.truncate()
                    print(f'Page {pagename} removed from your project')

            except FileNotFoundError:
                raise FileExistsError(f'Unable to remove page: {pagename}')
        else:
            raise FileExistsError(f'\n Template with name: {pagename} is not a directory ')
    else:
        raise FileExistsError(f'\n Page with name: {pagename} does not exist')


def handle_arg(value, pagename):
    if value == "add":
        generate(pagename)
    elif value == "remove":
        remove_page(pagename)
    else:
        print(f"Invalid command: {value}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a text file.")
    parser.add_argument("pagename", help="Name of the page to create")
    parser.add_argument("--run", choices=["add", "remove"], default="page", help="Adds a page <name>")

    args = parser.parse_args()

    if args.run:
        handle_arg(args.run, args.pagename)
    else:
        print("Usage: python manage.py --add <pagename>")
        sys.exit(1)
