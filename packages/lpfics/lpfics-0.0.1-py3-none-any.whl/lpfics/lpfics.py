#! usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
**This module enables to identify a set of constraints which leads to an
overconstrainted problem for MILP (Mixed Integer Linear Programming) problems**

..
    Copyright © 2016 Guillaume Verger
    Modifications Copyright © 2019 G2Elab / MAGE

    Permission is hereby granted, free of charge, to any person obtaining a
    copy
    of this software and associated documentation files (the "Software"), to
    deal in the Software without restriction, including without limitation the
    rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS
    IN THE SOFTWARE.
"""

import sys

from pulp import LpStatus

from omegalpes.general.optimisation.elements import *

if sys.platform not in ['cli']:
    # iron python does not like an OrderedDict
    try:
        from odict import OrderedDict

        _DICT_TYPE = OrderedDict
    except ImportError:
        pass
    try:
        # python 2.7 or 3.1
        from collections import OrderedDict

        _DICT_TYPE = OrderedDict
    except ImportError:
        pass


def find_infeasible_constraint_set(lp_model):
    """
    Identifies a set of constraints creating infeasibility

    :param lp_model: lp model of the project
    :return: new_lp_constraints : the set of constraints of the lp model
    """
    print('\nWith LPFICS:\n'
          'Testing if the project is feasible.\n'
          'If not, finding a set of constraints leading to the '
          'infeasibility\n')

    new_lp = lp_model.copy()

    new_lp_constraints = _find_infeasible_cst(lp_model, new_lp)

    return new_lp_constraints


def find_definition_and_actor_infeasible_constraints_set(lp_model):
    """
    Identifies a set of external constraints - without technical constraints -
    creating infeasibility

    :param lp_model: lp model of the project
    :return: new_lp_constraints : the set of constraints of the lp model
    """
    print('\nWith LPFICS:\n'
          '\nTesting if the project is feasible considering the actors '
          'constraints\n'
          'If not, finding a set of constraints leading to the '
          'infeasibility.\n')

    new_lp = lp_model.copy()

    new_lp = _def_actor_csts(lp_model=new_lp)

    new_lp_constraints = _find_infeasible_cst(lp_model, new_lp)

    return new_lp_constraints


def find_definition_and_technical_infeasible_constraints_set(lp_model):
    """
    Identifies a set of physical constraints - without external constraints -
    creating infeasibility

    :param lp_model: lp model of the project
    :return: new_lp_constraints : the set of constraints of the lp model
    """
    print('\nWith LPFICS:\n'
          '\nTesting if the project is technicaly feasible.\n'
          'If not, finding a set of constraints leading to the '
          'infeasibility.\n')

    new_lp = lp_model.copy()

    new_lp = _def_tech_csts(lp_model=new_lp)

    new_lp_constraints = _find_infeasible_cst(lp_model, new_lp)

    if not new_lp_constraints:
        print("Even if the model is infeasible, it is not due to technical "
              "constraint only. It may be due to external constraints or both")
    return new_lp_constraints


def _find_infeasible_cst(lp_model, new_lp):
    """
    Identifies a set of constraints creating infeasibility, considering the
    model given

    :param lp_model: initial lp model of the project
    :param new_lp: given lp model
    :return: new_lp.constraints : the set of constraints of the lp model
    """
    # initialisation
    clusters = [new_lp.numConstraints()]
    conflict_set_size = 0

    while True:
        range_index = _first_set_failing(conflict_set_size, new_lp)

        new_lp = _restrict_to_n_constraint(
            lp=new_lp, n_constraints=range_index.stop + 1)
        new_lp = _move_constraint_to_start(lp=new_lp,
                                           range_index=range_index)

        clusters.insert(0, len(range_index) + 1)
        clusters[-1] = range_index.start - conflict_set_size
        conflict_set_size += len(range_index) + 1

        # Test on a second model lp2, and keep it if infeasible
        lp2 = _restrict_to_n_constraint(
            lp=new_lp, n_constraints=conflict_set_size)
        # lp2_status = 1 means that lp2 has solutions
        # lp2_status = -1 means that lp2 is infeasible
        lp2_status = lp2.solve()

        if LpStatus[lp2_status] == 'Infeasible':
            del clusters[-1]
            if len(clusters) == conflict_set_size:
                break
            new_lp = lp2
        else:
            pass

        nb_cluster_one_constraint = 0
        for elements in reversed(clusters):
            if elements > 1:
                break
            nb_cluster_one_constraint += 1

        if nb_cluster_one_constraint > 0:
            # rearrange the order of the constraints in order to
            # test
            #  another set of constraints to identify an
            # infeasible one
            new_lp = _move_constraint_to_start(
                lp=new_lp, range_index=range(new_lp.numConstraints() -
                                             nb_cluster_one_constraint,
                                             new_lp.numConstraints()
                                             - 1))

            clusters_clone = clusters.copy()
            for j in range(nb_cluster_one_constraint, len(clusters)):
                clusters[j] = clusters_clone[
                    j - nb_cluster_one_constraint]
            for i in range(nb_cluster_one_constraint):
                clusters[i] = 1

        conflict_set_size = new_lp.numConstraints() - clusters[-1]

    print('\nThe following constraints create an INFEASIBLE problem.\n'
          'Becarefull, relaxing these constraints may not be enough to lead '
          'to '
          'a feasible problem. You may have to identify other constraints '
          'while '
          'relaxing these ones.\n'
          'Becarefull, You should NOT release '
          'constraints of DefinitionConstraints type\n\n'
          'Constraint type::                Constraint_name:          '
          'Constraint '
          'definition\n'
          '----------------                ---------------           '
          '---------------------'
          )

    for key, value in new_lp.constraints.items():
        print(type(value.cst).__name__ + " :: ", key + " : ",
              value)
    print('\n')

    return new_lp.constraints


def _def_tech_actor_order_csts(lp_model):
    """
    Gives a new model - with physical, basic and then external constraints -
    which should be studied in order to identify a set of constraints creating
    infeasibility

    :param lp_model: lp model of the project
    :return: lp_organised : the model without the external constraints
    """
    lp_organised = lp_model.copy()
    def_constraints_dic = OrderedDict()
    tech_constraints_dic = OrderedDict()
    actor_constraints_dic = OrderedDict()
    basic_constraints_dic = OrderedDict()
    all_constraints = OrderedDict()

    # divide the external constraints from the other constraints
    for key, value in lp_organised.constraints.items():
        if isinstance(value.cst,
                      DefinitionConstraint or DefinitionDynamicConstraint):
            def_constraints_dic.__setitem__(key, value)
        elif isinstance(value.cst,
                        TechnicalConstraint or TechnicalDynamicConstraint):
            tech_constraints_dic.__setitem__(key, value)
        elif isinstance(value.cst,
                        ActorConstraint or ActorDynamicConstraint):
            actor_constraints_dic.__setitem__(key, value)
        else:
            basic_constraints_dic.__setitem__(key, value)

    # Reassemble the constraints with first physical constraints and then
    # constraints and then external constraints
    for key, value in def_constraints_dic.items():
        all_constraints.__setitem__(key, value)
    for key, value in basic_constraints_dic.items():
        all_constraints.__setitem__(key, value)
    for key, value in tech_constraints_dic.items():
        all_constraints.__setitem__(key, value)
    for key, value in actor_constraints_dic.items():
        all_constraints.__setitem__(key, value)

    lp_organised.constraints = all_constraints

    return lp_organised


def _def_actor_csts(lp_model):
    """
    Gives a new model with external constraints AND physical constraints which
    should be studied in order to identify a set of external constraints
    creating infeasibility

    :param lp_model: lp model of the project
    :return: lp_organised : the model without the external constraints
    """
    lp_organised = lp_model.copy()
    def_constraints_dic = OrderedDict()
    tech_constraints_dic = OrderedDict()
    actor_constraints_dic = OrderedDict()
    basic_constraints_dic = OrderedDict()
    def_basic_actor_constraints = OrderedDict()

    # divide the external constraints from the other constraints
    for key, value in lp_organised.constraints.items():
        if isinstance(value.cst,
                      DefinitionConstraint or DefinitionDynamicConstraint):
            def_constraints_dic.__setitem__(key, value)
        elif isinstance(value.cst,
                        TechnicalConstraint or TechnicalDynamicConstraint):
            tech_constraints_dic.__setitem__(key, value)
        elif isinstance(value.cst,
                        ActorConstraint or ActorDynamicConstraint):
            actor_constraints_dic.__setitem__(key, value)
        else:
            basic_constraints_dic.__setitem__(key, value)

    for key, value in def_constraints_dic.items():
        def_basic_actor_constraints.__setitem__(key, value)
    for key, value in basic_constraints_dic.items():
        def_basic_actor_constraints.__setitem__(key, value)
    for key, value in actor_constraints_dic.items():
        def_basic_actor_constraints.__setitem__(key, value)

    lp_organised.constraints = def_basic_actor_constraints

    return lp_organised


def _def_tech_csts(lp_model):
    """
    Gives a new model with - without external constraints - which should be
    studied in order to identify a set of "hard" constraints creating
    infeasibility

    :param lp_model: lp model of the project
    :return: lp_organised : the model without the external constraints
    """
    lp_organised = lp_model.copy()
    def_constraints_dic = OrderedDict()
    tech_constraints_dic = OrderedDict()
    actor_constraints_dic = OrderedDict()
    basic_constraints_dic = OrderedDict()
    def_basic_tech_constraints = OrderedDict()

    # divide the external constraints from the other constraints
    for key, value in lp_organised.constraints.items():
        if isinstance(value.cst,
                      DefinitionConstraint or DefinitionDynamicConstraint):
            def_constraints_dic.__setitem__(key, value)
        elif isinstance(value.cst,
                        TechnicalConstraint or TechnicalDynamicConstraint):
            tech_constraints_dic.__setitem__(key, value)
        elif isinstance(value.cst,
                        ActorConstraint or ActorDynamicConstraint):
            actor_constraints_dic.__setitem__(key, value)
        else:
            basic_constraints_dic.__setitem__(key, value)

    for key, value in def_constraints_dic.items():
        def_basic_tech_constraints.__setitem__(key, value)
    for key, value in basic_constraints_dic.items():
        def_basic_tech_constraints.__setitem__(key, value)
    for key, value in tech_constraints_dic.items():
        def_basic_tech_constraints.__setitem__(key, value)

    lp_organised.constraints = def_basic_tech_constraints

    return lp_organised


def _first_set_failing(conflict_set_size, newLp):
    """
    Identifies a reduced set of constraints which should be studied in
    order to identify a set of constraints creating infeasibility

    :param conflict_set_size: min size of the set of the conflict
    :param newLp: lp model
    :return: range(min_index, max_index) : minimal and maximum indexes of a
    set of
    constraints  which should be studied in order to identify a set of
    constraints creating infeasibility
    """
    # Initialisation
    min_index = conflict_set_size
    max_index = newLp.numConstraints() - 1

    if max_index != min_index:
        half_constraint_index = int((max_index + min_index) / 2)

        lp2 = _restrict_to_n_constraint(lp=newLp,
                                        n_constraints=half_constraint_index
                                                      + 1)

        lp2_status = lp2.solve()
        if LpStatus[lp2_status] == 'Infeasible':
            # only the first part of the set of constraints needs to be
            # studied
            max_index = half_constraint_index
        else:
            # only the second part of the set of constraints needs to be
            # studied
            min_index = half_constraint_index + 1

    return range(min_index, max_index)


def _restrict_to_n_constraint(lp, n_constraints):
    """
    Creates a submodel of the lp model keeping the first nConstraints,
    and deleting the objective and the variables (they will be reinitialised
    in the solving process)

    :param lp: lp model
    :param n_constraints: the number of the constraints which should be
    kept in
    the model, only the first nConstraints will be kept
    :return: lp_restricted: Return the model retricted to the 'nConstraints'
    """
    # Initialisation
    lp_restricted = lp.copy()
    constraints = OrderedDict()
    n = 0

    # get the n_constraints first constraints
    for key, value in lp.constraints.items():
        constraints.__setitem__(key, value)
        n += 1
        if n == n_constraints:
            break

    # Keep only the first 'n_constraints' constraints into the model
    lp_restricted.constraints = constraints
    # Delete the variables, they will be added during the solving time
    lp_restricted._variables.clear()
    # Delete the objective as it is useless
    lp_restricted.objective.clear()

    # Return the model retricted to the 'n_constraints'
    return lp_restricted


def _move_constraint_to_start(lp, range_index):
    """
    Moves the constraints in the range_index (start to end) to the
    beginning of
    the ordereddict of the constraints

    :param lp: lp model
    :param range_index: range of indexes of the constraints which should be
    moved to the beginning of the ordereddict of the constraints
    :return: lp model
    """

    key_list = []
    for key, v in lp.constraints.items():
        key_list.append(key)

    if not key_list:
        raise ValueError(
            'your problem is feasible! Try another method:\n'
            '- find_infeasible_constraint_set(your_model)'
            '- find_physical_and_external_infeasible_constraint_set('
            'your_model)\n'
            '- find_physical_and_basic_infeasible_constraint_set('
            'your_model)\n')

    for i in range(range_index.stop, range_index.start - 1, -1):
        if i < 0:
            raise ValueError(
                'your problem is feasible! Try another method:\n'
                '- find_infeasible_constraint_set(your_model)\n'
                '- find_definition_and_actor_infeasible_constraints_set('
                'your_model)\n'
                '- find_definition_and_technical_infeasible_constraints_set('
                'your_model)\n')
        else:
            lp.constraints.move_to_end(key_list[i], last=False)

    return lp
