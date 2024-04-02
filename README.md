# STOK - Simple TOKamak
A tool for parametric generation of simple tokamaks with rectangular cross-section.

Authors: Anže Gabrijel, Aljaž Čufar

## DESCRIPTION
STOK is an attempt to solve long model development times in fusion. The code is meant to create relatively simple simulation models for Monte Carlo simulations, e.g. .stl files for use in Serpent 2. It is meant to be a sort of a book of receipts for reactor components that the user can either use or omit when creating a model that is tailored to their needs. It is completely parametric, meaning that no building block is fixed; all of them can be changed with one or more parameters. Once its parameters are specified STOK draws a specified component, which can then be exported into various CAD (Computer Aided Design) formats for further use. 

STOK is completely based on [CadQuery](https://github.com/CadQuery) and returns [CadQuery](https://github.com/CadQuery) objects, so every object can be further modified with it.

For exporting .stl files [CadQuery](https://github.com/CadQuery) was found to produce leaky meshes, so we opted to use [pygmsh](https://github.com/nschloe/pygmsh) which is a meshing tool that is better suited for creating meshes than CadQuery.

Initial internal development of STOK perdates the public release of [Paramak](https://github.com/fusion-energy/paramak) but this released version also draws some inspiration from it as some of the underlying workflow is similar. In our oppinion even with future updates STOK should remain in the domain of very simple reactor models while users requiring more realistic models should use [Paramak](https://github.com/fusion-energy/paramak).

## INSTALLATION AND DEPENDENCIES
Installing STOK can be done through pip in the following way:
```bash
pip install git+https://github.com/A-Gabrijel/STOK@<branch-or-tag>
```

For example, to install directly from master the syntax would be:
```bash
pip install git+https://github.com/A-Gabrijel/STOK@main
```
## ACKNOWLEDGEMENTS
The authors acknowledge the financial support from the Slovenian Research an Innovation Agency (research project Z2-3201, research program No. P2-0073).
