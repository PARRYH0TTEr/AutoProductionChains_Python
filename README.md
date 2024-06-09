# Automating the creation of production chains in Factorio

This repository hosts the implementation of the program I developed alongside my bachelors thesis.

## Usage

Make sure you have Factorio installed, as the project utilizes the "import string" feature to import the generated production chains..

### Downloading

You can either download the program via : Code -> Download ZIP and then extracing the contents, or by opening a Git terminal and cloning the repository with the following command
```
git clone git@github.com:PARRYH0TTEr/AutoProductionChains_Python.git
```

### Dependencies

The following dependencies are required to run the program:
* [Factorio-Draftsman, v1.1.1](https://github.com/redruin1/factorio-draftsman) - An API to interact and communicate with the blueprint system.
* [Pyperclip, v1.8.2](https://github.com/asweigart/pyperclip) - Library that copies the generated production chain string directly to the clipboard, so you don't have to.
* [Treelib, v1.7.0](https://github.com/caesar0301/treelib) - Library to represent N-ary trees in the code.

### Running the program

Once the program has been downloaded, navigate to "AutoProductionChains_Python" folder. 

Open a terminal window inside this folder and run the following command:
```
python Main.py <outputAmount> <outputType> <outputRate> <runOrTest>
```
* &lt;outputAmount&gt;: Not implemented yet. Just input some random integer for now.
* &lt;outputType&gt;: Implemented and works with the following output types:
    - Coal -> ```coal```
    - Iron ore -> ```iron-ore```
    - Copper ore -> ```copper-ore```
    - Iron plate -> ```ironplate```
    - Copper plate -> ```copperplate```
    - Iron gear wheel -> ```irongearwheel```
    - Copper cable -> ```coppercable```
    - Automation science pack -> ```automationsciencepack```
* &lt;outputRate&gt;: Not implemeted yet. Just input some random single character like 's' for now.
* &lt;runOrTest&gt;: Implemented and denotes if the program execution should be ran in normal or testing mode. It supports the following parameters:
    - Normal mode -> ```-r```
    - Test mode -> ```-t```
    - Verbose test mode -> ```-tverbose```
 
As an example, running the following command will generate a production chain that can produce copper plates:
```
python Main.py 0 copperplate s -r
```
A string-representation of the production chain will automatically be copied to your clipboard and ready to be pasted into Factorio.

### Importing the production chain into Factorio

NOTE: If you are already familiar with Factorio and how to use its blueprint system, you can skip this section

Step 01: Start by launching Factorio and open the "Map Editor"

![Step 01](https://github.com/PARRYH0TTEr/AutoProductionChains_Python/blob/master/GithubRepo/Images/Factorio_Guide01.png)

Step 02: Press "New Scenario"

![Step 02](https://github.com/PARRYH0TTEr/AutoProductionChains_Python/blob/master/GithubRepo/Images/Factorio_Guide02.png)

Step 03: Select the "SandBox" game scenario and press "Next"

![Step 03](https://github.com/PARRYH0TTEr/AutoProductionChains_Python/blob/master/GithubRepo/Images/Factorio_Guide03.png)

Step 04: Press "Play" in the new window

![Step 04](https://github.com/PARRYH0TTEr/AutoProductionChains_Python/blob/master/GithubRepo/Images/Factorio_Guide04.png)

Step 05: Once ingame, press the "Import String" button

![Step 05](https://github.com/PARRYH0TTEr/AutoProductionChains_Python/blob/master/GithubRepo/Images/Factorio_Guide05.png)

Step 06: Paste in the generated string from running the program in the textbox and press "Import"

![Step 06](https://github.com/PARRYH0TTEr/AutoProductionChains_Python/blob/master/GithubRepo/Images/Factorio_Guide06.png)

Step 07: A blueprint of the production chain that can generate the output type you provided the program appears and you can freely place it into the game world

![Step 07](https://github.com/PARRYH0TTEr/AutoProductionChains_Python/blob/master/GithubRepo/Images/Factorio_Guide07.png) ![Step 08](https://github.com/PARRYH0TTEr/AutoProductionChains_Python/blob/master/GithubRepo/Images/Factorio_Guide08.png)

