from scikit_mcda import dmuu
import pprint
from tabulate import tabulate


def main():

    print("######### DMMU ############")

    print("\n@ Defining labels for Alternatives and States")
    print("-----------------------------------------------")
    df = dmuu.dataframe([[5000, 2000, 100],
                         [50, 50, 500]],
                        ["ALT_A", "ALT_B"],
                        ["STATE A", "STATE B", "STATE C"]
                        )
    print(tabulate(df, headers='keys', tablefmt='psql'))

    # print("\n@ Defining labels for Alternatives and States automatically")
    # print("-------------------------------------------------------------")
    # df = dmuu.dataframe([[5000, 2000, 100],
    #                      [50, 50, 500]]
    #                     )
    # print(tabulate(df, headers='keys', tablefmt='psql'))

    print("\n@ Defining specific crietria")
    print("------------------------------")
    df_calc = dmuu.calc(df, ["minimax-regret", "hurwicz"], 0.7)
    print("\n", tabulate(df_calc, headers='keys', tablefmt='psql'))

    result = dmuu.decision_making(df, ["minimax-regret", "hurwicz"])
    print("\nResult:\n")
    pprint.pprint(result)

    print("\n@ Not specifing crietria")
    print("------------------------------")
    df_calc = dmuu.calc(df)
    print(tabulate(df_calc, headers='keys', tablefmt='psql'))

    result = dmuu.decision_making(df)
    print("\nResult:\n")
    pprint.pprint(result)


main()
