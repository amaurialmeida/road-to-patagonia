import streamlit as st
import folium
from folium.plugins import AntPath
from streamlit_folium import st_folium
import pandas as pd
import plotly.graph_objects as go
import json
import os
import base64
import re
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

import requests

st.set_page_config(
    page_title="Expedição Patagônia · Elétrico vs Combustão",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SISTEMA DE IDIOMAS (PT / ES / EN)
# ============================================================
if "lang" not in st.session_state:
    st.session_state.lang = "pt"

TRANSLATIONS = {
    "pt": {
        "page_title": "Expedição Patagônia · Elétrico vs Combustão",
        "hero_tag": "PESQUISA DE CAMPO CIENTÍFICA & AUTOMOTIVA · 2024–2026",
        "hero_title": "Expedição Patagônia:\nElétrico vs Combustão",
        "hero_subtitle": "Simulação autônoma em tempo real: o veículo percorre a rota sozinho de São Paulo (Mooca) ao Fim do Mundo (Ushuaia & Puerto Williams) com opção de Pausa e Inspeção de Paradas.",
        "badge1": "🔋 Tesla Model 3 Long Range", "badge2": "⛽ Hyundai Tucson 2.0", "badge3": "🇧🇷 🇺🇾 🇦🇷 🇨🇱 4 Países",
        "badge4": "~5.100 KM", "badge5": "13 Pontos Mapeados",
        "nav_title": "Navegação da Expedição",
        "nav_home": "🌟 Visão Geral & Painel",
        "nav_map": "🗺️ Modo Auto-Drive & Frota Animada",
        "nav_stops": "📍 Diário de Bordo & Paradas",
        "nav_specs": "🔬 Ficha Técnica & Custos",
        "nav_tech": "⚙️ Metodologia & Dados",
        "m1": "Distância Total (Ida)", "m2": "Custo Estimado (Tesla)", "m3": "Custo Estimado (Tucson)", "m4": "Economia do Elétrico",
        "map_label": "MODO AUTO-DRIVE ATIVO", "map_title": "Veículo Autônomo em Rota: Condução Contínua com Pause/Play",
        "map_hint": "🕹️ <strong>Controle de Condução:</strong> O veículo anda sozinho pela rota patagônica. Use os botões abaixo para <strong>Pausar</strong> ou <strong>Retomar</strong> a viagem a qualquer momento, e clique em qualquer marcador para inspecionar os detalhes da parada.",
        "details_label": "ESTAÇÕES DA ROTA", "details_title": "Raio-X dos Pontos de Parada",
        "specs_label": "ANÁLISE COMPARATIVA", "specs_title": "Custos, Emissões e Desafios Logísticos",
        "why_go_title": "Por que esta expedição importa?",
        "why_go_text": "A transição energética para a mobilidade elétrica enfrenta seu teste definitivo nas rodovias remotas da América do Sul. O modo Auto-Drive permite acompanhar a viagem de forma contínua, simulando o ritmo real de condução e os desafios de autonomia.",
        "route_overview_title": "Itinerário Completo da Rota",
        "route_overview_text": "Início: São Paulo (Mooca), BR → Curitiba → Florianópolis → Porto Alegre → Chuí (Fronteira Brasil-Uruguai) → Punta del Este → Buenos Aires → Bahía Blanca → Puerto Madryn → Comodoro Rivadavia → Río Gallegos → Fim 1: Ushuaia (Argentina) → Fim 2: Puerto Williams (Chile, Isla Navarino).",
        "tech_label": "TECNOLOGIAS & PILHA DE DADOS",
        "footer_title": "🚗 Amauri Almeida · Pesquisador & Autor",
        "footer_desc": "Tecnólogo em Gestão Ambiental (FATEC Jundiaí) · Pós-Graduando em IA, Machine Learning & Data Science e Big Data<br>Análise e Desenvolvimento de Sistemas (FACINT Maringá)",
        "footer_links": "📍 Brasil · Uruguai · Argentina · Chile",
    },
    "es": {
        "page_title": "Expedición Patagonia · Eléctrico vs Combustión",
        "hero_tag": "INVESTIGACIÓN DE CAMPO CIENTÍFICA & AUTOMOTOR · 2024–2026",
        "hero_title": "Expedición Patagonia:\nEléctrico vs Combustión",
        "hero_subtitle": "Simulación autónoma en tiempo real: el vehículo recorre la ruta solo desde São Paulo (Mooca) hasta el Fin del Mundo con opción de pausa e inspección.",
        "badge1": "🔋 Tesla Model 3 Long Range", "badge2": "⛽ Hyundai Tucson 2.0", "badge3": "🇧🇷 🇺🇾 🇦🇷 🇨🇱 4 Países",
        "badge4": "~5.100 KM", "badge5": "13 Puntos Mapeados",
        "nav_title": "Navegación de la Expedición",
        "nav_home": "🌟 Visión General & Panel",
        "nav_map": "🗺️ Modo Auto-Drive & Flota Animada",
        "nav_stops": "📍 Diario de Ruta & Paradas",
        "nav_specs": "🔬 Ficha Técnica & Costos",
        "nav_tech": "⚙️ Metodología & Datos",
        "m1": "Distancia Total", "m2": "Costo Estimado (Tesla)", "m3": "Costo Estimado (Tucson)", "m4": "Ahorro del Eléctrico",
        "map_label": "MODO AUTO-DRIVE ACTIVO", "map_title": "Conducción Autónoma en Ruta: Movimiento Continuo",
        "map_hint": "🕹️ <strong>Control:</strong> El vehículo avanza solo. Use los botones para Pausar o Reanudar.",
        "details_label": "ESTACIONES DE LA RUTA", "details_title": "Rayos X de los Puntos de Parada",
        "specs_label": "ANÁLISIS COMPARATIVO", "specs_title": "Costos y Desafíos",
        "why_go_title": "¿Por qué importa esta expedición?",
        "why_go_text": "La transición energética hacia la movilidad eléctrica.",
        "route_overview_title": "Itinerario Completo",
        "route_overview_text": "Inicio: São Paulo → Ushuaia → Puerto Williams.",
        "tech_label": "TECNOLOGÍAS",
        "footer_title": "🚗 Amauri Almeida",
        "footer_desc": "Investigador",
        "footer_links": "📍 Brasil · Uruguay · Argentina · Chile",
    },
    "en": {
        "page_title": "Patagonia Expedition · Electric vs Combustion",
        "hero_tag": "SCIENTIFIC FIELD RESEARCH & AUTOMOTIVE · 2024–2026",
        "hero_title": "Patagonia Expedition:\nElectric vs Combustion",
        "hero_subtitle": "Autonomous real-time simulation: the vehicle drives along the route automatically from São Paulo to the End of the World with pause and inspection options.",
        "badge1": "🔋 Tesla Model 3 Long Range", "badge2": "⛽ Hyundai Tucson 2.0", "badge3": "🇧🇷 🇺🇾 🇦🇷 🇨🇱 4 Countries",
        "badge4": "~5,000 KM", "badge5": "13 Mapped Points",
        "nav_title": "Expedition Navigation",
        "nav_home": "🌟 Overview & Dashboard",
        "nav_map": "🗺️ Auto-Drive Mode & Animated Fleet",
        "nav_stops": "📍 Expedition Log & Stops",
        "nav_specs": "🔬 Tech Specs & Costs",
        "nav_tech": "⚙️ Methodology & Data",
        "m1": "Total Distance", "m2": "Estimated Cost (Tesla)", "m3": "Estimated Cost (Tucson)", "m4": "EV Savings",
        "map_label": "ACTIVE AUTO-DRIVE MODE", "map_title": "Autonomous Route Driving: Continuous Motion with Pause/Play",
        "map_hint": "🕹️ <strong>Driving Control:</strong> The vehicle drives itself along the Patagonian route. Use the buttons below to <strong>Pause</strong> or <strong>Resume</strong> the journey anytime.",
        "details_label": "ROUTE STATIONS", "details_title": "X-Ray of Stop Points",
        "specs_label": "COMPARATIVE ANALYSIS", "specs_title": "Costs & Challenges",
        "why_go_title": "Why does this expedition matter?",
        "why_go_text": "The energy transition toward electric mobility.",
        "route_overview_title": "Complete Route Itinerary",
        "route_overview_text": "Start: São Paulo → Ushuaia → Puerto Williams.",
        "tech_label": "TECHNOLOGIES",
        "footer_title": "🚗 Amauri Almeida",
        "footer_desc": "Researcher",
        "footer_links": "📍 Brazil · Uruguay · Argentina · Chile",
    }
}

# ============================================================
# ESTILOS CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono&display=swap');

:root {
    --primary: #1b3b6f;
    --primary-light: #218380;
    --accent: #ffb703;
    --ice: #e0fbfc;
    --dark: #0b132b;
    --card-bg: #ffffff;
    --text-main: #1d3557;
    --text-muted: #64748b;
    --danger: #e63946;
    --success: #2a9d8f;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text-main);
}

.stApp {
    background: linear-gradient(180deg, #f8fafc 0%, #edf2f7 100%);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b132b 0%, #1b3b6f 100%);
    color: white;
}
[data-testid="stSidebar"] .stRadio label {
    color: #e2e8f0 !important;
    font-weight: 500;
}

.hero-wrap {
    background: linear-gradient(135deg, #0b132b 0%, #1b3b6f 50%, #218380 100%);
    border-radius: 24px;
    padding: 3.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(11, 19, 43, 0.25);
}
.hero-wrap::after {
    content: "🚗";
    font-size: 160px;
    position: absolute;
    right: 20px;
    bottom: -30px;
    opacity: 0.15;
}
.hero-tag {
    background: rgba(255, 183, 3, 0.2);
    color: #ffb703;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 6px 14px;
    border-radius: 6px;
    display: inline-block;
    margin-bottom: 1.2rem;
    border: 1px solid rgba(255, 183, 3, 0.4);
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 900;
    color: #ffffff;
    line-height: 1.15;
    margin-bottom: 1rem;
    white-space: pre-line;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: rgba(255, 255, 255, 0.85);
    max-width: 720px;
    line-height: 1.6;
    margin-bottom: 1.8rem;
}
.hero-badges {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}
.badge {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #ffffff;
    font-size: 0.78rem;
    font-family: 'JetBrains Mono', monospace;
    padding: 6px 14px;
    border-radius: 30px;
}
.badge-highlight {
    background: rgba(42, 157, 143, 0.3);
    border-color: #2a9d8f;
    color: #99f6e4;
}

.metric-box {
    background: var(--card-bg);
    border-radius: 18px;
    padding: 1.5rem;
    border-top: 4px solid var(--primary-light);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.04);
    text-align: center;
}
.metric-box.danger { border-top-color: var(--danger); }
.metric-box.success { border-top-color: var(--success); }
.metric-val {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 900;
    color: var(--primary);
    line-height: 1.1;
    margin-bottom: 0.4rem;
}
.metric-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
}

.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--primary-light);
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 0.4rem;
    font-weight: 700;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 1.5rem;
}

.info-card {
    background: var(--card-bg);
    border-radius: 18px;
    padding: 1.8rem;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.04);
    border-left: 5px solid var(--primary-light);
    margin-bottom: 1.2rem;
}
.alert-box {
    background: #e0fbfc;
    border-left: 5px solid var(--primary-light);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin: 1.2rem 0;
    font-size: 0.92rem;
    color: #0b132b;
}

.footer-wrap {
    background: linear-gradient(135deg, #0b132b 0%, #1b3b6f 100%);
    border-radius: 20px;
    padding: 2.5rem;
    color: rgba(255, 255, 255, 0.85);
    text-align: center;
    margin-top: 4rem;
}
.footer-title {
    font-family: 'Playfair Display', serif;
    color: #ffb703;
    font-size: 1.4rem;
    margin-bottom: 0.6rem;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 🌐 Idioma / Language")
    selected_lang = st.selectbox(
        "Selecione o idioma:",
        options=["pt", "es", "en"],
        format_func=lambda x: {"pt": "🇧🇷 Português", "es": "🇪🇸 Español", "en": "🇺🇸 English"}[x],
        index=["pt", "es", "en"].index(st.session_state.lang)
    )
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

    T = TRANSLATIONS[st.session_state.lang]

    st.markdown("---")
    st.markdown(f"### {T['nav_title']}")
    nav_choice = st.radio(
        "Navegação",
        options=[T["nav_home"], T["nav_map"], T["nav_stops"], T["nav_specs"], T["nav_tech"]],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 🚗 Frota Auto-Drive")
    st.info("🔋 **Tesla Model 3** (Autônomo)\n\n⛽ **Hyundai Tucson** (Autônomo)")
    st.markdown("---")
    st.markdown("### 🇦🇺 Rota Transnacional")
    st.markdown("🇧🇷 **Brasil** ➔ 🇺🇾 **Uruguai** ➔ 🇦🇷 **Argentina** ➔ 🇨🇱 **Chile**")

# ============================================================
# DADOS E IMAGENS
# ============================================================
@st.cache_data
def load_route_data():
    path = "route_data_enhanced.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

route_data = load_route_data()

@st.cache_data(ttl=86400, show_spinner=False)
def load_economics(refresh_online=True):
    """Carrega o snapshot local e tenta atualizar fontes públicas no máximo uma vez por dia."""
    with open("route_economics.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data["runtime"] = {
        "loaded_at": datetime.now(timezone.utc).astimezone().strftime("%d/%m/%Y %H:%M"),
        "online_attempted": bool(refresh_online),
        "online_updates": [],
        "online_errors": []
    }
    if not refresh_online:
        return data

    headers = {"User-Agent": "Road-to-Patagonia/2.0 (research dashboard)"}

    def parse_number(value):
        value = str(value).strip()
        if "," in value and "." in value:
            if value.rfind(",") > value.rfind("."):
                value = value.replace(".", "").replace(",", ".")
            else:
                value = value.replace(",", "")
        elif "," in value:
            value = value.replace(",", ".")
        return float(value)

    def update_gpp(code, fuel, url, currency, label):
        try:
            html = requests.get(url, headers=headers, timeout=3).text
            text = re.sub(r"\s+", " ", html.replace("&nbsp;", " "))
            pattern = rf"The current {fuel} price in .*? is {currency}\s*([0-9,.]+) per liter.*?updated on ([0-9]{{2}}-[A-Za-z]{{3}}-[0-9]{{4}})"
            match = re.search(pattern, text, flags=re.I)
            if match:
                data["prices"][code][fuel] = parse_number(match.group(1))
                data["prices"][code]["collected_at"] = datetime.strptime(match.group(2), "%d-%b-%Y").strftime("%Y-%m-%d")
                data["prices"][code]["source"] = label
                data["prices"][code]["source_url"] = url
                data["runtime"]["online_updates"].append(f"{code}:{fuel}")
        except Exception as exc:
            data["runtime"]["online_errors"].append(f"{code}:{fuel}:{type(exc).__name__}")

    gpp_tasks = [
        ("BR", "gasoline", "https://www.globalpetrolprices.com/Brazil/gasoline_prices/", "BRL", "GlobalPetrolPrices / referência ANP"),
        ("AR", "gasoline", "https://www.globalpetrolprices.com/Argentina/gasoline_prices/", "ARS", "GlobalPetrolPrices / Secretaría de Energía"),
        ("CL", "gasoline", "https://www.globalpetrolprices.com/Chile/gasoline_prices/", "CLP", "GlobalPetrolPrices / CNE"),
        ("CL", "diesel", "https://www.globalpetrolprices.com/Chile/diesel_prices/", "CLP", "GlobalPetrolPrices / CNE")
    ]
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(update_gpp, *task) for task in gpp_tasks]
        for future in futures:
            future.result()

    try:
        html = requests.get("https://www.ancap.com.uy/10564/1/historico-precios-combustibles.html", headers=headers, timeout=3).text
        text = re.sub(r"\s+", " ", html)
        row = re.search(r"01/08/2026\s+([0-9]+,[0-9]+)\s+([0-9]+,[0-9]+)\s+([0-9]+,[0-9]+)", text)
        if row:
            data["prices"]["UY"]["gasoline"] = parse_number(row.group(1))
            data["prices"]["UY"]["diesel"] = parse_number(row.group(3))
            data["prices"]["UY"]["collected_at"] = "2026-08-01"
            data["runtime"]["online_updates"].append("UY:ANCAP")
    except Exception as exc:
        data["runtime"]["online_errors"].append(f"UY:ANCAP:{type(exc).__name__}")
    return data

with st.sidebar:
    refresh_online = st.checkbox("🔄 Tentar atualização diária das fontes", value=True, help="Consulta fontes públicas quando disponível. Os dados são armazenados em cache por 24 horas e preservam o último snapshot se uma fonte falhar.")
    if st.button("Atualizar preços agora"):
        load_economics.clear()
        st.rerun()

economics = load_economics(refresh_online)

with st.sidebar:
    st.markdown("### 💱 Câmbio de referência")
    st.caption("Edite para aproximar a simulação da data da sua viagem. Os preços continuam exibidos na moeda local.")
    fx = {
        "BR": st.number_input("1 USD em BRL", min_value=0.01, value=5.50, step=0.05, key="fx_brl"),
        "UY": st.number_input("1 USD em UYU", min_value=0.01, value=40.00, step=0.50, key="fx_uyu"),
        "AR": st.number_input("1 USD em ARS", min_value=0.01, value=1485.00, step=10.00, key="fx_ars"),
        "CL": st.number_input("1 USD em CLP", min_value=0.01, value=910.00, step=5.00, key="fx_clp")
    }

COUNTRY_CODE = {
    "Brasil": "BR", "Brasil / Uruguai": "BR", "Uruguai": "UY",
    "Argentina": "AR", "Chile": "CL"
}


def country_for_stop(stop):
    country = stop.get("country", "")
    if country == "Brasil / Uruguai":
        return "UY" if stop.get("id", 0) >= 5 else "BR"
    return COUNTRY_CODE.get(country, "AR")


def distance_km(value):
    match = re.search(r"([0-9,.]+)", str(value))
    return float(match.group(1).replace(".", "").replace(",", ".")) if match else 0.0


def money(value, code):
    symbols = {"BR": "R$", "UY": "$U", "AR": "$", "CL": "$"}
    decimals = 0 if code in {"AR", "CL"} else 2
    return f"{symbols.get(code, '')} {value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def usd(value, code):
    return value / fx[code]


def build_segment_costs(route, econ):
    assumptions = econ["assumptions"]
    rows = []
    previous = None
    for stop in route:
        total_km = distance_km(stop.get("distance_from_start", "0"))
        if previous is None:
            previous = {"name": stop["name"], "total_km": total_km, "code": country_for_stop(stop)}
            continue
        code = country_for_stop(stop)
        # A fronteira Chuí passa a ser tratada como Uruguai a partir da parada 5.
        km = max(total_km - previous["total_km"], 0)
        is_water_crossing = previous["name"].startswith("Ushuaia") and stop["name"].startswith("Puerto Williams")
        drive_km = 0 if is_water_crossing else km
        price = econ["prices"][code]
        tucson_l = drive_km / assumptions["tucson_km_per_litre"]
        tesla_kwh = drive_km * assumptions["tesla_kwh_per_100km"] / 100 * (1 + assumptions["tesla_charge_loss"])
        gas_cost = tucson_l * price["gasoline"]
        ev_cost = tesla_kwh * price["electricity_kwh"]
        rows.append({
            "Trecho": f"{previous['name']} → {stop['name']}",
            "Destino": stop["name"],
            "País": price["country"],
            "Moeda": price["currency"],
            "km": km,
            "drive_km": drive_km,
            "modal": "Água / ferry" if is_water_crossing else "Rodovia",
            "gas_price": price["gasoline"],
            "elec_price": price["electricity_kwh"],
            "gas_cost": gas_cost,
            "ev_cost": ev_cost,
            "gas_l": tucson_l,
            "tesla_kwh": tesla_kwh,
            "tucson_co2": tucson_l * assumptions["gasoline_co2_kg_per_litre"],
            "tesla_co2": tesla_kwh * assumptions["grid_co2_kg_per_kwh"][code],
            "price_date": price["collected_at"],
            "price_source": price["source"],
            "code": code
        })
        previous = {"name": stop["name"], "total_km": total_km, "code": code}
    return pd.DataFrame(rows)


def ferry_costs(econ):
    records = []
    for ferry in econ["ferries"]:
        code = "AR" if ferry["currency"] == "ARS" else None
        vehicle_cost = ferry.get("indicative_vehicle_fare", 0)
        passenger_cost = ferry.get("passenger_fare", 0) + ferry.get("port_fee", 0)
        records.append({
            "Travessia": ferry["name"],
            "Trecho": ferry["route"],
            "Operador": ferry["operator"],
            "Veículo embarca": "Sim" if ferry.get("vehicle_included") else "Não",
            "Tarifa veículo": money(vehicle_cost, code) if code else "—",
            "Passageiro + taxa": f"US$ {passenger_cost:,.0f}" if passenger_cost else "—",
            "Duração": f"{ferry['duration_minutes']} min",
            "Status": ferry["status"]
        })
    return pd.DataFrame(records)


def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return ""

img_tesla_front = f"data:image/png;base64,{get_image_base64('tesla_front.png')}"
img_tesla_back = f"data:image/png;base64,{get_image_base64('tesla_back.png')}"
img_tucson_front = f"data:image/png;base64,{get_image_base64('tucson_front.png')}"
img_tucson_back = f"data:image/png;base64,{get_image_base64('tucson_back.png')}"

segment_df = build_segment_costs(route_data, economics)
if not segment_df.empty:
    total_tucson_cost = float(segment_df["gas_cost"].sum())
    total_tesla_cost = float(segment_df["ev_cost"].sum())
    total_tucson_co2 = float(segment_df["tucson_co2"].sum())
    total_tesla_co2 = float(segment_df["tesla_co2"].sum())
else:
    total_tucson_cost = total_tesla_cost = total_tucson_co2 = total_tesla_co2 = 0.0

total_tesla_usd_home = sum(usd(v, c) for v, c in zip(segment_df["ev_cost"], segment_df["code"])) if not segment_df.empty else 0.0
total_tucson_usd_home = sum(usd(v, c) for v, c in zip(segment_df["gas_cost"], segment_df["code"])) if not segment_df.empty else 0.0

# ============================================================
# HERO
# ============================================================
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-tag">{T['hero_tag']}</div>
    <div class="hero-title">{T['hero_title']}</div>
    <div class="hero-subtitle">{T['hero_subtitle']}</div>
    <div class="hero-badges">
        <span class="badge badge-highlight">{T['badge1']}</span>
        <span class="badge badge-highlight">{T['badge2']}</span>
        <span class="badge">{T['badge3']}</span>
        <span class="badge">{T['badge4']}</span>
        <span class="badge">{T['badge5']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SEÇÃO 1: HOME ───────────────────────────────────────────
if nav_choice == T["nav_home"]:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-box"><div class="metric-val">~5.100 km</div><div class="metric-label">{T["m1"]}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-box success"><div class="metric-val">US$ {total_tesla_usd_home:,.0f}</div><div class="metric-label">{T["m2"]}</div></div>'.replace(",", "."), unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-box danger"><div class="metric-val">US$ {total_tucson_usd_home:,.0f}</div><div class="metric-label">{T["m3"]}</div></div>'.replace(",", "."), unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-box"><div class="metric-val">2.7×</div><div class="metric-label">{T["m4"]}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.2, 1])
    with col_l:
        st.markdown(f'<div class="section-label">CONTEXTO DA PESQUISA</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">{T["why_go_title"]}</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-card">
            <p style="line-height: 1.7; font-size: 0.98rem; color: #1d3557;">
            {T['why_go_text']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown(f'<div class="section-label">ROTA MUNDIAL DO FIM DO MUNDO</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">De São Paulo à Isla Navarino</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-card" style="border-left-color: #218380;">
            <strong>{T['route_overview_title']}</strong><br><br>
            <p style="font-size: 0.9rem; color: #334155; line-height: 1.6;">
            {T['route_overview_text']}
            </p>
        </div>
        """, unsafe_allow_html=True)

# ── SEÇÃO 2: MODO AUTO-DRIVE COM PAUSE/PLAY & INTERATIVIDADE ──────────────
elif nav_choice == T["nav_map"]:
    st.markdown(f'<div class="section-label">{T["map_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["map_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="alert-box">{T["map_hint"]}</div>', unsafe_allow_html=True)

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        selected_car = st.selectbox(
            "🚗 Selecione o Veículo Autônomo:",
            options=["Tesla Model 3 Long Range", "Hyundai Tucson 2.0"],
            format_func=lambda x: "🔋 Tesla Model 3 (Elétrico Autônomo)" if "Tesla" in x else "⛽ Hyundai Tucson (Combustão Autônomo)"
        )
    with col_c2:
        selected_direction = st.selectbox(
            "🔄 Sentido da Viagem Auto-Drive:",
            options=["Ida (São Paulo ➔ Ushuaia / Puerto Williams)", "Volta (Puerto Williams / Ushuaia ➔ São Paulo)"],
            format_func=lambda x: "⬇️ Rumo ao Fim do Mundo (De Frente)" if "Ida" in x else "⬆️ Retorno a São Paulo (De Costas)"
        )

    if route_data:
        is_tesla = "Tesla" in selected_car
        is_outbound = "Ida" in selected_direction

        if is_tesla:
            car_img_data = img_tesla_front if is_outbound else img_tesla_back
        else:
            car_img_data = img_tucson_front if is_outbound else img_tucson_back

        points = [[c['lat'], c['lon']] for c in route_data]
        if not is_outbound:
            points = list(reversed(points))

        m = folium.Map(location=[-40, -62], zoom_start=4, tiles='CartoDB positron')

        folium.PolyLine(points, color="#1b3b6f", weight=3, opacity=0.4, tooltip="Rota da Expedição").add_to(m)

        AntPath(
            points,
            color="#218380" if is_outbound else "#e63946",
            weight=5,
            opacity=0.85,
            delay=1200,
            dash_array=[15, 25],
            pulse_color="#ffffff",
            tooltip="Malha Rodoviária Ativa"
        ).add_to(m)

        for stop in route_data:
            icon_name, icon_color, prefix_val = "info-sign", "blue", "glyphicon"
            if stop['type'] == "Start":
                icon_name, icon_color = "play", "green"
            elif "End" in stop['type']:
                icon_name, icon_color = "flag", "red"
            elif "Tesla" in stop['type'] or "Grid" in stop['type']:
                icon_name, icon_color = "flash", "cadetblue"
            elif "Gas" in stop['type'] or "Fuel" in stop['type']:
                icon_name, icon_color = "gas-pump", "orange", "fa"

            popup_html = f"""
            <div style="font-family: 'Plus Jakarta Sans'; width: 220px; padding: 5px;">
                <h4 style="margin: 0 0 5px 0; color: #1b3b6f; font-family: 'Playfair Display';">{stop['name']}</h4>
                <p style="margin: 3px 0; font-size: 12px;"><b>País:</b> {stop['country']}</p>
                <p style="margin: 3px 0; font-size: 12px;"><b>Distância:</b> {stop['distance_from_start']}</p>
                <p style="margin: 3px 0; font-size: 12px; color: #218380;"><i>{stop['highlights']}</i></p>
            </div>
            """
            folium.Marker(
                [stop['lat'], stop['lon']],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"#{stop['id']} - {stop['name']}",
                icon=folium.Icon(color=icon_color, icon=icon_name, prefix=prefix_val)
            ).add_to(m)

        # Script JS com Auto-Drive (Loop automático) e botões de Pause / Resume inspirados na referência do Globo
        route_js_points = json.dumps(points)
        car_animation_js = f"""
        <div id="autodrive-controls" style="margin-bottom: 10px; display: flex; gap: 10px; align-items: center; background: #ffffff; padding: 10px 15px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
            <span style="font-family: 'JetBrains Mono'; font-size: 12px; font-weight: 700; color: #1b3b6f;">🎮 CONTROLE AUTO-DRIVE:</span>
            <button id="btnPause" onclick="toggleDrive()" style="background: #e63946; color: white; border: none; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 12px;">⏸️ Pausar Viagem</button>
            <span id="driveStatus" style="font-size: 12px; color: #2a9d8f; font-weight: 600;">Status: Veículo andando sozinho 🚗💨</span>
        </div>

        <script>
        var isDriving = true;
        function toggleDrive() {{
            isDriving = !isDriving;
            var btn = document.getElementById('btnPause');
            var status = document.getElementById('driveStatus');
            if (isDriving) {{
                btn.style.background = '#e63946';
                btn.innerHTML = '⏸️ Pausar Viagem';
                status.style.color = '#2a9d8f';
                status.innerHTML = 'Status: Veículo andando sozinho 🚗💨';
            }} else {{
                btn.style.background = '#2a9d8f';
                btn.innerHTML = '▶️ Retomar Viagem';
                status.style.color = '#e63946';
                status.innerHTML = 'Status: Viagem pausada (Clique nos marcadores para inspecionar) 🛑';
            }}
        }}

        (function() {{
            function initAutoDrive() {{
                var mapContainer = null;
                var mapKeys = Object.keys(window).filter(function(k) {{ return k.indexOf('map_') === 0; }});
                for (var i = 0; i < mapKeys.length; i++) {{
                    if (window[mapKeys[i]] && window[mapKeys[i]]._container) {{
                        mapContainer = window[mapKeys[i]];
                    }}
                }}
                if (!mapContainer) {{ setTimeout(initAutoDrive, 300); return; }}

                var routePoints = {route_js_points};
                var carIcon = L.divIcon({{
                    html: '<div style="background: rgba(255,255,255,0.95); padding: 4px; border-radius: 50%; box-shadow: 0 4px 12px rgba(0,0,0,0.35);"><img src="{car_img_data}" style="width: 55px; height: 38px; object-fit: contain; transform: translate(-50%, -50%); display: block;" /></div>',
                    className: 'custom-car-autodrive',
                    iconSize: [55, 38],
                    iconAnchor: [27, 19]
                }});

                var carMarker = L.marker(routePoints[0], {{icon: carIcon, zIndexOffset: 3000}}).addTo(mapContainer);

                var segIndex = 0;
                var steps = 140; // Ritmo suave e devagar
                var stepCount = 0;

                function lerp(a, b, t) {{ return a + (b - a) * t; }}

                function driveStep() {{
                    if (isDriving) {{
                        var start = routePoints[segIndex];
                        var end = routePoints[(segIndex + 1) % routePoints.length];
                        var progress = stepCount / steps;
                        var lat = lerp(start[0], end[0], progress);
                        var lon = lerp(start[1], end[1], progress);
                        carMarker.setLatLng([lat, lon]);

                        stepCount++;
                        if (stepCount > steps) {{
                            stepCount = 0;
                            segIndex = (segIndex + 1) % routePoints.length; // Loop infinito automático
                        }}
                    }}
                    setTimeout(function() {{ requestAnimationFrame(driveStep); }}, 90);
                }}
                driveStep();
            }}
            setTimeout(initAutoDrive, 600);
        }})();
        </script>
        """
        m.get_root().html.add_child(folium.Element(car_animation_js))
        st_folium(m, width=1250, height=620)
    else:
        st.error("Dados da rota não encontrados.")

# ── SEÇÃO 3: PARADAS ───────────────────────────────────────
elif nav_choice == T["nav_stops"]:
    st.markdown(f'<div class="section-label">{T["details_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["details_title"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-box">Cada parada combina contexto geográfico, infraestrutura, preços de referência e os riscos operacionais do próximo trecho. Clique também nos marcadores do mapa para abrir o mesmo contexto durante o Auto-Drive.</div>', unsafe_allow_html=True)

    selected_stop = st.selectbox("Selecione uma parada da expedição:", options=[s['name'] for s in route_data])
    stop_info = next((s for s in route_data if s['name'] == selected_stop), route_data[0])
    stop_row = segment_df[segment_df["Destino"] == selected_stop].iloc[0] if not segment_df[segment_df["Destino"] == selected_stop].empty else None
    code = country_for_stop(stop_info)
    price = economics["prices"][code]

    col_a, col_b = st.columns([1.15, 1])
    with col_a:
        st.markdown(f"""
        <div class="info-card">
            <h3>📍 #{stop_info['id']} — {stop_info['name']}</h3>
            <p><b>País / moeda:</b> {stop_info['country']} · {price['currency']}</p>
            <p><b>Distância acumulada:</b> {stop_info['distance_from_start']}</p>
            <p><b>Elevação:</b> {stop_info['elevation']}</p>
            <p><b>Clima:</b> verão {stop_info['climate_summer']} · inverno {stop_info['climate_winter']}</p>
            <p><b>Recarga:</b> {stop_info['charging_infra']}</p>
            <p><b>Combustível:</b> {stop_info['gas_infra']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="info-card" style="border-left-color: #ffb703;">
            <h3>🔍 Contexto de campo</h3>
            <p>{stop_info['highlights']}</p>
            <p><b>Desafio logístico:</b> {stop_info['logistics']}</p>
        </div>
        """, unsafe_allow_html=True)

    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.metric("Gasolina/nafta", money(price["gasoline"], code) + "/L")
    with p2:
        st.metric("Diesel/gasoil", money(price["diesel"], code) + "/L")
    with p3:
        st.metric("Recarga pública", money(price["electricity_kwh"], code) + "/kWh")
    with p4:
        st.metric("Data do preço", price["collected_at"])

    if stop_row is not None:
        st.markdown("#### Custos estimados do trecho que chega a esta parada")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Distância", f"{stop_row['km']:,.0f} km".replace(",", "."))
        c2.metric("Tucson", money(stop_row["gas_cost"], code))
        c3.metric("Tesla", money(stop_row["ev_cost"], code))
        c4.metric("CO₂ evitado", f"{max(stop_row['tucson_co2'] - stop_row['tesla_co2'], 0):,.0f} kg".replace(",", "."))
    else:
        st.info("Esta é a origem da expedição; o primeiro trecho começa aqui.")

# ── SEÇÃO 4: SPECS & CUSTOS ────────────────────────────────
elif nav_choice == T["nav_specs"]:
    st.markdown(f'<div class="section-label">{T["specs_label"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Dossiê Financeiro, Energético e Ambiental</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-box">Os valores abaixo são uma simulação auditável: o preço por litro/kWh tem data e fonte, o câmbio é editável e as tarifas de balsa aparecem separadas para não confundir passagem de passageiro com embarque do veículo.</div>', unsafe_allow_html=True)

    # Resumo financeiro em USD usando o câmbio informado na barra lateral.
    total_tesla_usd = sum(usd(row["ev_cost"], row["code"]) for _, row in segment_df.iterrows()) if not segment_df.empty else 0
    total_tucson_usd = sum(usd(row["gas_cost"], row["code"]) for _, row in segment_df.iterrows()) if not segment_df.empty else 0
    saving_usd = total_tucson_usd - total_tesla_usd
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tesla — energia", f"US$ {total_tesla_usd:,.0f}".replace(",", "."))
    m2.metric("Tucson — gasolina", f"US$ {total_tucson_usd:,.0f}".replace(",", "."))
    m3.metric("Diferença estimada", f"US$ {saving_usd:,.0f}".replace(",", "."))
    m4.metric("CO₂ operacional evitado", f"{max(total_tucson_co2 - total_tesla_co2, 0):,.0f} kg".replace(",", "."))

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown(f"""
        <div class="info-card" style="border-left-color: #2a9d8f;">
            <h3>🔋 Tesla Model 3 Long Range</h3>
            <p><b>Consumo modelado:</b> {economics['assumptions']['tesla_kwh_per_100km']:.1f} kWh/100 km + {economics['assumptions']['tesla_charge_loss']:.0%} de perdas de recarga.</p>
            <p><b>Energia da viagem:</b> {segment_df['tesla_kwh'].sum():,.0f} kWh</p>
            <p><b>CO₂ da eletricidade:</b> {total_tesla_co2:,.0f} kg</p>
            <p><b>Premissa:</b> a tarifa pública por kWh varia por rede; o valor exibido pode ser alterado na base de dados.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_v2:
        st.markdown(f"""
        <div class="info-card" style="border-left-color: #e63946;">
            <h3>⛽ Hyundai Tucson 2.0</h3>
            <p><b>Consumo modelado:</b> {economics['assumptions']['tucson_km_per_litre']:.1f} km/L.</p>
            <p><b>Gasolina consumida:</b> {segment_df['gas_l'].sum():,.0f} L</p>
            <p><b>CO₂ direto:</b> {total_tucson_co2:,.0f} kg</p>
            <p><b>Fator aplicado:</b> {economics['assumptions']['gasoline_co2_kg_per_litre']:.3f} kg CO₂/L, conforme referência EPA/IPCC.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### Comparação de custo por segmento")
    if not segment_df.empty:
        chart_df = segment_df[["Destino", "gas_cost", "ev_cost"]].copy()
        chart_df["Tucson"] = [usd(v, c) for v, c in zip(segment_df["gas_cost"], segment_df["code"])]
        chart_df["Tesla"] = [usd(v, c) for v, c in zip(segment_df["ev_cost"], segment_df["code"])]
        fig = go.Figure(data=[
            go.Bar(name="Tesla — eletricidade", x=chart_df["Destino"], y=chart_df["Tesla"], marker_color="#2a9d8f"),
            go.Bar(name="Tucson — gasolina", x=chart_df["Destino"], y=chart_df["Tucson"], marker_color="#e63946")
        ])
        fig.update_layout(barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", yaxis_title="US$ por trecho", xaxis_title="Próxima parada", height=460)
        st.plotly_chart(fig, use_container_width=True)

        table = segment_df[["Trecho", "País", "modal", "km", "drive_km", "gas_price", "elec_price", "gas_cost", "ev_cost", "price_date"]].copy()
        table.columns = ["Trecho", "País", "Modal", "km da rota", "km rodoviários", "Gasolina/nafta (local/L)", "Energia (local/kWh)", "Tucson (local)", "Tesla (local)", "Data"]
        st.dataframe(table, use_container_width=True, hide_index=True)

    st.markdown("#### Travessias por água e custos que não são rodoviários")
    ferry_table = ferry_costs(economics)
    st.dataframe(ferry_table, use_container_width=True, hide_index=True)
    first_angostura = economics["ferries"][0]
    beagle = economics["ferries"][1]
    ferry_vehicle_usd = first_angostura["indicative_vehicle_fare"] / fx["AR"]
    beagle_passenger_usd = beagle["passenger_fare"] + beagle["port_fee"]
    f1, f2, f3 = st.columns(3)
    f1.metric("Balsa + veículo", f"US$ {ferry_vehicle_usd:,.0f}".replace(",", "."))
    f2.metric("Canal Beagle — 1 passageiro", f"US$ {beagle_passenger_usd:,.0f}".replace(",", "."))
    f3.metric("Transporte do carro no Beagle", "Cotação especial")
    st.caption("A balsa Primera Angostura é modelada como embarque do veículo. O cruce Ushuaia–Puerto Williams aparece como serviço de passageiros: o app não soma automaticamente o transporte do Tesla/Tucson porque o embarque do carro exige cotação específica.")

    st.markdown("#### Preços observados por país")
    market_rows = []
    for code, item in economics["prices"].items():
        market_rows.append({
            "País": item["country"],
            "Gasolina/nafta": f"{money(item['gasoline'], code)}/L",
            "Diesel/gasoil": f"{money(item['diesel'], code)}/L",
            "Recarga pública (hipótese)": f"{money(item['electricity_kwh'], code)}/kWh",
            "Última coleta": item["collected_at"],
            "Frequência": item["frequency"],
            "Fonte": item["source"]
        })
    st.dataframe(pd.DataFrame(market_rows), use_container_width=True, hide_index=True)
    st.caption(f"Última tentativa de atualização da sessão: {economics['runtime']['loaded_at']}. Atualizações online aceitas: {', '.join(economics['runtime']['online_updates']) or 'nenhuma; usando snapshot local'}.")

# ── SEÇÃO 5: METODOLOGIA ───────────────────────────────────
elif nav_choice == T["nav_tech"]:
    st.markdown(f'<div class="section-label">{T["tech_label"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Metodologia, fontes e limites da simulação</div>', unsafe_allow_html=True)
    st.markdown("<div class='info-card'>O painel combina rota geográfica, um snapshot local versionado e tentativas de atualização online com cache de 24 horas. Se uma fonte falhar, o último valor válido continua visível junto da data de coleta; isso é mais seguro do que apagar o dado ou inventar um preço.</div>", unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    with a1:
        st.markdown("#### Hipóteses editáveis")
        assumptions = economics["assumptions"]
        assumptions_df = pd.DataFrame([
            {"Parâmetro": "Tesla — consumo", "Valor": f"{assumptions['tesla_kwh_per_100km']:.1f} kWh/100 km"},
            {"Parâmetro": "Tesla — perdas de recarga", "Valor": f"{assumptions['tesla_charge_loss']:.0%}"},
            {"Parâmetro": "Tucson — consumo", "Valor": f"{assumptions['tucson_km_per_litre']:.1f} km/L"},
            {"Parâmetro": "Gasolina — CO₂ direto", "Valor": f"{assumptions['gasoline_co2_kg_per_litre']:.3f} kg/L"},
            {"Parâmetro": "Diesel — CO₂ direto", "Valor": f"{assumptions['diesel_co2_kg_per_litre']:.3f} kg/L"}
        ])
        st.dataframe(assumptions_df, use_container_width=True, hide_index=True)
    with a2:
        st.markdown("#### Fatores de eletricidade por país")
        grid_df = pd.DataFrame([{"País": economics["prices"][c]["country"], "Hipótese": f"{v:.2f} kg CO₂/kWh"} for c, v in assumptions["grid_co2_kg_per_kwh"].items()])
        st.dataframe(grid_df, use_container_width=True, hide_index=True)
        st.caption(assumptions["assumption_note"])

    st.markdown("#### Fontes consultadas")
    sources_df = pd.DataFrame(economics["sources"])
    st.dataframe(sources_df, use_container_width=True, hide_index=True)
    st.markdown("#### Status da atualização nesta sessão")
    st.json(economics["runtime"])

# RODAPÉ
st.markdown(f"""
<div class="footer-wrap">
    <div class="footer-title">{T['footer_title']}</div>
    <p style="margin: 0.5rem 0; font-size: 0.92rem;">{T['footer_desc']}</p>
    <p style="margin: 1rem 0; font-size: 0.85rem;">{T['footer_links']} &nbsp;|&nbsp; 🌐 <a href="https://amaurialmeida.github.io/environmental-portfolio/" style="color:#ffb703">Portfólio</a></p>
</div>
""", unsafe_allow_html=True)
