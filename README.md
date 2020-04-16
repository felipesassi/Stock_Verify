# Stock Verify

Nesse projeto foi desenvolvida uma *dashboard* para análise de ações listadas na bolsa de valores brasileira.  Além disso, foi realizado o *deploy* da aplicação no Heroku


## Dados utilizados

Os dados utilizados nesse projeto foram obtidos por meio de web scraping no site fundamentus. Após a obtenção dos dados os mesmo foram tratados para sua posterior utilização. Nessa etapa dois módulos foram utilizados, o *requests* para tratar das requisições web necessárias e o *BeautifulSoup* para extração das informações.

## Criação da *dashboard*

Para criação da *dashboard* a biblioteca Streamlit foi utilizada. Essa biblioteca permite o desenvolvimento de aplicações visuais de maneira rápida e tem total integração com a biblioteca pandas para análise dos dados e plotly para análises gráficas.

A *dashboard* desenvolvida conta com três páginas:

- Análise de papéis: onde pode-se verificar informações sobre determinado papel, como preço e alguns indicadores fundamentalistas. Além disso nessa página é apresentado um índice de similaridade do papel selecionado com os outros que compõe o banco de dados;
- Análise de setor: nessa parte pode-se verificar informações dos papeis agrupados por setor. Além disso pode-se verificar o histórico de cotações dos papéis;
- Análise de indicadores: nessa parte pode-se selecionar os indicadores de interesse para busca de papéis com determinadas características.

### Análise de papéis

A figura abaixo apresenta a interface dessa seção.

![Tela 1](/images/tela_1.png)

### Análise de setor

### Análise de indicadores

## Cálculo do índice de similaridade

Na seção **análise dos papeis** um índice de similaridade é calculado. Esse índice é calculado por meio da similaridade do cosseno. Para realizar esse cálculo são utilizados indicadores fundamentalistas para cada papel (como seus atributos). Esses indicadores são, 

