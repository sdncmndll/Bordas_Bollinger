import streamlit as st
import investpy as inv
import time
import datetime
import history as hist
import bollinger_bands as bollinger
import pandas as pd
#https://www.youtube.com/watch?v=PZhnF6e4jJQ, sobre o github

#Biblioteca usada para retornar o nome dos tickers das ações
tickers = inv.get_stocks_list("brazil")

#Setup da barra lateral
st.set_page_config(
    page_title="Stock Exchange",
    page_icon="bar-chart",
    layout="wide"
)

#Título da página
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Stock Analysis</p>', unsafe_allow_html=True)

#Definição da sidebar
with st.sidebar:
    #lista de ações
    ticker = st.selectbox(
        "Select the Action or Real Estate Fund",
        tickers
    )

    #Data atual e seleção
    date_reference = st.date_input(
        "Select a init of period",
        datetime.datetime.today()
    )

    #Dias de análise, default 30
    default_number_of_days=30
    number_of_days = st.number_input("Insert a number of days", value=30)

    #Tempo de atualização da página
    sleep_time = st.select_slider(
        'Select update time (seconds)',
        options=[5,10,15,30,60]
    )


    init_date = date_reference + datetime.timedelta (days=-(default_number_of_days + number_of_days))
    #print(init_date)
    end_date = date_reference
    #print(end_date)

    #Comentário das colunas abaixo do botão toggle
    toogle_column1, toogle_column2 = st.columns(2)

    with toogle_column1:
        st.write(f"Auto Refresh ({sleep_time})")

    with toogle_column2:
        toogle=st.toggle('Activate')

#df_hist = pd.DataFrame()
#df_div = pd.DataFrame()

#Função para plotar na página proincipal
def prepare_history_visualization():
    #Pega informações do módulo history com parâmetros para obter os dados em history e a instância da
    #Biblioteca de dados das ações
    history, instance = hist.get(ticker=ticker, init_date=init_date, end_date=end_date) if init_date else hist.get(ticker)
    #print("CURRENT PRICE ->", history["Close"].iat[-1])

    #Pega os dados e passa para o módulo bollinger_bands montar o gráfico
    bollinger_figure = bollinger.get(ticker, history)
   
    #Com base nos dados de history, monta os cards superiores
    current_value.metric("Current Value",
                         f"R$ {round(history['Close'][history.index.max()],2)}",
                         f"{round((history['Close'][history.index.max()] / history['Close'][history.index[-2]] - 1) * 100,2)}%")
    
    min_value.metric("Minimun Value",
                         f"R$ {round(history['Close'][history.index.min()],2)}",
                         f"{round((history['Close'][history.index.min()] / history['Close'][history.index.max()] - 1) * 100,2)}%")

    max_value.metric("Maximun Value",
                         f"R$ {round(history['Close'][history.index.max()],2)}",
                         f"{round((history['Close'][history.index.max()] / history['Close'][history.index.min()] - 1) * 100,2)}%")    
    div_value.metric("Dividens",
                        f"R$ {round(history['Dividends'].sum(),2)}") 

    graph.plotly_chart(bollinger_figure, use_container_width=True, sharing="streamlit")
    
    #Monta as tabelas inferiores com informações das ações
    col5, col6 = st.columns([3.5,2])
    with col5:
        st.write('Stock Values')
        df_hist=history.sort_index(ascending=False)
        st.dataframe(df_hist.drop(columns=['Dividends']))
    with col6:
        st.write('Dividends')
        df_div=df_hist[['Open','Close','Dividends']]
        df_div=df_div[df_div['Dividends']>0]
        df_div.insert(3,"DY(%)",round((df_div['Dividends']/df_div['Close'])*100,2))
        st.dataframe(df_div)
        
#Aqui é montada a atualização automática selecionada pelo tempo de atualização
if ticker and sleep_time:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        current_value = st.empty()
    with col2:
        min_value = st.empty()
    with col3:
        max_value = st.empty()
    with col4:
        div_value = st.empty()    

    graph = st.empty()


    #Tempo de refresh da página
    while toogle:
        prepare_history_visualization()
        time.sleep(sleep_time)
    else:
        prepare_history_visualization()


    

    



