#Se instalan las librerias plotly-express y openpyxl"""
#El programa se arranca con streamlit run y el nombre del archivo ejemplo: datos.py

import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(page_title='Ventas', page_icon=':bar_chart:', layout='wide')

tabla = pd.read_excel(io='ventas.xlsx', #archivo excel
                      engine="openpyxl", #libreria
                      sheet_name="Sales", #nombre hoja
                      skiprows=3, #espaciado
                      usecols="B:R", #columnas
                      nrows=1000) #filas


st.sidebar.header("elige una opción: ")
ciudad = st.sidebar.multiselect(
    "Seleciona la ciudad... ", 
    options=tabla["City"].unique(), 
    default=tabla["City"].unique())

customer = st.sidebar.multiselect(  #seleecion por cliente
    "Seleciona el cliente... ", 
    options=tabla["Customer_type"].unique(), 
    default=tabla["Customer_type"].unique())

gender = st.sidebar.multiselect( #selección por gènero
    "Seleciona el género... ", 
    options=tabla["Gender"].unique(), 
    default=tabla["Gender"].unique())

selectorDf = tabla.query(
                    "City == @ciudad & Customer_type == @customer & Gender == @ gender") #filtra ciudad y clientes




#st.dataframe(tabla)
st.title("KPI Ventas")
st.markdown('#'*5)
totalVentas = int(selectorDf["Total"].sum())
media = round(selectorDf["Rating"].mean(), 1)
stars = ":stars:"*int(round(media, 0))
transaction = round(selectorDf["Total"].mean(), 2)
col1,col2,colmean = st.columns(3)
with col1:
    st.write("**Ventas Totales:**")
    st.subheader(f'${totalVentas:}')
with colmean:
    st.write("**Rango Ventas:**")
    st.subheader(f'{media} {stars}')

with col2:
    st.write("**Transiciones Ventas:**")
    st.subheader(f'{transaction}')

st.markdown('--')

ventasProducto = (
                 selectorDf.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
                 )

graficoProducto = px.bar(
                        ventasProducto,
                        x="Total",
                        y=ventasProducto.index,
                        orientation="h",
                        title="<b>Ventas por producto</b>",
                        color_discrete_sequence=["0083B8"]*len(ventasProducto),
                        template="plotly_white",
                        )

st.plotly_chart(graficoProducto)

