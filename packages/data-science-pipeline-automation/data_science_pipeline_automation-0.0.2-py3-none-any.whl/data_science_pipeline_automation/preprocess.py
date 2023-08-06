from data_science_pipeline_automation.logic.preprocess import reformat

def transform_cl_target(series, positive_values, negative_values, positive_label=1, negative_label=0):
    """
    Transform target values into desired positive & negative labels 
    Args:
        series (pandas series): the target column series
        positive_values (set or list-like): The sequence of positive values
        negative_values (set or list-like): The sequence of negative values 
        positive_label (optional): Default=1. The desired positive label
        negative_label (optional): Default=0. The desired negative label
    Returns:
        pandas.Series
    """
    return reformat.transform_cl_target(series, positive_values, negative_values, positive_label, negative_label)