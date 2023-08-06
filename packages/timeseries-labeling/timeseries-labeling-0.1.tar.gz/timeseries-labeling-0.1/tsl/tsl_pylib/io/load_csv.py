import numpy as np 
import pandas as pd

def csv_to_numpy(filename: str, sep: str =',') -> np.ndarray:
    x = np.genfromtxt(filename, delimiter=sep)
    return x

def csv_to_df(filename: str, sep: str =',') -> pd.DataFrame:
    df = pd.read_csv(filename, sep = sep)
    return df