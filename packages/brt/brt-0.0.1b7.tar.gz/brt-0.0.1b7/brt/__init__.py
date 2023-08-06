import pandas as pd
from pandasql import sqldf
import numpy as np 
import scipy.stats as stats
import warnings
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from IPython.display import display, Markdown
from functools import reduce
import pandas_datareader.data as web
import datetime
from sklearn.metrics import confusion_matrix 
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate_catalog(y:list, predicted:list):
    '''
    Evaluate predicated catalog results

    Parameters
    ----------
    y : list
        Actual result.
    predicted : list
        Predicted results.

    Returns
    -------
    None.

    '''
    results = pd.DataFrame()
    results['actual'] = y
    results['predicted'] = predicted
    results['n'] = results['actual']==results['predicted']
    print(results['n'].mean())
    
    output = results.groupby(['actual', 'predicted']).count().reset_index()
    actual = output.groupby(['actual']).sum().reset_index()
    actual.pop('predicted')
    actual.columns = ['actual', 'actual_total'] 
    
    predicted = output.groupby(['predicted']).sum().reset_index()
    predicted.pop('actual')
    predicted.columns = ['predicted', 'predicted_total'] 
    
    output = output.merge(actual, on='actual').merge(predicted, on='predicted') 
    output['% of actual'] = output['n']/output['actual_total']
    output['% of predicted'] = output['n']/output['predicted_total']
    display(output)
    sns.set_theme(style="whitegrid")

    penguins = sns.load_dataset("penguins")

    # Draw a nested barplot by species and sex
    g = sns.catplot(
        data=output, kind="bar",
        x="actual", y="% of actual", hue="predicted",
        ci="sd", palette="dark", alpha=.6, height=6
    )
    g.despine(left=True)
    g.set_axis_labels("", "Predicted (%)")
    g.legend.set_title("Recall Rate")

    g = sns.catplot(
        data=output, kind="bar",
        x="predicted", y="% of predicted", hue="actual",
        ci="sd", palette="dark", alpha=.6, height=6
    )
    g.despine(left=True)
    g.set_axis_labels("", "actual (%)")
    g.legend.set_title("Accuracy Rate")
    
    
    
    
    conf_matrix = confusion_matrix(y, predicted) 
    plt.figure(figsize =(12, 12)) 
    sns.heatmap(conf_matrix,  xticklabels = results['actual'].unique(), yticklabels = results['predicted'].unique(), annot = True, fmt ="d"); 
    plt.title("Confusion matrix") 
    plt.ylabel('True class') 
    plt.xlabel('Predicted class') 
    plt.show()
    
    
def add_dummy(data, var:str, dummy_na = False):
    '''
    Add dummy variables for variable 'var'

    Parameters
    ----------
    data : TYPE
        Input data.
    var : str
        Catagory variable.
    dummy_na : TYPE, optional
        Add a column to indicate NaNs, if False NaNs are ignored. The default is False.

    Returns
    -------
    TYPE
        New data frame, added dummy variable names.

    '''
    
    dummy = pd.get_dummies(data[var], prefix = var, dummy_na = dummy_na)
    return pd.concat([data, dummy],axis=1), dummy.columns.array.to_numpy()



def balance(data:pd.DataFrame, key:str):
    '''
    Balance a dataset by column 'key'

    Parameters
    ----------
    data : pd.DataFrame
        Input data.
    key : str
        The key of column used to balance data.

    Returns
    -------
    output : TYPE
        Balanced data.

    '''
    value = data[key].value_counts().reset_index().sort_values(key, ascending = False)
    output = data[data[key] == value.loc[0, 'index']]
    l = len(output)
    for r in range(1, value.shape[0]):
        d = data[data[key] == value.loc[0, 'index']].reset_index()
        d = d.loc[np.random.choice(np.arange(len(d)), l)]
        output = pd.concat([output, d])
    return output



def split(data:pd.DataFrame, train:float=20, validation:float=2, test:float=1, label:str='label', groupby:str=None):
    '''
    Split data into train, validation, and test datasets.

    Parameters
    ----------
    data : pd.DataFrame
        Input data.
    train : float, optional
        Train portion. The default is 20.
    validation : float, optional
        Validation portion. The default is 2.
    test : float, optional
        Test protion. The default is 1.
    label : str, optional
        Label key. The default is 'label'.
    groupby : str, optional
        If set, sample will be splited within each subsample grouped by 'groupby' column. The default is None.

    Returns
    -------
    Labeled dataset.

    '''
    total=train+validation+test
    if(groupby==None):
        l = data.shape[0]
        trainn = int(l/total*train)
        validn = int(l/total*(train+validation)) 
        data = data.sample(frac=1).reset_index()
        data.loc[:trainn, label] = 'train'
        data.loc[trainn:validn, label] = 'valid'
        data.loc[validn:, label] = 'test'
        print('Number of train data: ' + str(trainn))
        print('Number of validation data: ' + str(validn - trainn))
        print('Number of test data: ' + str(l - validn))
        return data
    else:
        output = []
        for group in data[groupby].unique():
            print('Group: ' + str(group))
            output.append(split(data[data[groupby] == group], train, validation, test, label))
        return pd.concat(output)    
 
def add_econ_variables(data:pd.DataFrame, datekey:str, tickers:list, start:datetime = datetime.datetime(1910, 1, 1), change:bool = False):
    '''
    Add econ variables to the input data from https://www.econdb.com/. All data is from 

    Parameters
    ----------
    data : pd.DataFrame
        Input data.
    datekey : str
        Date key.
    tickers : list
        List of tickers which will be added to the input data.
    start : datetime, optional
        Start date of added data. The default is datetime.datetime(1910, 1, 1).
    change : bool, optional
        Weather add yearly change to the data. The default is False.

    Returns
    -------
    TYPE
        The new data and the added keys.

    '''
    
    
    
    econs=[]
    for ticker in tickers:
        econ = web.DataReader(('ticker='+ticker), 'econdb', start).reset_index().sort_index()
        econ.columns = ['date', ticker + '_1']
        d = (econ.date - econ.shift(1).date)/pd.offsets.Day(1)/30
        f = int(12/(d.round().mean()))   
        for i in range(1, f):
            econ[ticker + '_' + str(i+1)] = econ.shift(i)[ticker+ '_1']
        econ[ticker+ '_ttm'] = econ.iloc[:,1:].sum(axis=1, skipna= False)
        if(change):
            columns = econ.columns[1:]
            econ['chg_' + columns] = econ[columns]/econ.shift(1)[columns]-1
        econs.append(econ)
    output =  reduce(lambda  left,right: pd.merge(left,right,on=['date'],
                                            how='outer'), econs)
    output.fillna(method='ffill', inplace=True)
    keys = output.columns[1:]
    return pd.merge_asof(data.sort_values(datekey), output.sort_values('date'), left_on=datekey, right_on='date', direction ='forward',allow_exact_matches =False), keys


def shift(data:pd.DataFrame, keys:list, period:int, groupby:list):
    '''
    Add lag or lead values to the input data.

    Parameters
    ----------
    data : pd.DataFrame
        Input data.
    keys : list
        List of columns to lag or lead.
    period : int
        The period of lag or lead..
    groupby : list
        Group keys.

    Returns
    -------
    shiftkeys : TYPE
        The new keys of added variables.

    '''
    
    shiftkeys = [] 
    for i, key in enumerate(keys):
        shiftkey = key+'_' + str(period)
        shiftkeys.append(shiftkey)
        data[shiftkey] = data.groupby(groupby)[key].shift(period)
    return shiftkeys



def add_ff5(input:pd.DataFrame , sic: str = 'sic', code: str = 'ff5', description: str = None):
    '''    
    Add Fama-French 5-factor code and description.

    Parameters
    ----------
    input : TYPE
        Input data.
    sic : str, optional
        SIC column name. The default is 'sic'.
    code : str, optional
        FF5 output column name. The default is 'ff5'.
    description : str, optional
        FF5 description output column name. Description will only be added if it is not None. The default is None.

    Returns
    -------
    input : TYPE
        DataFrame with added FF5 code and description if 'description' is not None.

    '''
    
     
    input[code] = np.nan
    if(description!=None):
        input[description] = np.nan
    input.loc[(input[sic].between(100,999)) | (input[sic].between(2000,2399)) | (input[sic].between(2700,2749)) | (input[sic].between(2770,2799)) | (input[sic].between(3100,3199)) | (input[sic].between(3940,3989)) | (input[sic].between(2500,2519)) | (input[sic].between(2590,2599)) | (input[sic].between(3630,3659)) | (input[sic].between(3710,3711)) | (input[sic].between(3714,3714)) | (input[sic].between(3716,3716)) | (input[sic].between(3750,3751)) | (input[sic].between(3792,3792)) | (input[sic].between(3900,3939)) | (input[sic].between(3990,3999)) | (input[sic].between(5000,5999)) | (input[sic].between(7200,7299)) | (input[sic].between(7600,7699)), code] = 1
    if(description!=None):
        input.loc[(input[sic].between(100,999)) | (input[sic].between(2000,2399)) | (input[sic].between(2700,2749)) | (input[sic].between(2770,2799)) | (input[sic].between(3100,3199)) | (input[sic].between(3940,3989)) | (input[sic].between(2500,2519)) | (input[sic].between(2590,2599)) | (input[sic].between(3630,3659)) | (input[sic].between(3710,3711)) | (input[sic].between(3714,3714)) | (input[sic].between(3716,3716)) | (input[sic].between(3750,3751)) | (input[sic].between(3792,3792)) | (input[sic].between(3900,3939)) | (input[sic].between(3990,3999)) | (input[sic].between(5000,5999)) | (input[sic].between(7200,7299)) | (input[sic].between(7600,7699)), description] = 'Cnsmr  Consumer Durables, Nondurables, Wholesale, Retail, and Some Services (Laundries, Repair Shops)'
    input.loc[(input[sic].between(2520,2589)) | (input[sic].between(2600,2699)) | (input[sic].between(2750,2769)) | (input[sic].between(2800,2829)) | (input[sic].between(2840,2899)) | (input[sic].between(3000,3099)) | (input[sic].between(3200,3569)) | (input[sic].between(3580,3621)) | (input[sic].between(3623,3629)) | (input[sic].between(3700,3709)) | (input[sic].between(3712,3713)) | (input[sic].between(3715,3715)) | (input[sic].between(3717,3749)) | (input[sic].between(3752,3791)) | (input[sic].between(3793,3799)) | (input[sic].between(3860,3899)) | (input[sic].between(1200,1399)) | (input[sic].between(2900,2999)) | (input[sic].between(4900,4949)), code] = 2
    if(description!=None):
        input.loc[(input[sic].between(2520,2589)) | (input[sic].between(2600,2699)) | (input[sic].between(2750,2769)) | (input[sic].between(2800,2829)) | (input[sic].between(2840,2899)) | (input[sic].between(3000,3099)) | (input[sic].between(3200,3569)) | (input[sic].between(3580,3621)) | (input[sic].between(3623,3629)) | (input[sic].between(3700,3709)) | (input[sic].between(3712,3713)) | (input[sic].between(3715,3715)) | (input[sic].between(3717,3749)) | (input[sic].between(3752,3791)) | (input[sic].between(3793,3799)) | (input[sic].between(3860,3899)) | (input[sic].between(1200,1399)) | (input[sic].between(2900,2999)) | (input[sic].between(4900,4949)), description] = 'Manuf  Manufacturing, Energy, and Utilities'
    input.loc[(input[sic].between(3570,3579)) | (input[sic].between(3622,3622)) | (input[sic].between(3660,3692)) | (input[sic].between(3694,3699)) | (input[sic].between(3810,3839)) | (input[sic].between(7370,7372)) | (input[sic].between(7373,7373)) | (input[sic].between(7374,7374)) | (input[sic].between(7375,7375)) | (input[sic].between(7376,7376)) | (input[sic].between(7377,7377)) | (input[sic].between(7378,7378)) | (input[sic].between(7379,7379)) | (input[sic].between(7391,7391)) | (input[sic].between(8730,8734)) | (input[sic].between(4800,4899)), code] = 3
    if(description!=None):
        input.loc[(input[sic].between(3570,3579)) | (input[sic].between(3622,3622)) | (input[sic].between(3660,3692)) | (input[sic].between(3694,3699)) | (input[sic].between(3810,3839)) | (input[sic].between(7370,7372)) | (input[sic].between(7373,7373)) | (input[sic].between(7374,7374)) | (input[sic].between(7375,7375)) | (input[sic].between(7376,7376)) | (input[sic].between(7377,7377)) | (input[sic].between(7378,7378)) | (input[sic].between(7379,7379)) | (input[sic].between(7391,7391)) | (input[sic].between(8730,8734)) | (input[sic].between(4800,4899)), description] = 'HiTec  Business Equipment, Telephone and Television Transmission'
    input.loc[(input[sic].between(2830,2839)) | (input[sic].between(3693,3693)) | (input[sic].between(3840,3859)) | (input[sic].between(8000,8099)), code] = 4
    if(description!=None):
        input.loc[(input[sic].between(2830,2839)) | (input[sic].between(3693,3693)) | (input[sic].between(3840,3859)) | (input[sic].between(8000,8099)), description] = 'Hlth   Healthcare, Medical Equipment, and Drugs'
    input.loc[(input[sic].notnull()) & (input[code].isnull()), code] = 5
    if(description!=None):
        input.loc[(input[sic].notnull()) & (input[code].isnull()), description] = 'Other  Other -- Mines, Constr, BldMt, Trans, Hotels, Bus Serv, Entertainment, Finance'
    return input

def add_ff12(input:pd.DataFrame, sic='sic', code = 'ff12', description = None):
    '''    
    Add Fama-French 12-factor code and description.

    Parameters
    ----------
    input : TYPE
        Input data.
    sic : str, optional
        SIC column name. The default is 'sic'.
    code : str, optional
        FF12 output column name. The default is 'ff12'.
    description : str, optional
        FF12 description output column name. Description will only be added if it is not None. The default is None.

    Returns
    -------
    input : TYPE
        DataFrame with added FF12 code and description if 'description' is not None.

    '''
    
    
    input[code] = np.nan
    if(description!=None):
        input[description] = np.nan
    input.loc[(input[sic].between(100,999)) | (input[sic].between(2000,2399)) | (input[sic].between(2700,2749)) | (input[sic].between(2770,2799)) | (input[sic].between(3100,3199)) | (input[sic].between(3940,3989)), code] = 1
    if(description!=None):
        input.loc[(input[sic].between(100,999)) | (input[sic].between(2000,2399)) | (input[sic].between(2700,2749)) | (input[sic].between(2770,2799)) | (input[sic].between(3100,3199)) | (input[sic].between(3940,3989)), description] = 'NoDur  Consumer Nondurables -- Food, Tobacco, Textiles, Apparel, Leather, Toys'
    input.loc[(input[sic].between(2500,2519)) | (input[sic].between(2590,2599)) | (input[sic].between(3630,3659)) | (input[sic].between(3710,3711)) | (input[sic].between(3714,3714)) | (input[sic].between(3716,3716)) | (input[sic].between(3750,3751)) | (input[sic].between(3792,3792)) | (input[sic].between(3900,3939)) | (input[sic].between(3990,3999)), code] = 2
    if(description!=None):
        input.loc[(input[sic].between(2500,2519)) | (input[sic].between(2590,2599)) | (input[sic].between(3630,3659)) | (input[sic].between(3710,3711)) | (input[sic].between(3714,3714)) | (input[sic].between(3716,3716)) | (input[sic].between(3750,3751)) | (input[sic].between(3792,3792)) | (input[sic].between(3900,3939)) | (input[sic].between(3990,3999)), description] = 'Durbl  Consumer Durables -- Cars, TVs, Furniture, Household Appliances'
    input.loc[(input[sic].between(2520,2589)) | (input[sic].between(2600,2699)) | (input[sic].between(2750,2769)) | (input[sic].between(3000,3099)) | (input[sic].between(3200,3569)) | (input[sic].between(3580,3629)) | (input[sic].between(3700,3709)) | (input[sic].between(3712,3713)) | (input[sic].between(3715,3715)) | (input[sic].between(3717,3749)) | (input[sic].between(3752,3791)) | (input[sic].between(3793,3799)) | (input[sic].between(3830,3839)) | (input[sic].between(3860,3899)), code] = 3
    if(description!=None):
        input.loc[(input[sic].between(2520,2589)) | (input[sic].between(2600,2699)) | (input[sic].between(2750,2769)) | (input[sic].between(3000,3099)) | (input[sic].between(3200,3569)) | (input[sic].between(3580,3629)) | (input[sic].between(3700,3709)) | (input[sic].between(3712,3713)) | (input[sic].between(3715,3715)) | (input[sic].between(3717,3749)) | (input[sic].between(3752,3791)) | (input[sic].between(3793,3799)) | (input[sic].between(3830,3839)) | (input[sic].between(3860,3899)), description] = 'Manuf  Manufacturing -- Machinery, Trucks, Planes, Off Furn, Paper, Com Printing'
    input.loc[(input[sic].between(1200,1399)) | (input[sic].between(2900,2999)), code] = 4
    if(description!=None):
        input.loc[(input[sic].between(1200,1399)) | (input[sic].between(2900,2999)), description] = 'Enrgy  Oil, Gas, and Coal Extraction and Products'
    input.loc[(input[sic].between(2800,2829)) | (input[sic].between(2840,2899)), code] = 5
    if(description!=None):
        input.loc[(input[sic].between(2800,2829)) | (input[sic].between(2840,2899)), description] = 'Chems  Chemicals and Allied Products'
    input.loc[(input[sic].between(3570,3579)) | (input[sic].between(3660,3692)) | (input[sic].between(3694,3699)) | (input[sic].between(3810,3829)) | (input[sic].between(7370,7379)), code] = 6
    if(description!=None):
        input.loc[(input[sic].between(3570,3579)) | (input[sic].between(3660,3692)) | (input[sic].between(3694,3699)) | (input[sic].between(3810,3829)) | (input[sic].between(7370,7379)), description] = 'BusEq  Business Equipment -- Computers, Software, and Electronic Equipment'
    input.loc[(input[sic].between(4800,4899)), code] = 7
    if(description!=None):
        input.loc[(input[sic].between(4800,4899)), description] = 'Telcm  Telephone and Television Transmission'
    input.loc[(input[sic].between(4900,4949)), code] = 8
    if(description!=None):
        input.loc[(input[sic].between(4900,4949)), description] = 'Utils  Utilities'
    input.loc[(input[sic].between(5000,5999)) | (input[sic].between(7200,7299)) | (input[sic].between(7600,7699)), code] = 9
    if(description!=None):
        input.loc[(input[sic].between(5000,5999)) | (input[sic].between(7200,7299)) | (input[sic].between(7600,7699)), description] = 'Shops  Wholesale, Retail, and Some Services (Laundries, Repair Shops)'
    input.loc[(input[sic].between(2830,2839)) | (input[sic].between(3693,3693)) | (input[sic].between(3840,3859)) | (input[sic].between(8000,8099)), code] = 10
    if(description!=None):
        input.loc[(input[sic].between(2830,2839)) | (input[sic].between(3693,3693)) | (input[sic].between(3840,3859)) | (input[sic].between(8000,8099)), description] = 'Hlth   Healthcare, Medical Equipment, and Drugs'
    input.loc[(input[sic].between(6000,6999)), code] = 11
    if(description!=None):
        input.loc[(input[sic].between(6000,6999)), description] = 'Money  Finance'
    input.loc[(input[sic].notnull()) & (input[code].isnull()), code] = 12
    if(description!=None):
        input.loc[(input[sic].notnull()) & (input[code].isnull()), description] = 'Other  Other -- Mines, Constr, BldMt, Trans, Hotels, Bus Serv, Entertainment'
    return input

def add_ff38(input:pd.DataFrame, sic='sic', code = 'ff38', description = None):
    
    '''    
    Add Fama-French 38-factor code and description.

    Parameters
    ----------
    input : TYPE
        Input data.
    sic : str, optional
        SIC column name. The default is 'sic'.
    code : str, optional
        FF38 output column name. The default is 'ff38'.
    description : str, optional
        FF38 description output column name. Description will only be added if it is not None. The default is None.

    Returns
    -------
    input : TYPE
        DataFrame with added FF38 code and description if 'description' is not None.

    '''
    
    input[code] = np.nan
    if(description!=None):
        input[description] = np.nan
    input.loc[(input[sic].between(100,999)), code] = 1
    if(description!=None):
        input.loc[(input[sic].between(100,999)), description] = 'Agric  Agriculture, forestry, and fishing'
    input.loc[(input[sic].between(1000,1299)), code] = 2
    if(description!=None):
        input.loc[(input[sic].between(1000,1299)), description] = 'Mines  Mining'
    input.loc[(input[sic].between(1300,1399)), code] = 3
    if(description!=None):
        input.loc[(input[sic].between(1300,1399)), description] = 'Oil    Oil and Gas Extraction'
    input.loc[(input[sic].between(1400,1499)), code] = 4
    if(description!=None):
        input.loc[(input[sic].between(1400,1499)), description] = 'Stone  Nonmetallic Minerals Except Fuels'
    input.loc[(input[sic].between(1500,1799)), code] = 5
    if(description!=None):
        input.loc[(input[sic].between(1500,1799)), description] = 'Cnstr  Construction'
    input.loc[(input[sic].between(2000,2099)), code] = 6
    if(description!=None):
        input.loc[(input[sic].between(2000,2099)), description] = 'Food   Food and Kindred Products'
    input.loc[(input[sic].between(2100,2199)), code] = 7
    if(description!=None):
        input.loc[(input[sic].between(2100,2199)), description] = 'Smoke  Tobacco Products'
    input.loc[(input[sic].between(2200,2299)), code] = 8
    if(description!=None):
        input.loc[(input[sic].between(2200,2299)), description] = 'Txtls  Textile Mill Products'
    input.loc[(input[sic].between(2300,2399)), code] = 9
    if(description!=None):
        input.loc[(input[sic].between(2300,2399)), description] = 'Apprl  Apparel and other Textile Products'
    input.loc[(input[sic].between(2400,2499)), code] = 10
    if(description!=None):
        input.loc[(input[sic].between(2400,2499)), description] = 'Wood   Lumber and Wood Products'
    input.loc[(input[sic].between(2500,2599)), code] = 11
    if(description!=None):
        input.loc[(input[sic].between(2500,2599)), description] = 'Chair  Furniture and Fixtures'
    input.loc[(input[sic].between(2600,2661)), code] = 12
    if(description!=None):
        input.loc[(input[sic].between(2600,2661)), description] = 'Paper  Paper and Allied Products'
    input.loc[(input[sic].between(2700,2799)), code] = 13
    if(description!=None):
        input.loc[(input[sic].between(2700,2799)), description] = 'Print  Printing and Publishing'
    input.loc[(input[sic].between(2800,2899)), code] = 14
    if(description!=None):
        input.loc[(input[sic].between(2800,2899)), description] = 'Chems  Chemicals and Allied Products'
    input.loc[(input[sic].between(2900,2999)), code] = 15
    if(description!=None):
        input.loc[(input[sic].between(2900,2999)), description] = 'Ptrlm  Petroleum and Coal Products'
    input.loc[(input[sic].between(3000,3099)), code] = 16
    if(description!=None):
        input.loc[(input[sic].between(3000,3099)), description] = 'Rubbr  Rubber and Miscellaneous Plastics Products'
    input.loc[(input[sic].between(3100,3199)), code] = 17
    if(description!=None):
        input.loc[(input[sic].between(3100,3199)), description] = 'Lethr  Leather and Leather Products'
    input.loc[(input[sic].between(3200,3299)), code] = 18
    if(description!=None):
        input.loc[(input[sic].between(3200,3299)), description] = 'Glass  Stone, Clay and Glass Products'
    input.loc[(input[sic].between(3300,3399)), code] = 19
    if(description!=None):
        input.loc[(input[sic].between(3300,3399)), description] = 'Metal  Primary Metal Industries'
    input.loc[(input[sic].between(3400,3499)), code] = 20
    if(description!=None):
        input.loc[(input[sic].between(3400,3499)), description] = 'MtlPr  Fabricated Metal Products'
    input.loc[(input[sic].between(3500,3599)), code] = 21
    if(description!=None):
        input.loc[(input[sic].between(3500,3599)), description] = 'Machn  Machinery, Except Electrical'
    input.loc[(input[sic].between(3600,3699)), code] = 22
    if(description!=None):
        input.loc[(input[sic].between(3600,3699)), description] = 'Elctr  Electrical and Electronic Equipment'
    input.loc[(input[sic].between(3700,3799)), code] = 23
    if(description!=None):
        input.loc[(input[sic].between(3700,3799)), description] = 'Cars   Transportation Equipment'
    input.loc[(input[sic].between(3800,3879)), code] = 24
    if(description!=None):
        input.loc[(input[sic].between(3800,3879)), description] = 'Instr  Instruments and Related Products'
    input.loc[(input[sic].between(3900,3999)), code] = 25
    if(description!=None):
        input.loc[(input[sic].between(3900,3999)), description] = 'Manuf  Miscellaneous Manufacturing Industries'
    input.loc[(input[sic].between(4000,4799)), code] = 26
    if(description!=None):
        input.loc[(input[sic].between(4000,4799)), description] = 'Trans  Transportation'
    input.loc[(input[sic].between(4800,4829)), code] = 27
    if(description!=None):
        input.loc[(input[sic].between(4800,4829)), description] = 'Phone  Telephone and Telegraph Communication'
    input.loc[(input[sic].between(4830,4899)), code] = 28
    if(description!=None):
        input.loc[(input[sic].between(4830,4899)), description] = 'TV     Radio and Television Broadcasting'
    input.loc[(input[sic].between(4900,4949)), code] = 29
    if(description!=None):
        input.loc[(input[sic].between(4900,4949)), description] = 'Utils  Electric, Gas, and Water Supply'
    input.loc[(input[sic].between(4950,4959)), code] = 30
    if(description!=None):
        input.loc[(input[sic].between(4950,4959)), description] = 'Garbg  Sanitary Services'
    input.loc[(input[sic].between(4960,4969)), code] = 31
    if(description!=None):
        input.loc[(input[sic].between(4960,4969)), description] = 'Steam  Steam Supply'
    input.loc[(input[sic].between(4970,4979)), code] = 32
    if(description!=None):
        input.loc[(input[sic].between(4970,4979)), description] = 'Water  Irrigation Systems'
    input.loc[(input[sic].between(5000,5199)), code] = 33
    if(description!=None):
        input.loc[(input[sic].between(5000,5199)), description] = 'Whlsl  Wholesale'
    input.loc[(input[sic].between(5200,5999)), code] = 34
    if(description!=None):
        input.loc[(input[sic].between(5200,5999)), description] = 'Rtail  Retail Stores'
    input.loc[(input[sic].between(6000,6999)), code] = 35
    if(description!=None):
        input.loc[(input[sic].between(6000,6999)), description] = 'Money  Finance, Insurance, and Real Estate'
    input.loc[(input[sic].between(7000,8999)), code] = 36
    if(description!=None):
        input.loc[(input[sic].between(7000,8999)), description] = 'Srvc   Services'
    input.loc[(input[sic].between(9000,9999)), code] = 37
    if(description!=None):
        input.loc[(input[sic].between(9000,9999)), description] = 'Govt   Public Administration'
    input.loc[(input[sic].notnull()) & (input[code].isnull()), code] = 38
    if(description!=None):
        input.loc[(input[sic].notnull()) & (input[code].isnull()), description] = 'Other  Almost Nothing'
    return input

def add_ff48(input:pd.DataFrame, sic='sic', code = 'ff48', description = None):
    '''    
    Add Fama-French 48-factor code and description.

    Parameters
    ----------
    input : TYPE
        Input data.
    sic : str, optional
        SIC column name. The default is 'sic'.
    code : str, optional
        FF48 output column name. The default is 'ff48'.
    description : str, optional
        FF48 description output column name. Description will only be added if it is not None. The default is None.

    Returns
    -------
    input : TYPE
        DataFrame with added FF48 code and description if 'description' is not None.

    '''
    
    
    input[code] = np.nan
    if(description!=None):
        input[description] = np.nan
    input.loc[(input[sic].between(100,199)) | (input[sic].between(200,299)) | (input[sic].between(700,799)) | (input[sic].between(910,919)) | (input[sic].between(2048,2048)), code] = 1
    if(description!=None):
        input.loc[(input[sic].between(100,199)) | (input[sic].between(200,299)) | (input[sic].between(700,799)) | (input[sic].between(910,919)) | (input[sic].between(2048,2048)), description] = 'Agric  Agriculture'
    input.loc[(input[sic].between(2000,2009)) | (input[sic].between(2010,2019)) | (input[sic].between(2020,2029)) | (input[sic].between(2030,2039)) | (input[sic].between(2040,2046)) | (input[sic].between(2050,2059)) | (input[sic].between(2060,2063)) | (input[sic].between(2070,2079)) | (input[sic].between(2090,2092)) | (input[sic].between(2095,2095)) | (input[sic].between(2098,2099)), code] = 2
    if(description!=None):
        input.loc[(input[sic].between(2000,2009)) | (input[sic].between(2010,2019)) | (input[sic].between(2020,2029)) | (input[sic].between(2030,2039)) | (input[sic].between(2040,2046)) | (input[sic].between(2050,2059)) | (input[sic].between(2060,2063)) | (input[sic].between(2070,2079)) | (input[sic].between(2090,2092)) | (input[sic].between(2095,2095)) | (input[sic].between(2098,2099)), description] = 'Food   Food Products'
    input.loc[(input[sic].between(2064,2068)) | (input[sic].between(2086,2086)) | (input[sic].between(2087,2087)) | (input[sic].between(2096,2096)) | (input[sic].between(2097,2097)), code] = 3
    if(description!=None):
        input.loc[(input[sic].between(2064,2068)) | (input[sic].between(2086,2086)) | (input[sic].between(2087,2087)) | (input[sic].between(2096,2096)) | (input[sic].between(2097,2097)), description] = 'Soda   Candy & Soda'
    input.loc[(input[sic].between(2080,2080)) | (input[sic].between(2082,2082)) | (input[sic].between(2083,2083)) | (input[sic].between(2084,2084)) | (input[sic].between(2085,2085)), code] = 4
    if(description!=None):
        input.loc[(input[sic].between(2080,2080)) | (input[sic].between(2082,2082)) | (input[sic].between(2083,2083)) | (input[sic].between(2084,2084)) | (input[sic].between(2085,2085)), description] = 'Beer   Beer & Liquor'
    input.loc[(input[sic].between(2100,2199)), code] = 5
    if(description!=None):
        input.loc[(input[sic].between(2100,2199)), description] = 'Smoke  Tobacco Products'
    input.loc[(input[sic].between(920,999)) | (input[sic].between(3650,3651)) | (input[sic].between(3652,3652)) | (input[sic].between(3732,3732)) | (input[sic].between(3930,3931)) | (input[sic].between(3940,3949)), code] = 6
    if(description!=None):
        input.loc[(input[sic].between(920,999)) | (input[sic].between(3650,3651)) | (input[sic].between(3652,3652)) | (input[sic].between(3732,3732)) | (input[sic].between(3930,3931)) | (input[sic].between(3940,3949)), description] = 'Toys   Recreation'
    input.loc[(input[sic].between(7800,7829)) | (input[sic].between(7830,7833)) | (input[sic].between(7840,7841)) | (input[sic].between(7900,7900)) | (input[sic].between(7910,7911)) | (input[sic].between(7920,7929)) | (input[sic].between(7930,7933)) | (input[sic].between(7940,7949)) | (input[sic].between(7980,7980)) | (input[sic].between(7990,7999)), code] = 7
    if(description!=None):
        input.loc[(input[sic].between(7800,7829)) | (input[sic].between(7830,7833)) | (input[sic].between(7840,7841)) | (input[sic].between(7900,7900)) | (input[sic].between(7910,7911)) | (input[sic].between(7920,7929)) | (input[sic].between(7930,7933)) | (input[sic].between(7940,7949)) | (input[sic].between(7980,7980)) | (input[sic].between(7990,7999)), description] = 'Fun    Entertainment'
    input.loc[(input[sic].between(2700,2709)) | (input[sic].between(2710,2719)) | (input[sic].between(2720,2729)) | (input[sic].between(2730,2739)) | (input[sic].between(2740,2749)) | (input[sic].between(2770,2771)) | (input[sic].between(2780,2789)) | (input[sic].between(2790,2799)), code] = 8
    if(description!=None):
        input.loc[(input[sic].between(2700,2709)) | (input[sic].between(2710,2719)) | (input[sic].between(2720,2729)) | (input[sic].between(2730,2739)) | (input[sic].between(2740,2749)) | (input[sic].between(2770,2771)) | (input[sic].between(2780,2789)) | (input[sic].between(2790,2799)), description] = 'Books  Printing and Publishing'
    input.loc[(input[sic].between(2047,2047)) | (input[sic].between(2391,2392)) | (input[sic].between(2510,2519)) | (input[sic].between(2590,2599)) | (input[sic].between(2840,2843)) | (input[sic].between(2844,2844)) | (input[sic].between(3160,3161)) | (input[sic].between(3170,3171)) | (input[sic].between(3172,3172)) | (input[sic].between(3190,3199)) | (input[sic].between(3229,3229)) | (input[sic].between(3260,3260)) | (input[sic].between(3262,3263)) | (input[sic].between(3269,3269)) | (input[sic].between(3230,3231)) | (input[sic].between(3630,3639)) | (input[sic].between(3750,3751)) | (input[sic].between(3800,3800)) | (input[sic].between(3860,3861)) | (input[sic].between(3870,3873)) | (input[sic].between(3910,3911)) | (input[sic].between(3914,3914)) | (input[sic].between(3915,3915)) | (input[sic].between(3960,3962)) | (input[sic].between(3991,3991)) | (input[sic].between(3995,3995)), code] = 9
    if(description!=None):
        input.loc[(input[sic].between(2047,2047)) | (input[sic].between(2391,2392)) | (input[sic].between(2510,2519)) | (input[sic].between(2590,2599)) | (input[sic].between(2840,2843)) | (input[sic].between(2844,2844)) | (input[sic].between(3160,3161)) | (input[sic].between(3170,3171)) | (input[sic].between(3172,3172)) | (input[sic].between(3190,3199)) | (input[sic].between(3229,3229)) | (input[sic].between(3260,3260)) | (input[sic].between(3262,3263)) | (input[sic].between(3269,3269)) | (input[sic].between(3230,3231)) | (input[sic].between(3630,3639)) | (input[sic].between(3750,3751)) | (input[sic].between(3800,3800)) | (input[sic].between(3860,3861)) | (input[sic].between(3870,3873)) | (input[sic].between(3910,3911)) | (input[sic].between(3914,3914)) | (input[sic].between(3915,3915)) | (input[sic].between(3960,3962)) | (input[sic].between(3991,3991)) | (input[sic].between(3995,3995)), description] = 'Hshld  Consumer Goods'
    input.loc[(input[sic].between(2300,2390)) | (input[sic].between(3020,3021)) | (input[sic].between(3100,3111)) | (input[sic].between(3130,3131)) | (input[sic].between(3140,3149)) | (input[sic].between(3150,3151)) | (input[sic].between(3963,3965)), code] = 10
    if(description!=None):
        input.loc[(input[sic].between(2300,2390)) | (input[sic].between(3020,3021)) | (input[sic].between(3100,3111)) | (input[sic].between(3130,3131)) | (input[sic].between(3140,3149)) | (input[sic].between(3150,3151)) | (input[sic].between(3963,3965)), description] = 'Clths  Apparel'
    input.loc[(input[sic].between(8000,8099)), code] = 11
    if(description!=None):
        input.loc[(input[sic].between(8000,8099)), description] = 'Hlth   Healthcare'
    input.loc[(input[sic].between(3693,3693)) | (input[sic].between(3840,3849)) | (input[sic].between(3850,3851)), code] = 12
    if(description!=None):
        input.loc[(input[sic].between(3693,3693)) | (input[sic].between(3840,3849)) | (input[sic].between(3850,3851)), description] = 'MedEq  Medical Equipment'
    input.loc[(input[sic].between(2830,2830)) | (input[sic].between(2831,2831)) | (input[sic].between(2833,2833)) | (input[sic].between(2834,2834)) | (input[sic].between(2835,2835)) | (input[sic].between(2836,2836)), code] = 13
    if(description!=None):
        input.loc[(input[sic].between(2830,2830)) | (input[sic].between(2831,2831)) | (input[sic].between(2833,2833)) | (input[sic].between(2834,2834)) | (input[sic].between(2835,2835)) | (input[sic].between(2836,2836)), description] = 'Drugs  Pharmaceutical Products'
    input.loc[(input[sic].between(2800,2809)) | (input[sic].between(2810,2819)) | (input[sic].between(2820,2829)) | (input[sic].between(2850,2859)) | (input[sic].between(2860,2869)) | (input[sic].between(2870,2879)) | (input[sic].between(2890,2899)), code] = 14
    if(description!=None):
        input.loc[(input[sic].between(2800,2809)) | (input[sic].between(2810,2819)) | (input[sic].between(2820,2829)) | (input[sic].between(2850,2859)) | (input[sic].between(2860,2869)) | (input[sic].between(2870,2879)) | (input[sic].between(2890,2899)), description] = 'Chems  Chemicals'
    input.loc[(input[sic].between(3031,3031)) | (input[sic].between(3041,3041)) | (input[sic].between(3050,3053)) | (input[sic].between(3060,3069)) | (input[sic].between(3070,3079)) | (input[sic].between(3080,3089)) | (input[sic].between(3090,3099)), code] = 15
    if(description!=None):
        input.loc[(input[sic].between(3031,3031)) | (input[sic].between(3041,3041)) | (input[sic].between(3050,3053)) | (input[sic].between(3060,3069)) | (input[sic].between(3070,3079)) | (input[sic].between(3080,3089)) | (input[sic].between(3090,3099)), description] = 'Rubbr  Rubber and Plastic Products'
    input.loc[(input[sic].between(2200,2269)) | (input[sic].between(2270,2279)) | (input[sic].between(2280,2284)) | (input[sic].between(2290,2295)) | (input[sic].between(2297,2297)) | (input[sic].between(2298,2298)) | (input[sic].between(2299,2299)) | (input[sic].between(2393,2395)) | (input[sic].between(2397,2399)), code] = 16
    if(description!=None):
        input.loc[(input[sic].between(2200,2269)) | (input[sic].between(2270,2279)) | (input[sic].between(2280,2284)) | (input[sic].between(2290,2295)) | (input[sic].between(2297,2297)) | (input[sic].between(2298,2298)) | (input[sic].between(2299,2299)) | (input[sic].between(2393,2395)) | (input[sic].between(2397,2399)), description] = 'Txtls  Textiles'
    input.loc[(input[sic].between(800,899)) | (input[sic].between(2400,2439)) | (input[sic].between(2450,2459)) | (input[sic].between(2490,2499)) | (input[sic].between(2660,2661)) | (input[sic].between(2950,2952)) | (input[sic].between(3200,3200)) | (input[sic].between(3210,3211)) | (input[sic].between(3240,3241)) | (input[sic].between(3250,3259)) | (input[sic].between(3261,3261)) | (input[sic].between(3264,3264)) | (input[sic].between(3270,3275)) | (input[sic].between(3280,3281)) | (input[sic].between(3290,3293)) | (input[sic].between(3295,3299)) | (input[sic].between(3420,3429)) | (input[sic].between(3430,3433)) | (input[sic].between(3440,3441)) | (input[sic].between(3442,3442)) | (input[sic].between(3446,3446)) | (input[sic].between(3448,3448)) | (input[sic].between(3449,3449)) | (input[sic].between(3450,3451)) | (input[sic].between(3452,3452)) | (input[sic].between(3490,3499)) | (input[sic].between(3996,3996)), code] = 17
    if(description!=None):
        input.loc[(input[sic].between(800,899)) | (input[sic].between(2400,2439)) | (input[sic].between(2450,2459)) | (input[sic].between(2490,2499)) | (input[sic].between(2660,2661)) | (input[sic].between(2950,2952)) | (input[sic].between(3200,3200)) | (input[sic].between(3210,3211)) | (input[sic].between(3240,3241)) | (input[sic].between(3250,3259)) | (input[sic].between(3261,3261)) | (input[sic].between(3264,3264)) | (input[sic].between(3270,3275)) | (input[sic].between(3280,3281)) | (input[sic].between(3290,3293)) | (input[sic].between(3295,3299)) | (input[sic].between(3420,3429)) | (input[sic].between(3430,3433)) | (input[sic].between(3440,3441)) | (input[sic].between(3442,3442)) | (input[sic].between(3446,3446)) | (input[sic].between(3448,3448)) | (input[sic].between(3449,3449)) | (input[sic].between(3450,3451)) | (input[sic].between(3452,3452)) | (input[sic].between(3490,3499)) | (input[sic].between(3996,3996)), description] = 'BldMt  Construction Materials'
    input.loc[(input[sic].between(1500,1511)) | (input[sic].between(1520,1529)) | (input[sic].between(1530,1539)) | (input[sic].between(1540,1549)) | (input[sic].between(1600,1699)) | (input[sic].between(1700,1799)), code] = 18
    if(description!=None):
        input.loc[(input[sic].between(1500,1511)) | (input[sic].between(1520,1529)) | (input[sic].between(1530,1539)) | (input[sic].between(1540,1549)) | (input[sic].between(1600,1699)) | (input[sic].between(1700,1799)), description] = 'Cnstr  Construction'
    input.loc[(input[sic].between(3300,3300)) | (input[sic].between(3310,3317)) | (input[sic].between(3320,3325)) | (input[sic].between(3330,3339)) | (input[sic].between(3340,3341)) | (input[sic].between(3350,3357)) | (input[sic].between(3360,3369)) | (input[sic].between(3370,3379)) | (input[sic].between(3390,3399)), code] = 19
    if(description!=None):
        input.loc[(input[sic].between(3300,3300)) | (input[sic].between(3310,3317)) | (input[sic].between(3320,3325)) | (input[sic].between(3330,3339)) | (input[sic].between(3340,3341)) | (input[sic].between(3350,3357)) | (input[sic].between(3360,3369)) | (input[sic].between(3370,3379)) | (input[sic].between(3390,3399)), description] = 'Steel  Steel Works Etc'
    input.loc[(input[sic].between(3400,3400)) | (input[sic].between(3443,3443)) | (input[sic].between(3444,3444)) | (input[sic].between(3460,3469)) | (input[sic].between(3470,3479)), code] = 20
    if(description!=None):
        input.loc[(input[sic].between(3400,3400)) | (input[sic].between(3443,3443)) | (input[sic].between(3444,3444)) | (input[sic].between(3460,3469)) | (input[sic].between(3470,3479)), description] = 'FabPr  Fabricated Products'
    input.loc[(input[sic].between(3510,3519)) | (input[sic].between(3520,3529)) | (input[sic].between(3530,3530)) | (input[sic].between(3531,3531)) | (input[sic].between(3532,3532)) | (input[sic].between(3533,3533)) | (input[sic].between(3534,3534)) | (input[sic].between(3535,3535)) | (input[sic].between(3536,3536)) | (input[sic].between(3538,3538)) | (input[sic].between(3540,3549)) | (input[sic].between(3550,3559)) | (input[sic].between(3560,3569)) | (input[sic].between(3580,3580)) | (input[sic].between(3581,3581)) | (input[sic].between(3582,3582)) | (input[sic].between(3585,3585)) | (input[sic].between(3586,3586)) | (input[sic].between(3589,3589)) | (input[sic].between(3590,3599)), code] = 21
    if(description!=None):
        input.loc[(input[sic].between(3510,3519)) | (input[sic].between(3520,3529)) | (input[sic].between(3530,3530)) | (input[sic].between(3531,3531)) | (input[sic].between(3532,3532)) | (input[sic].between(3533,3533)) | (input[sic].between(3534,3534)) | (input[sic].between(3535,3535)) | (input[sic].between(3536,3536)) | (input[sic].between(3538,3538)) | (input[sic].between(3540,3549)) | (input[sic].between(3550,3559)) | (input[sic].between(3560,3569)) | (input[sic].between(3580,3580)) | (input[sic].between(3581,3581)) | (input[sic].between(3582,3582)) | (input[sic].between(3585,3585)) | (input[sic].between(3586,3586)) | (input[sic].between(3589,3589)) | (input[sic].between(3590,3599)), description] = 'Mach   Machinery'
    input.loc[(input[sic].between(3600,3600)) | (input[sic].between(3610,3613)) | (input[sic].between(3620,3621)) | (input[sic].between(3623,3629)) | (input[sic].between(3640,3644)) | (input[sic].between(3645,3645)) | (input[sic].between(3646,3646)) | (input[sic].between(3648,3649)) | (input[sic].between(3660,3660)) | (input[sic].between(3690,3690)) | (input[sic].between(3691,3692)) | (input[sic].between(3699,3699)), code] = 22
    if(description!=None):
        input.loc[(input[sic].between(3600,3600)) | (input[sic].between(3610,3613)) | (input[sic].between(3620,3621)) | (input[sic].between(3623,3629)) | (input[sic].between(3640,3644)) | (input[sic].between(3645,3645)) | (input[sic].between(3646,3646)) | (input[sic].between(3648,3649)) | (input[sic].between(3660,3660)) | (input[sic].between(3690,3690)) | (input[sic].between(3691,3692)) | (input[sic].between(3699,3699)), description] = 'ElcEq  Electrical Equipment'
    input.loc[(input[sic].between(2296,2296)) | (input[sic].between(2396,2396)) | (input[sic].between(3010,3011)) | (input[sic].between(3537,3537)) | (input[sic].between(3647,3647)) | (input[sic].between(3694,3694)) | (input[sic].between(3700,3700)) | (input[sic].between(3710,3710)) | (input[sic].between(3711,3711)) | (input[sic].between(3713,3713)) | (input[sic].between(3714,3714)) | (input[sic].between(3715,3715)) | (input[sic].between(3716,3716)) | (input[sic].between(3792,3792)) | (input[sic].between(3790,3791)) | (input[sic].between(3799,3799)), code] = 23
    if(description!=None):
        input.loc[(input[sic].between(2296,2296)) | (input[sic].between(2396,2396)) | (input[sic].between(3010,3011)) | (input[sic].between(3537,3537)) | (input[sic].between(3647,3647)) | (input[sic].between(3694,3694)) | (input[sic].between(3700,3700)) | (input[sic].between(3710,3710)) | (input[sic].between(3711,3711)) | (input[sic].between(3713,3713)) | (input[sic].between(3714,3714)) | (input[sic].between(3715,3715)) | (input[sic].between(3716,3716)) | (input[sic].between(3792,3792)) | (input[sic].between(3790,3791)) | (input[sic].between(3799,3799)), description] = 'Autos  Automobiles and Trucks'
    input.loc[(input[sic].between(3720,3720)) | (input[sic].between(3721,3721)) | (input[sic].between(3723,3724)) | (input[sic].between(3725,3725)) | (input[sic].between(3728,3729)), code] = 24
    if(description!=None):
        input.loc[(input[sic].between(3720,3720)) | (input[sic].between(3721,3721)) | (input[sic].between(3723,3724)) | (input[sic].between(3725,3725)) | (input[sic].between(3728,3729)), description] = 'Aero   Aircraft'
    input.loc[(input[sic].between(3730,3731)) | (input[sic].between(3740,3743)), code] = 25
    if(description!=None):
        input.loc[(input[sic].between(3730,3731)) | (input[sic].between(3740,3743)), description] = 'Ships  Shipbuilding, Railroad Equipment'
    input.loc[(input[sic].between(3760,3769)) | (input[sic].between(3795,3795)) | (input[sic].between(3480,3489)), code] = 26
    if(description!=None):
        input.loc[(input[sic].between(3760,3769)) | (input[sic].between(3795,3795)) | (input[sic].between(3480,3489)), description] = 'Guns   Defense'
    input.loc[(input[sic].between(1040,1049)), code] = 27
    if(description!=None):
        input.loc[(input[sic].between(1040,1049)), description] = 'Gold   Precious Metals'
    input.loc[(input[sic].between(1000,1009)) | (input[sic].between(1010,1019)) | (input[sic].between(1020,1029)) | (input[sic].between(1030,1039)) | (input[sic].between(1050,1059)) | (input[sic].between(1060,1069)) | (input[sic].between(1070,1079)) | (input[sic].between(1080,1089)) | (input[sic].between(1090,1099)) | (input[sic].between(1100,1119)) | (input[sic].between(1400,1499)), code] = 28
    if(description!=None):
        input.loc[(input[sic].between(1000,1009)) | (input[sic].between(1010,1019)) | (input[sic].between(1020,1029)) | (input[sic].between(1030,1039)) | (input[sic].between(1050,1059)) | (input[sic].between(1060,1069)) | (input[sic].between(1070,1079)) | (input[sic].between(1080,1089)) | (input[sic].between(1090,1099)) | (input[sic].between(1100,1119)) | (input[sic].between(1400,1499)), description] = 'Mines  Non-Metallic and Industrial Metal Mining'
    input.loc[(input[sic].between(1200,1299)), code] = 29
    if(description!=None):
        input.loc[(input[sic].between(1200,1299)), description] = 'Coal   Coal'
    input.loc[(input[sic].between(1300,1300)) | (input[sic].between(1310,1319)) | (input[sic].between(1320,1329)) | (input[sic].between(1330,1339)) | (input[sic].between(1370,1379)) | (input[sic].between(1380,1380)) | (input[sic].between(1381,1381)) | (input[sic].between(1382,1382)) | (input[sic].between(1389,1389)) | (input[sic].between(2900,2912)) | (input[sic].between(2990,2999)), code] = 30
    if(description!=None):
        input.loc[(input[sic].between(1300,1300)) | (input[sic].between(1310,1319)) | (input[sic].between(1320,1329)) | (input[sic].between(1330,1339)) | (input[sic].between(1370,1379)) | (input[sic].between(1380,1380)) | (input[sic].between(1381,1381)) | (input[sic].between(1382,1382)) | (input[sic].between(1389,1389)) | (input[sic].between(2900,2912)) | (input[sic].between(2990,2999)), description] = 'Oil    Petroleum and Natural Gas'
    input.loc[(input[sic].between(4900,4900)) | (input[sic].between(4910,4911)) | (input[sic].between(4920,4922)) | (input[sic].between(4923,4923)) | (input[sic].between(4924,4925)) | (input[sic].between(4930,4931)) | (input[sic].between(4932,4932)) | (input[sic].between(4939,4939)) | (input[sic].between(4940,4942)), code] = 31
    if(description!=None):
        input.loc[(input[sic].between(4900,4900)) | (input[sic].between(4910,4911)) | (input[sic].between(4920,4922)) | (input[sic].between(4923,4923)) | (input[sic].between(4924,4925)) | (input[sic].between(4930,4931)) | (input[sic].between(4932,4932)) | (input[sic].between(4939,4939)) | (input[sic].between(4940,4942)), description] = 'Util   Utilities'
    input.loc[(input[sic].between(4800,4800)) | (input[sic].between(4810,4813)) | (input[sic].between(4820,4822)) | (input[sic].between(4830,4839)) | (input[sic].between(4840,4841)) | (input[sic].between(4880,4889)) | (input[sic].between(4890,4890)) | (input[sic].between(4891,4891)) | (input[sic].between(4892,4892)) | (input[sic].between(4899,4899)), code] = 32
    if(description!=None):
        input.loc[(input[sic].between(4800,4800)) | (input[sic].between(4810,4813)) | (input[sic].between(4820,4822)) | (input[sic].between(4830,4839)) | (input[sic].between(4840,4841)) | (input[sic].between(4880,4889)) | (input[sic].between(4890,4890)) | (input[sic].between(4891,4891)) | (input[sic].between(4892,4892)) | (input[sic].between(4899,4899)), description] = 'Telcm  Communication'
    input.loc[(input[sic].between(7020,7021)) | (input[sic].between(7030,7033)) | (input[sic].between(7200,7200)) | (input[sic].between(7210,7212)) | (input[sic].between(7214,7214)) | (input[sic].between(7215,7216)) | (input[sic].between(7217,7217)) | (input[sic].between(7219,7219)) | (input[sic].between(7220,7221)) | (input[sic].between(7230,7231)) | (input[sic].between(7240,7241)) | (input[sic].between(7250,7251)) | (input[sic].between(7260,7269)) | (input[sic].between(7270,7290)) | (input[sic].between(7291,7291)) | (input[sic].between(7292,7299)) | (input[sic].between(7395,7395)) | (input[sic].between(7500,7500)) | (input[sic].between(7520,7529)) | (input[sic].between(7530,7539)) | (input[sic].between(7540,7549)) | (input[sic].between(7600,7600)) | (input[sic].between(7620,7620)) | (input[sic].between(7622,7622)) | (input[sic].between(7623,7623)) | (input[sic].between(7629,7629)) | (input[sic].between(7630,7631)) | (input[sic].between(7640,7641)) | (input[sic].between(7690,7699)) | (input[sic].between(8100,8199)) | (input[sic].between(8200,8299)) | (input[sic].between(8300,8399)) | (input[sic].between(8400,8499)) | (input[sic].between(8600,8699)) | (input[sic].between(8800,8899)) | (input[sic].between(7510,7515)), code] = 33
    if(description!=None):
        input.loc[(input[sic].between(7020,7021)) | (input[sic].between(7030,7033)) | (input[sic].between(7200,7200)) | (input[sic].between(7210,7212)) | (input[sic].between(7214,7214)) | (input[sic].between(7215,7216)) | (input[sic].between(7217,7217)) | (input[sic].between(7219,7219)) | (input[sic].between(7220,7221)) | (input[sic].between(7230,7231)) | (input[sic].between(7240,7241)) | (input[sic].between(7250,7251)) | (input[sic].between(7260,7269)) | (input[sic].between(7270,7290)) | (input[sic].between(7291,7291)) | (input[sic].between(7292,7299)) | (input[sic].between(7395,7395)) | (input[sic].between(7500,7500)) | (input[sic].between(7520,7529)) | (input[sic].between(7530,7539)) | (input[sic].between(7540,7549)) | (input[sic].between(7600,7600)) | (input[sic].between(7620,7620)) | (input[sic].between(7622,7622)) | (input[sic].between(7623,7623)) | (input[sic].between(7629,7629)) | (input[sic].between(7630,7631)) | (input[sic].between(7640,7641)) | (input[sic].between(7690,7699)) | (input[sic].between(8100,8199)) | (input[sic].between(8200,8299)) | (input[sic].between(8300,8399)) | (input[sic].between(8400,8499)) | (input[sic].between(8600,8699)) | (input[sic].between(8800,8899)) | (input[sic].between(7510,7515)), description] = 'PerSv  Personal Services'
    input.loc[(input[sic].between(2750,2759)) | (input[sic].between(3993,3993)) | (input[sic].between(7218,7218)) | (input[sic].between(7300,7300)) | (input[sic].between(7310,7319)) | (input[sic].between(7320,7329)) | (input[sic].between(7330,7339)) | (input[sic].between(7340,7342)) | (input[sic].between(7349,7349)) | (input[sic].between(7350,7351)) | (input[sic].between(7352,7352)) | (input[sic].between(7353,7353)) | (input[sic].between(7359,7359)) | (input[sic].between(7360,7369)) | (input[sic].between(7370,7372)) | (input[sic].between(7374,7374)) | (input[sic].between(7375,7375)) | (input[sic].between(7376,7376)) | (input[sic].between(7377,7377)) | (input[sic].between(7378,7378)) | (input[sic].between(7379,7379)) | (input[sic].between(7380,7380)) | (input[sic].between(7381,7382)) | (input[sic].between(7383,7383)) | (input[sic].between(7384,7384)) | (input[sic].between(7385,7385)) | (input[sic].between(7389,7390)) | (input[sic].between(7391,7391)) | (input[sic].between(7392,7392)) | (input[sic].between(7393,7393)) | (input[sic].between(7394,7394)) | (input[sic].between(7396,7396)) | (input[sic].between(7397,7397)) | (input[sic].between(7399,7399)) | (input[sic].between(7519,7519)) | (input[sic].between(8700,8700)) | (input[sic].between(8710,8713)) | (input[sic].between(8720,8721)) | (input[sic].between(8730,8734)) | (input[sic].between(8740,8748)) | (input[sic].between(8900,8910)) | (input[sic].between(8911,8911)) | (input[sic].between(8920,8999)) | (input[sic].between(4220,4229)), code] = 34
    if(description!=None):
        input.loc[(input[sic].between(2750,2759)) | (input[sic].between(3993,3993)) | (input[sic].between(7218,7218)) | (input[sic].between(7300,7300)) | (input[sic].between(7310,7319)) | (input[sic].between(7320,7329)) | (input[sic].between(7330,7339)) | (input[sic].between(7340,7342)) | (input[sic].between(7349,7349)) | (input[sic].between(7350,7351)) | (input[sic].between(7352,7352)) | (input[sic].between(7353,7353)) | (input[sic].between(7359,7359)) | (input[sic].between(7360,7369)) | (input[sic].between(7370,7372)) | (input[sic].between(7374,7374)) | (input[sic].between(7375,7375)) | (input[sic].between(7376,7376)) | (input[sic].between(7377,7377)) | (input[sic].between(7378,7378)) | (input[sic].between(7379,7379)) | (input[sic].between(7380,7380)) | (input[sic].between(7381,7382)) | (input[sic].between(7383,7383)) | (input[sic].between(7384,7384)) | (input[sic].between(7385,7385)) | (input[sic].between(7389,7390)) | (input[sic].between(7391,7391)) | (input[sic].between(7392,7392)) | (input[sic].between(7393,7393)) | (input[sic].between(7394,7394)) | (input[sic].between(7396,7396)) | (input[sic].between(7397,7397)) | (input[sic].between(7399,7399)) | (input[sic].between(7519,7519)) | (input[sic].between(8700,8700)) | (input[sic].between(8710,8713)) | (input[sic].between(8720,8721)) | (input[sic].between(8730,8734)) | (input[sic].between(8740,8748)) | (input[sic].between(8900,8910)) | (input[sic].between(8911,8911)) | (input[sic].between(8920,8999)) | (input[sic].between(4220,4229)), description] = 'BusSv  Business Services'
    input.loc[(input[sic].between(3570,3579)) | (input[sic].between(3680,3680)) | (input[sic].between(3681,3681)) | (input[sic].between(3682,3682)) | (input[sic].between(3683,3683)) | (input[sic].between(3684,3684)) | (input[sic].between(3685,3685)) | (input[sic].between(3686,3686)) | (input[sic].between(3687,3687)) | (input[sic].between(3688,3688)) | (input[sic].between(3689,3689)) | (input[sic].between(3695,3695)) | (input[sic].between(7373,7373)), code] = 35
    if(description!=None):
        input.loc[(input[sic].between(3570,3579)) | (input[sic].between(3680,3680)) | (input[sic].between(3681,3681)) | (input[sic].between(3682,3682)) | (input[sic].between(3683,3683)) | (input[sic].between(3684,3684)) | (input[sic].between(3685,3685)) | (input[sic].between(3686,3686)) | (input[sic].between(3687,3687)) | (input[sic].between(3688,3688)) | (input[sic].between(3689,3689)) | (input[sic].between(3695,3695)) | (input[sic].between(7373,7373)), description] = 'Comps  Computers'
    input.loc[(input[sic].between(3622,3622)) | (input[sic].between(3661,3661)) | (input[sic].between(3662,3662)) | (input[sic].between(3663,3663)) | (input[sic].between(3664,3664)) | (input[sic].between(3665,3665)) | (input[sic].between(3666,3666)) | (input[sic].between(3669,3669)) | (input[sic].between(3670,3679)) | (input[sic].between(3810,3810)) | (input[sic].between(3812,3812)), code] = 36
    if(description!=None):
        input.loc[(input[sic].between(3622,3622)) | (input[sic].between(3661,3661)) | (input[sic].between(3662,3662)) | (input[sic].between(3663,3663)) | (input[sic].between(3664,3664)) | (input[sic].between(3665,3665)) | (input[sic].between(3666,3666)) | (input[sic].between(3669,3669)) | (input[sic].between(3670,3679)) | (input[sic].between(3810,3810)) | (input[sic].between(3812,3812)), description] = 'Chips  Electronic Equipment'
    input.loc[(input[sic].between(3811,3811)) | (input[sic].between(3820,3820)) | (input[sic].between(3821,3821)) | (input[sic].between(3822,3822)) | (input[sic].between(3823,3823)) | (input[sic].between(3824,3824)) | (input[sic].between(3825,3825)) | (input[sic].between(3826,3826)) | (input[sic].between(3827,3827)) | (input[sic].between(3829,3829)) | (input[sic].between(3830,3839)), code] = 37
    if(description!=None):
        input.loc[(input[sic].between(3811,3811)) | (input[sic].between(3820,3820)) | (input[sic].between(3821,3821)) | (input[sic].between(3822,3822)) | (input[sic].between(3823,3823)) | (input[sic].between(3824,3824)) | (input[sic].between(3825,3825)) | (input[sic].between(3826,3826)) | (input[sic].between(3827,3827)) | (input[sic].between(3829,3829)) | (input[sic].between(3830,3839)), description] = 'LabEq  Measuring and Control Equipment'
    input.loc[(input[sic].between(2520,2549)) | (input[sic].between(2600,2639)) | (input[sic].between(2670,2699)) | (input[sic].between(2760,2761)) | (input[sic].between(3950,3955)), code] = 38
    if(description!=None):
        input.loc[(input[sic].between(2520,2549)) | (input[sic].between(2600,2639)) | (input[sic].between(2670,2699)) | (input[sic].between(2760,2761)) | (input[sic].between(3950,3955)), description] = 'Paper  Business Supplies'
    input.loc[(input[sic].between(2440,2449)) | (input[sic].between(2640,2659)) | (input[sic].between(3220,3221)) | (input[sic].between(3410,3412)), code] = 39
    if(description!=None):
        input.loc[(input[sic].between(2440,2449)) | (input[sic].between(2640,2659)) | (input[sic].between(3220,3221)) | (input[sic].between(3410,3412)), description] = 'Boxes  Shipping Containers'
    input.loc[(input[sic].between(4000,4013)) | (input[sic].between(4040,4049)) | (input[sic].between(4100,4100)) | (input[sic].between(4110,4119)) | (input[sic].between(4120,4121)) | (input[sic].between(4130,4131)) | (input[sic].between(4140,4142)) | (input[sic].between(4150,4151)) | (input[sic].between(4170,4173)) | (input[sic].between(4190,4199)) | (input[sic].between(4200,4200)) | (input[sic].between(4210,4219)) | (input[sic].between(4230,4231)) | (input[sic].between(4240,4249)) | (input[sic].between(4400,4499)) | (input[sic].between(4500,4599)) | (input[sic].between(4600,4699)) | (input[sic].between(4700,4700)) | (input[sic].between(4710,4712)) | (input[sic].between(4720,4729)) | (input[sic].between(4730,4739)) | (input[sic].between(4740,4749)) | (input[sic].between(4780,4780)) | (input[sic].between(4782,4782)) | (input[sic].between(4783,4783)) | (input[sic].between(4784,4784)) | (input[sic].between(4785,4785)) | (input[sic].between(4789,4789)), code] = 40
    if(description!=None):
        input.loc[(input[sic].between(4000,4013)) | (input[sic].between(4040,4049)) | (input[sic].between(4100,4100)) | (input[sic].between(4110,4119)) | (input[sic].between(4120,4121)) | (input[sic].between(4130,4131)) | (input[sic].between(4140,4142)) | (input[sic].between(4150,4151)) | (input[sic].between(4170,4173)) | (input[sic].between(4190,4199)) | (input[sic].between(4200,4200)) | (input[sic].between(4210,4219)) | (input[sic].between(4230,4231)) | (input[sic].between(4240,4249)) | (input[sic].between(4400,4499)) | (input[sic].between(4500,4599)) | (input[sic].between(4600,4699)) | (input[sic].between(4700,4700)) | (input[sic].between(4710,4712)) | (input[sic].between(4720,4729)) | (input[sic].between(4730,4739)) | (input[sic].between(4740,4749)) | (input[sic].between(4780,4780)) | (input[sic].between(4782,4782)) | (input[sic].between(4783,4783)) | (input[sic].between(4784,4784)) | (input[sic].between(4785,4785)) | (input[sic].between(4789,4789)), description] = 'Trans  Transportation'
    input.loc[(input[sic].between(5000,5000)) | (input[sic].between(5010,5015)) | (input[sic].between(5020,5023)) | (input[sic].between(5030,5039)) | (input[sic].between(5040,5042)) | (input[sic].between(5043,5043)) | (input[sic].between(5044,5044)) | (input[sic].between(5045,5045)) | (input[sic].between(5046,5046)) | (input[sic].between(5047,5047)) | (input[sic].between(5048,5048)) | (input[sic].between(5049,5049)) | (input[sic].between(5050,5059)) | (input[sic].between(5060,5060)) | (input[sic].between(5063,5063)) | (input[sic].between(5064,5064)) | (input[sic].between(5065,5065)) | (input[sic].between(5070,5078)) | (input[sic].between(5080,5080)) | (input[sic].between(5081,5081)) | (input[sic].between(5082,5082)) | (input[sic].between(5083,5083)) | (input[sic].between(5084,5084)) | (input[sic].between(5085,5085)) | (input[sic].between(5086,5087)) | (input[sic].between(5088,5088)) | (input[sic].between(5090,5090)) | (input[sic].between(5091,5092)) | (input[sic].between(5093,5093)) | (input[sic].between(5094,5094)) | (input[sic].between(5099,5099)) | (input[sic].between(5100,5100)) | (input[sic].between(5110,5113)) | (input[sic].between(5120,5122)) | (input[sic].between(5130,5139)) | (input[sic].between(5140,5149)) | (input[sic].between(5150,5159)) | (input[sic].between(5160,5169)) | (input[sic].between(5170,5172)) | (input[sic].between(5180,5182)) | (input[sic].between(5190,5199)), code] = 41
    if(description!=None):
        input.loc[(input[sic].between(5000,5000)) | (input[sic].between(5010,5015)) | (input[sic].between(5020,5023)) | (input[sic].between(5030,5039)) | (input[sic].between(5040,5042)) | (input[sic].between(5043,5043)) | (input[sic].between(5044,5044)) | (input[sic].between(5045,5045)) | (input[sic].between(5046,5046)) | (input[sic].between(5047,5047)) | (input[sic].between(5048,5048)) | (input[sic].between(5049,5049)) | (input[sic].between(5050,5059)) | (input[sic].between(5060,5060)) | (input[sic].between(5063,5063)) | (input[sic].between(5064,5064)) | (input[sic].between(5065,5065)) | (input[sic].between(5070,5078)) | (input[sic].between(5080,5080)) | (input[sic].between(5081,5081)) | (input[sic].between(5082,5082)) | (input[sic].between(5083,5083)) | (input[sic].between(5084,5084)) | (input[sic].between(5085,5085)) | (input[sic].between(5086,5087)) | (input[sic].between(5088,5088)) | (input[sic].between(5090,5090)) | (input[sic].between(5091,5092)) | (input[sic].between(5093,5093)) | (input[sic].between(5094,5094)) | (input[sic].between(5099,5099)) | (input[sic].between(5100,5100)) | (input[sic].between(5110,5113)) | (input[sic].between(5120,5122)) | (input[sic].between(5130,5139)) | (input[sic].between(5140,5149)) | (input[sic].between(5150,5159)) | (input[sic].between(5160,5169)) | (input[sic].between(5170,5172)) | (input[sic].between(5180,5182)) | (input[sic].between(5190,5199)), description] = 'Whlsl  Wholesale'
    input.loc[(input[sic].between(5200,5200)) | (input[sic].between(5210,5219)) | (input[sic].between(5220,5229)) | (input[sic].between(5230,5231)) | (input[sic].between(5250,5251)) | (input[sic].between(5260,5261)) | (input[sic].between(5270,5271)) | (input[sic].between(5300,5300)) | (input[sic].between(5310,5311)) | (input[sic].between(5320,5320)) | (input[sic].between(5330,5331)) | (input[sic].between(5334,5334)) | (input[sic].between(5340,5349)) | (input[sic].between(5390,5399)) | (input[sic].between(5400,5400)) | (input[sic].between(5410,5411)) | (input[sic].between(5412,5412)) | (input[sic].between(5420,5429)) | (input[sic].between(5430,5439)) | (input[sic].between(5440,5449)) | (input[sic].between(5450,5459)) | (input[sic].between(5460,5469)) | (input[sic].between(5490,5499)) | (input[sic].between(5500,5500)) | (input[sic].between(5510,5529)) | (input[sic].between(5530,5539)) | (input[sic].between(5540,5549)) | (input[sic].between(5550,5559)) | (input[sic].between(5560,5569)) | (input[sic].between(5570,5579)) | (input[sic].between(5590,5599)) | (input[sic].between(5600,5699)) | (input[sic].between(5700,5700)) | (input[sic].between(5710,5719)) | (input[sic].between(5720,5722)) | (input[sic].between(5730,5733)) | (input[sic].between(5734,5734)) | (input[sic].between(5735,5735)) | (input[sic].between(5736,5736)) | (input[sic].between(5750,5799)) | (input[sic].between(5900,5900)) | (input[sic].between(5910,5912)) | (input[sic].between(5920,5929)) | (input[sic].between(5930,5932)) | (input[sic].between(5940,5940)) | (input[sic].between(5941,5941)) | (input[sic].between(5942,5942)) | (input[sic].between(5943,5943)) | (input[sic].between(5944,5944)) | (input[sic].between(5945,5945)) | (input[sic].between(5946,5946)) | (input[sic].between(5947,5947)) | (input[sic].between(5948,5948)) | (input[sic].between(5949,5949)) | (input[sic].between(5950,5959)) | (input[sic].between(5960,5969)) | (input[sic].between(5970,5979)) | (input[sic].between(5980,5989)) | (input[sic].between(5990,5990)) | (input[sic].between(5992,5992)) | (input[sic].between(5993,5993)) | (input[sic].between(5994,5994)) | (input[sic].between(5995,5995)) | (input[sic].between(5999,5999)), code] = 42
    if(description!=None):
        input.loc[(input[sic].between(5200,5200)) | (input[sic].between(5210,5219)) | (input[sic].between(5220,5229)) | (input[sic].between(5230,5231)) | (input[sic].between(5250,5251)) | (input[sic].between(5260,5261)) | (input[sic].between(5270,5271)) | (input[sic].between(5300,5300)) | (input[sic].between(5310,5311)) | (input[sic].between(5320,5320)) | (input[sic].between(5330,5331)) | (input[sic].between(5334,5334)) | (input[sic].between(5340,5349)) | (input[sic].between(5390,5399)) | (input[sic].between(5400,5400)) | (input[sic].between(5410,5411)) | (input[sic].between(5412,5412)) | (input[sic].between(5420,5429)) | (input[sic].between(5430,5439)) | (input[sic].between(5440,5449)) | (input[sic].between(5450,5459)) | (input[sic].between(5460,5469)) | (input[sic].between(5490,5499)) | (input[sic].between(5500,5500)) | (input[sic].between(5510,5529)) | (input[sic].between(5530,5539)) | (input[sic].between(5540,5549)) | (input[sic].between(5550,5559)) | (input[sic].between(5560,5569)) | (input[sic].between(5570,5579)) | (input[sic].between(5590,5599)) | (input[sic].between(5600,5699)) | (input[sic].between(5700,5700)) | (input[sic].between(5710,5719)) | (input[sic].between(5720,5722)) | (input[sic].between(5730,5733)) | (input[sic].between(5734,5734)) | (input[sic].between(5735,5735)) | (input[sic].between(5736,5736)) | (input[sic].between(5750,5799)) | (input[sic].between(5900,5900)) | (input[sic].between(5910,5912)) | (input[sic].between(5920,5929)) | (input[sic].between(5930,5932)) | (input[sic].between(5940,5940)) | (input[sic].between(5941,5941)) | (input[sic].between(5942,5942)) | (input[sic].between(5943,5943)) | (input[sic].between(5944,5944)) | (input[sic].between(5945,5945)) | (input[sic].between(5946,5946)) | (input[sic].between(5947,5947)) | (input[sic].between(5948,5948)) | (input[sic].between(5949,5949)) | (input[sic].between(5950,5959)) | (input[sic].between(5960,5969)) | (input[sic].between(5970,5979)) | (input[sic].between(5980,5989)) | (input[sic].between(5990,5990)) | (input[sic].between(5992,5992)) | (input[sic].between(5993,5993)) | (input[sic].between(5994,5994)) | (input[sic].between(5995,5995)) | (input[sic].between(5999,5999)), description] = 'Rtail  Retail'
    input.loc[(input[sic].between(5800,5819)) | (input[sic].between(5820,5829)) | (input[sic].between(5890,5899)) | (input[sic].between(7000,7000)) | (input[sic].between(7010,7019)) | (input[sic].between(7040,7049)) | (input[sic].between(7213,7213)), code] = 43
    if(description!=None):
        input.loc[(input[sic].between(5800,5819)) | (input[sic].between(5820,5829)) | (input[sic].between(5890,5899)) | (input[sic].between(7000,7000)) | (input[sic].between(7010,7019)) | (input[sic].between(7040,7049)) | (input[sic].between(7213,7213)), description] = 'Meals  Restaurants, Hotels, Motels'
    input.loc[(input[sic].between(6000,6000)) | (input[sic].between(6010,6019)) | (input[sic].between(6020,6020)) | (input[sic].between(6021,6021)) | (input[sic].between(6022,6022)) | (input[sic].between(6023,6024)) | (input[sic].between(6025,6025)) | (input[sic].between(6026,6026)) | (input[sic].between(6027,6027)) | (input[sic].between(6028,6029)) | (input[sic].between(6030,6036)) | (input[sic].between(6040,6059)) | (input[sic].between(6060,6062)) | (input[sic].between(6080,6082)) | (input[sic].between(6090,6099)) | (input[sic].between(6100,6100)) | (input[sic].between(6110,6111)) | (input[sic].between(6112,6113)) | (input[sic].between(6120,6129)) | (input[sic].between(6130,6139)) | (input[sic].between(6140,6149)) | (input[sic].between(6150,6159)) | (input[sic].between(6160,6169)) | (input[sic].between(6170,6179)) | (input[sic].between(6190,6199)), code] = 44
    if(description!=None):
        input.loc[(input[sic].between(6000,6000)) | (input[sic].between(6010,6019)) | (input[sic].between(6020,6020)) | (input[sic].between(6021,6021)) | (input[sic].between(6022,6022)) | (input[sic].between(6023,6024)) | (input[sic].between(6025,6025)) | (input[sic].between(6026,6026)) | (input[sic].between(6027,6027)) | (input[sic].between(6028,6029)) | (input[sic].between(6030,6036)) | (input[sic].between(6040,6059)) | (input[sic].between(6060,6062)) | (input[sic].between(6080,6082)) | (input[sic].between(6090,6099)) | (input[sic].between(6100,6100)) | (input[sic].between(6110,6111)) | (input[sic].between(6112,6113)) | (input[sic].between(6120,6129)) | (input[sic].between(6130,6139)) | (input[sic].between(6140,6149)) | (input[sic].between(6150,6159)) | (input[sic].between(6160,6169)) | (input[sic].between(6170,6179)) | (input[sic].between(6190,6199)), description] = 'Banks  Banking'
    input.loc[(input[sic].between(6300,6300)) | (input[sic].between(6310,6319)) | (input[sic].between(6320,6329)) | (input[sic].between(6330,6331)) | (input[sic].between(6350,6351)) | (input[sic].between(6360,6361)) | (input[sic].between(6370,6379)) | (input[sic].between(6390,6399)) | (input[sic].between(6400,6411)), code] = 45
    if(description!=None):
        input.loc[(input[sic].between(6300,6300)) | (input[sic].between(6310,6319)) | (input[sic].between(6320,6329)) | (input[sic].between(6330,6331)) | (input[sic].between(6350,6351)) | (input[sic].between(6360,6361)) | (input[sic].between(6370,6379)) | (input[sic].between(6390,6399)) | (input[sic].between(6400,6411)), description] = 'Insur  Insurance'
    input.loc[(input[sic].between(6500,6500)) | (input[sic].between(6510,6510)) | (input[sic].between(6512,6512)) | (input[sic].between(6513,6513)) | (input[sic].between(6514,6514)) | (input[sic].between(6515,6515)) | (input[sic].between(6517,6519)) | (input[sic].between(6520,6529)) | (input[sic].between(6530,6531)) | (input[sic].between(6532,6532)) | (input[sic].between(6540,6541)) | (input[sic].between(6550,6553)) | (input[sic].between(6590,6599)) | (input[sic].between(6610,6611)), code] = 46
    if(description!=None):
        input.loc[(input[sic].between(6500,6500)) | (input[sic].between(6510,6510)) | (input[sic].between(6512,6512)) | (input[sic].between(6513,6513)) | (input[sic].between(6514,6514)) | (input[sic].between(6515,6515)) | (input[sic].between(6517,6519)) | (input[sic].between(6520,6529)) | (input[sic].between(6530,6531)) | (input[sic].between(6532,6532)) | (input[sic].between(6540,6541)) | (input[sic].between(6550,6553)) | (input[sic].between(6590,6599)) | (input[sic].between(6610,6611)), description] = 'RlEst  Real Estate'
    input.loc[(input[sic].between(6200,6299)) | (input[sic].between(6700,6700)) | (input[sic].between(6710,6719)) | (input[sic].between(6720,6722)) | (input[sic].between(6723,6723)) | (input[sic].between(6724,6724)) | (input[sic].between(6725,6725)) | (input[sic].between(6726,6726)) | (input[sic].between(6730,6733)) | (input[sic].between(6740,6779)) | (input[sic].between(6790,6791)) | (input[sic].between(6792,6792)) | (input[sic].between(6793,6793)) | (input[sic].between(6794,6794)) | (input[sic].between(6795,6795)) | (input[sic].between(6798,6798)) | (input[sic].between(6799,6799)), code] = 47
    if(description!=None):
        input.loc[(input[sic].between(6200,6299)) | (input[sic].between(6700,6700)) | (input[sic].between(6710,6719)) | (input[sic].between(6720,6722)) | (input[sic].between(6723,6723)) | (input[sic].between(6724,6724)) | (input[sic].between(6725,6725)) | (input[sic].between(6726,6726)) | (input[sic].between(6730,6733)) | (input[sic].between(6740,6779)) | (input[sic].between(6790,6791)) | (input[sic].between(6792,6792)) | (input[sic].between(6793,6793)) | (input[sic].between(6794,6794)) | (input[sic].between(6795,6795)) | (input[sic].between(6798,6798)) | (input[sic].between(6799,6799)), description] = 'Fin    Trading'
    input.loc[(input[sic].notnull()) & (input[code].isnull()), code] = 48
    if(description!=None):
        input.loc[(input[sic].notnull()) & (input[code].isnull()), description] = 'Other  Almost Nothing'
    return input



def show_sas_columns(file_path: str, keys: list = None, charset:str = 'utf-8'): 
    '''
    Show the information for SAS file columns.

    Parameters
    ----------
    file_path : str
        SAS file path.
    keys : list, optional
        The list of column names. If None, all columns' information will be returned. The default is None.
    charset : str, optional
        The charset of the SAS file. The default is 'utf-8'.


    '''
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(read_sas(file_path, keys = keys, chunksize = 1, charset = charset, batch = 0, progress=False).dtypes)


def get_sas_columns(file_path: str, keys: list = None, charset:str = 'utf-8'): 
    '''
    Get the information for SAS file columns.

    Parameters
    ----------
    file_path : str
        SAS file path.
    keys : list, optional
        The list of column names. If None, all columns' information will be returned. The default is None.
    charset : str, optional
        The charset of the SAS file. The default is 'utf-8'.

    Returns
    -------
    TYPE
        The names and types of columns specified by 'keys'.

    '''
    return read_sas(file_path, keys = keys, chunksize = 1, charset = charset, batch = 0, progress=False).dtypes

def read_sas(file_path: str, keys: list = None, chunksize:int = 10000, charset:str = 'utf-8', batch:int = None, progress:bool = True):
    '''
    Read sas file into a data frame.    

    Parameters
    ----------
    file_path : str
        SAS file path.
    keys : list, optional
        The list of column names. If None, all columns' information will be returned. The default is None.
    chunksize : int, optional
        The number of rows read each time. Lowering this value may solve the out of memory problem while loading SAS dataset. The default is 10000.
    charset : str, optional
        The charset of the SAS file. The default is 'utf-8'.
    batch : int, optional
        The number of times of reading the database by 'chunksize' rows. If it is None, all file will be read. The default is None.
    progress : bool, optional
        Whether shows the loading progress. The default is True.

    Returns
    -------
    Read dataframe.

    '''    
    
    keys = list(set(keys))
    
    data = pd.DataFrame()
    for df in pd.read_sas(file_path, chunksize=chunksize):
        if(keys==None):
            data = data.append(df)
        else:
            data = data.append(df[keys])
        if(progress):
            print('.', sep=' ', end='', flush=True)
        if(batch!=None):
            if(batch>0):
                batch-=1
            else:
                break
    for c in data.select_dtypes(include=['object']).columns:
        data[c] = data[c].str.decode(charset)
    return data

def add_permno(input: pd.DataFrame , ccmxpf_lnkhist: pd.DataFrame ):
    '''
    Add PERMNO column to CompuStat dataset. 
    

    Parameters
    ----------
    input : pd.DataFrame
        CompuStat dataset. It must contain 'gvkey' and 'datadate' columns.
    ccmxpf_lnkhist : pd.DataFrame
        ccmxpf_lnkhist dataset from CRSP.

    Returns
    -------
    input : TYPE
        CompuStat dataset with PERMNO column.

    '''   
    
        
    link = ccmxpf_lnkhist[ccmxpf_lnkhist.LINKTYPE.isin(["LC","LS","LU"]) & ccmxpf_lnkhist.LINKPRIM.isin(['P','C'])]
    input = sqldf("select distinct input.*, link.LPERMNO as PERMNO from input, link where input.gvkey=link.gvkey and (input.datadate>=link.LINKDT or link.LINKDT==NULL) and (input.datadate<=link.LINKENDDT or link.LINKENDDT==NULL);", locals())
    return input


def get_comp(input: pd.DataFrame):
    '''
    Filter Original CompuStat dataset as WRDS default.

    Parameters
    ----------
    input : pd.DataFrame
        Compustat dataset. It must contains 'datafmt', 'indfmt', 'consol', and 'popsrc' columns.

    Returns
    -------
    TYPE
        Filtered Compustat dataset.

    '''
    
    
    return input[(input['datafmt']=='STD') & (input['indfmt']=='INDL') & (input['consol']=='C') & (input['popsrc']=='D')]

def remove_na_sic(input: pd.DataFrame, sic_field: str):
    '''
    Remove all observations without SIC

    Parameters
    ----------
    input : pd.DataFrame
        Input dataset.
    sic_field : str
        SIC column name.

    Returns
    -------
    TYPE
        Dataset withou any observations without SIC.

    '''
    
    
    
    return input[(input[sic_field]>=1) & (input[sic_field]<=9999)]
    
def remove_sic_between(input: pd.DataFrame, sic_field, sic_from, sic_to):
    '''
    Remove observations with SIC between 'sic_from' and 'sic_to'

    Parameters
    ----------
    input : pd.DataFrame
        Input dataset.
    sic_field : str
        SIC column name.
    sic_from : TYPE
        The starting SIC code, inclusive.
    sic_to : TYPE
        The ending SIC code, inclusive.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    
    return input[~((input[sic_field]>=sic_from) & (input[sic_field]<=sic_to))]

def winsorize(data: pd.DataFrame, truncated:bool = False, columns:list = [], limits:float = 0.01, nan_policy = 'propagate'):
    '''
    Winsorize columns.

    Parameters
    ----------
    data : pd.DataFrame
        Input dataset.
    truncated : bool, optional
        Whether the columns will be truncated. The default is False.
    columns : List, optional
        List of the names of columns to be winsorized. The default is [].
    limits : float, optional
        Winsorization limit. The default is 0.01.
    nan_policy{‘propagate’, ‘raise’, ‘omit’}, optional
        Defines how to handle when input contains nan. The following options are available (default is ‘propagate’):
            ‘propagate’: allows nan values and may overwrite or propagate them
            ‘raise’: throws an error
            ‘omit’: performs the calculations ignoring nan values
    Returns
    -------
    data : TYPE
        Winsorized dataset.

    '''
    
    for col in columns: 
         data[col] = stats.mstats.winsorize(data[col], limits=limits, inclusive = (truncated, truncated), nan_policy = nan_policy)
    return data

class Sample:
    
    
    
    def __init__(self):
        self.sample = pd.DataFrame(columns=['','Observations'])
    def add(self, data: pd.DataFrame, description: str):
        self.sample.loc[len(self.sample)] = [description, data.shape[0]]
    def save(self, path='data/sample.pkl'):
        self.sample.to_pickle(path)
    def load(self, path='data/sample.pkl'):
        self.sample = pd.read_pickle(path)
    def get(self):
        return self.sample
    def print(self):
        display(Markdown(self.sample.sample.to_markdown(index=False)))    
        
        
        
        
    
    
class GroupByTimeSeris:
    def __init__(self, data: pd.DataFrame, idkey:str, xkeys: list, ykeys: list, timestep:int, xtype =  tf.dtypes.float32, ytype =  tf.dtypes.float32, xscaler =  StandardScaler(), yscaler =  StandardScaler(), labelkey:str = 'label', train_label:str = 'train', valid_label:str = 'valid', test_label:str = 'test', balancekey:str = None, resample_key = None):
        self.keys = [idkey, labelkey] + xkeys + ykeys
        self.balancekey = balancekey
        self.xtype = xtype
        self.ytype = ytype
        if(self.balancekey!=None):
            self.keys+=[self.balancekey]
        self.data = data[self.keys].copy().reset_index(drop=True)
        self.idkey = idkey
        self.xkeys = xkeys
        self.ykeys = ykeys 
        self.xscaler = xscaler 
        self.yscaler = yscaler 
        self.labelkey = labelkey 
        self.train_label = train_label
        self.valid_label = valid_label
        self.test_label = test_label
        self.timestep = timestep
        #self.resample_keys = resample_keys
        if(self.xscaler!=None):
            xscaler.fit(self.data.loc[self.data[labelkey]==self.train_label, self.xkeys])
            self.data[self.xkeys] = xscaler.transform(self.data[self.xkeys])
        if(self.yscaler!=None):
            yscaler.fit(self.data.loc[self.data[labelkey]==self.train_label, self.ykeys])
            self.data[self.ykeys] = yscaler.transform(self.data[self.ykeys]) 
        self.group = self.data.groupby(idkey)
        self.set_resample_key(resample_key)
    
    def set_resample_key(self, resample_key:str):
        if(resample_key in self.data.columns):
            self.resample_key = resample_key
            self.resample_counts = self.data.groupby(resample_key)[resample_key].count()
        else:
            self.resample_key = None
        
    def _generator(self, label:str, resample_value = None):
        
        label = label.decode()
        for name, group in self.group:
            c = group.reset_index(drop=True)
            for i in range(self.timestep-1, c.shape[0]): 
                label_i = c.loc[i,self.labelkey]  
                print(c.loc[i])
                if(self.resample_key != None):
                    sample = c.loc[i,self.resample_key] == resample_value
                else:
                    sample = True
                if((label==label_i) & sample): 
                    x = c[i-self.timestep+1:i+1][self.xkeys].to_numpy()
                    y = c.loc[i,self.ykeys].to_numpy()
                    if((not pd.isnull(x).any()) & (not pd.isnull(y).any()) ):
                        yield x, y
    
    def make_dataset(self, type):
        if(self.resample_key==None):
            return tf.data.Dataset.from_generator(
                self._generator,
                output_types=(self.xtype, self.ytype),
                output_shapes=(tf.TensorShape([self.timestep, len(self.xkeys)]), tf.TensorShape([len(self.ykeys),])),
                args=(type,) 
            )
        else:
            mode = self.resample_counts.idxmax() 
            output = []
            for i in self.resample_counts.index:
                output.append(tf.data.Dataset.from_generator(
                    self._generator,
                    output_types=(self.xtype, self.ytype),
                    output_shapes=(tf.TensorShape([self.timestep, len(self.xkeys)]), tf.TensorShape([len(self.ykeys),])),
                    args=(type, i) 
                ))
            return tf.data.experimental.sample_from_datasets(output)
                
    
    @property
    def train(self):
      return self.make_dataset(self.train_label)

    @property
    def val(self):
      return self.make_dataset(self.valid_label)

    @property
    def test(self):
      return self.make_dataset(self.test_label)
