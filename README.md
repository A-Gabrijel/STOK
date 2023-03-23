# STOK - Simple TOKamak
A tool for parametric generation of simple rectangular tokamaks.

*Note that this tool is in its infancy and a lot of things will change.*

## DESCRIPTION
STOK is an attempt to solve long model develeopment times in fusion. The code was inspired by [paramak](https://github.com/fusion-energy/paramak) and is meant to create simulation models for MC (Monte Carlo) simulations. It returns a specified component, which can then be exported into various CAD (Computer Aided Design) formats for further use.

STOK is meant to be a sort of Lego set of components that the user can use or omitt and create a model that is tailored to his need. It is completely parametric, meaning no building block is fixed; all of them can be changed with one or more parameters.

It's completely based on [CadQuery](https://github.com/CadQuery) and returns [CadQuery](https://github.com/CadQuery) objects, so every object can be further improve uppon with it.

For exporting .stl files [CadQuery](https://github.com/CadQuery) was found to produce leaky meshes, so we opted to use [pygmsh](https://github.com/nschloe/pygmsh) which is a meshing tool that is better suited for creating meshes than CadQuery.

## STOK usage
STOK is controlled through a set of .txt files with which we controll the boundaries of the reactor model. After the parameters in the configuration files are set, build.py can be inported and classes inside can be used.
Each function is meant to be run in a for loop where the index paramater of the function is the index i in the loop. The functions return a CQ.shape object that can then be exported with the help of [CadQuery](https://github.com/CadQuery)
