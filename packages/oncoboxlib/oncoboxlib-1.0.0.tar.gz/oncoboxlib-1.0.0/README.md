# oncoboxlib

Oncobox Library which calculates scores.

## Installation

```
pip install oncoboxlib
```

## How to run the example

1. Create any directory that will be used a sandbox. Let's assume it is named `sandbox`.


2. Extract `resources/databases.zip` into `sandbox/databases/`.
  <br> (You may download it from 
  `https://gitlab.com/oncobox/oncoboxlib/-/blob/master/resources/databases.zip`)
  

3. Extract example data `resources/cyramza_normalized_counts.txt.zip` into `sandbox`.
  <br> (You may download it from 
  `https://gitlab.com/oncobox/oncoboxlib/-/blob/master/resources/cyramza_normalized_counts.txt.zip`)
  

What it looks like now:
```
   - sandbox
       - databases
           - Balanced 1.123
           - KEGG Adjusted 1.123
           ...
       - cyramza_normalized_counts.txt  
```

4. Change directory to `sandbox` and execute the command:
```
calculate_scores --databases-path=databases/ --samples-file=cyramza_normalized_counts.txt
```
It will create a result file `sandbox\pal.csv`.


Alternatively, you can use it as a library in your source code.
For details lease see `examples` directory.
