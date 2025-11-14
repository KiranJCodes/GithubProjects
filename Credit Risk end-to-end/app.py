#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 05:17:11 2025

@author: daydreamer
"""

import streamlit as st
import pandas as pd
import joblib

model = joblib.load('XGB_Classifier_model.pkl')

encoders = {col: joblib.load(f"{col}_encoder.pkl")for col in ['Sex','Housing','Saving accounts',
            'Checking account']}
st.markdown("<h1 style='text-align: center;'>Credit Risk Predictor</h1>", unsafe_allow_html=True)

st.write("Enter Apllication information to proceed")

age = st.number_input("Age",min_value=18,max_value=80,value=30)
sex = st.selectbox("Sex",['male','female'])
job = st.number_input("Job (0-3)",min_value=0,max_value=3,value=1)
housing = st.selectbox('Housing',['own','rent','free'])
savings = st.selectbox('Savings', ['little','moderate','quite rich','rich'])
checking = st.selectbox('Checking',['little','moderate','rich'])
credit = st.number_input('Credit amount',min_value=0,value=100)
duration = st.number_input("Duration (months)",min_value=1,value=12)

inputdf = pd.DataFrame(
    {
     "Age": [age],
     "Sex": [encoders['Sex'].transform([sex])[0]],
     "Job": [job],
     "Housing": [encoders['Housing'].transform([housing])[0]],
     "Saving accounts": [encoders['Saving accounts'].transform([savings])[0]],
     "Checking account": [encoders['Checking account'].transform([checking])[0]],
     "Credit amount": [credit],
     "Duration": [duration],
     })



if st.button("Check risk"):
    pred = model.predict(inputdf)[0]
    
    if pred == 1:
        st.markdown("""
            <div style="text-align: center; padding: 20px; background-color: #d4edda; border-radius: 10px;">
                <h1 style="color: #155724;">✅ GOOD RISK</h1>
                <p style="font-size: 50px;">👍</p>
                <p style="color:Black;">Low risk customer - Approval recommended</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background-color: #f8d7da; border-radius: 10px;">
            <h1 style="color: #721c24;">🚨 BAD RISK</h1>
            <p style="font-size: 50px;">👎</p>
            <p style="color:Black;">High risk customer - Further review needed</p>
        </div>
        """, unsafe_allow_html=True)