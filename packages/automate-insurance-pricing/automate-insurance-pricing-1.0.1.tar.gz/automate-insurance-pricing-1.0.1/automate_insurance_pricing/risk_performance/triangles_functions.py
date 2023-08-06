import pandas as pd
import seaborn as sns

import chainladder as cl

import matplotlib.pyplot as plt



def add_ibnr(row, ibnr_rates, extraction_year, claims_column_name='asif_total_capped_cost', occurrence_date_column_name='occurrence_date'):

    claim_year = row[occurrence_date_column_name].year

    try:
        rates_index = int(extraction_year - claim_year)
    except:
        rates_index = 0

    return row[claims_column_name] * (1 + ibnr_rates[rates_index]) 


def get_triangle_projections(triangles, average_methods=None, n_periods=None, grain='OYDY'):
    """
        Generates the main kpis such as ultimate loss, ibnr, loss development factors
        Arguments --> A dict of triangles or a single triangle,
                    the methods to derive the LDF (simple or volume average) defined as a list if there are several ultimate triangles to produce,
                    the number of periods to look at (-1 means all periods by default)
                    the origin/development pattern ('OxDy' with x and y in (Y, M, Q))
        Returns --> a dict composed where keys are the name of the figures (cost, count of claims, etc.) and the kpis like ldf, ibnr

    """

    triangles_values = triangles.values() if isinstance(triangles, dict) else [triangles]
    triangles_keys = triangles.keys() if isinstance(triangles, dict) else [1]

    selected_average_methods = ['volume'] * len(triangles_keys) if average_methods is None else \
                                average_methods if isinstance(average_methods, list) else [average_methods]

    selected_n_periods = [-1] * len(triangles_keys) if n_periods is None else \
                        n_periods if isinstance(n_periods, list) else [n_periods]

    # Gets the different types of figures we are studying (asif cost, cost excl LL, count, etc.)
    triangles_names = [triangle.columns[0] for triangle in triangles_values]

    # Builds the triangle transformer with development attributes ; loops through the triangles
    triangles_dev = [cl.Pipeline([('dev', cl.Development(average=selected_average_methods[index], n_periods=selected_n_periods[index]))])
                     .fit_transform(triangle.grain(grain)) for index, triangle in enumerate(triangles_values)]

    # Loops through the triangles_dev to derive the ldfs, cdfs and the fit method
    triangles_model = [(triangle_dev.ldf_, triangle_dev.cdf_, cl.Chainladder().fit(triangle_dev)) for triangle_dev in triangles_dev]

    # Loops through the triangles_model to build a dict with the name of the figures (claims cost, count, etc.)
    # as primary key and the main triangle characteristics as second keys
    return {value: {
                    'ldf': triangles_model[index][0],
                    'cdf': triangles_model[index][1],
                    'fit': triangles_model[index][2],
                    'full_triangle': pd.concat([triangles_model[index][2].full_triangle_.to_frame(), triangles_model[index][2].ibnr_.to_frame()] \
                                               , axis=1).rename(columns={9999: 'Ultimates', value: 'IBNR'})
                    }
            for index, value in enumerate(triangles_names)}


def plot_triangles_dev(triangles, columns=None, grain=None, save=True, prefix_name_fig='ibnr', folder='Charts'):
    """
        Plots the development patterns for the desired figures
        Arguments --> the triangles dict gathering triangles of different types of figures (amounts, counts, etc.),
                    the kpis we want to plot and the origin/development pattern ('OxDy' with x and y in (Y, M, Q)),
                    arguments to indicate if the graphs must be saved and with which prefix name
        Returns --> Nothing. It just displays the graphs
    """

    new_columns =  list(triangles.keys()) if columns is None else columns if isinstance(columns, list) == True else [columns]

    # Gets the triangles from the dict and derives the cumulative percentage
    if grain is not None:
        percentage_development = [triangles[column].grain(grain).T / triangles[column].grain(grain).T.max() for column in new_columns]
    else:
        percentage_development = [triangles[column].T / triangles[column].T.max() for column in new_columns]

    for index, dev in enumerate(percentage_development):
        column_name = new_columns[index].replace('asif_', '').replace('_', ' ')
        dev.plot()
        plt.xlabel('{} Developement in percentage'.format(column_name[0].capitalize() + column_name[1:]))

        if save == True:
            plt.savefig(folder + '/' + prefix_name_fig + '_' + column_name + '.png')


def select_triangles(multi_triangles, all_indexes_total=True, columns=None):
    """
        Gets the triangles from a chainladder triangle class depending
        Arguments --> the chainladder multi triangles class,
                    a boolean indicating if the function must build the total triangle ignoring its index values.
                    Index values are equivalent to a groupby aggregation variable ; so setting all_indexes_total to True is equivalent to undo the aggregation and to get the triangle for the whole portfolio,
                    setting it to False will make you get a triangle for each of the index (e.g. a triangle by guarantee)
                    the columns (KPIs) to look at,
        Returns --> a dict of triangles with index_values and columns as keys and triangles as values
    """

    triangles = []
    new_columns = multi_triangles.columns if columns is None else [columns] if isinstance(columns, str) == True else columns

    # Gets a triangle for each index of the chainladder multi triangle
    if all_indexes_total == False:
        # Gets all possible combinaisons for the index (this is all the groupby formed by the chainladder triangle)
        triangles_index_values = multi_triangles.index.values

        # Gets the appropriate triangle for the index_value combinaison and the desired column (i.e. figure summed by the chainladder)
        triangles = [[multi_triangles.loc[tuple(index_value)][column] for index_value in triangles_index_values] for column in new_columns]

        # Converts the list into a dict so that it is easier to retrieve it after
        triangles = {tuple(triangle.index.values[0]) + tuple(triangle.columns): triangle for triangles_list in triangles for triangle in triangles_list}

    # Only one total triangle for each column without filtering by any index value
    else:

        # There is no index in the multi triangle, simply retrieves desired figures thanks to the columns names
        if multi_triangles.index.shape[0]  == 1:
            triangles = {column: multi_triangles[column] for column in new_columns}

        # There are indexes in the multi triangle. To get for each column the total amount, ignoring the indexes, a sum must be applied.
        else:
            # Creates the triangle for each column specified in the arguments
            triangles = {column: multi_triangles[column].sum() for column in new_columns}

    return triangles