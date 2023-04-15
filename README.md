# LinesOfLang - LoL
LinesOfLang - also called LoL - is a command line application that tells you the how much lines of code of (a) language(s) you have written inside a specified path (including subfolders).

## Usage
The default argument ```-e``` or ```--extensions``` gives you the languages shown inside the [langs.toml](./src/langs.toml). If you don't see your language please add it to the [langs.toml](./src/langs.toml) in order to use the default value of extensions. If you execute the following command path argument will take the current working directory as its value:
```
python lines_of_langs.py
```
This will generate the following output:
```
path                lines of code  found languages    found extensions
----------------  ---------------  -----------------  ------------------
C:\repos\LoL\src               96  ['Python']         ['.py']
```

If you want to search inside a folder other than your current working directory then feel free to use the ```-p``` or ```--path``` argument:
```
python lines_of_langs.py -p C:\repos\TomlForge
```
This will produce the following output:
```
path                   lines of code  found languages    found extensions
-------------------  ---------------  -----------------  ------------------
C:\repos\TomlForge\               26  ['PowerShell']     ['.ps1']
```

If there is there is a specific file extension you are searching for just use the ```-e``` or ```--extensions``` argument:
```
python lines_of_langs.py -p C:\repos\TomlForge -e ps1
```
```
path                   lines of code  found languages    found extensions
-------------------  ---------------  -----------------  ------------------
C:\repos\TomlForge\               26  []                 ['ps1']
```

As you can see he language does not get added to the found languages column. I am currently working on fixing this small issue. In the future you will also be able to load your own [langs.toml](./src/langs.toml) file with ```-l``` or ```--load``` but for now you'll have to rename the current one and replace it with your own.
