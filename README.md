# agent-based-model
Agent based model developed during a set of university Python programming course practicals.
This program has been developed with guidance and material provided by the University of Leeds.

Agents are able to move about the environment, eat from the environment store at their position, be sick and deposit most of their store at their current position if they have consumed too much, and share their resources equally with other agents within a specified radius of themselves.

The user has control over a number of input paramenters:
  - number of agents
  - store capacity
  - consumption rate
  - move cost
  - neighbourhood
  - environment growth rate
  - number of iterations
  - animation frame interval

There are two stopping conddtions: 
  - the specified number of iterations has been completed 
  - one of the agents stores has fallen below zero after the eating, moving, sharing with neighbours actions have been resolved for that       iteration (a message will appear in the command prompt if this has occurred).

Guidance to run the files: 
Download and save the files to your computer. Maintain the file structure provided. The program will generate a Model_output folder in which the output files of your program runs will be saved. Main is 'model.py' for a single model run or 'model_runner.py' if multiple combinations of input parameters are to be set and automatically run through to generate a full set of results. 'model_runner.py' can be run using the provided Windows Batch File, however you must edit the input parameters directly inside 'model_runner.py'. Alternatively, in the directory that you saved the program files, the program can be run by entering 'python model_runner.py' once the parameters are set or 'python model.py' and following the instructions at the command line. 'model_runner.py' can also be run from an integrated development environment (IDE), however, 'model_runner.py' cannot.

Please note: This file has been created using Python 3.6. There may be compatibility issues if using other versions of Python. This file has been written using a Windows operating system for a Windows operating system. There may be compatibility issues if running using a different operating system.
