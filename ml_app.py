import streamlit as st
import numpy as np
import joblib
import os

#encoding manual (tanpa menggunakan label encoder)
dep = {
    'Sales & Marketing' :1, 'Operations' :2, 'Technology' :3, 'Analytics' :4,
    'R&D' :5, 'Procurement': 6, 'Finance' :7, 'HR' :8, 'Legal' :9}
edu = {
'Below Secondary' :1, "Bachelor's" :2, "Master's & above":3}
rec = {
    'referred' :1, 'sourcing':2, 'others':3}
gen = {
    'm' :1, 'f' :2}
reg = {
    'region_2' :1,'region_22' :2,'region_7' :3,'region_15' :4,'region_13' :5,
'region_26' :6,'region_31' :7,'region_4' :8,'region_27' :9,'region_16' :10,'region_11' :11,'region_28' :12,'region_23' :14,'region_29' :15,
'region_19' :16,'region_20' :17,'region_14' :18,'region_32' :19,'region_17' :20,'region_25' :21,'region_5' :22,'region_10' :23,'region_30' :24,'region_8' :25,
'region_6' :26,'region_1' :27,'region_24' :28,'region_12' :29,'region_21' :30,'region_9' :31,'region_3' :32,'region_33' :33,'region_34' :34,'region_18' :35}

#fungsi bantuan untuk mendapatkan value dari key kolom categorycal
def get_value(val, my_dict):
    for key, value in my_dict.items():
        if val == key:
            return value    

def run_ml_app():
    st.subheader('ML Section')
    department = st.selectbox('Department', ['Sales & Marketing', 'Operations', 'Technology', 'Analytics',
                                             'R&D', 'Procurement', 'Finance', 'HR', 'Legal'])
    region = st.selectbox('Region', ['region_2','region_22','region_7','region_15','region_13',
'region_26','region_31','region_4','region_27','region_16','region_11','region_28','region_23','region_29',
'region_19','region_20','region_14','region_32','region_17','region_25','region_5','region_10','region_30','region_8',
'region_6','region_1','region_24','region_12','region_21','region_9','region_3','region_33','region_34','region_18'])
    education = st.selectbox('Education', ['Below Secondary', "Bachelor's", "Master's & above"])
    gender = st.radio('Gender', ['m','f'])
    recruitment = st.selectbox ("Recruitment Channel", ['referred','sourcing','others'])

    training = st.number_input('No of Training', 1,10)
    age = st.number_input('Age', 10,60)
    rating = st.number_input('Previous Year Rating', 1,5)
    service = st.number_input('Length of Service', 1,37)
    awards = st.radio('Awards Won', [0,1])
    avg_training = st.number_input('Average Training Score', 0,100)

    with st.expander("Your Selected Options"):
        result = {
           'Department' : department ,
           'Region' : region,
           'Education' : education,
           'Gender' : gender,
           'Recruitment Channel' : recruitment,
           'No of Training' : training,
           'Age' : age,
           'Previous Year Rating' : rating,
           'Length of Service' : service,
           'Awards Won' : awards,
           'Average Training Score' : avg_training

        }
        st.write(result)

#dapatkan hasil encoding untuk setiap kolom
        encoded_result = []
        for i in result.values():
            if type(i) == int:
                encoded_result.append(i)
            elif i in ['Sales & Marketing', 'Operations', 'Technology', 'Analytics',
                                             'R&D', 'Procurement', 'Finance', 'HR', 'Legal']:
                res = get_value(i, dep)
                encoded_result.append(res)
            elif i in ['region_2','region_22','region_7','region_15','region_13',
'region_26','region_31','region_4','region_27','region_16','region_11','region_28','region_23','region_29',
'region_19','region_20','region_14','region_32','region_17','region_25','region_5','region_10','region_30','region_8',
'region_6','region_1','region_24','region_12','region_21','region_9','region_3','region_33','region_34','region_18']:
                res = get_value(i, reg)
                encoded_result.append(res)   
            elif i in ['Below Secondary', "Bachelor's", "Master's & above"]:
                res = get_value(i, edu)
                encoded_result.append(res) 
            elif i in ['m','f']:
                res = get_value(i, gen)
                encoded_result.append(res) 
            elif i in ['referred','sourcing','others']:
                res = get_value(i, rec)
                encoded_result.append(res) 
        
    st.write(encoded_result)
    single_array = np.array(encoded_result).reshape(1,-1)

    st.subheader('Prediction result: ')

    model = joblib.load(open(os.path.join('model_grad.pkl'), 'rb'))
    prediction = model.predict(single_array)

    if prediction ==1:
        st.success('Congrats, you get promotion!')
    else:
        st.warning('need to improve')

    