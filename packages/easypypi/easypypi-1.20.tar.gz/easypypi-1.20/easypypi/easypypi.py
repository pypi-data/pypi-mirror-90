from .classifiers import CLASSIFIER_LIST
from .licenses import LICENSE_NAMES
from .licenses import LICENSES
from .shared_functions import create_file
from .shared_functions import update_line
from .utils import GROUP_CLASSIFIERS
from .utils import REPLACEMENTS
from .utils import SETUP_FIELDS
from .utils import SG_KWARGS
from cleverdict import CleverDict
from decimal import Decimal as decimal
from keyring.errors import PasswordDeleteError
from mechanicalsoup.utils import LinkNotFoundError
from pathlib import Path
from PySimpleGUI import ICON_BUY_ME_A_COFFEE
import click  # used to get cross-platform folder path for config file
import datetime
import getpass
import json
import keyring
import mechanicalsoup
import os
from pprint import pprint
import PySimpleGUI as sg
import shutil
import webbrowser


class Package(CleverDict):
    """
    Methods and data relating to a Python module/package in preparation for
    publishing on the Python Package Index (PyPI).

    Makes use of CleverDict's auto-save feature to store values in a config
    file, and .get_aliases() to keep a track of newly created attributes.

    Exits early if review is False or _break is True

    redirect : Send stdout and stderr to PySimpleGUI Debug Window

    """

    sg.change_look_and_feel("DarkAmber")
    easypypi_dirpath = Path(__file__).parent
    config_filepath = Path(click.get_app_dir("easyPyPI")) / ("config.json")

    def __init__(self, name=None, **kwargs):
        options, kwargs = self.get_options_from_kwargs(**kwargs)
        # ⚠ If kwargs are supplied, autosave will overwrite JSON config
        super().__init__(**kwargs)
        if name:
            self.name = name
        else:
            self.name = sg.popup_get_text(
                "Please enter a name for this package (all lowercase, underscores if needed):",
                default_text=self.get("name") or "as_easy_as_pie",
                **SG_KWARGS,
            )
        self.load_defaults()
        print(
            f"\n ⓘ  easyPyPI template files are located in:\n  {self.__class__.easypypi_dirpath}",
            **options if kwargs.get("redirect") else {},
        )
        print(
            f"\n ⓘ  Your easyPyPI config file is:\n  {self.__class__.config_filepath}"
        )
        if options["_break"] is True:
            return
        # As above... must Load before Setting any other values with autosave on
        if self.name and self.get("setup_filepath_str"):
            self.get_user_input()

    def __str__(self):
        output = self.info(as_str=True)
        return output.replace("CleverDict", type(self).__name__, 1)

    def save(self, key=None, value=None):
        """
        This method is called by CleverDict whenever a value or attribute
        changes.  Used here to update the config file automatically.

        NB because values are loaded from the config file into attributes during
        __init__, if you want to DELETE an entry from the config file e.g.
        during debugging you'll need to delete the attribute then run .save:

        del self.x
        self.save()
        """
        with open(self.__class__.config_filepath, "w") as file:
            # CleverDict.get_aliases finds attributes created after __init__:
            fields_dict = {
                x: self.get(x)
                for x in self.get_aliases()
                if "password" not in x.lower()
            }
            json.dump(fields_dict, file)
        if key:
            if "password" in key.lower():
                location = "memory but NOT saved to file"
            else:
                location = self.__class__.config_filepath

    def get_options_from_kwargs(self, **kwargs):
        """ Separate actionable options from general data in kwargs."""
        options = {}
        for key, default_value in {"_break": False}.items():
            if isinstance(kwargs.get(key), bool):
                options[key] = kwargs.get(key)
                del kwargs[key]
            else:
                options[key] = default_value
        return options, kwargs

    def load_defaults(self):
        """
        Entry point for loading default Package values as attributes.
        Choose between last updated JSON config file, and setup.py if it exists.
        """
        self.create_skeleton_config_file()
        self.load_defaults_from_config_file()
        self.create_folder_structure()
        if self.setup_filepath.is_file() and self.setup_filepath.stat().st_size:
            # If setup.py exists & isn't empty, overwrite default values
            self.load_defaults_from_setup_py()

    def load_defaults_from_config_file(self):
        """
        Loads default metadata from last updated config file.
        Creates .scriptlines as a copy of setup_template.py
        """
        with open(self.__class__.config_filepath, "r") as file:
            values = json.load(file)
        for key, value in values.items():
            setattr(self, key, value)
        setup = self.__class__.easypypi_dirpath / "setup_template.py"
        with open(setup, "r") as file:
            self.script_lines = file.readlines()

    def load_defaults_from_setup_py(self):
        """
        Loads default metadata from previously created setup.py
        Creates .scriptlines as a copy of setup.py
        """
        with open(self.setup_filepath, "r") as file:
            lines = file.readlines()
        for line in lines:
            for field, attribute in SETUP_FIELDS.items():
                if line.startswith(field.upper() + " = "):
                    # Use eval in case the value isn't simply a string:
                    setattr(self, attribute, eval(line.split(" = ")[-1]))
        with open(self.setup_filepath, "r") as file:
            self.script_lines = file.readlines()

    def create_skeleton_config_file(self):
        """
        Uses click to find & create a platform-appropriate easyPyPI folder, then
        creates a skeleton json file there to store persistent data (if one
        doesn't already exist or if the current one is empty).
        """
        if (
            self.__class__.config_filepath.is_file()
            and self.__class__.config_filepath.stat().st_size
        ):
            return
        try:
            os.makedirs(self.__class__.config_filepath.parent)
            print(f"\n ⓘ  Folder created:\n {self.__class__.config_filepath.parent}")
        except FileExistsError:
            pass
        with open(self.__class__.config_filepath, "w") as file:
            json.dump({"version": "0.1"}, file)  # Create skeleton .json file
        print(
            f"\n ⚠  Skeleton config file created:\n  {self.__class__.config_filepath}"
        )

    def create_folder_structure(self):
        """
        Creates skeleton folder structure for a package and starter files.
        Creates .setup_filepath_str.
        """
        parent_path_str = ""
        while not parent_path_str:
            parent_path_str = sg.popup_get_folder(
                "Please select the parent folder for your package i.e. WITHOUT the package name",
                default_path=self.get_default_filepath(),
                **SG_KWARGS,
            )
            if parent_path_str is None:
                return
        setup_dirpath = Path(parent_path_str) / self.name
        self.setup_filepath_str = str(setup_dirpath / "setup.py")
        try:
            os.makedirs(setup_dirpath / self.name)
            print(f"\n✓ Created package folder:\n  {setup_dirpath}")
        except FileExistsError:
            print(f"\n ⓘ  Package folder already exists:\n  {setup_dirpath}")

    def get_username(self, account):
        """
        Loads username for a given account from `keyring` or prompts for a
        value if (account, None) fails e.g. on iOS.

        Parameters:
        account -> "Github", "PyPI" or "Test_PyPI"

        Sets:
        .{account}_username

        Returns:
        True if successful
        False if "cancel", "", or "X".
        """
        if not self.get(f"{account}_username"):
            try:
                username = keyring.get_credential(account, None).username
            except AttributeError:
                username = sg.popup_get_text(
                    f'Please enter your {account.replace("_", " ")} username (saved securely with `keyring`):',
                    default_text=self.get("Github_username"),
                    **SG_KWARGS,
                )
            if not username:
                return False
            setattr(self, f"{account}_username", username)
        return self.get(f"{account}_username")

    def set_password(self, account, pw=""):
        """Sets a new value for .accoutn_password and also in `keyring`.

        If no pw is supplied, set pw to "", which will trigger a pw prompt
        when check_password() is called.

        Returns:

        True if password is set successsfully,
        False if password is not set successfully.
        """
        keyring.set_password(account, getattr(self, account + "_username"), pw)
        setattr(self, f"{account}_password", pw)
        return self.check_password(account)

    def check_password(self, account):
        """
        Checks that a password exists for a given account using `keyring` or
        prompts for a value if not.

        Parameters:
        account -> "Github", "PyPI" or "Test_PyPI"

        Sets:
        keyring credentials
        .{account}_password

        Returns:
        True if successful
        False if "cancel", "", or "X".
        """
        if not self.get(f"{account}_password"):
            pw = keyring.get_password(account, getattr(self, account + "_username"))
            if not pw:
                pw = sg.popup_get_text(
                    f'Please enter your {account.replace("_", " ")} password (not saved to file):',
                    password_char="*",
                    **SG_KWARGS,
                )
            if not pw:
                return False
            setattr(self, f"{account}_password", pw)
            keyring.set_password(account, getattr(self, account + "_username"), pw)
        return True

    def delete_credentials(self, account):
        """
        Delete password AND username from keyring.
        .username remains in memory but .password was only ever an @property.
        """
        username = self.get(f"{account}_username")
        choice = sg.popup_yes_no(
            f"Do you really want to delete {account} credentials for {username}?",
            **SG_KWARGS,
        )
        if choice == "Yes":
            for key in [f"{account}_username", f"{account}_password"]:
                if self.get(key):
                    del self[key]
            try:
                keyring.delete_password(account, username)
            except PasswordDeleteError:
                print(
                    "\n ⓘ  keyring Credentials couldn't be deleted. Perhaps they already were?"
                )

    @property
    def setup_filepath(self):
        """
        json.dump can't serialise pathlib objects so this method creates them
        from setup_filepath_str.

        This approach ensures the property doesn't appear in .get_aliases which
        is used for deciding what attributes get auto-saved to the config file.
        """
        return Path(self.setup_filepath_str)

    @property
    def next_version(self):
        """ Suggests next package version number based on simple schemas """
        decimal_version = decimal(str(self.version))
        try:
            _, digits, exponent = decimal_version.as_tuple()
            if exponent == 0:  # i.e. 0 decimal places:
                increment = "0.1"
            else:
                increment = "0.01"
            return str(decimal_version + decimal(increment))
        except dec.InvalidOperation:
            return f"{self.version}-new"

    def get_default_filepath(self):
        path = Path(self.get("setup_filepath_str") or Path().cwd())
        # Default path should be the parent of self.name and not include it
        while path.parts[-1] in [self.name, "setup.py"]:
            path = Path().joinpath(*path.parts[:-1])
        return str(path)

    def get_default_version(self):
        return "0.1"

    def get_default_url(self):
        username = self.get_username("Github")
        default = f"https://github.com/{username or 'username'}"
        return default + f"/{self.name}"

    def get_default_author(self):
        return getpass.getuser()

    def get_default_email(self):
        return f"{getpass.getuser().lower()}@gmail.com"

    def get_default_keywords(self):
        default = f"{self.name}, "
        default += f"{self.author}, "
        return default + f"{self.Github_username}, "

    def get_default_requirements(self):
        return "cleverdict, "

    def get_main_layout_inputs(self):
        """
        Generates input boxes as part of the main layout.
        Returns: layout (PySimpleGUI list)
        """
        prompts = {
            "name": "Package Name (all lowercase, underscores if needed):",
            "version": "Latest Version number:",
            "Github_username": "Your Github (or other repository) Username:",
            "PyPI_username": "Your PyPI Username:",
            "Test_PyPI_username": "Your Test PyPI Username:",
            "url": "Link to the Package Repository:",
            "description": "Description (with escape characters for \\ \" ' etc.):",
            "author": "Full Name of the Author:",
            "email": "E-mail Address for the Author:",
            "keywords": "Keywords (separated by a comma):",
            "requirements": "Any additional packages/modules required:",
        }
        self.version = self.get("version") or self.get_default_version()
        self.get_username("Github")  # .Github_username created in place
        self.url = self.get_default_url()
        self.description = self.get("description")
        self.author = self.get("author") or self.get_default_author()
        self.email = self.get("email") or self.get_default_email()
        self.keywords = self.get("keywords") or self.get_default_keywords()
        self.requirements = self.get("requirements") or self.get_default_requirements()
        layout = [[sg.Text(" " * 200, font="calibri 6")]]
        for key, prompt in prompts.items():
            default = self.get(key)
            layout += [
                [
                    sg.Text(prompt, size=(40, 0)),
                    sg.Input(self.get(key), key=key, size=(50, 0)),
                ]
            ]
        return layout

    def get_main_layout_classifiers(self, layout):
        """
        Adds input boxes for Classifier lists to the main window layout.
        Returns: layout (PySimpleGUI list), choices, selected_choices
        """
        choices = {}
        selected_choices = {}
        layout += [[sg.Text(" " * 200, font="calibri 6")]]
        for group, group_text in GROUP_CLASSIFIERS.items():
            choices[group] = [x for x in CLASSIFIER_LIST if x.startswith(group)]
            self.classifiers = self.get("classifiers") or ""
            selected_choices[group] = [
                x for x in self.classifiers.split(", ") if x.startswith(group)
            ]
            if (
                group == "Programming Language :: Python"
                and not selected_choices[group]
            ):
                selected_choices[group] = [
                    x
                    for x in choices[group]
                    if any([x.endswith(y) for y in ["3.6", "3.7", "3.8", "3.9"]])
                ]
            if group == "License :: OSI Approved ::":
                # License names aren't identical between PyPI and Github
                choices[group] = [
                    x
                    for x in choices[group]
                    if any([x.endswith(y) for y in LICENSE_NAMES.values()])
                ]
                if not selected_choices[group]:
                    selected_choices[group] = ["License :: OSI Approved :: MIT License"]
            for group_name, default in {
                "Operating System": "OS Independent",
                "Development Status": "- Alpha",
                "Intended Audience": "Developers",
            }.items():
                if group == group_name and not selected_choices[group]:
                    selected_choices[group] = [
                        x for x in choices[group] if x.endswith(default)
                    ]
            layout += [
                [
                    sg.Text(group_text, size=(40, 0)),
                    sg.Text(
                        "\n".join(selected_choices[group]),
                        key=("classifiers", group),
                        enable_events=True,
                        size=(44, 0),
                        background_color=sg.theme_input_background_color(),
                        text_color=sg.theme_text_color(),
                    ),
                ]
            ]
        return layout, choices, selected_choices

    def get_main_layout_buttons(self, layout):
        """
        Adds action buttons to the main window layout.
        Returns: layout (PySimpleGUI list)
        """
        layout += [
            [sg.Text(" " * 200, font="calibri 6")],
            [
                sg.Button("Save", tooltip="Save current values to config.json."),
                sg.Button("Upversion", tooltip="Update Version number incrementally."),
                sg.Button(
                    "Generate",
                    tooltip="Create/update setup.py and tar.gz files ready for publishing.",
                ),
                sg.Button(
                    "Publish", tooltip="Upload/update package on PyPI and/or TestPyPI."
                ),
                sg.Button(
                    image_data=ICON_BUY_ME_A_COFFEE,
                    key="Coffee",
                    tooltip="Show your appreciation for all the time you're saving with easyPyPI.",
                ),
                sg.Button(
                    "Create Accounts",
                    tooltip="Create an account on PyPI, TestPyPI and/or Github.",
                ),
                sg.Button(
                    "Github Push",
                    tooltip="Automatically create an initial repository on Github.",
                ),
                sg.Button("config.json", tooltip="Open/Edit your config.json file."),
            ],
        ]
        return layout

    def get_user_input(self):
        """
        Check config file for previous values.  If no value is set, prompts for
        a value and updates the relevant Package attribute.
        """
        layout = self.get_main_layout_inputs()
        layout, choices, selected_choices = self.get_main_layout_classifiers(layout)
        layout = self.get_main_layout_buttons(layout)
        window = sg.Window(
            "easyPyPI",
            layout,
            keep_on_top=SG_KWARGS["keep_on_top"],
            icon=SG_KWARGS["icon"],
            element_justification="center",
        )
        while True:
            event, values = window.read()
            if event is None:
                window.close()
                return False
            if event == "Save":
                self.save_user_input(values, selected_choices)
            if event == "Upversion":
                self.version = self.next_version
                window["version"].update(value=self.version)
                values["version"] = self.version
            if event == "Generate":
                self.save_user_input(values, selected_choices)
                print(values)
                self.generate_files_and_folders()
            if event == "Publish":
                self.upload_with_twine()
            if event == "Accounts":
                self.register_accounts()
            if event == "Github":
                self.create_github_repository()
            if event == "Config":
                webbrowser.open(self.config_filepath)
            if event == "Coffee":
                webbrowser.open("https://www.buymeacoffee.com/pfython")
            if isinstance(event, tuple):
                group = event[1]
                prompt_with_choices(
                    group,
                    choices=choices[group],
                    selected_choices=selected_choices[group],
                )
                window[event].update(value="\n".join(selected_choices[group]))

    def save_user_input(self, values, selected_choices):
        """
        Update package attributes based on main window input

        """
        for key, value in values.items():
            setattr(self, key, value)
        self.classifiers = []
        for value in selected_choices.values():
            self.classifiers.extend(value)
        self.classifiers = ", ".join(self.classifiers)
        self.license_name_pypi = selected_choices["License :: OSI Approved ::"]
        self.license_name_pypi = self.license_name_pypi[0].split(":: ")[-1]
        for spdx_id, pypi_name in LICENSE_NAMES.items():
            if self.license_name_pypi.endswith(pypi_name):
                self.license_name_github = [
                    x.name for x in LICENSES if x.spdx_id == spdx_id
                ][0]
                break
        self.create_license()
        self.update_script_lines()

    def create_license(self):
        """
        Use Classifiers/License as key to create LICENSE data from licenses.json

        Sets:

        .license_text and makes common substitutions e.g. data and author.
        """
        license_dict = [x for x in LICENSES if x.name == self.license_name_github][0]
        year = str(datetime.datetime.now().year)
        replacements = dict()
        self.license_text = license_dict.body
        if license_dict.key == "lgpl-3.0":
            self.license_text += (
                "\nThis license is an additional set of permissions to the "
                '<a href="/licenses/gpl-3.0">GNU GPLv3</a> license which is reproduced below:\n\n'
            )
            gpl3 = [x for x in LICENSES if x.key == "gpl-3.0"][0]
            self.license_text += gpl3.body
        if license_dict.key == "mit":
            replacements = {"[year]": year, "[fullname]": self.author}
        if license_dict.key in ["gpl-3.0", "lgpl-3.0", "agpl-3.0"]:
            replacements = {
                "<year>": year,
                "<name of author>": self.author,
                "<program>": self.name,
                "Also add information on how to contact you by electronic and paper mail.": f"    Contact email: {self.email}",
                "<one line to give the program's name and a brief idea of what it does.>": f"{self.name}: {self.description}",
            }
        if license_dict.key == "apache-2.0":
            replacements = {"[yyyy]": year, "[name of copyright owner]": self.author}
        if replacements:
            for old, new in replacements.items():
                self.license_text = self.license_text.replace(old, new)

    def update_script_lines(self):
        for keyword, attribute_name in SETUP_FIELDS.items():
            old_line_starts = keyword.upper() + " = "
            new_value = getattr(self, attribute_name)
            self.script_lines = update_line(
                self.script_lines, old_line_starts, new_value
            )

    def register_accounts(self, filter=None):
        """
        Prompts for TestPyPI/PyPI account names for twine to use.

        This approach avoids the need for a .pypirc config file:
        https://packaging.python.org/specifications/pypirc/#common-configurations

        Creates the following attributes in place:

        .pypi_username
        .pypi_test_username
        .github_username

        filter : restricts the function to the account specified

        """
        url = r"https://pypi.org/account/register/"
        accounts = {
            "Github": "https://github.com/join",
            "PyPI": url,
            "Test PyPI": url.replace("pypi", "test.pypi"),
        }
        if filter:
            accounts = {k: v for k, v in accounts.items() if k == filter}
        for account, url in accounts.items():
            if not self.get(account + "username"):
                response = sg.popup_yes_no(
                    f"Do you need to register for an account on {account}?", **SG_KWARGS
                )
                if response is None:
                    return
                if response == "Yes":
                    print(
                        f"\n ⚠  Please create a {account} account, "
                        f"then return to easyPyPI to continue the process..."
                    )
                    webbrowser.open(url)

    def generate_files_and_folders(self):
        """
        Recreates setup.py & creates a new tar.gz package ready for publishing.
        """
        self.copy_other_files()
        choice = sg.popup_yes_no(
            "Do you want to generate new package files "
            "(setup.py, README, LICENSE, tar.gz, etc) from the current metadata?\n",
            **SG_KWARGS,
        )
        if choice != "Yes":
            return
        self.create_essential_files()
        self.run_setup_py()
        print("\n ✓  Files and folders generated ready for publishing.")

    def copy_other_files(self):
        """
        Prompts for additional files to copy over into the newly created folder:
        \package_name\package_name
        """
        files = sg.popup_get_file(
            "Please select any other files to copy to new project folder",
            **SG_KWARGS,
            default_path="",
            multiple_files=True,
        )
        if files is None:
            return
        for file in [Path(x) for x in files.split(";")]:
            new_file = self.setup_filepath.parent / self.name / file.name
            if new_file.is_file():
                response = sg.popup_yes_no(
                    f"WARNING\n\n{file.name} already exists in\n{new_file.parent}\n\n Overwrite?",
                    **SG_KWARGS,
                )
                if response == "No":
                    continue
            if file.is_file():
                shutil.copy(file, new_file)
                print(f"\n✓ Copied {file.name} to:\n {new_file.parent}")

    def create_essential_files(self):
        """
        Creates essential files for the new package:
        /setup.py
        /README.md
        /LICENSE
        /package_name/__init__.py
        /package_name/package_name.py
        /package_name/test_PACKAGE_NAME.py
        """
        sfp = self.setup_filepath.parent
        # setup.py and LICENSE can be be overwritten as they're most likely to
        # be changed by user after publishing, and no code changes will be lost:
        create_file(sfp / "LICENSE", self.license_text, overwrite=True)
        create_file(self.setup_filepath, self.script_lines, overwrite=True)
        # Other files are just bare-bones initially, imported from templates:
        templates = {
            "readme_template.md": sfp / "README.md",
            "init_template.py": sfp / self.name / "__init__.py",
            "script_template.py": sfp / self.name / (self.name + ".py"),
            "test_template.py": sfp / self.name / ("test_" + self.name + ".py"),
        }
        # Read in, make replacements, create in new folder structure
        for template_filepath, destination_path in templates.items():
            template_filepath = self.easypypi_dirpath / template_filepath
            with open(template_filepath, "r") as file:
                text = file.read()
            for replacement in REPLACEMENTS:
                text = text.replace(replacement, eval(f"f'{replacement}'"))
            create_file(destination_path, text)

    def run_setup_py(self):
        """ Creates a .tar.gz distribution file with setup.py """
        try:
            import setuptools
            import twine
        except ImportError:
            print("\n> Installing setuptools and twine if not already present...")
            os.system('cmd /c "python -m pip install setuptools wheel twine"')
        os.chdir(self.setup_filepath.parent)
        print(f"\n> Running {self.setup_filepath / 'setup.py'}...")
        os.system('cmd /c "setup.py sdist"')

    def upload_with_twine(self):
        """ Uploads to PyPI or Test PyPI with twine """
        account = sg.popup(
            f"Do you want to upload {self.name} to\nTest PyPI, or go FULLY PUBLIC on the real PyPI?\n",
            **SG_KWARGS,
            custom_text=("Test PyPI", "PyPI"),
        )
        if not account:
            return
        if account == "PyPI":
            params = "pypi"
        if account == "Test PyPI":
            params = "testpypi"
            account = "Test_PyPI"
        if not self.get_username(account):
            return
        username = getattr(self, f"{account}_username")
        if not self.check_password(account):
            return
        params += f" dist/*-{self.version}.tar.gz "
        os.chdir(self.setup_filepath.parent)
        if os.system(
            f'cmd /c "python -m twine upload '
            f"--repository {params} "
            f"-u {username} "
            f'-p {keyring.get_password(account, username)}"'
        ):
            # A return value of 1 (True) indicates an error
            print("\n ⚠  Problem uploading with Twine; probably either:")
            print("   - An authentication issue.  Check your username and password?")
            print("   - Using an existing version number.  Try a new version number?")
        else:
            url = "https://"
            url += "" if account == "PyPI" else "test."
            webbrowser.open(url + f"pypi.org/project/{self.name}")
            response = sg.popup_yes_no(
                "Fantastic! Your package should now be available in your webbrowser, "
                "although you might need to wait a few minutes before it registers as the 'latest' version.\n\n"
                "Do you want to install it now using pip?\n",
                **SG_KWARGS,
            )
            if response == "Yes":
                print()
                if not os.system(
                    f'cmd /c "python -m pip install -i https://test.pypi.org/simple/ {self.name} --upgrade"'
                ):
                    # A return value of 1 indicates an error, 0 indicates success
                    print(
                        f"\n ⓘ  You can view your package's details using 'pip show {self.name}':\n"
                    )
                    os.system(f'cmd /c "pip show {self.name}"')

    def publish_to_github(self):
        """ Uploads initial package to Github using Git"""
        account = "Github"
        if not self.get_username(account):
            return
        commands = f"""
        git init
        git add *.*
        git commit -m "Committing version {self.version}"
        git branch -M main
        git remote add origin https://github.com/{self.Github_username}/{self.name}.git
        git push -u origin main
        """
        choice = sg.popup_yes_no(
            f"Do you want to upload (Push) your package to Github?\n\n ⚠   CAUTION - "
            f"Only recommended when creating your repository for the first time!  "
            f"This automation will run the following commands:\n\n{commands}",
            **SG_KWARGS,
        )
        if choice != "Yes":
            return
        os.chdir(self.setup_filepath.parent)
        for command in commands.splitlines()[1:]:  # Ignore first blank line
            if not os.system(f"cmd /c {command}"):
                # A return value of 1 indicates an error, 0 indicates success
                print(f"\n ⓘ  Your package is now online at:\n  {self.url}':\n")

    def create_github_repository(self):
        """ Creates an empty repository on Github """
        choice = sg.popup_yes_no(
            f"Do you want to create a repository on Github?\n",
            **SG_KWARGS,
        )
        if choice != "Yes":
            return
        account = "Github"
        if not self.get_username(account):
            return
        if not self.check_password(account):
            return
        browser = mechanicalsoup.StatefulBrowser(
            soup_config={"features": "lxml"},
            raise_on_404=True,
            user_agent="MyBot/0.1: mysite.example.com/bot_info",
        )
        browser.open("https://github.com/login")
        browser.select_form("#login form")
        browser["login"] = self.Github_username
        browser["password"] = self.Github_password
        resp = browser.submit_selected()
        browser.open("https://github.com/new")
        try:
            browser.select_form('form[action="/repositories"]')
        except LinkNotFoundError:
            print(
                f"\n ⚠  Unable to log in to Github with username {self.Github_username}.  Please resubmit Github password, double check your username, and try again..."
            )
            self.set_password("Github")
            browser.close()
            return
        browser["repository[name]"] = self.name
        browser["repository[description]"] = self.description
        browser["repository[visibility]"] = "private"
        resp = browser.submit_selected()
        self.publish_to_github()
        webbrowser.open(self.url)
        # browser.launch_browser()


def prompt_with_choices(group, choices, selected_choices):
    """
    Creates a scrollable popup using PySimpleGui checkboxes or radio buttons.
    Returns a set of selected choices, or and empty set
    """
    if group in ["Development Status", "License :: OSI Approved ::"]:
        layout = [
            [
                sg.Radio(
                    text=choice,
                    group_id=group,
                    key=choice,
                    default=choice in selected_choices,
                )
            ]
            for choice in choices
        ]
    else:
        layout = [
            [sg.Checkbox(text=choice, key=choice, default=choice in selected_choices)]
            for choice in choices
        ]
    buttons = [sg.Button("Accept"), sg.Button("Cancel")]
    if group == "License :: OSI Approved ::":
        buttons += [sg.Button("License Help")]
    choices_window = sg.Window(
        f"Classifiers for the {group.title()} group",
        [
            "",
            [
                sg.Column(
                    layout + [buttons],
                    scrollable=True,
                    vertical_scroll_only=True,
                    size=(600, 300),
                )
            ],
        ],
        size=(600, 300),
        resizable=True,
        keep_on_top=SG_KWARGS["keep_on_top"],
        icon=SG_KWARGS["icon"],
    )
    while True:
        event, values = choices_window.read(close=False)
        if event == "Accept":
            selected_choices.clear()
            selected_choices.extend(k for k in choices if values[k])
            choices_window.close()
            return True
        if event == "License Help":
            webbrowser.open("https://choosealicense.com/licenses/")
        if event is None or event == "Cancel":
            choices_window.close()
            return False
