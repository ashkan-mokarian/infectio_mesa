# Description
infectio_mesa

Virus spread simulation using ABM (in mesa) implementing simple Random walk cell motility.

# How to run
`python run.py`.

# Notes
Running with naive assumptions:

* motility: RW with fixed speed conditioned on state
* cell-cell infection: arbitrary numbers for a sigmoid probability model
* cell death: after 50 steps of infection

Missing elements:

* lysis
* molecular diffusion
