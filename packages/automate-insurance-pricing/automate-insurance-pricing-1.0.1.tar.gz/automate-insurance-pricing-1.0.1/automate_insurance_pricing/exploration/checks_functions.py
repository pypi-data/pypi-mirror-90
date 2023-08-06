import pandas as pd
import numpy as np

from scipy import stats

from copy import deepcopy
from datetime import date, timedelta, datetime



def update_costs_for_year(x, df, policy_id_column_name, main_column_contract_date, claim_occurrence_date, unknown_row_name, number_of_days):
    """Checks if the line should be in the df or if it is a wrong or true duplicate that should be removed"""

    row = df.loc[x]
    policy_id = row[policy_id_column_name]
    year_name = main_column_contract_date
    result = 0
    effective_date = row[year_name]
    effective_dates = df[df[policy_id_column_name]==policy_id][year_name]

    # For policy_id with UNKNOWN value, we keep all claims because we cannot link them to a policy but we group them in an UNKNOWN block so that we don't understimate the total cost
    if policy_id != unknown_row_name:
        # Contract started after the claim occurrence
        if effective_date > row[claim_occurrence_date]:
            result = 1
        # The claim did not occurr during the yearly contract cover;
        # By prudency, also checks if there is a contract amendment. if not we assume it is a date mistake and we do not set the cost to 0
        elif effective_date + timedelta(number_of_days) <= row[claim_occurrence_date] and effective_date < effective_dates.max():
            result = 1

    return result


def add_back_lines(df, df_removed, main_column_contract_date, claim_id_column_name, claim_occurrence_date_column_name, lines_ro_remove_name):
    """
        Add backs lines that were mistakenly removed from the df
        Arguments --> the reduced df and the df that stores the removed lines
        Returns --> a new df which now have back the lines that were wrongly removed
    """

    year_name = main_column_contract_date

    # To find these claims we look at the claims that were in the original claims data but are not in the newly created
    wrongly_removed = df_removed[~df_removed[claim_id_column_name].isin(df[claim_id_column_name])].drop_duplicates(subset=claim_id_column_name, keep='last')

    # We add them back in our claims because we prefer being wrong in the occurrence dates rather than reducing the total costs
    new_df = pd.concat((df, wrongly_removed), sort=False).reset_index(drop=True)

    # Changes the dates so that it is now consistent. It means there might be cost overestimation for some occurrence year, but it won't have any impact overall
    new_df.loc[new_df.shape[0]-wrongly_removed.shape[0]:, claim_occurrence_date_column_name] = new_df.loc[new_df.shape[0]-wrongly_removed.shape[0]:, year_name] + timedelta(days=1)

    return new_df.drop(columns=lines_ro_remove_name, errors='ignore')



def find_wrong_lines(df, main_column_contract_date, lines_ro_remove_name, number_of_days=None, remove=False):
    """
        Finds the lines that seems to be wrong either because they are true duplicates or because a date inconsistency has been detected
        Arguments --> the df on which we are doing the check, the number of days that should serve as a threshold \n \
                    i.e. for a given policy and its effective date, a claim occurring beyond that number of days should not be associate to it,
                    and a remove argument that if set to True means all the lines considered wrong are removed from the df
        Returns --> 2 df, one which is either with a flat for potential wrong lines or with all these lines removed, \n \
and a new one which contains only the removed lines
    """

    new_df = deepcopy(df)
    number_of_days = 365 if number_of_days is None else number_of_days

    new_df[lines_ro_remove_name] = new_df.index.to_frame()[0].apply(lambda x: update_costs_for_year(x, new_df, main_column_contract_date, number_of_days))

    if remove == True:
        df_removed_lines = new_df[new_df[lines_ro_remove_name] == 1]
        line_to_remove_index = df_removed_lines.index
        new_df = new_df.drop(labels=line_to_remove_index).drop(columns=lines_ro_remove_name)
    else:
        df_removed_lines = pd.DataFrame()
        print('You just tagged the lines that are incorrect and should most likely be removed.\n \
Retreat these lines, then run again this function with the remove argument set to True to delete remaining unnecessary lines')

    return new_df.reset_index(drop=True), df_removed_lines



def create_unknown_policy(df_portfolio, df_claims, features_analysis, policy_id_column_name='policy_id', unknown_row_name='UNKNOWN'):
    """ Finds policies that are in the claims data but not in the porfolio, and generates a new policy on the portfolio data to represent these unknown policies"""

    new_df_portfolio, new_df_claims = deepcopy(df_portfolio), deepcopy(df_claims)

    # Finds the claimants that do not exist in the portfolio data
    mask = ~new_df_claims[policy_id_column_name].isin(new_df_portfolio[policy_id_column_name])
    df_not_existing_policies = new_df_claims[mask]

    new_df_claims.loc[df_not_existing_policies.index, policy_id_column_name] = unknown_row_name

    # Reseting df index just in case to be sure we take the last row using shape
    new_df_portfolio = new_df_portfolio.reset_index(drop=True)
    # Gets the last row values and affect them to a new row
    new_row_df = new_df_portfolio.loc[new_df_portfolio.shape[0]-1]
    new_df_portfolio.loc[new_df_portfolio.shape[0]] = new_row_df
    new_df_portfolio.loc[new_df_portfolio.shape[0]-1:, [policy_id_column_name]] = unknown_row_name

    # For each feature, derives the mode or the average and assigns it to the new row (a simple fillna might be faster)
    for feature in features_analysis:
        if new_df_portfolio[feature].dtype in ['object']:
            new_df_portfolio.loc[new_df_portfolio.shape[0]-1:, feature] = new_df_portfolio[feature].mode()[0]
        elif new_df_portfolio[feature].dtype in ['float64', 'int64', 'int32']:
            new_df_portfolio.loc[new_df_portfolio.shape[0]-1:, feature] = new_df_portfolio[feature].mean()

    print('There are {} policies in the claims that cannot be found in the porfolio data'.format(df_not_existing_policies.shape[0]))

    return new_df_portfolio, new_df_claims



def find_outliers(df, columns=None, method='interquartile', z_score_threshold=3, interquartile_lower_bound=0.25, interquartile_upper_bound=0.75):
    """
        Finds outliers for the specified features
        Arguments --> the df on which to find outliers, the features as a name or list of names and the method to use to find outliers
        Returns --> a full copy of df, the df with only outliers and the new df without the outliers
    """

    new_df = deepcopy(df)

    if method == 'interquartile':
        new_columns = [columns] if isinstance(columns, str) == True else columns

        for column in new_columns:
            quantile_25 = df[column].quantile(interquartile_lower_bound)
            quantile_75 = df[column].quantile(interquartile_upper_bound)

            interquartile_range = quantile_75 - quantile_25
            lower_bound = quantile_25 - 1.5 * interquartile_range
            upper_bound = quantile_75 + 1.5 * interquartile_range

            new_df = new_df[(new_df[column] >= lower_bound) & (new_df[column] <= upper_bound)]

    else:

        z_score = np.abs(stats.zscore(df[columns]))
        new_df = new_df[z_score<3] if isinstance(columns, str) == True else new_df[(z_score<3).all(axis=1)]

    df_outliers = df[~df.index.isin(new_df.index)]
    proportion_outliers = len(df_outliers) / len(df)

    if proportion_outliers > 0.05:
        print("Outliers represent a high proportion of the data: {}%. We should not remove them all".format(proportion_outliers))
        return deepcopy(df), df_outliers, df
    else:
        print('{} rows have been removed'.format(df_outliers.shape[0]))
        return deepcopy(df), df_outliers, new_df
    
    

def perform_sense_check(df, new_cell_name=None, **kwargs):
    """
       Finds data which is inconsistent on the columns specified in the kwargs
       Arguments --> the df, the name of the new column created to flag if the comparison is true or not,
                if not specified, then the function creates a new df composed of the rows for which the comparison check is true
                   kwargs --> tuples like (column1, column2, comparison_to_do, strict_comparison)
                   or (column1, integer, comparison_to_do) ; comparison_to_do must be 0 for ==, 1 for <=, 2 for >=
                    if strict_comparison is True, then the comparison must be strict
       Returns --> either a new df containing all rows that meet the comparison check or the current df with a new cell that flags them
   """

    def get_compare():
        """
            Defines if the second argument to compare with is a integer/float or a pandas serie
            Returns --> the right element that must be used for the comparison
        """

        if isinstance(value[1], str) == True:
            # The second element of the tuple being a column name, we get the pandas serie
            compare = df[value[1]]            
        else:
            # The second element of the tuple being a number, we just retrieve the number itself
            compare = value[1]
            

        return compare


    def create_new_cell_or_df(): 
        """ Returns the concatenated df validating the check or updates the df column used to flag if the comparison is true or not"""

        # Cell name not being defined, it means the function must create a dataframe
        if new_cell_name is None:
            # As several checks can be done, a concatenation between the previous check and the new one is made
            return pd.concat((df_check, df[mask]), axis=0).drop_duplicates(keep='first')
        else:
            # The original df is modified with a new column that will have true/false value. If there are several checks performed, the row will be flagged true if it validates at least 1 check
            df[new_cell_name] = df[new_cell_name] | mask if new_cell_name in df.columns else mask

         
    df_check = pd.DataFrame()
    
    # Loops trough the kwargs
    for value in kwargs.values():

        # These lines checks the comparison operation to do
        if value[2] == 0:
            compare = get_compare()           
            mask = df[value[0]] == compare

        elif value[2] == 1:
            compare = get_compare()
            mask = df[value[0]] <= compare if len(value) < 4 or value[3] == False else df[value[0]] < compare
            
        else:
            compare = get_compare()
            mask = df[value[0]] >= compare if len(value) < 4 or value[3] == False else df[value[0]] > compare
        
        df_check = create_new_cell_or_df()
            
    if new_cell_name is None:
        print('There are {} rows concerned'.format(df_check.shape[0]))
        return df_check
      


def build_duplicated_df(df, columns=None, keep_method=False):
    """ Finds the duplicated values depending on the args
        columns --> columns names specified by the user as a list. Can be just a string if it is for only one column
        Returns --> a new dataframe with only duplicated values
    """

    return df[df.duplicated(subset=columns, keep=keep_method)].sort_values(columns)