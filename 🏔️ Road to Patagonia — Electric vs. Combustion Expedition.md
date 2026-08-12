# 🏔️ Road to Patagonia — Electric vs. Combustion Expedition

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B?logo=streamlit&logoColor=white)](https://road-to-patagonia.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

🌐 **Languages:** [Português](README.md) | [Español](README.es.md) | [English](README.en.md)

**Independent Field Research — Applied Automotive & Energy Case Study (2024–2026)**  
Route: São Paulo (Mooca), Brazil → Ushuaia, Argentina & Puerto Williams, Chile  
**Author:** Amauri Almeida de Souza Junior  

---

## 🌟 Visão Geral da Modernização

Inspirado nas visualizações imersivas de alta interatividade (como o painel global de temperaturas), o projeto **Road to Patagonia** foi profundamente modernizado para proporcionar uma experiência visual de impacto imediato ("WOW"). A nova interface une design editorial, navegação por abas intuitivas, seletor trilíngue dinâmico (PT / ES / EN), mapa geoespacial vetorial com animações de trajeto e dossiês detalhados ponto a ponto.

---

## ❓ Questão de Pesquisa

> *"Em uma viagem rodoviária real de aproximadamente 5.000 km de São Paulo ao extremo sul da América do Sul, cruzando Brasil, Uruguai, Argentina e Chile — como um veículo 100% elétrico se compara a um veículo a combustão interna em termos de custo de viagem e logística de autonomia?"*

**Conclusão:** O veículo elétrico (Tesla Model 3 Long Range) apresenta, neste snapshot configurável, custo operacional de energia inferior ao veículo a combustão. O resultado muda com câmbio, preço local, consumo, perdas de recarga e disponibilidade de carregadores. O desafio reside na assimetria de infraestrutura de recarga rápida nas regiões mais austrais da Patagônia.

---

## 📍 Os 13 Pontos Mapeados da Rota

| # | Parada / Local | País | Distância Acumulada | Infraestrutura Principal |
|---|---|---|---|---|
| 1 | São Paulo (Mooca) | 🇧🇷 Brasil | 0 km | Supercharger & Rede Rodoviária |
| 2 | Curitiba | 🇧🇷 Brasil | 408 km | Eletropostos BR-116 & Shopping |
| 3 | Florianópolis | 🇧🇷 Brasil | 705 km | Destination Chargers & Costa |
| 4 | Porto Alegre | 🇧🇷 Brasil | 1.160 km | Eletropostos Urbanos & Rede Sul |
| 5 | Chuí | 🇧🇷/🇺🇾 BR / UY | 1.680 km | Rota Elétrica UTE (Uruguai) |
| 6 | Punta del Este | 🇺🇾 Uruguai | 1.920 km | Malha UTE & Postos Ancap |
| 7 | Buenos Aires | 🇦🇷 Argentina | 2.350 km | Supercharger & Postos YPF |
| 8 | Bahía Blanca | 🇦🇷 Argentina | 2.980 km | Porta de entrada patagônica (YPF) |
| 9 | Puerto Madryn | 🇦🇷 Argentina | 3.420 km | Península Valdés & Fauna Marinha |
| 10 | Comodoro Rivadavia | 🇦🇷 Argentina | 3.850 km | Capital do Petróleo & Eólica |
| 11 | Río Gallegos | 🇦🇷 Argentina | 4.450 km | Portal patagônico austral |
| 12 | Ushuaia | 🇦🇷 Argentina | 5.020 km | Fim da Ruta 3 (Terra do Fogo) |
| 13 | Puerto Williams | 🇨🇱 Chile | 5.100 km | Cidade mais austral (Isla Navarino) |

---

## 🔬 Metodologia & Diferenciais

- **Mapeamento Geoespacial Avançado:** Folium com camadas temáticas, linhas animadas de trajeto (*AntPath*) e marcadores interativos com fichas completas.
- **Auto-Drive contínuo:** Tesla Model 3 ou Hyundai Tucson percorrem a rota automaticamente; o usuário pode pausar e inspecionar cada parada.
- **Dossiê financeiro por segmento:** O app calcula litros de gasolina, kWh comprados, preço local, custo em moeda local e conversão para USD por trecho.
- **Atualização diária com fallback:** A aplicação tenta consultar fontes públicas uma vez a cada 24 horas, exibe a data e a frequência real do dado e preserva o snapshot local quando uma fonte falha.
- **Emissões operacionais:** A comparação separa CO₂ direto da gasolina e CO₂ associado à eletricidade, com hipóteses editáveis e fatores EPA/IPCC documentados.
- **Travessias por água:** Ushuaia → Puerto Williams é tratado como ferry/água, não como estrada. A Primera Angostura aparece como tarifa de veículo; o Canal Beagle é separado como tarifa de passageiro e exige cotação própria para embarcar o carro.
- **Tradução Instantânea:** Suporte completo para Português, Espanhol e Inglês diretamente na barra lateral.
- **Design Imersivo:** Paleta de cores inspirada em expedições polares e patagônicas, com cartões interativos e tipografia refinada (*Playfair Display* e *Plus Jakarta Sans*).

### Dados e fontes

O arquivo `route_economics.json` centraliza preços de gasolina, diesel, eletricidade, hipóteses de consumo, fatores de emissão e travessias. As fontes indicadas incluem [ANP](https://app.powerbi.com/view?r=eyJrIjoiMGM0NDhhMTUtMjQwZi00N2RlLTk1M2UtYjkxZTlkNzM1YzE5IiwidCI6IjQ0OTlmNGZmLTI0YTYtNGI0Mi1iN2VmLTEyNGFmY2FkYzkxMyJ9), [ANCAP](https://www.ancap.com.uy/10564/1/historico-precios-combustibles.html), [Secretaría de Energía da Argentina](http://res1104.se.gob.ar/consultaprecios.eess.php), [CNE Chile](https://apidocs.cne.cl/), [TABSA](https://www.tabsa.cl/rutas/primera-angostura) e [EPA/IPCC](https://www.epa.gov/energy/greenhouse-gas-equivalencies-calculator-calculations-and-references). Preço nacional ou de referência não substitui cotação por posto, data, rede, câmbio e disponibilidade.

---

## 🚀 Como Executar Localmente

```bash
# Clonar o repositório
git clone https://github.com/amaurialmeida/road-to-patagonia.git
cd road-to-patagonia

# Instalar dependências
pip install -r requirements.txt

# Executar a aplicação Streamlit
streamlit run app.py
```

---

## 🔗 Links Profissionais & Portfólio

- **Lattes:** [http://lattes.cnpq.br/9545242042800090](http://lattes.cnpq.br/9545242042800090)
- **Escavador:** [https://www.escavador.com/sobre/8577779/amauri-almeida-de-souza-junior](https://www.escavador.com/sobre/8577779/amauri-almeida-de-souza-junior)
- **Portfólio Ambiental:** [https://amaurialmeida.github.io/environmental-portfolio/](https://amaurialmeida.github.io/environmental-portfolio/)

---

© 2024–2026 · Amauri Almeida de Souza Junior · Expedição Patagônia · Pesquisa de Campo
