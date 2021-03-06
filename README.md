# Stock Verify

Nesse projeto foi desenvolvida uma *dashboard* para análise de ações listadas na bolsa de valores brasileira.  Além disso, foi realizado o *deploy* da aplicação no Heroku.

A aplicação está hospedada [aqui](https://stock-verify.herokuapp.com/).

## Dados utilizados

Os dados utilizados nesse projeto foram obtidos por meio de web scraping no site [Fundamentus](http://fundamentus.com.br/). Após a obtenção dos dados os mesmo foram tratados para sua posterior utilização. Nessa etapa dois módulos foram utilizados, o [requests](https://requests.readthedocs.io/pt_BR/latest/user/quickstart.html) para tratar das requisições web necessárias e o [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) para extração das informações.

Para obter os dados históricos de preços a plataforma [Alpha Vantage](https://www.alphavantage.co/) foi utilizada.

## Criação da *dashboard*

Para criação da *dashboard* a biblioteca [streamlit](streamlit.io) foi utilizada. Essa biblioteca permite o desenvolvimento de aplicações visuais de maneira rápida e tem total integração com a biblioteca pandas para análise dos dados e [plotly](https://plotly.com/python/) para análises gráficas.

A *dashboard* desenvolvida conta com três páginas:

- Análise de papéis: onde pode-se verificar informações sobre determinado papel, como preço e alguns indicadores fundamentalistas. Além disso nessa página é apresentado um índice de similaridade do papel selecionado com os outros que compõe o banco de dados;
- Análise de setor: nessa parte pode-se verificar informações dos papeis agrupados por setor. Além disso pode-se verificar o histórico de cotações dos papéis;
- Análise de indicadores: nessa parte pode-se selecionar os indicadores de interesse para busca de papéis com determinadas características.

### Análise de papéis

A figura abaixo apresenta a interface dessa seção. Todas as informações apresentadas são em relação ao papel selecionado, nesse caso, **TIET4**.

![Tela 1](/images/tela_1.png)

### Análise de setor

A figura abaixo apresenta a interface dessa seção. Pode-se verificar as informações setoriais, bem como a possibilidade de análise de cotações mais recentes e análise de dados históricos de cotações.

![Tela 1](/images/tela_2.png)

### Análise de indicadores

A figura abaixo apresenta a interface dessa seção. Nessa seção deve-se escolher o indicador a ser analisado bem como os intervalos de análise. Após isso a ferramente se encarrega de encontrar os papéis que satisfazem os requisitos impostos.

![Tela 1](/images/tela_3.png)

## Cálculo do índice de similaridade

Na seção [análise dos papéis](#análise-de-papéis) um índice de similaridade é calculado. Esse índice é calculado por meio da [similaridade do cosseno](https://en.wikipedia.org/wiki/Cosine_similarity). Para realizar esse cálculo são utilizados indicadores fundamentalistas para cada papel (como seus atributos). Esses indicadores são, P/L, P/VP, P/EBIT, PSR, P/Ativos, P/Cap. Giro, P/Ativ. Circ. Liq., Div. Yield, EV/EBITDA, EV/EBIT, Cresc. Rec. (5 anos), LPA, VPA, Marg. Bruta, Marg. Líquida, EBIT/Ativo, ROIC, ROE, Liquidez Corrente, DB/PL, Giro Ativos.

## Como usar

### Requirements

- seaborn==0.9.0
- numpy==1.16.4
- streamlit==0.57.3
- pandas==0.24.1
- matplotlib==3.1.1
- tornado==5.0
- plotly==4.6.0
- requests==2.18.4
- beautifulsoup4==4.9.0
- lxml==4.5.0

Para instalar todos os requerimentos o seguinte comando pode ser utilizado:

```
pip install -r requirements.txt
```
### Obtenção dos dados

Para realizar o *download* do conjunto de dados o seguinte comando deverá ser utilizado:

```
python3 web_scrap/main.py
```

### Geração do *dashboard*

Para gerar o *dashboard* o seguinte comando deverá ser utilizado:

```
streamlit run dashboard.py
```

## Descrição dos arquivos do projeto

### dashboard

Aqui ficam os códigos responsáveis pela criação da *dashboard*.

### web_scrap

Aqui ficam os códigos responsácei pelo web scraping dos dados e posterior processamento dos mesmos.

