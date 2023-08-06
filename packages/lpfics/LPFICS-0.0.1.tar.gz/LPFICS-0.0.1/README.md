LPFICS Lib to find incompatible constraints set in Linear Problems
================================================================

LPFICS Idea
-----------
**Objective**: This project aims to enable to find ONE incompatible constraint set if a 
model is considered infeasible once resolved.
Note that it MAY NOT be the ONLY ONE set of constraints making your problem infeasible.

This project is based on PuLP (https://github.com/coin-or/pulp) a LP modeler written 
in Python. PuLP integrates the solver CBC. This solution works with CBC, and GLPK solvers
but does not work with Gurobi (as the output is always NotSolved and not Infeasible if 
the problem is overconstrainted).


Here is a simplified explaination:
If a problem is overconstrainted, the problem will:
- test to solve the problem with the first half of the constraints
    - if there is no solution it continues taking the first half (of the half) 
    of the constraints
    - if there is a solution, it will test the other half
        - if the second half has no solution it will continue dividing the second half
        set of constraints to test it
        - if the second half has a solution it will rearrange the constraints and 
        test again


References
----------
The methodology (quickXplain) on which the program is based is described, discussed and modeled on the following references: 

Junker, Ulrich. 2004. « QUICKXPLAIN: Preferred Explanations and Relaxations 
for Over-Constrained Problems », In: _AAAI-04_. San Jose. https://www.aaai
.org/Papers/AAAI/2004/AAAI04-027.pdf

Morriet, Lou, Benoit Delinchant, Gilles Debizet, Frédéric Wurtz. 2020. « 
Algorithme d identification de contraintes incompatibles pour les problemes 
d optimisation : application à un projet energetique ». In: _soumis à IBPSA 
2020_. 

Rodler, Patrick. 2020. « Understanding the QuickXPlain Algorithm: Simple 
Explanation and Formal Proof ». ArXiv:2001.01835, janvier. http://arxiv
.org/abs/2001.01835.

Verger, Guillaume, 2016. Ruby-Cbc [Logiciel]. Ruby. In : _Github_. Consulte
 le 15 novembre 2020, https://github.com/gverger/ruby-cbc.



Installation Help
-----------------
Please install LPFICS Lib with pip using the command prompt and type:   

pip install git+https://gricad-gitlab.univ-grenoble-alpes.fr/omegalpes/lpfics.git

Please ask omegalpes-users@groupes.renater.fr if you are struggling during your installation


Library Installation Requirements
---------------------------------
PuLP > 1.6.10
 
 
Copyright
=========
This project contains a derivative work based on https://github.com/gverger/ruby-cbc. 
Project ruby-cbc is released under the MIT license, Copyright 2016 Guillaume Verger.
Modifications Copyright 2019 G2Elab / MAGE
See the LICENSE file for copyright information.
 
 
Main Authors: 
=============
Guillaume VERGER

Lou MORRIET


Partners:
=========
Univ. Grenoble Alpes, CNRS, Grenoble INP, G2Elab, CEA, Université Paris-Sud


Acknowledgments:
================
This work has been partially supported by the CDP Eco-SESA receiving fund from the French National Research 
Agency in the framework of the "Investissements d’avenir" program (ANR-15-IDEX-02), by the ADEME, the French Agency for Environment and Energy
Management, with the RETHINE project and by the Region Auvergne Rhône Alpes with the project OREBE.
