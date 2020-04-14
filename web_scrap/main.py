from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

def create_numbers(data):
  data_new = data.split(".")
  string = ""
  for n in data_new:
    string += n
  return float(string)

def remove_perc(data):
  data_new = data.split("%")
  if len(data_new) > 1:
    data_new = data_new[0].replace(",", ".")
    return float(data_new)
  else:
    data = data.split(".")
    string = ""
    for n in data:
      string += n
    return float(string)

def scrap_web_data():
    df = pd.read_html("http://www.grafbolsa.com/")[1]
    page = requests.get("https://www.fundamentus.com.br/detalhes.php?papel=PETR4")
    data = {}
    soup = BeautifulSoup(page.content, "html.parser")
    for text in soup.find_all(class_ = "label"):
        key = text.get_text().split("?")
        data[key[-1]] = []
    names = df[9].values[3:]
    for name in names:
        url = "https://www.fundamentus.com.br/detalhes.php?papel=" + name
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        for label, value in zip(soup.find_all(class_ = "label"), soup.find_all(class_ = "data")):
            key = label.get_text().split("?")
            if key[-1] in data:
                try:
                    value = value.get_text().strip()
                    data[key[-1]].append(value)
                except:
                    data[key[-1]].append("NaN")
    clean_dict = {}
    for key in data.keys(): 
        if len(data[key]) == len(data["Papel"]):
            clean_dict[key] = data[key]
    df = pd.DataFrame(clean_dict)
    df.to_csv("temp_df.csv", index = False)
    df = pd.read_csv("temp_df.csv", decimal = ",", na_values = "-")
    df.drop(columns = ["Unnamed: 44"], inplace = True)
    df_nan = pd.DataFrame(100*df.isna().sum()/df.shape[0])
    sel = df_nan[0] > 0
    remove = list(df_nan[sel].index)
    df_clean = df.dropna(subset=remove)
    df_clean.to_csv("clean.csv", index = False)
    df_clean["Vol $ méd (2m)"] = df_clean["Vol $ méd (2m)"].apply(create_numbers)
    df_clean["Valor de mercado"] = df_clean["Valor de mercado"].apply(create_numbers)
    df_clean["Valor da firma"] = df_clean["Valor da firma"].apply(create_numbers)
    df_clean["Nro. Ações"] = df_clean["Nro. Ações"].apply(create_numbers)
    df_clean["Ativo"] = df_clean["Ativo"].apply(create_numbers)
    df_clean["Patrim. Líq"] = df_clean["Patrim. Líq"].apply(create_numbers)
    df_clean["P/EBIT"] = df_clean["P/EBIT"].apply(lambda x: float(x.replace(".", "").replace(",", ".")))
    df_clean["EV / EBIT"] = df_clean["EV / EBIT"].apply(lambda x: float(x.replace(".", "").replace(",", ".")))
    df_clean["P/Ativ Circ Liq"] = df_clean["P/Ativ Circ Liq"].apply(lambda x: float(x.replace(".", "").replace(",", ".")))
    df_clean["Dia"] = df_clean["Dia"].apply(remove_perc)
    df_clean["Mês"] = df_clean["Mês"].apply(remove_perc)
    df_clean["30 dias"] = df_clean["30 dias"].apply(remove_perc)
    df_clean["Marg. Bruta"] = df_clean["Marg. Bruta"].apply(remove_perc)
    df_clean["12 meses"] = df_clean["12 meses"].apply(remove_perc)
    df_clean["Marg. EBIT"] = df_clean["Marg. EBIT"].apply(remove_perc)
    df_clean["2020"] = df_clean["2020"].apply(remove_perc)
    df_clean["Marg. Líquida"] = df_clean["Marg. Líquida"].apply(remove_perc)
    df_clean["2019"] = df_clean["2019"].apply(remove_perc)
    df_clean["EBIT / Ativo"] = df_clean["EBIT / Ativo"].apply(remove_perc)
    df_clean["2018"] = df_clean["2018"].apply(remove_perc)
    df_clean["ROIC"] = df_clean["ROIC"].apply(remove_perc)
    df_clean["2017"] = df_clean["2017"].apply(remove_perc)
    df_clean["Div. Yield"] = df_clean["Div. Yield"].apply(remove_perc)
    df_clean["ROE"] = df_clean["ROE"].apply(remove_perc)
    df_clean["2016"] = df_clean["2016"].apply(remove_perc)
    df_clean["2015"] = df_clean["2015"].apply(remove_perc)
    df_clean["Cres. Rec (5a)"] = df_clean["Cres. Rec (5a)"].apply(remove_perc)
    df_clean.to_csv("../data/processed.csv", index = False)

if __name__ == "__main__":
  try:
    scrap_web_data()
  except:
    pass