import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
st.set_page_config(layout="wide",page_title="Carbon Footprint Calculator")
st.title("Carbon Footprint Calculator")
st.header("Fossil Fuels")
col1,col2=st.columns(2)
with col1:
    st.subheader("Facility")
    d=st.selectbox("",["Choose Facility","Residential Areas","Hostels","Academic Area","Health Centre","Schools","Visitor's Hostel","Servants Quaters","Shops/Bank/PO"])


    st.subheader("Year")
    d=st.selectbox("",["Choose Year","2024","2023","2022","2021","2020","2019","2018","2017","2016","2015"])


    st.subheader("Month")
    d=st.selectbox("",["Choose Month","January","February","March","April","May","June","July","August","September","November","December"])

with col2:
     st.subheader("Fuel Type")
     d=st.selectbox("",["Choose Fuel Type","CNG","Petrol/Gasoline","Diesel","PNG","LPG"])


     st.subheader("Unit")
     d=st.selectbox("",["Choose Unit","Kg","Tonne"])


     st.subheader("Amount Consumed")
     d=st.number_input("Enter Amount", min_value=1, max_value=10000)





