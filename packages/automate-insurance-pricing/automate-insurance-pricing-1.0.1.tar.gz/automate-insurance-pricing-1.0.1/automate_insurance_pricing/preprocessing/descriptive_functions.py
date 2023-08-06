import pandas as pd


def derive_termination_rate_year(df, start_business_year, extraction_year, main_column_contract_date, policy_id_column_name, column_to_sum_name):
    """Derive the termination rates per year"""

    df_previous_year = df[df[main_column_contract_date].dt.year == start_business_year].drop_duplicates(subset=policy_id_column_name, keep='first')
    policies_previous_year = df_previous_year[policy_id_column_name]
    termination_rates = {}
    gwp_year = df_previous_year[column_to_sum_name].sum()
    total_gwp = gwp_year
    weighted_rates = 0

    for year in range(start_business_year+1, extraction_year+1):

        df_next_year = df[df[main_column_contract_date].dt.year == year].drop_duplicates(subset=policy_id_column_name, keep='first')
        policies_next_year = df_next_year[policy_id_column_name]

        policies_from_previous_year = df_next_year[df_next_year[policy_id_column_name].isin(policies_previous_year)]

        termination_rate = (len(policies_previous_year) - len(policies_from_previous_year)) / len(policies_previous_year)
        termination_rates[year-1] = termination_rate

        weighted_rates += termination_rate * gwp_year
        gwp_year = df_next_year[column_to_sum_name].sum()
        total_gwp += gwp_year

        policies_previous_year = policies_next_year

    termination_rates['weighted_average'] = weighted_rates / total_gwp

    return termination_rates



def create_df_unique_values(df, features):
    """
        Creates a dataframe
        features --> list of features
        Returns --> A new df with features and number of unique values for each
    """

    if len(features) > 0:
        df_feature_unique_values = pd.DataFrame.from_dict({'feature': features, 'number_of_uniques': df[features].nunique().values})
        return df_feature_unique_values.reset_index()

    else:
        print('Your list of features is empty. Add at least one feature to study.')