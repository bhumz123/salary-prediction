import streamlit as st 
import pickle
import numpy as np
import pandas as pd

def load_model():
    
    with open('saved_steps.pkl', 'rb') as file:
        data=pickle.load(file)
    return data
data=load_model()


dec_tree_reg_loaded=data["model"]
le_country=data["le_country"]
le_education=data["le_education"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict your salary!""")

    countries=(
        "United States of America",                               
"Germany",                  
"United Kingdom of Great Britain and Northern Ireland",  
"India",                                                   
"Canada",                                                  
"France",                                                  
"Brazil",                                                  
"Spain",                                               
"Netherlands",                                              
"Australia",                                                
"Italy",                                                    
"Poland",                                                   
"Sweden",                                                  
 "Russian Federation" ,                                      
"Switzerland",                                              
"Turkey ",                                                  
"Israel"  ,                                                 
"Austria"         
    )

    education=(
        'Master’s degree', 'Bachelor’s degree', 'Less than a Bachelors',
       'Professional degree'
    )

    countries=st.selectbox("Select your Country", countries)
    education=st.selectbox("Select Your Education Level", education)
    
    codeyear= st.slider("Years of Coding",0,40,1)  

    experience= st.slider("Years of Experience",0,50,2) 

    ok=st.button("Calculate your Salary")
    if ok:
        x=np.array([[countries,education,codeyear,experience]])
        x[:,0]=le_country.transform(x[:,0])
        x[:,1]=le_education.transform(x[:,1])
        x=x.astype(float)

        salary=dec_tree_reg_loaded.predict(x)
        st.subheader(f"The estimated salary is:  ${salary[0]:.2f}")

    



