import http.client
import pandas as pd
from .config import Config


def get(dataset, **kwargs):
    """
    Return DataFrame of requested DecisionForest dataset.
    Args:
        dataset (str): Dataset codes are available on DecisionForest.com, example: dataset='SMD'
        ** date (str): Date, example: date='2018-12-28'
        ** start, end (str): Date filters, example: start='2018-12-28', end='2018-12-30'
        ** symbol (str): Symbol codes are available on DecisionForest.com on the product page , example: symbol='AAPL'
    """

    conn = http.client.HTTPSConnection(Config.DOMAIN)
    u = f"/api/{dataset}/?key={Config.KEY}"

    for key, value in kwargs.items():
        u = f'{u}&{key}={value}'

    conn.request("GET", u)
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = eval(data)

    if dataset == 'SMD':
        d = {}
        for i in range(len(data)):
            d[i] = {}
            d[i]['date'] = data[i]['date']
            d[i]['symbol'] = data[i]['symbol']
            d[i]['sentiment'] = data[i]['sentiment']
            d[i]['probability'] = data[i]['probability']
            d[i]['ratio'] = data[i]['ratio']

        df = pd.DataFrame.from_dict(d, orient='index')
        df = df.sort_values(by=['date'])
        df.reset_index(drop=True, inplace=True)

    elif dataset == 'DFCF':
        d = {}
        for i in range(len(data)):
            d[i] = {}
            d[i]['date'] = data[i]['date']
            d[i]['symbol'] = data[i]['symbol']
            d[i]['intrinsic_value_per_share'] = float(
                data[i]['intrinsic_value_per_share'])
            d[i]['de'] = float(data[i]['de'])
            d[i]['cr'] = float(data[i]['cr'])
            d[i]['roe'] = float(data[i]['roe'])
            d[i]['close'] = float(data[i]['price'])
            d[i]['move'] = float(data[i]['move'])

        df = pd.DataFrame.from_dict(d, orient='index')
        df = df.sort_values(by=['date'])
        df.reset_index(drop=True, inplace=True)

    elif dataset == 'STAT':
        d = {}
        for i in range(len(data)):
            d[i] = {}
            d[i]['date'] = data[i]['date']
            d[i]['symbol'] = data[i]['symbol']
            d[i]['adf_stat'] = float(data[i]['adf_stat'])
            d[i]['adf_pvalue'] = float(data[i]['adf_pvalue'])
            d[i]['adf_cv'] = float(data[i]['adf_cv'])
            d[i]['adf_corr'] = float(data[i]['adf_corr'])
            d[i]['h'] = float(data[i]['h'])
            d[i]['c'] = float(data[i]['c'])
            d[i]['var_stat'] = float(data[i]['var_stat'])
            d[i]['var_pvalue'] = float(data[i]['var_pvalue'])
            d[i]['var_corr'] = float(data[i]['var_corr'])
            d[i]['var'] = data[i]['var']
            d[i]['coef'] = float(data[i]['coef'])
            d[i]['half'] = float(data[i]['half'])       

        df = pd.DataFrame.from_dict(d, orient='index')
        df = df.sort_values(by=['date'])
        df.reset_index(drop=True, inplace=True)

    elif dataset == 'STAX':
        d = {}
        for i in range(len(data)):
            d[i] = {}
            d[i]['date'] = data[i]['date']
            d[i]['symbol'] = data[i]['symbol']
            d[i]['adf_stat'] = float(data[i]['adf_stat'])
            d[i]['adf_pvalue'] = float(data[i]['adf_pvalue'])
            d[i]['adf_cv'] = float(data[i]['adf_cv'])
            d[i]['adf_corr'] = float(data[i]['adf_corr'])
            d[i]['h'] = float(data[i]['h'])
            d[i]['c'] = float(data[i]['c'])
            d[i]['var_stat'] = float(data[i]['var_stat'])
            d[i]['var_pvalue'] = float(data[i]['var_pvalue'])
            d[i]['var_corr'] = float(data[i]['var_corr'])
            d[i]['var'] = data[i]['var']
            d[i]['coef'] = float(data[i]['coef'])
            d[i]['half'] = float(data[i]['half'])
            d[i]['adf_stat_6'] = float(data[i]['adf_stat_6'])
            d[i]['adf_pvalue_6'] = float(data[i]['adf_pvalue_6'])
            d[i]['adf_cv_6'] = float(data[i]['adf_cv_6'])
            d[i]['adf_corr_6'] = float(data[i]['adf_corr_6'])
            d[i]['h_6'] = float(data[i]['h_6'])
            d[i]['c_6'] = float(data[i]['c_6'])
            d[i]['var_stat_6'] = float(data[i]['var_stat_6'])
            d[i]['var_pvalue_6'] = float(data[i]['var_pvalue_6'])
            d[i]['var_corr_6'] = float(data[i]['var_corr_6'])
            d[i]['var_6'] = data[i]['var_6']
            d[i]['coef_6'] = float(data[i]['coef_6'])
            d[i]['half_6'] = float(data[i]['half_6'])  
            d[i]['adf_stat_12'] = float(data[i]['adf_stat_12'])
            d[i]['adf_pvalue_12'] = float(data[i]['adf_pvalue_12'])
            d[i]['adf_cv_12'] = float(data[i]['adf_cv_12'])
            d[i]['adf_corr_12'] = float(data[i]['adf_corr_12'])
            d[i]['h_12'] = float(data[i]['h_12'])
            d[i]['c_12'] = float(data[i]['c_12'])
            d[i]['var_stat_12'] = float(data[i]['var_stat_12'])
            d[i]['var_pvalue_12'] = float(data[i]['var_pvalue_12'])
            d[i]['var_corr_12'] = float(data[i]['var_corr_12'])
            d[i]['var_12'] = data[i]['var_12']
            d[i]['coef_12'] = float(data[i]['coef_12'])
            d[i]['half_12'] = float(data[i]['half_12'])  

        df = pd.DataFrame.from_dict(d, orient='index')
        df = df.sort_values(by=['date'])
        df.reset_index(drop=True, inplace=True)

    else:
        df = pd.DataFrame()

    return df
