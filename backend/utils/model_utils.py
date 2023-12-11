import pandas as pd

def get_neighboor_columns(col : str) -> list[str]:
    """ Returns a list of neighboor columns for a given column """
    col_root = col.split('_')[0]

    res = [f'{col_root}_last', f'{col_root}_sec_last', f'{col_root}_third_last'][::-1]

    res.remove(col)

    return res

def get_column_neighboorhood(col : str) -> list[str]:
    col_root = col.split('_')[0]

    return [f'{col_root}_last', f'{col_root}_sec_last', f'{col_root}_third_last']

def handle_nulls(df):
    # Iterate through columns
    for col in df.columns:
        # Go through each row
        for i, val in enumerate(df[col]):
            if pd.isnull(val):
                neighboor_columns = get_neighboor_columns(col)

                non_null_neighboor = False

                # Go through neighboor columns
                for neighboor_col in neighboor_columns:
                    if neighboor_col not in df.columns:
                        continue
                    if pd.isnull(df[neighboor_col][i]):
                        continue

                    df[col][i] = df[neighboor_col][i]
                    non_null_neighboor = True
                    break

                if not non_null_neighboor:
                    cols = get_column_neighboorhood(col)

                    for _col in cols:
                        if _col not in df.columns:
                            continue
                        df[_col][i] = 1

    return df
