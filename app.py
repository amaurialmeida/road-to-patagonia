import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import json

# Configuração da página
st.set_page_config(page_title="Patagonia Expedition 2024", layout="wide", page_icon="🏔️")

# Inicialização do Estado de Idioma (Padrão: BR/PT)
if 'lang' not in st.session_state:
    st.session_state.lang = 'PT'

# Dicionário de traduções integrado com o novo layout
translations = {
    "PT": {
        "title": "Expedição Patagônia: Elétrico vs Combustão",
        "subtitle": "De São Paulo (Mooca) ao Fim do Mundo (Ushuaia & Puerto Williams)",
        "vehicle_specs": "Especificações dos Veículos",
        "route_map": "Mapa da Rota e Pontos de Recarga / Abastecimento",
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

t = translations[st.session_state.lang]

# Estilização CSS Avançada (Banner e Layout limpo)
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 0rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    .custom-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 2.5rem;
        border-radius: 0px 0px 15px 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    .custom-banner h1 {
        color: #38bdf8 !important;
        font-size: 2.6rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem;
    }
    .custom-banner h3 {
        color: #e2e8f0 !important;
        font-size: 1.3rem !important;
        font-weight: 400 !important;
    }
    .lang-container {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
        padding-top: 10px;
    }
    </style>
""", unsafe_style_html=True)

# Barra Dinâmica de Idiomas no Topo Direito (Substituindo a Sidebar)
cols_header = st.columns([8.2, 0.6, 0.6, 0.6])
with cols_header[1]:
    if st.button("🇺🇸 EN", key="btn_en"): 
        st.session_state.lang = 'EN'
        st.rerun()
with cols_header[2]:
    if st.button("🇧🇷 BR", key="btn_pt"): 
        st.session_state.lang = 'PT'
        st.rerun()
with cols_header[3]:
    if st.button("🇪🇸 ES", key="btn_es"): 
        st.session_state.lang = 'ES'
        st.rerun()

# Banner Superior Estilizado
st.markdown(f"""
    <div class="custom-banner">
        <h1>{t['title']}</h1>
        <h3>{t['subtitle']}</h3>
    </div>
""", unsafe_style_html=True)

# Sidebar apenas com a seção de Motivação/Contexto
st.sidebar.header(t["why_go"])
st.sidebar.write(t["motivation"])

# Seção de Dados Técnicos dos Veículos
st.header(t["vehicle_specs"])
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

# Seção do Mapa customizado e blindado
st.header(t["route_map"])

# Carregar dados da rota
with open('route_data.json', 'r') as f:
    route_data = json.load(f)

# Inicializar mapa folium usando a camada 'CartoDB Positron' para ocultação refinada
m = folium.Map(location=[-38.0000, -58.3816], zoom_start=4, tiles="CartoDB positron")

# Adicionar linhas da rota
points = [[c['lat'], c['lon']] for c in route_data]
folium.PolyLine(points, color="#10b981", weight=3, opacity=0.9).add_to(m)

# Adicionar marcadores baseados na lista oficial
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

# ─── CAMADA EXCLUSIVA: OCULTAÇÃO E TRADUÇÃO GEOPOLÍTICA (ILHAS MALVINAS) ───
malvinas_coords = [-51.75, -59.16]

# Máscara circular opaca com a cor exata do oceano do CartoDB Positron (#e6edf1)
folium.Circle(
    location=malvinas_coords,
    radius=115000, 
    color="#e6edf1",
    fill=True,
    fill_color="#e6edf1",
    fill_opacity=1.0,
    weight=0
).add_to(m)

# Injeção do rótulo correto respeitando os clientes da América Latina
folium.map.Marker(
    location=[-51.45, -59.55],
    icon=folium.features.DivIcon(
        html="""<div style="font-family: sans-serif; font-size: 11px; font-weight: bold; color: #475569; width: 180px; text-shadow: 1px 1px 0px #fff;">Islas Malvinas<br><span style="font-size:9px; font-weight:normal; opacity:0.7;">(Ilhas Malvinas)</span></div>"""
    )
).add_to(m)
# ──────────────────────────────────────────────────────────────────────────

st_folium(m, width=1200, height=600)

# Detalhes da Rota em Tabela
st.header(t["details"])
df_route = pd.DataFrame(route_data)
st.table(df_route[['name', 'lat', 'lon', 'type']])

# Comparativo de Custo Gráfico (Plotly)
st.header(t["cost_est"])
fig = go.Figure(data=[
    go.Bar(name='Tesla Model 3 (Charging)', x=['São Paulo -> Ushuaia / Puerto Williams'], y=[450], marker_color='#10b981'),
    go.Bar(name='Hyundai Tucson (Gasoline)', x=['São Paulo -> Ushuaia / Puerto Williams'], y=[1200], marker_color='#ef4444')
])
fig.update_layout(barmode='group', title="Estimated Cost (USD)", yaxis_title="Cost in USD", plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig)

st.markdown("---")
st.write(t["footer"])
