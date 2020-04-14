import streamlit as st
import pandas as pd
import pickle
from dashboard.dashboard_design import *

@st.cache
def load_data():
    df = pd.read_csv("data/processed.csv")
    df = df.drop(index = 49).reset_index(drop = True)
    prices_pkl = open("data/prices.pkl", "rb")
    prices = pickle.load(prices_pkl)
    prices_pkl.close()
    similarity_pkl = open("data/similarity.pkl", "rb")
    similarity = pickle.load(similarity_pkl)
    similarity_pkl.close()
    return df, prices, similarity

def main():
    st.title("Análise de ações B3")
    df, prices, similarity = load_data()
    opt = render_sidebar(df)
    options = ("Análise de papéis", "Análise de setores", "Análise de indicadores")
    if opt == options[0]:
        show_stock_page(df, similarity)
    elif opt == options[1]:
        show_sector_page(df, prices)
    else:
        show_comparision_page(df)

if __name__ == "__main__":
    main()