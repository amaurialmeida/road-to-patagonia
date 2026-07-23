import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import json
import os

# Configuração da página profissional
st.set_page_config(
    page_title="Patagonia Expedition 2024 · Elétrico vs Combustão",
    page_icon="🏔️",
    layout="wide"
)

# ============================================================
# SISTEMA DE TRADUÇÕES UNIFICADO (PT / EN / ES)
# ============================================================
translations = {
    "PT": {
        "title": "Expedição Patagônia: Elétrico vs Combustão",
        "subtitle": "De São Paulo (Mooca) ao Fim do Mundo (Ushuaia & Puerto Williams)",
        "vehicle_specs": "Especificações dos Veículos",
        "route_map": "Mapa de Rotas, Carregadores (Tesla) & Postos de Gasolina (Tucson)",
        "comparison": "Comparativo de Custo (Estimativa USD)",
        "tesla_range": "Autonomia Tesla (Est.):",
        "tucson_range": "Autonomia Tucson (Est.):",
        "total_dist": "Distância Total Aprox.:",
        "details": "Detalhamento das Coordenadas e Pontos de Parada",
        "why_go": "Por que ir para a Patagônia?",
        "motivation": "A Patagônia oferece paisagens únicas no mundo. Viajar de carro permite uma conexão profunda com a natureza, cruzando fronteiras e desafiando limites tecnológicos.",
        "tab1": "🗺️ Rotas & Pontos de Parada (Tesla vs Tucson)",
        "tab2": "🔬 Especificações & Custos",
        "footer": "Projeto desenvolvido para Portfólio - Amauri Almeida"
    },
    "EN": {
        "title": "Patagonia Expedition: Electric vs Combustion",
        "subtitle": "From São Paulo (Mooca) to the End of the World (Ushuaia & Puerto Williams)",
        "vehicle_specs": "Vehicle Specifications",
        "route_map": "Route Map, Chargers (Tesla) & Gas Stations (Tucson)",
        "comparison": "Trip Cost Comparison (Estimated USD)",
        "tesla_range": "Tesla Range (Est.):",
        "tucson_range": "Tucson Range (Est.):",
        "total_dist": "Total Approx. Distance:",
        "details": "Route Coordinates & Stop Points Breakdown",
        "why_go": "Why go to Patagonia?",
        "motivation": "Patagonia offers unique landscapes. Traveling by car allows a deep connection with nature, crossing borders and challenging technological limits.",
        "tab1": "🗺️ Routes & Stop Points (Tesla vs Tucson)",
        "tab2": "🔬 Specs & Financial Analysis",
        "footer": "Project developed for Portfolio - Amauri Almeida"
    },
    "ES": {
        "title": "Expedición Patagonia: Eléctrico vs Combustión",
        "subtitle": "De São Paulo (Mooca) al Fin del Mundo (Ushuaia & Puerto Williams)",
        "vehicle_specs": "Especificaciones de los Vehículos",
        "route_map": "Mapa de Ruta, Cargadores (Tesla) y Estaciones de Servicio (Tucson)",
        "comparison": "Comparativa de Costo (Estimación USD)",
        "tesla_range": "Autonomía Tesla (Est.):",
        "tucson_range": "Autonomía Tucson (Est.):",
        "total_dist": "Distancia Total Aprox.:",
        "details": "Detalles de Coordenadas y Puntos de Parada",
        "why_go": "¿Por qué ir a la Patagonia?",
        "motivation": "La Patagonia oferece paisajes únicos en el mundo. Viajar en auto permite una conexión profunda con a la naturaleza, cruzando fronteras y desafiando límites tecnológicos.",
        "tab1": "🗺️ Rutas y Puntos de Parada (Tesla vs Tucson)",
        "tab2": "🔬 Especificaciones y Costos",
        "footer": "Proyecto desarrollado para Portafolio - Amauri Almeida"
    }
}

# Seleção de idioma na barra lateral
lang = st.sidebar.selectbox("Language / Idioma", ["PT", "EN", "ES"])
t = translations[lang]

# ── INJEÇÃO DE ESTILOS CSS CUSTOMIZADOS (DESIGN PREMIUM) ───────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&family=DM+Mono&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.hero-wrap {
  background: linear-gradient(135deg, #2D3A4A 0%, #1A3A6E 50%, #1E4A8A 100%);
  border-radius: 20px; padding: 2.5rem; margin-bottom: 2rem; color: white;
}
.hero-title { font-family: 'Playfair Display', serif; font-size: 2.6rem; font-weight: 900; line-height: 1.2; }
.hero-subtitle { font-size: 1.1rem; opacity: 0.85; margin-top: 0.5rem; }
.metric-box {
  background: white; border-radius: 16px; padding: 1.2rem; border-top: 4px solid #3A7ACA;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06); text-align: center; margin-bottom: 1rem;
}
.metric-val { font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 900; color: #1A3A6E; }
.metric-label { font-size: 0.75rem; color: #6A7888; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.2rem;}
</style>
""", unsafe_allow_html=True)

# Cabeçalho Principal (Hero Section)
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-title">{t['title']}</div>
    <div class="hero-subtitle">{t['subtitle']}</div>
</div>
""", unsafe_allow_html=True)

# Informações de Motivação na Barra Lateral
st.sidebar.markdown(f"### {t['why_go']}")
st.sidebar.write(t["motivation"])

# Menu de Abas Simplificado (Aba de fotos removida)
tab1, tab2 = st.tabs([t["tab1"], t["tab2"]])

# ── ABA 1: MAPAS E TRAJETOS SIMULTÂNEOS ─────────────────────
with tab1:
    st.markdown(f"### {t['route_map']}")
    
    if os.path.exists('route_data.json'):
        with open('route_data.json', 'r') as f:
            route_data = json.load(f)
        
        # Gerar mapa interativo
        m = folium.Map(location=[-34.6037, -58.3816], zoom_start=4, tiles='CartoDB positron')
        
        # Linha do trajeto unificado (Mooca -> Uruguaiana -> Sul)
        points = [[c['lat'], c['lon']] for c in route_data]
        folium.PolyLine(points, color="#1A3A6E", weight=3, opacity=0.8, tooltip="Trajeto Geral da Expedição").add_to(m)
        
        # Mapeamento dinâmico de ícones por tipo de parada no JSON
        for city in route_data:
            icon_type = "info-sign"
            color_type = "orange"
            prefix_type = "glyphicon"
            
            if city['type'] == "Start":
                icon_type, color_type = "play", "green"
            elif "End" in city['type']:
                icon_type, color_type = "flag", "red"
            elif city['type'] in ["Tesla Charging", "Eletroposto"]:
                icon_type, color_type = "flash", "blue"
            elif city['type'] in ["Gas Station", "Posto Gasolina", "Posto"]:
                icon_type, color_type = "gas-pump", "cadetblue"
                prefix_type = "fa"  # Ativa suporte para ícone de bomba de combustível
            elif city['type'] == "Tesla/Gas":
                icon_type, color_type = "refresh", "purple"
                
            folium.Marker(
                [city['lat'], city['lon']],
                popup=f"<b>{city['name']}</b><br>Tipo: {city['type']}",
                tooltip=f"{city['name']} ({city['type']})",
                icon=folium.Icon(color=color_type, icon=icon_type, prefix=prefix_type)
            ).add_to(m)
        
        st_folium(m, width=1200, height=550)
        
        # Listagem estruturada das coordenadas do trajeto
        st.markdown(f"### {t['details']}")
        df_route = pd.DataFrame(route_data)
        st.dataframe(df_route[['name', 'lat', 'lon', 'type']], use_container_width=True)
    else:
        st.error("Arquivo 'route_data.json' não encontrado no diretório do projeto.")

# ── ABA 2: ESPECIFICAÇÕES TÉCNICAS & ANÁLISE DE CUSTOS ──────────
with tab2:
    st.markdown(f"### {t['vehicle_specs']}")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-val">Tesla Model 3</div>
            <div class="metric-label">2024 Long Range (100% Elétrico)</div>
        </div>
        """, unsafe_allow_html=True)
        st.image("https://www.tesla.com/sites/default/files/model3new/social/model-3-main.jpg", use_container_width=True)
        st.write(f"**{t['tesla_range']}** 550 km")
        st.write("**Bateria:** 78.1 kWh")
        st.write("**Infraestrutura:** Rede de Eletropostos / Conectores CCS2")
        
    with col_v2:
        st.markdown("""
        <div class="metric-box" style="border-top-color: #8B2515;">
            <div class="metric-val" style="color: #8B2515;">Hyundai Tucson</div>
            <div class="metric-label">2024 Engine (Combustão Interna)</div>
        </div>
        """, unsafe_allow_html=True)
        st.image("https://www.hyundai.com/content/dam/hyundai/ww/en/images/find-a-car/tucson/highlights/hyundai-tucson-nx4-highlights-exterior-pc.jpg", use_container_width=True)
        st.write(f"**{t['tucson_range']}** 750 km")
        st.write("**Tanque de Combustível:** 54 L")
        st.write("**Infraestrutura:** Redes de Postos (Ipiranga, YPF, Copec)")

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown(f"### {t['comparison']}")
    
    # Gráfico comparativo Plotly
    fig = go.Figure(data=[
        go.Bar(name='Tesla Model 3 (Charging)', x=['São Paulo ➔ Ushuaia'], y=[450], marker_color='#2D7A3A'),
        go.Bar(name='Hyundai Tucson (Gasoline)', x=['São Paulo ➔ Ushuaia'], y=[1200], marker_color='#8B2515')
    ])
    fig.update_layout(
        barmode='group', 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title="Cost in USD ($)",
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

# Rodapé unificado para portfólio
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6A7888; font-size: 0.85rem; padding: 1rem;">
    {t['footer']} | 
    <a href="https://github.com/amaurialmeida" target="_blank" style="color: #3A7ACA; text-decoration: none;">GitHub</a>
</div>
""", unsafe_allow_html=True)
