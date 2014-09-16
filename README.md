Training of pileup jet ID with and without fast timing information
======

Requirements: 

1) Create flat ROOT trees from Bacon trees by running $CMSSW_BASE/src/SetupsAndPlotting/create_jet_trees.py for the needed scenarios and put them under ./data
2) A recent ROOT version including TMVA

======

Scripts
-------

plot_inputs.py: Plots the input distributions
tmva_cat_training.py: Performs the training with and without timing information
make_roc.py: Creates the ROC curves using the test trees from the TMVA training

