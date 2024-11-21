import pandas as pd


def initialize_data_frame():
    df = pd.DataFrame(
        {
            "Term to Remember": ['apple'],
            "Definition": ["a fruit"]
        }
    )

    return df

