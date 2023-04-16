# LinesOfLang - LoL
LinesOfLang - also called LoL - is a command line application that tells you the how much lines of code of (a) language(s) you have written inside a specified path (including subfolders).

## Documentation
NOTE: It is recommended to add [main.py](./src/main.py) to your path with a short name like "lol". I did this for the documentation. So please keep that in mind.

### Help
```
usage: main.py [-h] [-p path] [-e extensions [extensions ...]] [-r | --recursive | --no-recursive] [-t | --table | --no-table]

LoL.py is used to get the lines of code inside a directory

options:
  -h, --help            show this help message and exit
  -p path, --path path  specifies the path to the directory
  -e extensions [extensions ...], --extensions extensions [extensions ...]
                        specifies the file extensions that should be searched
  -r, --recursive, --no-recursive
                        states that the file search should not be recursive (default: True)
  -t, --table, --no-table
                        states that the output should be formatted to a (vertical) table (default: False)
```

### Examples
#### Default
The default value of the argmuent ```-e```/```--extensions``` gives you the languages shown inside the [langs.toml](./src/langs.toml). If you don't see your language please add it to the [langs.toml](./src/langs.toml) in order to use the default value of extensions. If you execute the following command path argument will take the current working directory as its value and search for files recursively by deafult:
```
$ lol
```
This will generate the following output:
```
----------------  ----------------------------
path              /home/rubi/repos/LinesOfLang
lines of code     251
found languages   ['Python']
found extensions  ['.py', '.pyc']
----------------  ----------------------------
```

#### Search inside specific path
If you want to search inside a folder other than your current working directory then feel free to use the ```-p```/```--path``` argument:
```
$ lol -p C:\repos\TomlForge
```
This will produce the following output:
```
----------------  ---------------------------
path              /home/rubi/repos/TomlForge/
lines of code     146
found languages   ['PowerShell']
found extensions  ['.psm1', '.ps1']
----------------  ---------------------------
```

#### Search for specific extension(s)/languages
If there is there is a specific file extension you are searching for just use the ```-e```/```--extensions``` argument:
```
$ lol -p C:\repos\TomlForge -e ps1
```
```
----------------  --------------------
path              /home/rubi/repos/dev
lines of code     367
found languages   []
found extensions  ['rb', 'rs']
----------------  --------------------
```

As you can see he language does not get added to the found languages column. I am currently working on fixing this small issue. In the future you will also be able to load your own [langs.toml](./src/langs.toml) file with ```-l```/```--load``` but for now you'll have to rename the current one and replace it with your own.

#### Format output to table
The output by default is a horizontally aligned list. In order to format it to a (vertical) table you need to use the ```-t```/```--table```argument. This is especially useful when you find a lot of languages/extensions. The table makes it more readable.
```
$ lol -t
```
```
path                    lines of code  found languages    found extensions
--------------------  ---------------  -----------------  ------------------
/home/rubi/repos/dev              676  JavaScript         .ps1
                                       Python             .rb
                                       Ruby               .py
                                       Rust               .js
                                       PowerShell         .pyc
                                                          .rs
```

#### Disable recursive search
The recursivce search for files is by deafult true. In order to disable this use the ```--no-recursive``` argument.
```
$ lol --no-recursive
```
```
----------------  ------------------------------
path              /home/rubi/repos/TomlForge/src
lines of code     184
found languages   []
found extensions  []
----------------  ------------------------------
```
