# Identifying Boundary Conditions 

## packages needed
```
spot
```
You may need to install Spot's python package according to Spot's introduction. https://spot.lrde.epita.fr/install.html

## Usage
Run the solver with default configuration:
```
python BC_solver.py
```
With the default configuration, `AAP` will be the case, and by the automate-based method `aut`.

See more configuration:
```
postman.py -h
```

## Data
The cases are listed in `goal_case\`. The BCs in the case file are computed by the previous work. 

The result of SemanticBC will be in `case_result\` and the result of SyntacBC be in `case_result_aut\`.