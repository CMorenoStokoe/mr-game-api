About:
These compilers/recompilers prepare data for use in the game's API. Used to produce new data (i.e., traits) for simulation.

Instructions:
1) First obtain new MR estimates using the MR compiler (requires R)
2) Run the MRNV compiler, which will take the R output, convert it to JSON and format it as a list of nodes and edges, D3-formatted, (requires Python)
3) Run the game recompiler, which will take formatted JSON file and re-format it for use in the game API