# Het Concertgebouw, an Agent Based Model Implementation

## Background
This repository contains the code used to model crowdflow simulation in Het Concertgebouw. 
The model is used to test whether changing the entrance to the north side will help with spreading crowd flow more evenly over the building. 
A statistical test concludes that the new entrance does help reducing crowd density.

## Code overview
Firstly, this repository started as a fork of @mblasiak [CrowdMovmentSimulation repository](https://github.com/mblasiak/CrowdMovmentSimulation). A huge thanks to them as a large
part of our code runs using their functions.

We have however pivoted the function of the original model (evacuation) to work for crowdflow simulations in a building.

### How to run:
0. `gradient_main.py` This is the main class which is used to start the simulations. You can run it without modifying the `MapConf` (parameters for the simulation)
by running it with the default values as `example_simulation = GradientMain(None).run()`

1. `SIM_compare_entrances.py` this file modifies the ConfigMap in order to start the simulations
as we have run them for our report. It then uses multiprocessing to run multiple instances of our model using the max
CPU's available. After these simulations have finished it continues to do the exact same as before however this time
the simulation is run with a different entrance. This simulations can be terminated with the density data being 
written to the src/Logs folder. 

2. `SIM_sensitivity_analysis.py` this file modifies the ConfigMap in order to start the simulations
as we have run them for our report. In this case multiple instances of the simulation are started
with different parameters, first using Sensitivity Analysis OFAT (one factor at a time), with the data
also being written to the src/Logs folder Afterwards, multiple Global SA instances are started 
of the model, where the output is also written to src/Logs.

> :warning: **ConfigMap passing works only on Linux/MacOS systems**

3. `analyse_compare_entrances.py` file which performs analysis of the `SIM_compare_entrances.py` data.
A boxplot is generated of the data in src/plots. It also outputs the t-test values to report on statistical difference
between the South vs North entrance of the simulations. 

4. `OFAT_analyses.py` file which performs analysis on the `SIM_sensitivity_analysis.py` data, only OFAT.
5. `Global_sa.py` file which performs analysis on the `SIM_sensitivity_analysis.py` data, but this time Global SA. 