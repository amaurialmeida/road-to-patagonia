import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import json
import os
from PIL import Image

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
        "route_map": "Mapa da Rota e Pontos de Recarga",
        "comparison": "Comparativo de Custo (Estimativa USD)",
        "tesla_range": "Autonomia Tesla (Est.):",
        "tucson_range": "Autonomia Tucson (Est.):",
        "total_dist": "Distância Total Aprox.:",
        "stops": "Principais Pontos de Parada",
        "charging_points": "Pontos de Recarga Tesla",
        "gas_stations": "Postos de Combustível",
        "cost_est": "Estimativa de Custo (Energia vs Gasolina)",
        "footer": "Projeto desenvolvido para Portfólio - Amauri Almeida",
        "details": "Detalhamento das Coordenadas da Rota",
        "why_go": "Por que ir para a Patagônia?",
        "motivation": "A Patagônia oferece paisagens únicas no mundo. Viajar de carro permite uma conexão profunda com a natureza, cruzando fronteiras e desafiando limites tecnológicos.",
        "tab1": "🗺️ Rota & Mapa Interativo",
        "tab2": "🔬 Especificações & Custos",
        "tab3": "📷 Registro Visual de Campo",
        "field_instructions_title": "📁 Gerenciamento de Ativos de Imagem",
        "field_instructions": "Para renderizar suas fotografias da expedição, armazene-as no diretório <code>assets/campo/</code> respeitando a nomenclatura indicada.",
    },
    "EN": {
        "title": "Patagonia Expedition: Electric vs Combustion",
        "subtitle": "From São Paulo (Mooca) to the End of the World (Ushuaia & Puerto Williams)",
        "vehicle_specs": "Vehicle Specifications",
        "route_map": "Route Map & Charging Points",
        "comparison": "Trip Cost Comparison (Estimated USD)",
        "tesla_range": "Tesla Range (Est.):",
        "tucson_range": "Tucson Range (Est.):",
        "total_dist": "Total Approx. Distance:",
        "stops": "Main Stop Points",
        "charging_points": "Tesla Charging Points",
        "gas_stations": "Gas Stations",
        "cost_est": "Cost Estimate (Energy vs Gas)",
        "footer": "Project developed for Portfolio - Amauri Almeida",
        "details": "Route Coordinates Breakdown",
        "why_go": "Why go to Patagonia?",
        "motivation": "Patagonia offers unique landscapes. Traveling by car allows a deep connection with nature, crossing borders and challenging technological limits.",
        "tab1": "🗺️ Route & Interactive Map",
        "tab2": "🔬 Specs & Financial Analysis",
        "tab3": "📷 Field Visual Record",
        "field_instructions_title": "📁 Static Photo Asset Management",
        "field_instructions": "To render your custom field images, store them inside the <code>assets/campo/</code> workspace folder using the proper filenames.",
    },
    "ES": {
        "title": "Expedición Patagonia: Eléctrico vs Combustión",
        "subtitle": "De São Paulo (Mooca) al Fin del Mundo (Ushuaia & Puerto Williams)",
        "vehicle_specs": "Especificaciones de los Vehículos",
        "route_map": "Mapa de Ruta y Puntos de Carga",
        "comparison": "Comparativa de Costo (Estimación USD)",
        "tesla_range": "Autonomía Tesla (Est.):",
        "tucson_range": "Autonomía Tucson (Est.):",
        "total_dist": "Distancia Total Aprox.:",
        "stops": "Principales Puntos de Parada",
        "charging_points": "Puntos de Carga Tesla",
        "gas_stations": "Estaciones de Servicio",
        "cost_est": "Estimación de Costo (Energía vs Nafta)",
        "footer": "Proyecto desarrollado para Portafolio - Amauri Almeida",
        "details": "Detalles de las Coordenadas de la Ruta",
        "why_go": "¿Por qué ir a la Patagonia?",
        "motivation": "La Patagonia ofrece paisajes únicos en el mundo. Viajar en auto permite una conexión profunda con la naturaleza, cruzando fronteras y desafiando límites tecnológicos.",
        "tab1": "🗺️ Ruta y Mapa Interactivo",
        "tab2": "🔬 Especificaciones y Costos",
        "tab3": "📷 Registro Visual de Campo",
        "field_instructions_title": "📁 Gestión de Activos de Imagen",
        "field_instructions": "Para renderizar sus fotografías de expedición, almacénelas en el directorio <code>assets/campo/</code> respetando la nomenclatura indicada.",
    }
}

# Seleção de idioma na barra lateral elegante
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
.info-card { background: white; border-radius: 16px; padding: 1.5rem; box-shadow: 0 2px 12px rgba(0,0,0,0.05); border-left: 4px solid #3A7ACA; margin-bottom: 1rem; }
.info-card.amber { border-left-color: #C47D0E; }
.photo-placeholder {
  background: #EEF4FF; border: 2px dashed #3A7ACA; border-radius: 12px; padding: 2rem;
  text-align: center; min-height: 200px; display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.photo-title { font-weight: 600; color: #1A3A6E; margin-top: 0.5rem; }
.photo-path { font-size: 0.65rem; color: #2555A0; font-family: 'DM Mono', monospace; margin-top: 0.5rem; background: #D8EAF8; padding: 3px 8px; border-radius: 4px; }
.photo-legenda { font-size: 0.72rem; color: #6A7888; font-style: italic; padding: 0.5rem; text-align: center; }
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

# Configuração das Abas de Navegação Moderna
tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

# ── ABAS 1: MAPA DA EXPEDIÇÃO & COORDENADAS ─────────────────────
with tab1:
    st.markdown(f"### {t['route_map']}")
    
    # Carregar dados da rota de forma segura com tratamento de erro
    if os.path.exists('route_data.json'):
        with open('route_data.json', 'r') as f:
            route_data = json.load(f)
        
        # Criação e renderização do mapa Folium
        m = folium.Map(location=[-34.6037, -58.3816], zoom_start=4, tiles='CartoDB positron')
        
        # Traçar linha azul conectando os pontos
        points = [[c['lat'], c['lon']] for c in route_data]
        folium.PolyLine(points, color="#1A3A6E", weight=3, opacity=0.8).add_to(m)
        
        # Inserção dinâmica de marcadores configurados
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
        
        st_folium(m, width=1200, height=550)
        
        # Detalhamento da tabela estruturada de dados geográficos
        st.markdown(f"### {t['details']}")
        df_route = pd.DataFrame(route_data)
        st.dataframe(df_route[['name', 'lat', 'lon', 'type']], use_container_width=True)
    else:
        st.error("Arquivo 'route_data.json' não encontrado no diretório raiz do projeto.")

# ── ABAS 2: ESPECIFICAÇÕES TÉCNICAS & COMPARAÇÃO FINANCEIRA ─────
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
        st.write("**Recarga Rápida:** 250 kW (CCS2)")
        
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
        st.write("**Consumo Médio (Estrada):** 14 km/l")

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown(f"### {t['comparison']}")
    
    # Gráfico Financeiro Customizado via Plotly
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

# ── ABAS 3: DIÁRIO FOTOGRÁFICO DE CAMPO ─────────────────────────
with tab3:
    st.markdown(f"### {t['tab3']}")
    st.markdown(f"""
    <div class="info-card amber">
      <strong>{t['field_instructions_title']}</strong><br>
      <div style="font-size:0.85rem;color:#5C3D1E;margin-top:0.3rem">{t['field_instructions']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Registro de cards dinâmicos estruturados com placeholders inteligentes
    photos_data = [
        {"emoji": "🇧🇷", "titulo": "Partida — São Paulo (Mooca)", "path": "assets/campo/01_sao_paulo.jpg", "desc": "Ponto zero da expedição continental testando a resiliência energética urbana inicial."},
        {"emoji": "🇦🇷", "titulo": "Travessia Pampas — Argentina", "path": "assets/campo/02_pampas.jpg", "desc": "Retas infinitas colocando à prova a estabilidade de consumo em velocidade de cruzeiro."},
        {"emoji": "🏔️", "titulo": "Chegada — Ushuaia", "path": "assets/campo/03_ushuaia.jpg", "desc": "O Fim do Mundo alcançado. Desafios de recarga elétrica sob temperaturas severas de congelamento."},
        {"emoji": "🏁", "titulo": "Ponto Final — Puerto Williams", "path": "assets/campo/04_puerto_williams.jpg", "desc": "A fronteira mais austral do planeta atingida com sucesso na Ilha Navarino."},
    ]

    col_img = st.columns(4)
    for idx, foto in enumerate(photos_data):
        with col_img[idx]:
            if os.path.exists(foto["path"]):
                try:
                    st.image(Image.open(foto["path"]), use_container_width=True)
                except Exception:
                    st.error(f"Erro ao ler imagem.")
            else:
                st.markdown(f"""
                <div class="photo-placeholder">
                  <div style="font-size: 2.5rem;">{foto['emoji']}</div>
                  <div class="photo-title">{foto['titulo']}</div>
                  <div style="font-size: 0.8rem; color: #6A7888; margin: 0.5rem 0;">{foto['desc']}</div>
                  <div class="photo-path">{foto['path']}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"<div class='photo-legenda'>{foto['titulo']}</div>", unsafe_allow_html=True)

# Rodapé institucional unificado de encerramento do Portfólio
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6A7888; font-size: 0.85rem; padding: 1rem;">
    {t['footer']} | 
    <a href="https://github.com/amaurialmeida" target="_blank" style="color: #3A7ACA; text-decoration: none;">GitHub</a>
</div>
""", unsafe_allow_html=True)
