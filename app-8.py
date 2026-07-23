import streamlit as st
import folium
from folium.plugins import AntPath
from streamlit_folium import st_folium
import pandas as pd
import plotly.graph_objects as go
import json
import os

st.set_page_config(
    page_title="Expedição Patagônia · Elétrico vs Combustão",
    page_icon="🚗",
    layout="wide"
)

# ============================================================
# SISTEMA DE IDIOMAS
# ============================================================
if "lang" not in st.session_state:
    st.session_state.lang = "pt"

TRANSLATIONS = {
    "pt": {
        "page_title": "Expedição Patagônia · Elétrico vs Combustão",
        "hero_tag": "Pesquisa de Campo · Automotivo & Energia · 2024–2026",
        "hero_title": "Expedição Patagônia:\nElétrico vs Combustão",
        "hero_subtitle": "De São Paulo (Mooca) ao Fim do Mundo (Ushuaia & Puerto Williams). Um trajeto real de ~5.000 km cruzando 4 países, comparando um Tesla Model 3 elétrico contra um Hyundai Tucson a combustão, ponto a ponto.",
        "badge1": "🔋 Tesla Model 3", "badge2": "⛽ Hyundai Tucson", "badge3": "BR · UY · AR · CL",
        "badge4": "~5.000 KM", "badge5": "13 PONTOS MAPEADOS",
        "protocol_title": "📋 Nota Metodológica:",
        "protocol_text": "Os custos de viagem apresentados são estimativas de trip-level baseadas em especificações dos veículos e preços regionais médios de energia/combustível — não faturamento medido em tempo real. Ver detalhamento na aba de Especificações & Custos.",
        "m1": "Distância total", "m2": "Custo estimado Tesla", "m3": "Custo estimado Tucson", "m4": "Economia do elétrico",
        "tab1": "🗺️ Rotas & Pontos de Parada", "tab2": "🔬 Especificações & Custos",
        "map_label": "VISUALIZAÇÃO GEOESPACIAL", "map_title": "Mapa de Rotas, Carregadores (Tesla) & Postos de Gasolina (Tucson)",
        "map_hint": "🚗 <strong>Interação:</strong> Clique em qualquer marcador para ver o tipo de parada. O carro no mapa percorre o trajeto real da expedição, ponto a ponto.",
        "details_label": "DETALHAMENTO", "details_title": "Coordenadas e Pontos de Parada",
        "specs_label": "FICHA TÉCNICA", "specs_title": "Especificações dos Veículos",
        "tesla_range": "Autonomia estimada:", "tucson_range": "Autonomia estimada:",
        "tesla_battery": "Bateria:", "tucson_tank": "Tanque de combustível:",
        "tesla_infra": "Infraestrutura:", "tucson_infra": "Infraestrutura:",
        "comparison_label": "ANÁLISE FINANCEIRA", "comparison_title": "Comparativo de Custo Estimado (USD)",
        "why_go_title": "Por que ir para a Patagônia?",
        "why_go_text": "A Patagônia oferece paisagens únicas no mundo. Viajar de carro permite uma conexão profunda com a natureza, cruzando fronteiras e desafiando limites tecnológicos — e testando, na prática, os limites reais da mobilidade elétrica em uma rota remota.",
        "route_overview_title": "Visão Geral do Trajeto",
        "route_overview_text": "Início → São Paulo (Mooca), BR<br>Trajeto → Curitiba → Florianópolis → Porto Alegre → Chuí (fronteira BR/UY)<br>→ Punta del Este → Buenos Aires → Bahía Blanca → Puerto Madryn<br>→ Comodoro Rivadavia → Río Gallegos<br>Fim (AR) → Ushuaia, Argentina<br>Fim (CL) → Puerto Williams, Chile",
        "tech_label": "TECNOLOGIAS UTILIZADAS",
        "footer_title": "🚗 Amauri Almeida",
        "footer_desc": "Tecnólogo em Gestão Ambiental · FATEC Jundiaí (3º ENADE)<br>Pós-Graduação em IA, Machine Learning & Data Science · Pós-Graduação em Ciência de Dados & Big Data<br>Análise e Desenvolvimento de Sistemas · FACINT Maringá",
        "footer_links": "📍 Brasil · Uruguai · Argentina · Chile",
    },
    "es": {
        "page_title": "Expedición Patagonia · Eléctrico vs Combustión",
        "hero_tag": "Investigación de Campo · Automotor & Energía · 2024–2026",
        "hero_title": "Expedición Patagonia:\nEléctrico vs Combustión",
        "hero_subtitle": "De São Paulo (Mooca) al Fin del Mundo (Ushuaia & Puerto Williams). Un trayecto real de ~5.000 km cruzando 4 países, comparando un Tesla Model 3 eléctrico contra un Hyundai Tucson a combustión, punto a punto.",
        "badge1": "🔋 Tesla Model 3", "badge2": "⛽ Hyundai Tucson", "badge3": "BR · UY · AR · CL",
        "badge4": "~5.000 KM", "badge5": "13 PUNTOS MAPEADOS",
        "protocol_title": "📋 Nota Metodológica:",
        "protocol_text": "Los costos de viaje presentados son estimaciones a nivel de trayecto basadas en especificaciones de los vehículos y precios regionales promedio de energía/combustible — no facturación medida en tiempo real. Ver detalle en la pestaña de Especificaciones y Costos.",
        "m1": "Distancia total", "m2": "Costo estimado Tesla", "m3": "Costo estimado Tucson", "m4": "Ahorro del eléctrico",
        "tab1": "🗺️ Rutas y Puntos de Parada", "tab2": "🔬 Especificaciones y Costos",
        "map_label": "VISUALIZACIÓN GEOESPACIAL", "map_title": "Mapa de Ruta, Cargadores (Tesla) y Estaciones de Servicio (Tucson)",
        "map_hint": "🚗 <strong>Interacción:</strong> Haga clic en cualquier marcador para ver el tipo de parada. El auto en el mapa recorre el trayecto real de la expedición, punto a punto.",
        "details_label": "DETALLE", "details_title": "Coordenadas y Puntos de Parada",
        "specs_label": "FICHA TÉCNICA", "specs_title": "Especificaciones de los Vehículos",
        "tesla_range": "Autonomía estimada:", "tucson_range": "Autonomía estimada:",
        "tesla_battery": "Batería:", "tucson_tank": "Tanque de combustible:",
        "tesla_infra": "Infraestructura:", "tucson_infra": "Infraestructura:",
        "comparison_label": "ANÁLISIS FINANCIERO", "comparison_title": "Comparativa de Costo Estimado (USD)",
        "why_go_title": "¿Por qué ir a la Patagonia?",
        "why_go_text": "La Patagonia ofrece paisajes únicos en el mundo. Viajar en auto permite una conexión profunda con la naturaleza, cruzando fronteras y desafiando límites tecnológicos — probando en la práctica los límites reales de la movilidad eléctrica en una ruta remota.",
        "route_overview_title": "Visión General del Trayecto",
        "route_overview_text": "Inicio → São Paulo (Mooca), BR<br>Trayecto → Curitiba → Florianópolis → Porto Alegre → Chuí (frontera BR/UY)<br>→ Punta del Este → Buenos Aires → Bahía Blanca → Puerto Madryn<br>→ Comodoro Rivadavia → Río Gallegos<br>Fin (AR) → Ushuaia, Argentina<br>Fin (CL) → Puerto Williams, Chile",
        "tech_label": "TECNOLOGÍAS UTILIZADAS",
        "footer_title": "🚗 Amauri Almeida",
        "footer_desc": "Tecnólogo en Gestión Ambiental · FATEC Jundiaí (3° ENADE)<br>Posgrado en IA, Machine Learning & Data Science · Posgrado en Ciencia de Datos & Big Data<br>Análisis y Desarrollo de Sistemas · FACINT Maringá",
        "footer_links": "📍 Brasil · Uruguay · Argentina · Chile",
    },
    "en": {
        "page_title": "Patagonia Expedition · Electric vs Combustion",
        "hero_tag": "Field Research · Automotive & Energy · 2024–2026",
        "hero_title": "Patagonia Expedition:\nElectric vs Combustion",
        "hero_subtitle": "From São Paulo (Mooca) to the End of the World (Ushuaia & Puerto Williams). A real ~5,000 km route crossing 4 countries, comparing an electric Tesla Model 3 against a combustion Hyundai Tucson, point by point.",
        "badge1": "🔋 Tesla Model 3", "badge2": "⛽ Hyundai Tucson", "badge3": "BR · UY · AR · CL",
        "badge4": "~5,000 KM", "badge5": "13 MAPPED POINTS",
        "protocol_title": "📋 Methodological Note:",
        "protocol_text": "Trip costs shown are trip-level estimates based on vehicle specifications and average regional energy/fuel prices — not real-time metered billing. See breakdown in the Specs & Costs tab.",
        "m1": "Total distance", "m2": "Estimated Tesla cost", "m3": "Estimated Tucson cost", "m4": "EV savings",
        "tab1": "🗺️ Routes & Stop Points", "tab2": "🔬 Specs & Costs",
        "map_label": "GEOSPATIAL VISUALIZATION", "map_title": "Route Map, Chargers (Tesla) & Gas Stations (Tucson)",
        "map_hint": "🚗 <strong>Interaction:</strong> Click any marker to see the stop type. The car on the map travels the expedition's real route, point by point.",
        "details_label": "BREAKDOWN", "details_title": "Coordinates & Stop Points",
        "specs_label": "TECH SHEET", "specs_title": "Vehicle Specifications",
        "tesla_range": "Estimated range:", "tucson_range": "Estimated range:",
        "tesla_battery": "Battery:", "tucson_tank": "Fuel tank:",
        "tesla_infra": "Infrastructure:", "tucson_infra": "Infrastructure:",
        "comparison_label": "FINANCIAL ANALYSIS", "comparison_title": "Estimated Cost Comparison (USD)",
        "why_go_title": "Why go to Patagonia?",
        "why_go_text": "Patagonia offers unique landscapes. Traveling by car allows a deep connection with nature, crossing borders and challenging technological limits — testing, in practice, the real limits of electric mobility on a remote route.",
        "route_overview_title": "Route Overview",
        "route_overview_text": "Start → São Paulo (Mooca), BR<br>Waypoints → Curitiba → Florianópolis → Porto Alegre → Chuí (BR/UY border)<br>→ Punta del Este → Buenos Aires → Bahía Blanca → Puerto Madryn<br>→ Comodoro Rivadavia → Río Gallegos<br>End (AR) → Ushuaia, Argentina<br>End (CL) → Puerto Williams, Chile",
        "tech_label": "TECHNOLOGIES USED",
        "footer_title": "🚗 Amauri Almeida",
        "footer_desc": "Environmental Management Technologist · FATEC Jundiaí (3rd ENADE)<br>Post-Grad in AI, Machine Learning & Data Science · Post-Grad in Data Science & Big Data<br>Systems Analysis and Development · FACINT Maringá",
        "footer_links": "📍 Brazil · Uruguay · Argentina · Chile",
    },
}

# ============================================================
# SELETOR DE IDIOMA — TOPO
# ============================================================
def render_lang_selector():
    col_space, col_pt, col_es, col_en = st.columns([8, 1, 1, 1])
    with col_pt:
        if st.button("🇧🇷 PT", use_container_width=True,
                     type="primary" if st.session_state.lang == "pt" else "secondary"):
            st.session_state.lang = "pt"
            st.rerun()
    with col_es:
        if st.button("🇪🇸 ES", use_container_width=True,
                     type="primary" if st.session_state.lang == "es" else "secondary"):
            st.session_state.lang = "es"
            st.rerun()
    with col_en:
        if st.button("🇺🇸 EN", use_container_width=True,
                     type="primary" if st.session_state.lang == "en" else "secondary"):
            st.session_state.lang = "en"
            st.rerun()

render_lang_selector()
T = TRANSLATIONS[st.session_state.lang]

# ============================================================
# ESTILOS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&family=DM+Mono&display=swap');
:root{--electric:#3A7ACA;--electric-dark:#1A3A6E;--night:#17324A;--night-mid:#1E4A8A;--cream:#F7F9FC;--warm-gray:#6A7888;--danger:#8B2515;--danger-soft:#F8E3DC;--black:#0D1117;}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background-color:var(--cream);color:var(--black);}
.hero-wrap{background:linear-gradient(135deg,var(--night) 0%,var(--electric-dark) 60%,var(--night-mid) 100%);border-radius:20px;padding:3rem 2.5rem 2rem;margin-bottom:2rem;position:relative;overflow:hidden;}
.hero-wrap::before{content:"🚗";font-size:180px;position:absolute;right:-20px;top:-20px;opacity:0.06;}
.hero-tag{background:var(--electric);color:white;font-family:'DM Mono',monospace;font-size:0.7rem;font-weight:bold;letter-spacing:2px;padding:4px 12px;border-radius:4px;display:inline-block;margin-bottom:1rem;text-transform:uppercase;}
.hero-title{font-family:'Playfair Display',serif;font-size:2.8rem;font-weight:900;color:#fff;line-height:1.15;margin-bottom:0.8rem;white-space:pre-line;}
.hero-subtitle{font-size:1rem;color:rgba(255,255,255,0.75);max-width:600px;line-height:1.6;margin-bottom:1.5rem;}
.hero-badges{display:flex;gap:10px;flex-wrap:wrap;}
.badge{background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.85);font-size:0.72rem;font-family:'DM Mono',monospace;padding:5px 12px;border-radius:20px;letter-spacing:0.5px;}
.badge-electric{background:rgba(58,122,202,0.25);border-color:var(--electric);color:#BFDBFF;}
.metric-box{background:white;border-radius:16px;padding:1.4rem 1.2rem;border-top:4px solid var(--electric);box-shadow:0 2px 12px rgba(0,0,0,0.06);text-align:center;}
.metric-box.danger{border-top-color:var(--danger);}
.metric-box.forest{border-top-color:#2D7A3A;}
.metric-val{font-family:'Playfair Display',serif;font-size:2.1rem;font-weight:900;color:var(--electric-dark);line-height:1;margin-bottom:0.3rem;}
.metric-label{font-size:0.75rem;color:var(--warm-gray);text-transform:uppercase;letter-spacing:1px;}
.section-label{font-family:'DM Mono',monospace;font-size:0.65rem;color:var(--electric);text-transform:uppercase;letter-spacing:3px;margin-bottom:0.3rem;}
.section-title{font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:700;color:var(--electric-dark);margin-bottom:1.2rem;line-height:1.2;}
.info-card{background:white;border-radius:16px;padding:1.5rem;box-shadow:0 2px 12px rgba(0,0,0,0.05);border-left:4px solid var(--electric);margin-bottom:1rem;}
.info-card.danger{border-left-color:var(--danger);}
.alert-box{background:#EAF1FB;border-left:4px solid var(--electric);border-radius:8px;padding:1rem 1.2rem;margin:1rem 0;font-size:0.9rem;}
.source-badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:0.8rem;}
.source-badge{background:var(--electric-dark);color:white;font-family:'DM Mono',monospace;font-size:0.65rem;padding:4px 10px;border-radius:4px;letter-spacing:1px;text-transform:uppercase;}
.footer-wrap{background:var(--electric-dark);border-radius:20px;padding:2rem;color:rgba(255,255,255,0.8);text-align:center;margin-top:3rem;}
.footer-title{font-family:'Playfair Display',serif;color:#6FA8FF;font-size:1.2rem;margin-bottom:0.5rem;}
.map-hint-icon{font-size:1rem;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HERO
# ============================================================
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-tag">{T['hero_tag']}</div>
    <div class="hero-title">{T['hero_title']}</div>
    <div class="hero-subtitle">{T['hero_subtitle']}</div>
    <div class="hero-badges">
        <span class="badge badge-electric">{T['badge1']}</span>
        <span class="badge badge-electric">{T['badge2']}</span>
        <span class="badge">{T['badge3']}</span>
        <span class="badge">{T['badge4']}</span>
        <span class="badge">{T['badge5']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""<div class="alert-box"><strong>{T['protocol_title']}</strong> {T['protocol_text']}</div>""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown(f'<div class="metric-box"><div class="metric-val">~5.000 km</div><div class="metric-label">{T["m1"]}</div></div>', unsafe_allow_html=True)
with col2: st.markdown(f'<div class="metric-box forest"><div class="metric-val">$450</div><div class="metric-label">{T["m2"]}</div></div>', unsafe_allow_html=True)
with col3: st.markdown(f'<div class="metric-box danger"><div class="metric-val">$1.200</div><div class="metric-label">{T["m3"]}</div></div>', unsafe_allow_html=True)
with col4: st.markdown(f'<div class="metric-box"><div class="metric-val">2.7×</div><div class="metric-label">{T["m4"]}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# ABAS
# ============================================================
tab1, tab2 = st.tabs([T['tab1'], T['tab2']])

# ── TAB 1: MAPA ──────────────────────────────────────────────
with tab1:
    st.markdown(f'<div class="section-label">{T["map_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["map_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card">{T["map_hint"]}</div>', unsafe_allow_html=True)

    if os.path.exists('route_data.json'):
        with open('route_data.json', 'r') as f:
            route_data = json.load(f)

        m = folium.Map(location=[-38, -60], zoom_start=4, tiles='CartoDB positron')

        points = [[c['lat'], c['lon']] for c in route_data]

        # Trajeto de base (linha sólida discreta)
        folium.PolyLine(points, color="#1A3A6E", weight=2, opacity=0.35).add_to(m)

        # Trajeto "formiga" — sensação de movimento constante ao longo da rota
        AntPath(
            points,
            color="#3A7ACA",
            weight=4,
            opacity=0.9,
            delay=800,
            dash_array=[12, 20],
            pulse_color="#FFFFFF",
            tooltip="Trajeto Geral da Expedição"
        ).add_to(m)

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
            elif city['type'] in ["Gas Station", "Posto Gasolina", "Posto", "Gas"]:
                icon_type, color_type = "gas-pump", "cadetblue"
                prefix_type = "fa"
            elif city['type'] == "Tesla/Gas":
                icon_type, color_type = "refresh", "purple"

            folium.Marker(
                [city['lat'], city['lon']],
                popup=f"<b>{city['name']}</b><br>Tipo: {city['type']}",
                tooltip=f"{city['name']} ({city['type']})",
                icon=folium.Icon(color=color_type, icon=icon_type, prefix=prefix_type)
            ).add_to(m)

        # ── CARRO TESLA ANIMADO PERCORRENDO O TRAJETO REAL ──────
        route_js_points = json.dumps(points)
        car_animation_js = f"""
        <script>
        (function() {{
            function initCarAnimation() {{
                var mapContainer = null;
                var mapKeys = Object.keys(window).filter(function(k) {{ return k.indexOf('map_') === 0; }});
                for (var i = 0; i < mapKeys.length; i++) {{
                    if (window[mapKeys[i]] && window[mapKeys[i]]._container) {{
                        mapContainer = window[mapKeys[i]];
                    }}
                }}
                if (!mapContainer) {{ setTimeout(initCarAnimation, 300); return; }}

                var routePoints = {route_js_points};
                var carIcon = L.divIcon({{
                    html: '<div style="font-size:26px; transform: translate(-50%,-50%); filter: drop-shadow(0 2px 3px rgba(0,0,0,0.45));">🚗</div>',
                    className: 'tesla-car-icon',
                    iconSize: [26, 26],
                    iconAnchor: [13, 13]
                }});
                var carMarker = L.marker(routePoints[0], {{icon: carIcon, zIndexOffset: 1000}}).addTo(mapContainer);

                var segIndex = 0;
                var steps = 60;
                var stepCount = 0;

                function lerp(a, b, t) {{ return a + (b - a) * t; }}

                function animate() {{
                    var start = routePoints[segIndex];
                    var end = routePoints[(segIndex + 1) % routePoints.length];
                    var progress = stepCount / steps;
                    var lat = lerp(start[0], end[0], progress);
                    var lon = lerp(start[1], end[1], progress);
                    carMarker.setLatLng([lat, lon]);

                    stepCount++;
                    if (stepCount > steps) {{
                        stepCount = 0;
                        segIndex = (segIndex + 1) % routePoints.length;
                    }}
                    setTimeout(function() {{ requestAnimationFrame(animate); }}, 40);
                }}
                animate();
            }}
            setTimeout(initCarAnimation, 500);
        }})();
        </script>
        """
        m.get_root().html.add_child(folium.Element(car_animation_js))

        st_folium(m, width=1200, height=550)

        st.markdown(f'<div class="section-label" style="margin-top:1.5rem">{T["details_label"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title" style="font-size:1.4rem">{T["details_title"]}</div>', unsafe_allow_html=True)
        df_route = pd.DataFrame(route_data)
        st.dataframe(df_route[['name', 'lat', 'lon', 'type']], use_container_width=True)

        st.markdown(f"""
        <div class="info-card" style="margin-top:1rem">
            <strong>{T['route_overview_title']}</strong><br><br>
            <div style="font-size:0.9rem;color:#3D4D5A;line-height:1.8">{T['route_overview_text']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Arquivo 'route_data.json' não encontrado no diretório do projeto.")

# ── TAB 2: ESPECIFICAÇÕES & CUSTOS ──────────────────────────
with tab2:
    st.markdown(f'<div class="section-label">{T["specs_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["specs_title"]}</div>', unsafe_allow_html=True)

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-val" style="font-size:1.5rem">Tesla Model 3</div>
            <div class="metric-label">2024 Long Range · 100% Elétrico</div>
        </div>
        """, unsafe_allow_html=True)
        st.image("https://www.tesla.com/sites/default/files/model3new/social/model-3-main.jpg", use_container_width=True)
        st.write(f"**{T['tesla_range']}** 550 km")
        st.write(f"**{T['tesla_battery']}** 78.1 kWh")
        st.write(f"**{T['tesla_infra']}** Rede de Eletropostos / Conectores CCS2")

    with col_v2:
        st.markdown("""
        <div class="metric-box danger">
            <div class="metric-val" style="font-size:1.5rem;color:#8B2515">Hyundai Tucson</div>
            <div class="metric-label">2024 · Combustão Interna</div>
        </div>
        """, unsafe_allow_html=True)
        st.image("https://www.hyundai.com/content/dam/hyundai/ww/en/images/find-a-car/tucson/highlights/hyundai-tucson-nx4-highlights-exterior-pc.jpg", use_container_width=True)
        st.write(f"**{T['tucson_range']}** 750 km")
        st.write(f"**{T['tucson_tank']}** 54 L")
        st.write(f"**{T['tucson_infra']}** Redes de Postos (Ipiranga, YPF, Copec)")

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-label">{T["comparison_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title" style="font-size:1.6rem">{T["comparison_title"]}</div>', unsafe_allow_html=True)

    fig = go.Figure(data=[
        go.Bar(name='Tesla Model 3 (Charging)', x=['São Paulo ➔ Ushuaia'], y=[450], marker_color='#2D7A3A'),
        go.Bar(name='Hyundai Tucson (Gasoline)', x=['São Paulo ➔ Ushuaia'], y=[1200], marker_color='#8B2515')
    ])
    fig.update_layout(
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title="USD ($)",
        font=dict(family='DM Sans'),
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class="info-card" style="margin-top:1rem">
        <strong>{T['why_go_title']}</strong><br><br>
        <p style="font-size:0.92rem;color:#3D4D5A;line-height:1.7">{T['why_go_text']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<br><div class='section-label'>{T['tech_label']}</div>", unsafe_allow_html=True)
    techs = ["Python 3.11", "Streamlit", "Folium", "Plotly", "Pandas", "JSON"]
    badges_html = "".join([f'<span class="source-badge">{tech}</span>' for tech in techs])
    st.markdown(f'<div class="source-badges">{badges_html}</div>', unsafe_allow_html=True)

# ============================================================
# RODAPÉ
# ============================================================
st.markdown(f"""
<div class="footer-wrap">
    <div class="footer-title">{T['footer_title']}</div>
    <p style="margin:0.5rem 0;font-size:0.9rem">{T['footer_desc']}</p>
    <p style="margin:1rem 0 0.5rem;font-size:0.85rem;opacity:0.7">
    {T['footer_links']} &nbsp;|&nbsp;
    🌐 <a href="https://amaurialmeida.github.io/environmental-portfolio/" style="color:#6FA8FF">Portfólio</a> &nbsp;|&nbsp;
    🐙 <a href="https://github.com/amaurialmeida" style="color:#6FA8FF">GitHub</a>
    </p>
    <p style="font-size:0.75rem;opacity:0.5;margin:0">© 2024–2026 · Expedição Patagônia · Pesquisa de Campo</p>
</div>
""", unsafe_allow_html=True)
