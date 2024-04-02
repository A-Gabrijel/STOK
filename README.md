# STOK - Simple TOKamak
A tool for parametric generation of simple rectangular tokamaks.

## DESCRIPTION
STOK is an attempt to solve long model develeopment times in fusion. The code was inspired by [paramak](https://github.com/fusion-energy/paramak) and is meant to create simulation models for MC (Monte Carlo) simulations. It returns a specified component, which can then be exported into various CAD (Computer Aided Design) formats for further use.

STOK is meant to be a sort of Lego set of components that the user can use or omitt and create a model that is tailored to his need. It is completely parametric, meaning no building block is fixed; all of them can be changed with one or more parameters.

It's completely based on [CadQuery](https://github.com/CadQuery) and returns [CadQuery](https://github.com/CadQuery) objects, so every object can be further improve uppon with it.

For exporting .stl files [CadQuery](https://github.com/CadQuery) was found to produce leaky meshes, so we opted to use [pygmsh](https://github.com/nschloe/pygmsh) which is a meshing tool that is better suited for creating meshes than CadQuery.

## INSTALLATION AND DEPENDANCIES
Installing STOK can be done trough pip in the following way:
```bash
pip install git+https://github.com/A-Gabrijel/STOK@<branch-or-tag>
```

For example to install directly from master the syntax would be:
```bash
pip install git+https://github.com/A-Gabrijel/STOK@main
```
