from ctypes import alignment
import streamlit as st 
import pandas as pd


sales_data = pd.read_csv("Processed_Sales_Overall.csv")
city = ['Bengaluru','Chennai','Delhi','Hyderabad','Kolkata','Mumbai','Overall']
dates = sales_data['trans_date'].unique()
dates.sort()
dates_range = pd.date_range(dates[0],dates[-1],freq='MS').strftime("%b-%Y").tolist()

st.title("MOM Comparision City Wise")
st.markdown(""" 
            
            """)

st.sidebar.header('User Input Features')
select_base_month = st.sidebar.selectbox("Compare Month",dates_range[::-1])

select_other_month = st.sidebar.selectbox("With Month",dates_range[::-1][1:])

select_city = st.sidebar.selectbox('City',city)

@st.cache
def comparision(base_month, comparing_month, data, city):
    data['month_year'] = pd.to_datetime(sales_data['trans_date']).dt.strftime('%b-%Y')
    if city == 'Overall':
        df_base = data[(data['month_year'] == base_month)]
        df_comparing = data[(data['month_year'] == comparing_month)]
    else:
        df_base = data[(data['month_year'] == base_month) & (data['City'] == city)]
        df_comparing = data[(data['month_year'] == comparing_month) & (data['City'] == city)]
    # print(df_base.head())
    df_base = df_base.groupby(['month_year','NS']).agg({'quantity':'sum','final_price':'sum'}).reset_index()
    df_comparing = df_comparing.groupby(['month_year','NS']).agg({'quantity':'sum','final_price':'sum'}).reset_index()
    base_price_name = base_month + ' Revenue'
    base_quantity_name =  base_month + ' Quantity'
    comparing_price_name = comparing_month + ' Price'
    comparing_quantity_name = comparing_month + ' Quantity'
    df_base.rename(columns = {'quantity':base_quantity_name,'final_price':base_price_name},inplace=True)
    df_comparing.rename(columns = {'quantity':comparing_quantity_name,'final_price':comparing_price_name},inplace=True)
    df_final = df_base.merge(df_comparing,on='NS')
    df_final['% Change in Quantity'] = round(((df_final[comparing_quantity_name] - df_final[base_quantity_name])/df_final[base_quantity_name])*100,2)
    df_final['% Change in Revenue'] = round(((df_final[comparing_price_name] - df_final[base_price_name])/df_final[base_price_name])*100,2)
    df_final = df_final[['NS',base_quantity_name,base_price_name,comparing_quantity_name,comparing_price_name,'% Change in Quantity','% Change in Revenue']]
    return df_final

data_comp = comparision(select_base_month,select_other_month,sales_data,select_city)
#sorted_unique_ns = sales_data[sales_data['NS']].unique()
#select_need_states = st.sidebar.multiselect('Need State',sorted_unique_ns,sorted_unique_ns)

# df_selected_ns = data_comp[data_comp.NS.isin(select_need_states)]

# st.header('Data Display')
# st.write('Data Dimension: '+ str(data_comp.shape[0]) + ' rows' + str(data_comp.shape[1]) + 'columns')
# st.dataframe(data_comp)

filter = st.multiselect('Filter by NEED STATE',data_comp['NS'].unique(),data_comp['NS'].unique()[:10])

filtered_NS = data_comp[(data_comp.NS.isin(filter))]
styler = filtered_NS.style.hide_index().format(decimal='.', precision=2)
st.write(styler.to_html(), unsafe_allow_html=True)