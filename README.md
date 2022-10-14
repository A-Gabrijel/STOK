# STOK
A tool for parametric generation of simple rectangular tokamaks.

*Note that this tool is in its infancy and a lot of things will change.*

## STOK usage
STOK is controlled through a set of .txt files with which we controll the boundaries of the reactor model. After the parameters in the configuration files are set, build.py can be inported and classes inside can be used.
Each function is meant to be run in a for loop where the index paramater of the function is the index i in the loop. The functions return a CQ.shape object that can then be exported with the help of [CadQuery](https://github.com/CadQuery)
