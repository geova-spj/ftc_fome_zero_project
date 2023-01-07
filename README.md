<p align="center">
  <img src= fome_zero_logo_new.png alt="Sublime's custom image"/>
</p>

# Problema de Negócio

A empresa Fome Zero é um marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.

O CEO da empresa foi recém contratado e precisa entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a Fome Zero. Para isso, ele precisa que seja feita uma análise nos dados da empresa e que sejam gerados dashboards, a partir dessas análises, de modo a mapear a base de restaurantes cadastrados e entender o andamento do negócio por meio das seguintes informações:

**📋 Visão geral**

  1. Quantidade de restaurantes cadastrados e onde estão localizados; 
  2. Quantidade de países e cidades onde a Fome Zero atua;
  3. Quantidade de culinárias ofertadas;
  4. Quantitativo de restaurantes conforme suas características:
     * Aceitam reserva?
     * Aceitam pedidos online?
     * Fazem entrega?
  5. Quantitativo de avaliações feitas na plataforma;
  6. Melhores restaurantes (maiores notas de avaliação).
    
**🌍 Visão país**

 1. Quantidade de restaurantes cadastrados em cada país de atuação;
 2. Quantidade de cidades onde a Fome Zero está presente nos países de atuação;
 3. Diversidade gastronômica de cada país (quantidade de culinárias únicas ofertadas);
 4. Países com maiores quantitativos de avaliações realizadas;
 5. Nota média de avaliação dos serviços de cada país;
 6. Média de custo dos países.
    
**🏨 Visão cidade**

 1. Quais as cidades de cada país de atuação as quais contemplam o maior número de restaurantes cadastrados?
 2. Cidades com as melhores e piores notas médias avaliativas e em que países estão;
 3. Cidades com maior diversidade gastronômica;
 4. Cidades com maiores custos e piores avaliações;
 5. Cidades com menores custos e melhores avaliações.
    
**🍴 Visão gastronômica**
 1. Tipos de pratos que são a base da oferta da Fome Zero;
 2. Pratos piores e melhores avaliados;
 3. Pratos mais caros e piores avaliados;
 4. Pratos mais baratos e melhores avaliados.

O desafio é responder a essas questões e transformar seus resultados em dashboards que permitam o rápido entendimento do andamento do negócio. Os dados da empresa podem ser obtidos no link do Kaggle abaixo (arquivo zomato.csv):
https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv

# Premissas do negócio

1. O modelo de negócio assumido é um Marketplace;
2. A base de dados não contém informações de data, portanto as análises não contemplam a dimensão temporal;
3. As visões analíticas adotadas foram: país, cidade e gastronomia; 
4. Foram excluídos da base restaurantes os quais apresentavam custo médio de prato para dois igual a 0 por não fazer sentido à análise;
5. Dado que os países de atuação da Fome Zero possuem moedas diferentes optou-se por não fazer uniformização dos dados financeiros - a definição do quão barato ou caro pode ser um restaurante foi dada pela variável “prince_range”, dela se condicionou a variável “price_type” com os seguintes valores:
    * 1 - Cheap (Barato);
    * 2 - Normal;
    * 3 - Expensive (Caro);
    * 4 - Gourmet.
6. Qualquer análise que contemple dados financeiros a moeda corrente do país será apresentada junto ao dado.

# Estratégia da solução

1. As análises partiram da resolução das questões propostas pelo CEO segmentadas pelas visões país, cidade e gastronomia;
2. Em termos de ferramental utilizou-se:
    * Jupyter Notebook - Análises prévias e rascunho do script final;
    * Bibliotecas de manipulação de dados - Pandas e Numpy;
    * Bibliotecas de visualização de dados - Matplotlib, Plotly, Folium;
    * Jupyter Lab - Script Python final;
    * Streamlit e Streamlit Cloud- Visualização do dashboard e coloca-lo em produção.

# Top 3 insights de dados

1. Apenas cerca da metade dos restaurantes que aceitam pedidos online também fazem entregas;
2. O Brasil possui a pior operação: apenas 3 cidades cadastradas, todas figurando no top 5 das cidades piores avaliadas, o que o coloca também como o país de pior nota média de avaliação. É o único da América do Sul;
3. Nenhuma das 10 culinárias mais ofertadas encontram-se entre as melhores avaliadas, pelos contrário, 6 delas estão entre as 20 mais caras e piores avaliadas (seafood, continental, pizza, italian, cafe e american).

# O produto final do projeto

Dashboard online hospedado na Streamlit Cloud o qual pode ser acessado pelo link:

https://geova-spj-ftc-fome-zero-project.streamlit.app/

# Conclusão

O objetivo do projeto foi criar uma visualização de dados a qual permitisse o acompanhamento das principais características do negócio e de como elas se distribuem geograficamente.

O marketplace Fome Zero tem atuação global com forte presença nos continentes asiático e norte americano apresentando significativa diversidade gastronômica tendo os pratos do norte da Índia como a base de seu cardápio. 

# Próximos Passos

1. Especializar a análise por país gerando métricas de acompanhamento mais local dos negócios de modo a tornar os processos decisórios mais precisos conforme as particularidades geográficas;
2. Padronizar os dados financeiros e de avaliação de modo a tornar a comparação entre restaurantes e países mais justas/precisas na análise;
3. Analisar o custo e/ou benefício de se expandir ou retrair a diversidade gastronômica considerando o preço dos pratos e as avaliações dos restaurantes.
