import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import plotly.express as px

def show_stock_page(dataframe):
    papeis = dataframe["Papel"].unique()
    sel = st.selectbox("Qual papel deseja analisar?", papeis)
    df_sel = dataframe[dataframe["Papel"] == sel]
    cotacao = df_sel["Cotação"].values[0]
    date = df_sel["Data últ cot"].values[0]
    st.markdown("## Última atualização dos balanços em {}" .format(date))
    st.markdown("## Informações gerais")
    setor = df_sel["Setor"].values[0]
    st.markdown("- Setor: {}" .format(setor))
    st.markdown("- Cotação: R${}" .format(cotacao))
    p_max = df_sel["Max 52 sem"].values[0]
    st.markdown("- Preço máximo (52 semanas): R${}" .format(p_max))
    p_min = df_sel["Min 52 sem"].values[0]
    st.markdown("- Preço mínimo (52 semanas): R${}" .format(p_min))
    st.markdown("## Indicadores fundamentalistas")
    pl = df_sel["P/L"].values[0]
    st.markdown("- Indicador P/L: {}" .format(pl))
    dy = df_sel["Div. Yield"].values[0]
    st.markdown("- Dividend Yield: {}%" .format(dy))
    pvp = df_sel["P/VP"].values[0]
    st.markdown("- Indicador P/VP: {}" .format(pvp))
    ml = df_sel["Marg. Líquida"].values[0]
    st.markdown("- Marg. Líquida: {}%" .format(ml))
    roe = df_sel["ROE"].values[0]
    st.markdown("- ROE: {}%" .format(roe))
    br = df_sel["Div Br/ Patrim"].values[0]
    st.markdown("- DB/PL: {}" .format(br))
    ev = df_sel["EV / EBIT"].values[0]
    st.markdown("- EV/EBIT: {}" .format(ev))
    st.markdown("## Similaridade entre papéis")
    qtt = st.slider('Número de ações para análise', 2, 20, 5)
    source = pd.DataFrame(similarity[sel]).head(qtt)
    fig = px.bar(source, x='Papel', y='Similaridade')
    fig.update_layout(xaxis_title = "", template = "presentation")
    st.plotly_chart(fig, use_container_width=True)

def show_indicators_graphs(indicator, dataframe, true_indicator=None):
    if true_indicator == None:
        true_indicator = indicator
    var_mean = np.mean(dataframe[true_indicator].values)
    var_max = np.max(dataframe[true_indicator].values)
    var_min = np.min(dataframe[true_indicator].values)
    stock_max = dataframe[dataframe[true_indicator] == var_max]["Papel"].values[0]
    stock_min = dataframe[dataframe[true_indicator] == var_min]["Papel"].values[0]
    source = pd.DataFrame(data = {"Papel": dataframe["Papel"], indicator: dataframe[true_indicator]})
    st.markdown("* O {} médio desses papéis é igual a {:.2f}." .format(indicator, var_mean))
    st.markdown("* * {} é o maior {} desse setor ({})." .format(stock_max, indicator, var_max))
    st.markdown("* * {} é o menor {} desse setor ({})." .format(stock_min, indicator, var_min))
    fig = px.bar(source, x='Papel', y='{}' .format(indicator), color = "Papel")
    fig.update_layout(xaxis_title = "", template = "presentation")
    st.plotly_chart(fig, use_container_width=True)

def show_sector_page(dataframe, prices_data):
    setor = dataframe["Setor"].unique()
    sel = st.selectbox("Qual setor deseja analisar?", setor)
    df_sel = dataframe[dataframe["Setor"] == sel]
    papeis = df_sel["Papel"].values
    st.write("Esse setor é composto por {} papéis." .format(len(papeis)))
    market_value = np.sum(df_sel["Valor de mercado"].values)/np.sum(dataframe["Valor de mercado"].values)
    st.write("Esses papéis correspondem a {:.2f}% do valor de mercado da bolsa de valores brasileira." .format(100*market_value))
    date = df_sel["Data últ cot"].values[0]
    st.write("Abaixo pode-se verificar as últimas cotações desses papéis (atualizadas em {})." .format(date))
    opcoes = ('Cotação mais recente', 'Histórico de cotações')
    option = st.radio('Selecione o formato desejado para apresentar as cotações', opcoes)
    if option == opcoes[0]:
        source = pd.DataFrame(data = {"Papel": df_sel["Papel"], "Cotação": df_sel["Cotação"]})
        fig = px.bar(source, x='Papel', y='Cotação', color = "Papel")
        fig.update_layout(xaxis_title = "", template = "presentation")
        st.plotly_chart(fig, use_container_width=True)
    if option == opcoes[1]:
        min_len = 100000
        for key in papeis:
            if key in prices_data:
                data_len = len(prices_data[key])
                if data_len <= min_len:
                    min_len = data_len
        data_dict = {}
        for key in papeis:
            if key in prices_data:
                qtd = len(prices_data[key]) - min_len
                data_dict[key] = prices_data[key][qtd:]
        if data_dict != {}:
            prices_df = pd.DataFrame(data_dict)
            days = np.arange(0, min_len, 1)
            prices_df["Semanas"] = days
            prices_df = prices_df.melt('Semanas', var_name='Papel', value_name='Cotação')
            fig = px.line(prices_df, x="Semanas", y="Cotação", color= "Papel")
            fig.layout.template = "presentation"
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Sem dados para mostrar.")
    st.markdown("## Abaixo podem ser analisados os principais indicadores fundamentalistas aplicados a ações do setor escolhido.")
    data = st.multiselect("Selecione os indicadores", ["P/L", "Div. Y", "P/VP", "Marg. L.", "ROE", "DB/PL", "EV/EBIT"], default="P/L")
    if "P/L" in data:
        show_indicators_graphs("P/L", df_sel)
    if "Div. Y" in data:
        show_indicators_graphs("Div. Y", df_sel, "Div. Yield")
    if "P/VP" in data:
        show_indicators_graphs("P/VP", df_sel)
    if "Marg. L." in data:
        show_indicators_graphs("Marg. L.", df_sel, "Marg. Líquida")
    if "ROE" in data:
        show_indicators_graphs("ROE", df_sel)
    if "DB/PL" in data:
        show_indicators_graphs("DB/PL", df_sel, "Div Br/ Patrim")
    if "EV/EBIT" in data:
        show_indicators_graphs("EV/EBIT", df_sel, "EV / EBIT")

def show_selected_indicator(dataframe, quantity, indicator):
    const_order = ("Descendente", "Ascendente")
    order = st.radio("Indicador {}" .format(indicator), const_order)
    low = st.number_input("Insira o valor mínimo de {}:" .format(indicator), value = 0)
    high = st.number_input("Insira o valor máximo de {}" .format(indicator), value = 5)
    if indicator == "DB/PL":
        source = pd.DataFrame(data = {"Papel": dataframe["Papel"], indicator: dataframe["Div Br/ Patrim"]})
    elif indicator == "EV/EBIT":
        source = pd.DataFrame(data = {"Papel": dataframe["Papel"], indicator: dataframe["EV / EBIT"]})
    else:
        source = pd.DataFrame(data = {"Papel": dataframe["Papel"], indicator: dataframe[indicator]})
    source = source[(source[indicator] > low) & (source[indicator] < high)]
    if order == const_order[0]:
        source = source.sort_values(by = "{}" .format(indicator), ascending = False).head(quantity)
    else:
        source = source.sort_values(by = "{}" .format(indicator), ascending = True).head(quantity)
    fig = px.bar(source, x='Papel', y='{}' .format(indicator), color = "Papel")
    fig.update_layout(xaxis_title = "", template = "presentation", title = "Indicador {}".format(indicator))
    st.plotly_chart(fig, use_container_width=True)
        
def show_comparision_page(dataframe):
    st.write("Aqui podem ser comparados os principais indicadores fundamentalistas entre diferentes setores.")
    const_opt = ("P/L", "Div. Yield", "P/VP", "Marg. Líquida", "ROE", "DB/PL", "EV/EBIT")
    sel = st.selectbox("Qual indicador deseja analisar?", const_opt)
    qtt = st.slider('Número de ações para análise', 2, 30, 5)    
    const_order = ("Descendente", "Ascendente")
    if sel == const_opt[0]:
        show_selected_indicator(dataframe, qtt, sel)
    elif sel == const_opt[1]:    
        show_selected_indicator(dataframe, qtt, sel)
    elif sel == const_opt[2]:
        show_selected_indicator(dataframe, qtt, sel)
    elif sel == const_opt[3]:
        show_selected_indicator(dataframe, qtt, sel)
    elif sel == const_opt[4]:
        show_selected_indicator(dataframe, qtt, sel)
    elif sel == const_opt[5]:
        show_selected_indicator(dataframe, qtt, sel)
    elif sel == const_opt[6]:
        show_selected_indicator(dataframe, qtt, sel)

def render_sidebar(dataframe):
    st.sidebar.title("O que deseja realizar?")
    options = ("Análise de papéis", "Análise de setores", "Análise de indicadores")
    opt = st.sidebar.selectbox("Selecione uma opção", options)
    for i in range(35):
        st.sidebar.markdown("")
    date = dataframe["Data últ cot"].values[0]
    st.sidebar.markdown("Os dados foram atualizados em **{}**." .format(date))
    return opt