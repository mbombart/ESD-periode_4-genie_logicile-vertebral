import pandas as pd
from src.data_processing import get_feat_and_target

def test_get_feat_and_target():
    list = [[0 ,0 ,1], [11,3,5],[0 ,0 ,1], [11,3,5],[0 ,0 ,1], [11,3,5]]
    df = pd.DataFrame(list, columns=['A', 'B', 'C'])
    target = 'B'
    x, y = get_feat_and_target(df, target)
    assert type(x)==type(df)
    assert type(y)==type(df)