import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import OrderedDict
from pprint import pprint
import pylab 
import scipy.stats as stats
from scipy.stats.stats import pearsonr

rename_demographic = OrderedDict([('q99','age'), ('gender','gender'),('q1110','race'), 
                      ('q102','househd_size'),('q103','num_child'),('q104','num_elder'),
                      ('q105','owner'),('q106','pets'),('q112','income'),('q113','edu')])
rename_house = OrderedDict([('q94','house_type'), ('q95','house_material')])
rename_loc = {'state':'state', 'samp':'county', 'city':'city', 'zip':'zip'}
rename_official = {"q43":"heard_order", 'q44':'order_type'}
rename_official_save = {"q43":"heard_order", 'q44':'order_type', 'q45':'door_to_door', 'q46':'order_first_src', 
                   'q47':'early_enough', 'q48':'clear_enough', "q49":"responsible"}
rename_info_src = OrderedDict([("q50a","src_local_radio"), ("q50b","src_local_tv"), 
            ("q50c","src_cable_cnn"), ("q50d","src_cable_weather_channel"), ("q50e","src_cable_other"),
            ("q50f","src_internet"), ("q50g","src_mouth")])
rename_src_importance = OrderedDict([("q58","importance_nhc"), ("q59","importance_local_media"), 
                         ("q60","trust_local_media"),('q61','seek_local_weather_office'), ('q62','see_track_map')])
rename_concern = OrderedDict([('q54','concern_wind'), ('q55','concern_fld_surge'), 
                              ('q56','concern_fld_rainfall'), ('q57','concern_tornado')])
rename_scenario = OrderedDict([('q65','sf_cat4_water'), ('q66','sf_cat4_wind_water'),
                   ('q67','sf_cat3_water'), ('q68','sf_cat3_wind_water'),
                   ('q69','sf_cat2_water'), ('q70','sf_cat2_wind_water')])
rename_evac = {'q2':'evac'}

map_info_src = {'none':0, 'a little':1, 'a fair amount':2, 'a great deal':3}
map_importance = {'not important':0, 'somewhat important':1, 'very important':2}

def one_var_plot():
    df = pd.read_csv(os.path.join('data', 'IvanExport.csv'))
    rename_all = {}
    rename_all.update(rename_demographic)
    rename_all.update(rename_house)
    rename_all.update(rename_official)
    df.rename(columns=rename_all, inplace=True)
    
#     # numerical var, use histogram
#     var = 'num_child'
#     df.hist(column=var)
#     plt.show()
    
    # categorical var, use bar plot
    var = 'income'
    print df[var].unique()
    df1 = df[var].value_counts(dropna=False)
    #df1 = df.groupby(var).size()
    print df1
    df1.plot(kind='bar', rot=0)
    plt.show()
    
    # Q-Q plot
#     df1 = df['age'].dropna()
#     stats.probplot(df1, dist="norm", plot=pylab)
#     pylab.show()
    
    
def two_var_bar_plot():
    df = pd.read_csv(os.path.join('data', 'IvanExport.csv'))
    
    rename_all = {}
    rename_all.update(rename_demographic)
    rename_all.update(rename_loc)
    rename_all.update(rename_official)
    df.rename(columns=rename_all, inplace=True)


    row_var  = 'county'
    col_var = 'heard_order'

    df1 = df.groupby([row_var, col_var]).size()
    #print df1
    #print df1.shape
    rows = df1.index.get_level_values(row_var).unique().values
    cols = df1.index.get_level_values(col_var).unique()
#     
#     print cols
#     print df[col_var].unique()
    
    vals = df1.values.reshape(len(rows),len(cols))
    df2 = pd.DataFrame(vals, rows, cols)
    df2.plot(kind='bar', rot=-90)
    plt.show()

def corr():
    df = pd.read_csv('Ivan_basic.csv')
    v1 = 'heard_order'
    v2 = 'evac'
    df1 = df[[v1, v2]]
    #print df1
    df1.fillna(0, inplace=True)
    #df1[v1].replace({0:0, 1:1,2:1,3:1,4:1,5:1,6:1,7:1},inplace=True)
    print df1[v1].unique()
    print df1.corr('pearson')
    print pearsonr(df1[v1],df1[v2])
    
################################################
# convert categorical var to dummy vars, fill in missing values
def prep():
    df = pd.read_csv(os.path.join('data', 'IvanExport.csv'))
    
    rename_all = OrderedDict()
    rename_all.update(rename_demographic)
    rename_all.update(rename_house)
    rename_all.update(rename_official)
    rename_all.update(rename_info_src)
    rename_all.update(rename_src_importance)
    rename_all.update(rename_concern)
    rename_all.update(rename_scenario)
    rename_all.update(rename_evac)

    cols = rename_all.values()
    df.rename(columns=rename_all, inplace=True)
    #pprint(cols)
    
#     for col in cols:
#         var = col
#         print '----------------------'
#         print var
#         print df[var].unique()
#         print df[var].value_counts(dropna=False)
    #print df
    
    df['gender'].replace({"male":0, "female":1}, inplace=True)
    df['race'].fillna(0, inplace=True)
    df['race'].replace({"white or caucasian":1, "african american or black":2, "hispanic":3, "american indian":4, "asian":5, "other":0}, inplace=True)
    df_race = pd.get_dummies(df['race'], drop_first=True)
    df_race.rename(columns={1:'r_white', 2:'r_black', 3:'r_hispanic', 4:'r_asian', 5:'r_native'}, inplace=True)
    df['owner'].replace({"own":1, "rent":0, 'other':0}, inplace=True)
    df['pets'].fillna(0, inplace=True)
    df['pets'].replace({'yes':1, "no [skip to q108]":0}, inplace=True)
    df['income'].replace({'less than $15,000':1, '$15,000 to $24,999':2, '$25,000 to $39,999':3, '$40,000 to $79,999':4, 'over $80,000':5}, inplace=True)
    df['edu'].fillna(0, inplace=True)
    df['edu'].replace({'some high school':1, 'high school graduate':2, 'some college':3, 'college graduate':4, 'post graduate':5}, inplace=True)
    df['house_type'].fillna(0, inplace=True)
    df['house_type'].replace({'detached single family home? [go to q95]':1, 'mobile home [skip to q96]':2, 
                              'duplex, triplex, quadraplex home? [skip to q99]':3, 'multi-fam bldg 4 stories or less? [apt/condo] [skip to q99]':3,
                              'multi-fam bldg more than 4 stories [apt/condo] [skip to q99]':3, 'manufactured home [skip to q96]':0,
                              'some other type of structure [skip to q99]':0}, inplace=True)
    df_house_type = pd.get_dummies(df['house_type'], drop_first=True)
    df_house_type.rename(columns={1:'ht_single_fam', 2:'ht_mobile', 3:'ht_condo'}, inplace=True)
    df['house_material'].fillna(0, inplace=True)
    df['house_material'].replace({'wood':1, 'brick':2, 'cement block':3, 'other [specify]':0}, inplace=True)
    df_house_materi = pd.get_dummies(df['house_material'], drop_first=True)
    df_house_materi.rename(columns={1:'hm_wood', 2:'hm_brick', 3:'hm_cement'}, inplace=True)
    
    df['heard_order'].replace({'yes [go to q44]':1, 'no [go to q49]':0}, inplace=True)

    #print df['heard_order'].value_counts(dropna=False)
    df['src_local_radio'].replace(map_info_src, inplace=True)
    df['src_local_tv'].replace(map_info_src, inplace=True)
    df['src_cable_cnn'].replace(map_info_src, inplace=True)
    df['src_cable_weather_channel'].replace(map_info_src, inplace=True)
    df['src_cable_other'].replace(map_info_src, inplace=True)
    df['src_internet'].replace(map_info_src, inplace=True)
    #df['src_mouth'] raw data was coded differently

    df['importance_nhc'].replace(map_importance, inplace=True)
    df['importance_local_media'].replace(map_importance, inplace=True)
    df['trust_local_media'].replace({'yes':1, 'no':0},inplace=True)
    df['seek_local_weather_office'].replace({'yes':1, 'no':0},inplace=True)
    df['see_track_map'].replace({'yes':1, 'no [skip to q65]':0},inplace=True)
    
    df['concern_wind'].replace(map_importance, inplace=True)
    df['concern_fld_surge'].replace(map_importance, inplace=True)
    df['concern_fld_rainfall'].replace(map_importance, inplace=True)
    df['concern_tornado'].replace(map_importance, inplace=True)
    
    # the question is actually about threat, therefore reverse yes no
    df['sf_cat4_water'].replace({'yes':0, 'no':1},inplace=True)
    df['sf_cat3_water'].replace({'yes':0, 'no':1},inplace=True)
    df['sf_cat2_water'].replace({'yes':0, 'no':1},inplace=True)
    df['sf_cat4_wind_water'].replace({'yes':1, 'no':0}, inplace=True)
    df['sf_cat3_wind_water'].replace({'yes':1, 'no':0}, inplace=True)
    df['sf_cat2_wind_water'].replace({'yes':1, 'no':0}, inplace=True)
    
    df['evac'].replace({'yes, evacuated':1,'no, did not evacuate':0}, inplace=True)
    
    df = pd.concat([df, df_race, df_house_type, df_house_materi], axis=1)
    
    ##################################################
    # age, fill in using normal distribution 
    # num_child, num_elder, set to 0 if househd_size=1
#     c1 = df['age'].dropna()
#     mu = np.mean(c1)
#     sigma = np.sqrt(np.var(c1))
#     np.random.seed(1)
#     samples_age = np.random.normal(mu, sigma, 141)
    #print s
#     plt.hist(s)
#     plt.show()
    #print df['age']
    j = 0
    for i, row in df.iterrows():
#         if pd.isnull(row['age']):
#             df.set_value(i, 'age', int(samples_age[j]))
#             j += 1

        if row['househd_size'] == 1:
            df.set_value(i, 'num_child', 0)
            df.set_value(i, 'num_elder', 0)
            
        #if row['heard_order'] == 1 and 

    ##################################################
    # income, 
 
    cols = ['age', 'gender','r_white', 'r_black', 'r_hispanic', 'r_asian', 'r_native',
            'househd_size', 'num_child', 'num_elder', 
            'income','edu','owner','pets',
            'ht_single_fam', 'ht_mobile', 'ht_condo',
            'hm_wood', 'hm_brick', 'hm_cement',
            'heard_order', 
            'src_local_radio', 'src_local_tv', 'src_cable_cnn', 'src_cable_weather_channel', 'src_cable_other', 'src_internet',
            'importance_nhc', 'importance_local_media', 'trust_local_media', 'seek_local_weather_office', 'see_track_map',
            'concern_wind', 'concern_fld_surge', 'concern_fld_rainfall', 'concern_tornado',
            'sf_cat4_water','sf_cat4_wind_water','sf_cat3_water','sf_cat3_wind_water','sf_cat2_water','sf_cat2_wind_water',
            'evac']

    df1 = df[cols].dropna()
    print len(df1)
    
    df1.to_csv('Ivan_basic.csv', columns=cols, index=False)
    #df1.to_csv('Ivan_all_common.csv', columns=cols, index=False)
    


    
if __name__ == '__main__':
    

    #one_var_plot()
    #corr()
    #prep()
    two_var_bar_plot()

    
