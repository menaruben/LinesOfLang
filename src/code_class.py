from argparse import ArgumentParser, Namespace, BooleanOptionalAction
from os import getcwd, walk, path, listdir
import sys
from pathlib import Path
from toml_langs import *

try:
    from tabulate import tabulate
    from toml import load
except ModuleNotFoundError:
    from subprocess import run, DEVNULL
    run(["pip", "install", "tabulate"], stdout=DEVNULL, stderr=DEVNULL, check=False)
    run(["pip", "install", "toml"], stdout=DEVNULL, stderr=DEVNULL, check=False)
    from tabulate import tabulate
    from toml import load

script_dir = Path( __file__ ).parent.absolute()
langs_toml = fr"{script_dir}/langs.toml"

parser = ArgumentParser(description="used to get the lines of code inside a directory")

# add argumentsBooleanOptionalAction
parser.add_argument("-p", "--path",
                    metavar="path",
                    type=str,
                    help="specifies the path to the directory",
                    default=f"{getcwd()}")

parser.add_argument("-e", "--extensions",
                    metavar="extensions",
                    nargs="+", type=str,
                    help="specifies the file extensions that should be searched",
                    default=get_default_extensions())

parser.add_argument("-r", "--recursive",
                    metavar="recursive",
                    type=bool,
                    action=BooleanOptionalAction,
                    help="states that the file search is (not) recursive",
                    default=True
                    )

parser.add_argument("-t", "--table",
                    metavar="table",
                    type=bool,
                    action=BooleanOptionalAction,
                    help="states that the output should be formatted to a (vertical) table",
                    default=False
                    )

args: Namespace = parser.parse_args()

# create code class
class Code:
    """
    stores all information about the code inside a specific path
    """

    def __init__(self) -> None:
        self.path = args.path
        self.extensions = args.extensions
        self.is_table = args.table
        self.is_recursive = args.recursive
        self.files = []
        self.num_of_lines = 0
        self.found_extensions = []
        self.found_languages = []

    def test_found_extensions(self, extension):
        """
        adds the extension given to the found_extensions
        array if it isn't already inside the array
        """
        try:
            if extension not in self.found_extensions:
                self.found_extensions.append(extension)

        except ValueError as exception_message:
            print(f"Error testing the found extensions: {exception_message}")

    def get_files_recursive(self):
        """
        stores all file paths to self.files with the extensions given (recusive)
        """
        try:
            for root, _, files in walk(self.path):
                for name in files:
                    for extension in self.extensions:
                        if name.endswith(extension):
                            file_path = path.join(root, name)
                            self.files.append(file_path)

                            self.test_found_extensions(extension)

        except ValueError as exception_message:
            print(f"Error searching for files: {exception_message}")
            sys.exit()

    def get_files_not_recursive(self):
        """
        stores all file paths to self.files with the extensions given (not recusive)
        """
        try:
            self.files = [file for file in listdir(self.path) if path.isfile(file)]
        except ValueError as exception_message:
            print(f"Error searching for files: {exception_message}")

    def test_files(self):
        """
        this tests wether or not the user wants to get the files recursively
        """
        if self.is_recursive:
            self.get_files_recursive()
        else:
            self.get_files_not_recursive()

    def count_lines(self):
        """
        counts the amount of lines of files array
        """
        try:
            count = 0
            for file_path in self.files:
                with open (file_path,"r", encoding="utf-8", errors="ignore") as file:
                    count += len(file.readlines())

            self.num_of_lines = count

        except TypeError as exception_message:
            print(f"Error coutning the number of lines: {exception_message}")
            sys.exit()

    def get_found_languages(self):
        """
        maps found extensions to found language and
        adds to found_language
        """
        try:
            with open(langs_toml, encoding="utf-8") as file_path:
                data = load(file_path)

            for lang in data:
                for extension in data[lang]["extensions"]:
                    if extension in self.found_extensions:
                        self.found_languages.append(lang)
                        break

        except FileNotFoundError as exception_message:
            print(f"Error mapping the found extensions to found languages: {exception_message}")

    def output_v(self):
        """
        prints the attributes to terminal in a formatted way
        """
        try:
            output_msg = [
                [self.path,
                self.num_of_lines,
                # self.found_languages,
                "\n".join(self.found_languages),
                # self.found_extensions
                "\n".join(self.found_extensions)
                ]
            ]

            print(
                tabulate(
                output_msg,
                headers=["path",
                        "lines of code",
                        "found languages",
                        "found extensions"
                        ]))
        except NameError as exception_message:
            print(f"Error printing the output to the terminal: {exception_message}")
            sys.exit()

    def output_h(self):
        """
        prints the attributes to terminal in a formatted way
        """
        try:
            output_msg = [
                ["path", self.path],
                ["lines of code", self.num_of_lines],
                ["found languages", self.found_languages],
                ["found extensions", self.found_extensions]
            ]

            print(
                tabulate(
                output_msg#,
                ))

        except NameError as exception_message:
            print(f"Error printing the output to the terminal: {exception_message}")
            sys.exit()

    def test_output(self):
        """
        checks wether the user wants the output to be printed out as a table
        """
        if self.is_table:
            self.output_v()
        else:
            self.output_h()
