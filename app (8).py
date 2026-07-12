import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import json

# Configuração da página
st.set_page_config(page_title="Patagonia Expedition 2024", layout="wide", page_icon="🏔️")

# Dicionário de traduções
translations = {
    "PT": {
        "title": "Expedição Patagônia: Elétrico vs Combustão",
        "subtitle": "De São Paulo (Mooca) ao Fim do Mundo (Ushuaia & Puerto Williams)",
        "lang_select": "Selecione o Idioma",
        "vehicle_specs": "Especificações dos Veículos",
        "route_map": "Mapa da Rota e Pontos de Recarga",
        "comparison": "Comparativo de Viagem",
        "tesla_range": "Autonomia Tesla (Est.):",
        "tucson_range": "Autonomia Tucson (Est.):",
        "total_dist": "Distância Total Aprox.:",
        "stops": "Principais Pontos de Parada",
        "charging_points": "Pontos de Recarga Tesla",
        "gas_stations": "Postos de Combustível",
        "cost_est": "Estimativa de Custo (Energia vs Gasolina)",
        "footer": "Projeto desenvolvido para Portfólio - Amauri Almeida",
        "details": "Detalhes da Rota",
        "why_go": "Por que ir para a Patagônia?",
        "motivation": "A Patagônia oferece paisagens únicas no mundo. Viajar de carro permite uma conexão profunda com a natureza, cruzando fronteiras e desafiando limites tecnológicos."
    },
    "EN": {
        "title": "Patagonia Expedition: Electric vs Combustion",
        "subtitle": "From São Paulo (Mooca) to the End of the World (Ushuaia & Puerto Williams)",
        "lang_select": "Select Language",
        "vehicle_specs": "Vehicle Specifications",
        "route_map": "Route Map & Charging Points",
        "comparison": "Trip Comparison",
        "tesla_range": "Tesla Range (Est.):",
        "tucson_range": "Tucson Range (Est.):",
        "total_dist": "Total Approx. Distance:",
        "stops": "Main Stop Points",
        "charging_points": "Tesla Charging Points",
        "gas_stations": "Gas Stations",
        "cost_est": "Cost Estimate (Energy vs Gas)",
        "footer": "Project developed for Portfolio - Amauri Almeida",
        "details": "Route Details",
        "why_go": "Why go to Patagonia?",
        "motivation": "Patagonia offers unique landscapes. Traveling by car allows a deep connection with nature, crossing borders and challenging technological limits."
    },
    "ES": {
        "title": "Expedición Patagonia: Eléctrico vs Combustión",
        "subtitle": "De São Paulo (Mooca) al Fin del Mundo (Ushuaia & Puerto Williams)",
        "lang_select": "Seleccione el Idioma",
        "vehicle_specs": "Especificaciones de los Vehículos",
        "route_map": "Mapa de Ruta y Puntos de Carga",
        "comparison": "Comparativa de Viaje",
        "tesla_range": "Autonomía Tesla (Est.):",
        "tucson_range": "Autonomía Tucson (Est.):",
        "total_dist": "Distancia Total Aprox.:",
        "stops": "Principales Puntos de Parada",
        "charging_points": "Puntos de Carga Tesla",
        "gas_stations": "Estaciones de Servicio",
        "cost_est": "Estimación de Costo (Energía vs Nafta)",
        "footer": "Proyecto desarrollado para Portafolio - Amauri Almeida",
        "details": "Detalles de la Ruta",
        "why_go": "¿Por qué ir a la Patagonia?",
        "motivation": "La Patagonia ofrece paisajes únicos en el mundo. Viajar en auto permite una conexión profunda con la naturaleza, cruzando fronteras y desafiando límites tecnológicos."
    }
}

# Seleção de idioma na barra lateral
lang = st.sidebar.selectbox("Language / Idioma", ["PT", "EN", "ES"])
t = translations[lang]

st.title(t["title"])
st.markdown(f"### {t['subtitle']}")

# Dados dos veículos
col1, col2 = st.columns(2)

with col1:
    st.image("https://www.tesla.com/sites/default/files/model3new/social/model-3-main.jpg", caption="Tesla Model 3 2024")
    st.write(f"**Tesla Model 3 2024 (Long Range)**")
    st.write(f"- {t['tesla_range']} 550 km")
    st.write("- Battery: 78.1 kWh")
    st.write("- Fast Charge: 250 kW (CCS2)")

with col2:
    st.image("https://www.hyundai.com/content/dam/hyundai/ww/en/images/find-a-car/tucson/highlights/hyundai-tucson-nx4-highlights-exterior-pc.jpg", caption="Hyundai Tucson 2024")
    st.write(f"**Hyundai Tucson 2024 (Gasoline)**")
    st.write(f"- {t['tucson_range']} 750 km")
    st.write("- Tank: 54 L")
    st.write("- Consumption: 14 km/l (Highway)")

# Mapa
st.header(t["route_map"])

# Carregar dados da rota
with open('route_data.json', 'r') as f:
    route_data = json.load(f)

# Criar mapa folium
m = folium.Map(location=[-34.6037, -58.3816], zoom_start=4)

# Adicionar rota
points = [[c['lat'], c['lon']] for c in route_data]
folium.PolyLine(points, color="blue", weight=2.5, opacity=1).add_to(m)

# Adicionar marcadores
for city in route_data:
    if city['type'] == "Start":
        icon, color = "play", "green"
    elif "End" in city['type']:
        icon, color = "flag", "red"
    elif city['type'] == "Tesla/Gas":
        icon, color = "flash", "blue"
    else:
        icon, color = "info-sign", "orange"
        
    folium.Marker(
        [city['lat'], city['lon']],
        popup=f"<b>{city['name']}</b><br>Type: {city['type']}",
        tooltip=city['name'],
        icon=folium.Icon(color=color, icon=icon)
    ).add_to(m)

st_folium(m, width=1200, height=600)

# Detalhes da Rota
st.header(t["details"])
df_route = pd.DataFrame(route_data)
st.table(df_route[['name', 'lat', 'lon']])

# Comparativo de Custo (Gráfico)
st.header(t["cost_est"])
fig = go.Figure(data=[
    go.Bar(name='Tesla Model 3 (Charging)', x=['São Paulo -> Ushuaia'], y=[450], marker_color='green'),
    go.Bar(name='Hyundai Tucson (Gasoline)', x=['São Paulo -> Ushuaia'], y=[1200], marker_color='red')
])
fig.update_layout(barmode='group', title="Estimated Cost (USD)", yaxis_title="Cost in USD")
st.plotly_chart(fig)

# Motivação
st.sidebar.header(t["why_go"])
st.sidebar.write(t["motivation"])

st.markdown("---")
st.write(t["footer"])
