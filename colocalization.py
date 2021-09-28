import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
from pandas.core.reshape.concat import concat 
import streamlit as st 
import os

name_input = st.text_input("Name of group:")
time_input = st.text_input("Time point associated with this dataset:")
uploaded_file = st.file_uploader("Select .csv file from CellProfiler pipeline:")
uploaded_df = pd.read_csv(uploaded_file, header= 0)

image_name = pd.Series(uploaded_df['FileName_Orig_Tumor'])
tumor_area = pd.Series(uploaded_df['Intensity_TotalArea_MaskVirus_MergedTumor'])
virus_totalintensity = pd.Series(uploaded_df['Intensity_TotalIntensity_MaskVirus_MergedTumor'])
rate = virus_totalintensity / tumor_area
colocalization_rate = rate.rename('TotalIntensity_over_TotalArea')

df = pd.concat([image_name, tumor_area, virus_totalintensity, colocalization_rate], axis= 1)
new_df = df.rename(columns= {'FileName_Orig_Tumor':'Image_Name', 'Intensity_TotalArea_MaskVirus_MergedTumor':'Total_Tumor_Area', 'Intensity_TotalIntensity_MaskVirus_MergedTumor':'Total_Fluorescent_Intensity', 'TotalIntensity_over_TotalArea': "Colocalization_Rate" })
st.write(new_df)

n_row = len(new_df.index)

#Colocalization Statistics 
co_mean = new_df['Colocalization_Rate'].mean()
co_std = new_df['Colocalization_Rate'].std()
co_sem = new_df['Colocalization_Rate'].sem()
co_summary = pd.DataFrame(data=[co_mean, co_std, co_sem, n_row], index= ['Average', 'SD', 'SEM', 'N'], columns= ['Colocalization_Rate'])

#Tumor Area Statistics 
tu_mean = new_df['Total_Tumor_Area'].mean()
tu_std = new_df['Total_Tumor_Area'].std()
tu_sem = new_df['Total_Tumor_Area'].sem()
tu_summary = pd.DataFrame(data=[tu_mean, tu_std, tu_sem, n_row], index= ['Average', 'SD', 'SEM', 'N'], columns= ['Total_Tumor_Area'])

#Fluorescent Intensity Statistics 
fi_mean = new_df['Total_Fluorescent_Intensity'].mean()
fi_std = new_df['Total_Fluorescent_Intensity'].std()
fi_sem = new_df['Total_Fluorescent_Intensity'].sem()
fi_summary = pd.DataFrame(data=[fi_mean, fi_std, fi_sem, n_row], index= ['Average', 'SD', 'SEM', 'N'], columns= ['Total_Fluorescent_Intensity'])

summary = pd.concat([tu_summary, fi_summary, co_summary], axis= 1)
st.write(summary)

with st.form('save_raw pixel_files') :
    save_dir = st.text_input('Type directory to save dataframe and summary .csv files:')
    df_csv = os.path.join(save_dir, name_input + '_' + time_input + '_colocalization_dataframe.csv')
    summary_csv = os.path.join(save_dir, name_input + '_' + time_input + '_colocalization_summary.csv')
    saved = st.form_submit_button('Save')
    if saved:
        new_df.to_csv(df_csv)
        summary.to_csv(summary_csv)
        st.write('_Files saved_')

