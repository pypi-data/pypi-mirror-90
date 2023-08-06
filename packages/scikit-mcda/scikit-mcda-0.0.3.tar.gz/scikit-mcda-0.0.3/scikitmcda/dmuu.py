'''
#########################################################
# SCI-KIT-MCDA Library                                  #
# Author: Antonio Horta                                 #
# https://gitlab.com/cybercrafter/scikit-mcda           #
# Cybercrafter ® 2021                                   #
#########################################################

Module: DMUU: Decision making under uncertainty
'''

import pandas as pd

'''
FUNCTION:
dataframe(alt_data, alt_labels=[], state_label=[]):

DESCRIPTION:
Function that mounts the base dataframe for DMMU

PARAMS:
alt_data: list of values of alternatives (ex: amount of money)
alt_labels: list of alternative names (opc.)
state_label: list of label of states (opc.)

OUTPUT:
base datarame

'''


def dataframe(alt_data, alt_labels=[], state_label=[]):

    # define state labels if not exists
    if state_label == []:
        for s in range(0, len(alt_data[0])):
            state_label.append("S" + str(s+1))

    # define alternative labels if not exists
    if alt_labels == []:
        for a in range(0, len(alt_data)):
            alt_labels.append("A" + str(a+1))

    df_data = pd.DataFrame(data=alt_data, columns=state_label)
    df_data.insert(loc=0,
                   column='alternatives',
                   value=alt_labels)
    df = df_data

    return df


'''
FUNCTION:
calc(dmuu_df, dmuu_criteria_list=["maximax", "maximin", "laplace", "minimax-regret", "hurwicz"], hurwicz_coeficient=0.5):

DESCRIPTION:
Function that calcs DMUU from dmuu_dataframe using criteria listed in dmuu_criteria_list

PARAMS:
dmuu_df: dataframe with alteratives and states
dmuu_criteria_list: list of criteria ["maximax", "maximin", "laplace", "minimax-regret", "hurwicz"]
hurwicz_coeficient: number between 0 and 1

OUTPUT:
datarame + dmuu_criteria_list with tuples (value, 0 or 1) where 1 is the alternative choosed
'''


def calc(dmuu_df, dmuu_criteria_list=[], hurwicz_coeficient=-1):

    # check dmuu_criteria_list
    dmuu_criteria_list = check_dmuu_criteria_list(dmuu_criteria_list)

    # check hurwicz_coeficient is ok. if not default is 0.5
    if check_hurwicz_coeficient(hurwicz_coeficient) is False:
        hurwicz_coeficient = 0.5

    # clean previous calcs passed in dataframe
    for c in ["maximax", "maximin", "laplace", "minimax-regret", "hurwicz"]:
        if c in dmuu_df:
            dmuu_df = dmuu_df.drop(columns=[c])

    df = dmuu_df

    if "minimax-regret" in dmuu_criteria_list:
        list_minimax_regret_max = dmuu_df.iloc[:, 1:].max(axis=0)
        df_minimax_regret_temp = dmuu_df.iloc[:, 1:] - list_minimax_regret_max
        # now apply maximin
        df_maximin_r = df_minimax_regret_temp.min(axis=1)
        result_maximin_r = df_maximin_r.max(axis=0)
        column_maximin_r = []
        for x in df_maximin_r.values:
            if x == result_maximin_r:
                column_maximin_r.append((x * -1, 1))
            else:
                column_maximin_r.append((x * -1, 0))
        df['minimax-regret'] = column_maximin_r

    if "maximax" in dmuu_criteria_list:
        df_maximax = dmuu_df.iloc[:, 1:].max(axis=1)
        result_maximax = df_maximax.max(axis=0)
        column_maximax = []
        for x in df_maximax.values:
            if x == result_maximax:
                column_maximax.append((x, 1))
            else:
                column_maximax.append((x, 0))
        df['maximax'] = column_maximax

    if "maximin" in dmuu_criteria_list:
        df_maximin = dmuu_df.iloc[:, 1:].min(axis=1)
        result_maximin = df_maximin.max(axis=0)
        column_maximin = []
        for x in df_maximin.values:
            if x == result_maximin:
                column_maximin.append((x, 1))
            else:
                column_maximin.append((x, 0))
        df['maximin'] = column_maximin

    if "laplace" in dmuu_criteria_list:
        df_laplace = dmuu_df.iloc[:, 1:].mean(axis=1)
        result_laplace = df_laplace.max(axis=0)
        column_laplace = []
        for x in df_laplace.values:
            if x == result_laplace:
                column_laplace.append((x, 1))
            else:
                column_laplace.append((x, 0))
        df['laplace'] = column_laplace

    if "hurwicz" in dmuu_criteria_list:
        df_hurwicz = dmuu_df.iloc[:, 1:].max(axis=1) * hurwicz_coeficient + dmuu_df.iloc[:, 1:].min(axis=1) * (1 - hurwicz_coeficient)
        result_hurwicz = df_hurwicz.max(axis=0)
        column_hurwicz = []
        for x in df_hurwicz.values:
            if x == result_hurwicz:
                column_hurwicz.append((x, 1, hurwicz_coeficient))
            else:
                column_hurwicz.append((x, 0, hurwicz_coeficient))
        df['hurwicz'] = column_hurwicz

    return df


'''
FUNCTION:
decision_making(dmuu_df, dmuu_criteria_list=[], hurwicz_coeficient=0.5):

DESCRIPTION:
Function that returns solutions DMUU from dmuu_dataframe or dmcu_dataframe_calculated of criteria listed in dmuu_criteria_list

PARAMS:
dmuu_df: dataframe with alteratives and states
dmuu_criteria_list: list of criteria ["maximax", "maximin", "laplace", "minimax-regret", "hurwicz"]

OUTPUT:
        list of dict         {"alternative": ,
                               "index": ,
                               "value": ,
                               "criteria":,
                               "result": [{"alternative": value}],
                               "type_dm": "DMUU",
                               'hurwicz_coeficient':
                               }
'''


def decision_making(dmuu_df, dmuu_criteria_list=[], hurwicz_coeficient=-1):

    # check dmuu_criteria_list
    dmuu_criteria_list = check_dmuu_criteria_list(dmuu_criteria_list)

    # check hurwicz_coeficient is ok. if not default is 0.5
    hurwicz_coeficient_empty = False
    if hurwicz_coeficient == -1:
        hurwicz_coeficient_empty = True

    if check_hurwicz_coeficient(hurwicz_coeficient) is False:
        hurwicz_coeficient = 0.5

    result = []

    # verify if dmuu_criteria_list is already calculated. if not, run calc
    columns = dmuu_df.columns.values
    for c in dmuu_criteria_list:
        if c not in columns or (c == "hurwicz" and dmuu_df["hurwicz"].iloc[0][2] != hurwicz_coeficient and hurwicz_coeficient_empty == False):
            dmuu_df = calc(dmuu_df, dmuu_criteria_list, hurwicz_coeficient)
            break

    # make result
    for l in dmuu_criteria_list:
        cols = list(dmuu_df[l])
        for c in cols:
            if c[1] == 1:
                hc = ""
                if l in "hurwicz":
                    hc = c[2]
                result.append({"alternative": dmuu_df.iloc[cols.index(c), 0],
                               "index": cols.index(c),
                               "value": c[0],
                               "criteria": l,
                               "result": dict(zip(dmuu_df["alternatives"], [i[0] for i in cols])),
                               "type_dm": "DMUU",
                               'hurwicz_coeficient': hc
                               })
    return result


'''
FUNCTION:
check_hurwicz_coeficient(hurwicz_coeficient):

DESCRIPTION:
Check if hurwicz_coeficient is >= 0 and <= 1
If not, put default 0.5

OUTPUT:
    True or False
'''


def check_hurwicz_coeficient(hurwicz_coeficient):
    result = True
    if type(hurwicz_coeficient) != float:
        if hurwicz_coeficient < 0 or hurwicz_coeficient > 1:
            result = False
    return result


'''
FUNCTION:
check_dmuu_criteria_list(dmuu_criteria_list=[]):

DESCRIPTION:
Check and transform if dmuu_criteria_list is a list of correct dmuu criteria
and defines default criteria for DMUU

OUTPUT:
    dmuu_criteria_list transformed or default
'''


def check_dmuu_criteria_list(dmuu_criteria_list=[]):

    # defines default criteria for DMUU
    default_list = ["maximax", "maximin", "laplace", "minimax-regret", "hurwicz"]

    if type(dmuu_criteria_list) != list:
        dmuu_criteria_list = [dmuu_criteria_list]

    for c in dmuu_criteria_list:
        if c not in default_list:
            dmuu_criteria_list.remove(c)

    if dmuu_criteria_list == []:
        dmuu_criteria_list = default_list

    return dmuu_criteria_list
