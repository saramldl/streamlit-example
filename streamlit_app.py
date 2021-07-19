import streamlit as st
from itertools import islice
import os
import numpy as np
import pandas as pd
st.set_option('deprecation.showfileUploaderEncoding', False)
import plotly.graph_objs as go

st.write("Change Excel sheet_name to = Block Shape Map --- Block Power Map")



def GetFile():
    uploaded_file = st.file_uploader("Choose a CSV file", type="xlsx")
    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file, sheet_name='Block Shape Map')
        return data
    try:
        data_csv = GetFile()
        st.write(data_csv.head())
    except:
        st.markdown("You must upload a dataset.")

def GetFile1():
    uploaded_file1 = st.file_uploader("Choose a CSV file", type="xlsx")
    if uploaded_file1 is not None:
        data1 = pd.read_excel(uploaded_file1, sheet_name='Block Power Map')
        return data1
    try:
        data_csv = GetFile1()
        st.write(data_csv.head())
    except:
        st.markdown("You must upload a dataset.")

st.sidebar.header("Power-Map")
menu1 = ["Selection", "Input", "Block Shape Map", "Plot Power Map", "3D Power Map","Power Split"]
PMP = st.sidebar.radio("Select", menu1)
if PMP == 'Selection':
    data_csv = GetFile()


if PMP == 'Input':

        #st.write('You selected `%s`' %GetFile)
    data_csv = GetFile1()
    A1 = data_csv.dropna(thresh=10, axis=0)
    Power = A1.dropna(thresh=10, axis=1)
    Power.reset_index(inplace=True)
    st.write("Selected file Block Power Map Dataframe is", Power.shape)
    st.write(Power.style.format("{:.6f}"))


if PMP == 'Block Shape Map':
    data_csv = GetFile()
    A1 = data_csv.dropna(thresh=10, axis=0)
    Shape = A1.dropna(thresh=10, axis=1)
    Shape.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Heatmap(z=Shape,
            colorscale=[[0, "rgb(166,206,227)"],
                    [0.25, "rgb(31,120,180)"],
                    [0.45, "rgb(178,223,138)"],
                    [0.65, "rgb(51,160,44)"],
                    [0.85, "rgb(251,154,153)"],
                    [1, "rgb(227,26,28)"]],
        ))
    fig.update_layout(height=600, width=800, yaxis=dict(autorange='reversed'))
    fig.update_xaxes(side="top")
    fig.update_layout(xaxis_nticks=20,yaxis_nticks=20)
    fig.update_layout(
            title={
                'text': "Die Block Shape",
                'y': 0.925,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
    st.plotly_chart(fig)
if PMP=='Plot Power Map':
    data_csv = GetFile1()
    A1 = data_csv.dropna(thresh=10, axis=0)
    Power = A1.dropna(thresh=10, axis=1)
    Power.reset_index()
    fig1 = go.Figure(data=go.Heatmap(z=Power, colorscale='JET'))
    fig1.update_layout(height=600, width=800, yaxis=dict(autorange='reversed'))
    fig1.update_xaxes(side="top")
    fig1.update_layout(xaxis_nticks=20,yaxis_nticks=20)
    fig1.update_layout(
            title={
                'text': "Die Power Map in mW",
                'y': 0.925,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
    st.plotly_chart(fig1)
if PMP == '3D Power Map':
    data_csv = GetFile1()
    A1 = data_csv.dropna(thresh=10, axis=0)
    Power = A1.dropna(thresh=10, axis=1)
    Power.reset_index()
    fig2 = go.Figure(data=[go.Surface(z=Power.values)])
    fig2.update_traces(contours_z=dict(show=True, usecolormap=True), colorscale='JET')
    fig2.update_layout(height=600, width=800)
    #fig2.write_image("fig1.png")
    st.plotly_chart(fig2)


if PMP == 'Power Split':
    data_csv = GetFile1()
    A1 = data_csv.dropna(thresh=10, axis=0)
    Power = A1.dropna(thresh=10, axis=1)
    Power.reset_index()
    counts = np.unique(Power.values, return_counts=True)

    a1 = pd.DataFrame(counts)
    a2 = a1.T
    a2.dropna(inplace=True)
    a2.columns = ['Unique_Power', 'No_of_Cells']
    a2.sort_values(by=['Unique_Power', 'No_of_Cells'])
    a2["Total Power"] = a2.Unique_Power * a2.No_of_Cells
    a3=a2.sort_values(by='Total Power', ascending = False)
    a3.reset_index(inplace=True, drop=True)
    st.table(a3)
    st.table(a3.sum())
