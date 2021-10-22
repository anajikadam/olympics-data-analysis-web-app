import pandas as pd

IMG_URL = 'https://stillmed.olympics.com/media/Images/OlympicOrg/IOC/The_Organisation/The-Olympic-Rings/Olympic_rings_TM_c_IOC_All_rights_reserved_1.jpg'


df = pd.read_csv('Data/athlete_events.csv')
region_df = pd.read_csv('Data/noc_regions.csv')

# df = pd.read_csv("https://raw.githubusercontent.com/anajikadam/MyRowData/main/olympics-data/athlete_events.csv")
# region_df = pd.read_csv("https://raw.githubusercontent.com/anajikadam/MyRowData/main/olympics-data/noc_regions.csv")

def preprocess(df,region_df):
    # filtering for summer olympics
    df = df[df['Season'] == 'Summer']
    # merge with region_df
    df = df.merge(region_df, on='NOC', how='left')
    # dropping duplicates
    df.drop_duplicates(inplace=True)
    # one hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df