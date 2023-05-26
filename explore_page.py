import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories,cutoff):
    categorical_map={}
    for i in range(len(categories)):
        if categories.values[i]>= cutoff:
            categorical_map[categories.index[i]]=categories.index[i]
        else:
            
            categorical_map[categories.index[i]]='Other'
    return categorical_map



def clean(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def cleaner(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x:
        return 'Professional degree'
    return 'Less than a Bachelors'

@st.cache_data
def load_data():
    df=pd.read_csv("survey_results_public.csv")
    df=df[['Country','EdLevel','YearsCodePro','YearsCode','Employment','ConvertedCompYearly']]
    df = df.rename({"ConvertedCompYearly":"Salary"},axis=1)
    
    df=df[df["Salary"].notnull()]
    df=df.dropna()
    df.isnull().sum()
    df = df[df["Employment"]=="Employed, full-time"]
    df=df.drop("Employment",axis=1)
    country_map=shorten_categories(df.Country.value_counts(),300)
    df['Country']=df['Country'].map(country_map)
    df=df[df['Salary']<=250000]
    df=df[df['Salary']>=10000]
    df=df[df['Country']!= 'Other']
    df['YearsCodePro']=df['YearsCodePro'].apply(clean)
    df['YearsCode']=df['YearsCode'].apply(cleaner)
    df['EdLevel']=df['EdLevel'].apply(education)
    return df
df=load_data()

def show_explore():
    st.title(" Explore Software Engineer Salaries")

    st.header("""### Stack Overflow Developer survey 2022""")



    st.write("""### Mean Salary Based On Country""")
    data=df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)