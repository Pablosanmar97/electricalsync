# electricalsync

Objective:

This project serves to analyse the synchronization between electrically coupled neurons in an spike-by-spike comparison and timing delays.


Structure:

It comprises a Main script which handles:
  1. signal processing
  2. spike detection
  3. spike relocation (one neuron should be aware of missing spikes in the other one)
  4. Several analyses

It also includes an adittional Utilities script with custom functions (filters, ...)

# installation

Download and in the main electricalsync folder run the following command: pip install -e .

This initializes the utilities script so that the Main one can use it
