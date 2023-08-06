scikit-mcda
===========

A python library made to provide multi-criteria decision aid for developers and operacional researchers.

Module for Decision-making Under Uncertainty (DMUU)
---------------------------------------------------

**dmuu**: Module for Decision-making Under Uncertainty

**criteria**:

- maximax
- maximin
- laplace
- minimax-regret
- hurwicz

**functions**:

- dataframe(alt_data, alt_labels=[], state_labels=[])
- calc(dmuu_df, dmuu_criteria_list=[], hurwicz_coeficient=-1)
- decision_making(dmuu_df, dmuu_criteria_list=[], hurwicz_coeficient=-1)

Example
-------

::

    from scikitmcda import dmuu 

    df = dmuu.dataframe([[5000, 2000, 100],
                         [50, 50, 500]],
                        ["ALT_A", "ALT_B"],
                        ["STATE A", "STATE B", "STATE C"])

    df
    +----+----------------+-----------+-----------+-----------+
    |    | alternatives   |   STATE A |   STATE B |   STATE C |
    |----+----------------+-----------+-----------+-----------|
    |  0 | ALT_A          |      5000 |      2000 |       100 |
    |  1 | ALT_B          |        50 |        50 |       500 |
    +----+----------------+-----------+-----------+-----------+

    df_calc = dmuu.calc(df, ["minimax-regret", "hurwicz"], 0.7)

    df_calc
    +----+----------------+-----------+-----------+-----------+------------------+------------------+
    |    | alternatives   |   STATE A |   STATE B |   STATE C | minimax-regret   | hurwicz          |
    |----+----------------+-----------+-----------+-----------+------------------+------------------|
    |  0 | ALT_A          |      5000 |      2000 |       100 | (400, 1)         | (3530.0, 1, 0.7) |
    |  1 | ALT_B          |        50 |        50 |       500 | (4950, 0)        | (365.0, 0, 0.7)  |
    +----+----------------+-----------+-----------+-----------+------------------+------------------+

    result = dmuu.decision_making(df)

    result

    [{'alternative': 'ALT_A',
      'criteria': 'maximax',
      'hurwicz_coeficient': '',
      'index': 0,
      'result': {'ALT_A': 5000, 'ALT_B': 500},
      'type_dm': 'DMUU',
      'value': 5000},
    ...
    {'alternative': 'ALT_A',
      'criteria': 'hurwicz',
      'hurwicz_coeficient': 0.5,
      'index': 0,
      'result': {'ALT_A': 2550.0, 'ALT_B': 275.0},
      'type_dm': 'DMUU',
      'value': 2550.0}]



