# Vmla-cli

This Python tool has two main purposes : 
- Easily extracting an ESXi or a vCenter log bundle file.
- Search for expressions within the extracted files, and generate a .json report file containing all the matching expressions found in the extracted log bundle.

This has been made and tested using : 
- Python 3.12 (with no additional modules)
- Fedora 40 / Ubuntu 24.04

Should also work on MacOS (I don't have a MacOS machine to test it though).

On Windows, I've quickly tested it but I ran into permission issues while extracting the log bundles, so I'm assuming it's not supported on this OS.

# How to use it

### 1. Run `main.py` once

This will create all the required subfolders in main vmla-cli folder : 
- `/sources_files`
- `/extracted_files`
- `/reports`
- `/custom_searches`

Quit the program and relaunch it then.

### 2. Put your log bundle file(s) in the /source_files folder

ESXi and vCenter log bundles are supported.

### 3. Extract at least one log bundle file

From the main menu, choose the "extract" entry; This should list all your .zip log bundle files found in the `/source_files` folder.
You can then choose to perform a normal extraction or a full extraction. 
- normal : nested .gz files won't be extracted.
- full : recursive extraction that will extract all the archived files found in the archive. ***WARNING*** This will use a lot a disk space !!

Depending on the log bundle size and computer's performances, it can take a while, please be patient.

All extracted files are put in the `/extracted_files` folder.

### 4. Analyse the extracted log bundle

Once you have extracted at least one log bundle, you can now go to the 'analyse' menu. 

Choose the folder to analyse, bundle type will be detected automatically (ESXi or vCenter), and from there you can choose to perform :
- A generic search : this will search for common errors patterns in the bundle.
- Custom search : this will use the custom expressions available in the `/custom_searches` sub folder. See next points for info.

***Note*** : from the main menu, you can activate ***verbose*** mode : as the name implies, you'll get a verbose output during the parsing/searching process.

### 5. Use custom search

To search for custom expressions of your choice, create a .txt file with these expressions.

Example : 

        Destroy VM called
        esx.problem
        vm-xxxxx

Put one expression by line, without quotes. Beware of case sensitivity.

Then save this file and it will available in the "custom search" menu. You can use multiple .txt files in this folder.

### 6. Get the search report

Once the search operation is done, a `.json` file containing the results will be generated and put in the `/reports` folder.
Any web browser can be used to display this file, or use the application / tool of your choice to work with the datas in this `.json` file.






