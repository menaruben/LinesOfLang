from argparse import ArgumentParser, Namespace
from os import getcwd, walk, path
import tabulate
import toml

def get_default_extensions() -> list:
    with open("langs.toml") as f:
        data = toml.load(f)

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

# store arguments to variables
args: Namespace = parser.parse_args()
arg_path = args.path
arg_extensions = args.extensions

# create code class
class Code:
    def __init__(self, path: str, extensions: str) -> None:
        self.path = path
        self.extensions = extensions
        self.files = []
        self.num_of_lines = 0
        self.found_extensions = []
        self.found_languages = []

    def get_files(self):
        for root, dirs, files in walk(self.path):
            for name in files:
                for extension in self.extensions:
                    if name.endswith(extension):
                        file_path = path.join(root, name)
                        self.files.append(file_path)

                        if extension not in self.found_extensions:
                            self.found_extensions.append(extension)

    def count_lines(self):
        count = 0
        for file in self.files:
            with open (file,"r", encoding="utf-8", errors="ignore") as f:
                count += len(f.readlines())

        self.num_of_lines = count

    def get_found_languages(self):
        found_languages = []
        with open("langs.toml") as f:
            data = toml.load(f)

        for lang in data:
            for extension in data[lang]["extensions"]:
                if extension in self.found_extensions:
                    self.found_languages.append(lang)
                    break

    def output(self):
        output_msg = [
            [self.path, self.num_of_lines, self.found_languages , self.found_extensions]
        ]

        print(tabulate.tabulate(output_msg,
                                headers=["path",
                                         "lines of code",
                                         "found languages",
                                         "found extensions"]))

# create Code object
code_obj = Code(arg_path, arg_extensions)

# get files and lines of code number
code_obj.get_files()
code_obj.count_lines()
code_obj.get_found_languages()

# output
code_obj.output()
