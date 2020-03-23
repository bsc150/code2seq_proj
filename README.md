# code2seq_proj 

### how to run
There is a auto.sh file in the code2seq directory that should run all of the preprocess of relevant to the project.
In order to run it use:
```
bash auto.sh
```

Explanation about the other files:

The code2seq directory is a clone of the code2seq github for comfort. Note that the github project is probably still in development so you might need to update it's content.

our_preprocess.py: gets a file name as a parameter, and outputs a file that we will later split into train, val and test files.

our_preprocess_blocks.py: acts the same as the previous file, except it does so while outputing a file with a different symbolic execution analisys (explained further in the report).

Our_preprocess_n_constraints.py: acts the same as our_preprocess.py but outputs only the first n contraints instead of the while trace and constraints into the output file.

bash_script.py: runs our_preprocess.py for all of the executable files in a directory and groups all of the results in a single output file.

post_preprocess.py: manipulates the preprocess output file, according to reseach method picked in the file.

splitted_data directory: has the files we generated for the network.
