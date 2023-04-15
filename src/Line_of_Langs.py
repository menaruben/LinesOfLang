from argparse import ArgumentParser, Namespace
from os import getcwd, walk, path, system
try:
    from tabulate import tabulate
    from toml import load
except:
    system("pip install tabulate")
    system("pip install toml")
    from tabulate import tabulate
    from toml import load

def get_default_extensions() -> list:
    """
    returns the default extensions from the langs.toml file (must be in the same folder)
    """
    with open("langs.toml", encoding="utf-8") as file_path:
        data = load(file_path)

    default_extensions = []
    for lang in data:
        default_extensions.extend(data[lang]["extensions"])

    return default_extensions

parser = ArgumentParser(description="LoL.py is used to get the lines of code inside a directory")

# add path and languages arguments
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

args: Namespace = parser.parse_args()

# create code class
class Code:
    """
    stores all information about the code inside a specific path
    """
    def __init__(self) -> None:
        self.path = args.path
        self.extensions = args.extensions
        self.files = []
        self.num_of_lines = 0
        self.found_extensions = []
        self.found_languages = []

    def test_found_extensions(self, extension):
        """
        adds the extension given to the found_extensions
        array if it isn't already inside the array
        """
        if extension not in self.found_extensions:
            self.found_extensions.append(extension)

    def get_files(self):
        """
        gets all files paths to file with the extensions given
        """
        for root, _, files in walk(self.path):
            for name in files:
                for extension in self.extensions:
                    if name.endswith(extension):
                        file_path = path.join(root, name)
                        self.files.append(file_path)

                        self.test_found_extensions(extension)

    def count_lines(self):
        """
        counts the amount of lines of files array
        """
        count = 0
        for file_path in self.files:
            with open (file_path,"r", encoding="utf-8", errors="ignore") as file:
                count += len(file.readlines())

        self.num_of_lines = count

    def get_found_languages(self):
        """
        maps found extensions to found language and
        adds to found_language
        """
        with open("langs.toml", encoding="utf-8") as file_path:
            data = load(file_path)

        for lang in data:
            for extension in data[lang]["extensions"]:
                if extension in self.found_extensions:
                    self.found_languages.append(lang)
                    break

    def output(self):
        """
        prints the attributes to terminal in a formatted way
        """
        output_msg = [
            [self.path, self.num_of_lines, self.found_languages , self.found_extensions]
        ]

        print(tabulate(output_msg,
                                headers=["path",
                                         "lines of code",
                                         "found languages",
                                         "found extensions"]))

# create Code object
code_obj = Code()

# get files and lines of code number
code_obj.get_files()
code_obj.count_lines()
code_obj.get_found_languages()

# output
code_obj.output()
