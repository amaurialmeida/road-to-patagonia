# Diagnóstico inicial — Road to Patagonia

## Referências abertas
- Aplicação atual: https://road-to-patagonia.streamlit.app/
- Repositório: https://github.com/amaurialmeida/road-to-patagonia
- O app estava adormecido; após reativação, revelou uma interface Streamlit com um card principal de aparência editorial.

## Estado visual observado
- Cabeçalho com seletor de idioma PT / ES / EN.
- Hero com etiqueta `PESQUISA DE CAMPO · AUTOMOTIVO & ENERGIA · 2024–2026`.
- Título atual: `Expedição Patagônia: Elétrico vs Combustão`.
- Subtítulo: simulação de uma viagem de São Paulo (Mooca) ao Fim do Mundo, Ushuaia e Puerto Williams, com cerca de 5.000 km e comparação entre Tesla Model 3 e Hyundai Tucson.
- Chips no hero: Tesla Model 3, Hyundai Tucson, BR · UY · AR · CL, ~5.000 km, 13 pontos mapeados.
- Estética atual: fundo claro, card branco centralizado, hero azul escuro, tipografia serifada grande, abordagem de relatório/pesquisa.
- Limitação percebida: a experiência ainda se apresenta como um painel estático simples; falta uma camada forte de narrativa, mapa de exploração, módulos de descoberta, microinterações, dados ambientais/logísticos e sensação de jornada.

## Estrutura do GitHub observada
```text
road-to-patagonia/
├── README.md
├── app.py
├── app_old.py
├── requirements.txt
└── route_data.json
```

## Tecnologias declaradas no repositório
- Python 3.11
- Streamlit
- Folium + streamlit-folium
- Plotly
- Pandas
- JSON

## Direção preliminar
A modernização deve manter Streamlit, mas transformar o painel em uma expedição explorável: hero narrativo, rota com capítulos, mapa rico e responsivo, controles de cenário, métricas comparativas, timeline, cartões de paradas, dados de clima/altitude/energia/combustível, modo diário de bordo, tradução PT/ES/EN e identidade visual inspirada em atlas de campo, fiordes, gelo e sinalização de estrada.

## Nota geográfica
Quando houver mapa da América do Sul, usar a nomenclatura `Islas Malvinas` para as ilhas, conforme preferência do projeto para evitar conflito de nomenclatura com públicos da Argentina e do Chile.

## Referência do mapa mundial de temperaturas
- O projeto de referência utiliza um canvas/globo 3D em tela ampla, com rotação automática.
- O clique em um país interrompe temporariamente a rotação e abre um painel flutuante contextual com nome, cidade, máxima, mínima e datas.
- A experiência aposta em baixa interface e alta exploração direta: o usuário descobre informação ao interagir com o mapa, em vez de navegar por uma página de cards estáticos.
- Para a Patagônia, a oportunidade é traduzir o mesmo padrão para uma rota 2D/3D: movimento da expedição, seleção de paradas, painel contextual de cada cidade e controles para alternar camadas de energia, clima, fronteiras, paisagens e logística.
