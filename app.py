import streamlit as st
import folium
from folium.plugins import AntPath
from streamlit_folium import st_folium
import pandas as pd
import plotly.graph_objects as go
import json
import base64
import re
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

import requests

# Textos nos 10 idiomas ficam em translations.py
from translations import TRANSLATIONS

st.set_page_config(
    page_title="Road to Patagonia · Expedição Patagônia",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# IDIOMAS (10) — seletor na barra lateral + 10 botões no topo
# ============================================================
LANGS = [
    ("pt", "🇧🇷", "PT"), ("en", "🇺🇸", "EN"), ("es", "🇪🇸", "ES"),
    ("it", "🇮🇹", "IT"), ("fr", "🇫🇷", "FR"), ("de", "🇩🇪", "DE"),
    ("zh", "🇨🇳", "ZH"), ("ar", "🇸🇦", "AR"), ("el", "🇬🇷", "EL"),
    ("af", "🇿🇦", "AF"),
]
CODES = [c for c, _, _ in LANGS]
FLAGS = {c: f"{flag} {label}" for c, flag, label in LANGS}
NATIVE = {"pt": "🇧🇷 Português", "en": "🇺🇸 English", "es": "🇪🇸 Español", "it": "🇮🇹 Italiano",
          "fr": "🇫🇷 Français", "de": "🇩🇪 Deutsch", "zh": "🇨🇳 中文", "ar": "🇸🇦 العربية",
          "el": "🇬🇷 Ελληνικά", "af": "🇿🇦 Afrikaans"}

DECIMAL = {"pt": ",", "en": ".", "es": ",", "it": ",", "fr": ",", "de": ",", "zh": ".", "ar": ".", "el": ",", "af": ","}
THOUSANDS = {"pt": ".", "en": ",", "es": ".", "it": ".", "fr": " ", "de": ".", "zh": ",", "ar": ",", "el": ".", "af": " "}
PLOTLY_SEP = {"pt": ",.", "en": ".,", "es": ",.", "it": ",.", "fr": ", ", "de": ",.", "zh": ".,", "ar": ".,", "el": ",.", "af": ", "}


def _initial_lang():
    q = st.query_params.get("lang")
    if isinstance(q, list):
        q = q[0] if q else None
    return q if q in CODES else "pt"


def _apply_lang(code):
    st.session_state.lang = code
    st.session_state.lang_pick = code
    st.session_state.lang_sb = code
    st.query_params["lang"] = code


def _on_pills():
    v = st.session_state.get("lang_pick")
    if v in CODES:
        _apply_lang(v)
    else:  # clique repetido desmarca o botão: mantém o idioma atual
        st.session_state.lang_pick = st.session_state.lang


def _on_sidebar():
    v = st.session_state.get("lang_sb")
    if v in CODES:
        _apply_lang(v)


if "lang" not in st.session_state:
    _apply_lang(_initial_lang())

LANG = st.session_state.lang
T = TRANSLATIONS[LANG]
RTL = LANG == "ar"


def numfmt(x, nd=0):
    """Número com separadores decimal e de milhar do idioma."""
    s = f"{x:,.{nd}f}"
    return s.replace(",", "\0").replace(".", DECIMAL[LANG]).replace("\0", THOUSANDS[LANG])


def plot(fig):
    fig.update_layout(separators=PLOTLY_SEP[LANG])
    try:
        st.plotly_chart(fig, width="stretch")
    except TypeError:
        st.plotly_chart(fig, use_container_width=True)


def show_table(df, **kw):
    try:
        st.dataframe(df, width="stretch", hide_index=True, **kw)
    except TypeError:
        st.dataframe(df, use_container_width=True, hide_index=True, **kw)


# ============================================================
# ESTILOS CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono&family=Noto+Serif:wght@700&family=Noto+Sans:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;700&family=Noto+Naskh+Arabic:wght@400;700&display=swap');

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
    font-family: 'Plus Jakarta Sans','Noto Sans','Noto Sans SC','Noto Naskh Arabic', sans-serif;
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
    font-family: 'JetBrains Mono','Noto Sans','Noto Sans SC','Noto Naskh Arabic', monospace;
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
    font-family: 'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic', serif;
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
    font-family: 'JetBrains Mono','Noto Sans','Noto Sans SC','Noto Naskh Arabic', monospace;
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
    font-family: 'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic', serif;
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
    font-family: 'JetBrains Mono','Noto Sans','Noto Sans SC','Noto Naskh Arabic', monospace;
    font-size: 0.7rem;
    color: var(--primary-light);
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 0.4rem;
    font-weight: 700;
}
.section-title {
    font-family: 'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic', serif;
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
    font-family: 'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic', serif;
    color: #ffb703;
    font-size: 1.4rem;
    margin-bottom: 0.6rem;
}
</style>
""", unsafe_allow_html=True)

if RTL:
    st.markdown("""
<style>
[data-testid="stMain"], [data-testid="stAppViewContainer"] .main, [data-testid="stSidebar"] { direction: rtl; text-align: right; }
.hero-wrap, .info-card, .alert-box { direction: rtl; text-align: right; }
.hero-wrap::before, .hero-wrap::after { right: auto; left: 2rem; }
.info-card, .alert-box { border-left: none; border-right: 4px solid var(--primary-light); }
.js-plotly-plot, iframe, .metric-val, [data-testid="stButtonGroup"] { direction: ltr; }
body, html, [class*="css"] { font-family: 'Noto Naskh Arabic','Plus Jakarta Sans',sans-serif; }
</style>""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR — mantida (seletor de idioma + navegação permanentes)
# ============================================================
with st.sidebar:
    st.markdown("### 🌐 Idioma / Language")
    st.selectbox(
        T["lang_select"], options=CODES, format_func=lambda c: NATIVE[c],
        key="lang_sb", on_change=_on_sidebar,
    )

    st.markdown("---")
    st.markdown(f"### {T['nav_title']}")
    NAV = [T["nav_home"], T["nav_map"], T["nav_stops"], T["nav_specs"], T["nav_tech"]]
    nav_idx = st.radio(
        T["nav_aria"], options=list(range(5)), format_func=lambda i: NAV[i],
        key="nav_idx", label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(f"### {T['sb_fleet']}")
    st.info(T["sb_fleet_info"])
    st.markdown("---")
    st.markdown(f"### {T['sb_route']}")
    st.markdown(T["sb_route_text"])

# 10 botões de idioma no topo (mesmo padrão dos demais projetos)
try:
    st.pills(
        "Language", CODES, selection_mode="single", format_func=lambda c: FLAGS[c],
        key="lang_pick", label_visibility="collapsed", on_change=_on_pills,
    )
except AttributeError:  # versões antigas do Streamlit sem st.pills
    st.radio(
        "Language", CODES, format_func=lambda c: FLAGS[c], horizontal=True,
        key="lang_pick", label_visibility="collapsed", on_change=_on_pills,
    )

# ============================================================
# DADOS DA ROTA — São Paulo → Ushuaia (Fim do Mundo 1) → Puerto Williams (Fim do Mundo 2)
# ============================================================
APP_DIR = Path(__file__).resolve().parent

# (nome, lat, lon, tipo, país, km acumulados)
ROUTE_RAW = [
    ("São Paulo (Mooca), BR", -23.5558, -46.6116, "Start", "BR", 0),
    ("Curitiba, BR", -25.4290, -49.2671, "Tesla/Gas", "BR", 408),
    ("Uruguaiana, BR", -29.7618, -57.0853, "Border", "BR", 1358),
    ("Paso de los Libres, AR", -29.7135, -57.0883, "Border", "AR", 1450),
    ("Buenos Aires, AR", -34.6037, -58.3816, "Hub", "AR", 2058),
    ("Bahía Blanca, AR", -38.7183, -62.2663, "Tesla/Gas", "AR", 2718),
    ("Puerto Madryn, AR", -42.7692, -65.0385, "Wildlife/Grid", "AR", 3388),
    ("Punta Tombo, AR", -44.0473, -65.1870, "Wildlife", "AR", 3748),
    ("Comodoro Rivadavia, AR", -45.8641, -67.4808, "Wind/Gas", "AR", 4188),
    ("Río Gallegos, AR", -51.6230, -69.2168, "Gateway", "AR", 4968),
    ("Punta Delgada, CL", -52.4500, -69.5000, "Ferry", "CL", 5138),
    ("Río Grande, AR", -53.7877, -67.7095, "Gas", "AR", 5356),
    ("Ushuaia, AR", -54.8019, -68.3030, "End (AR)", "AR", 5568),
    ("Puerto Williams, CL", -54.9333, -67.6167, "End (CL)", "CL", 5618),
]
WATER_LAST = True  # último trecho (Ushuaia → Puerto Williams) é travessia de balsa

route_data = []
for i, (name, lat, lon, stype, cc, km) in enumerate(ROUTE_RAW):
    info = T["stops"][i]
    route_data.append({
        "id": i + 1, "name": name, "lat": lat, "lon": lon, "type": stype, "cc": cc, "km": km,
        "country": T["countries"][cc], **info,
    })
IDX_END1 = len(route_data) - 2   # Ushuaia
IDX_END2 = len(route_data) - 1   # Puerto Williams
USED_CODES = []
for s in route_data:
    if s["cc"] not in USED_CODES:
        USED_CODES.append(s["cc"])
ROAD_KM_TOTAL = route_data[IDX_END1]["km"]

ECONOMICS_FALLBACK = {
    "prices": {
        "BR": {"country": "Brasil", "currency": "BRL", "gasoline": 6.55, "diesel": 6.57, "electricity_kwh": 1.50, "collected_at": "2026-08-10", "frequency": "semanal / referência ANP", "source": "GlobalPetrolPrices / referência ANP", "source_url": "https://www.globalpetrolprices.com/Brazil/gasoline_prices/"},
        "UY": {"country": "Uruguai", "currency": "UYU", "gasoline": 88.67, "diesel": 58.68, "electricity_kwh": 15.00, "collected_at": "2026-08-01", "frequency": "vigência mensal ANCAP", "source": "ANCAP", "source_url": "https://www.ancap.com.uy/10564/1/historico-precios-combustibles.html"},
        "AR": {"country": "Argentina", "currency": "ARS", "gasoline": 2055.00, "diesel": 2217.00, "electricity_kwh": 220.00, "collected_at": "2026-08-10", "frequency": "semanal / referência nacional", "source": "Secretaría de Energía / GlobalPetrolPrices", "source_url": "https://www.globalpetrolprices.com/Argentina/gasoline_prices/"},
        "CL": {"country": "Chile", "currency": "CLP", "gasoline": 1443.33, "diesel": 1193.00, "electricity_kwh": 250.00, "collected_at": "2026-08-10", "frequency": "referência CNE", "source": "CNE / GlobalPetrolPrices", "source_url": "https://api.cne.cl/"},
    },
    "assumptions": {
        "tesla_kwh_per_100km": 17.5, "tesla_charge_loss": 0.10, "tucson_km_per_litre": 12.5,
        "gasoline_co2_kg_per_litre": 2.348, "diesel_co2_kg_per_litre": 2.689,
        "grid_co2_kg_per_kwh": {"BR": 0.10, "UY": 0.20, "AR": 0.35, "CL": 0.25},
    },
    "ferries": [
        {"id": "magallanes_first_angostura", "vehicle_included": True, "currency": "ARS", "indicative_vehicle_fare": 43000, "port_fee": 0, "duration_minutes": 45, "source_url": "https://www.tabsa.cl/rutas/primera-angostura"},
        {"id": "beagle_passenger", "vehicle_included": False, "currency": "USD", "indicative_vehicle_fare": 0, "passenger_fare": 235, "port_fee": 10, "duration_minutes": 120, "source_url": "https://www.ushuaiapuertowilliams.com/cruce-canal-beagle/"},
    ],
    "sources": [
        {"url": "https://app.powerbi.com/view?r=eyJrIjoiMGM0NDhhMTUtMjQwZi00N2RlLTk1M2UtYjkxZTlkNzM1YzE5IiwidCI6IjQ0OTlmNGZmLTI0YTYtNGI0Mi1iN2VmLTEyNGFmY2FkYzkxMyJ9"},
        {"url": "https://www.ancap.com.uy/10564/1/historico-precios-combustibles.html"},
        {"url": "http://res1104.se.gob.ar/consultaprecios.eess.php"},
        {"url": "https://apidocs.cne.cl/"},
        {"url": "https://www.epa.gov/energy/greenhouse-gas-equivalencies-calculator-calculations-and-references"},
    ],
}

# (nome da fonte, índice em economics["sources"], índice da nota em T["sources_notes"])
SOURCES_USED = [("ANP (Brasil)", 0, 0), ("ANCAP (Uruguay)", 1, 1), ("Secretaría de Energía (Argentina)", 2, 2),
                ("CNE (Chile)", 3, 3), ("EPA / IPCC", 4, 4)]


@st.cache_data(ttl=86400, show_spinner=False)
def load_economics(refresh_online=True):
    """Carrega o snapshot local (route_economics.json) ou o fallback embutido; tenta atualizar preços online."""
    data = None
    economics_path = APP_DIR / "route_economics.json"
    try:
        if economics_path.exists() and economics_path.stat().st_size > 10:
            with economics_path.open("r", encoding="utf-8") as f:
                candidate = json.load(f)
            if isinstance(candidate, dict) and isinstance(candidate.get("prices"), dict):
                data = candidate
    except (OSError, json.JSONDecodeError, TypeError):
        data = None
    if data is None:
        data = json.loads(json.dumps(ECONOMICS_FALLBACK, ensure_ascii=False))
    data["runtime"] = {
        "loaded_at": datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M"),
        "online_attempted": bool(refresh_online),
        "online_updates": [],
        "online_errors": [],
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
        ("CL", "diesel", "https://www.globalpetrolprices.com/Chile/diesel_prices/", "CLP", "GlobalPetrolPrices / CNE"),
    ]
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(update_gpp, *task) for task in gpp_tasks]
        for future in futures:
            future.result()
    return data


with st.sidebar:
    refresh_online = st.checkbox(T["sb_refresh"], value=True, help=T["sb_refresh_help"])
    if st.button(T["sb_update_now"]):
        load_economics.clear()
        st.rerun()

economics = load_economics(refresh_online)

with st.sidebar:
    st.markdown(f"### {T['sb_fx_title']}")
    st.caption(T["sb_fx_caption"])
    fx = {
        "BR": st.number_input(T["sb_fx_label"].format(c="BRL"), min_value=0.01, value=5.50, step=0.05, key="fx_brl"),
        "AR": st.number_input(T["sb_fx_label"].format(c="ARS"), min_value=0.01, value=1485.00, step=10.00, key="fx_ars"),
        "CL": st.number_input(T["sb_fx_label"].format(c="CLP"), min_value=0.01, value=910.00, step=5.00, key="fx_clp"),
    }


def money(value, code):
    symbols = {"BR": "R$", "UY": "$U", "AR": "$", "CL": "$"}
    decimals = 0 if code in {"AR", "CL"} else 2
    return f"{symbols.get(code, '')} {numfmt(value, decimals)}"


def usd(value, code):
    return value / fx[code]


def usd_text(value):
    return f"US$ {numfmt(value, 0)}"


def build_segment_costs(route, econ):
    assumptions = econ["assumptions"]
    rows = []
    for idx in range(1, len(route)):
        prev, stop = route[idx - 1], route[idx]
        code = stop["cc"]
        km = max(stop["km"] - prev["km"], 0)
        is_water = WATER_LAST and idx == IDX_END2  # Ushuaia → Puerto Williams
        drive_km = 0 if is_water else km
        price = econ["prices"][code]
        tucson_l = drive_km / assumptions["tucson_km_per_litre"]
        tesla_kwh = drive_km * assumptions["tesla_kwh_per_100km"] / 100 * (1 + assumptions["tesla_charge_loss"])
        rows.append({
            "route": f"{prev['name']} → {stop['name']}",
            "dest_idx": idx,
            "country": T["countries"][code],
            "km": km, "drive_km": drive_km,
            "water": is_water,
            "gas_price": price["gasoline"], "elec_price": price["electricity_kwh"],
            "gas_cost": tucson_l * price["gasoline"],
            "ev_cost": tesla_kwh * price["electricity_kwh"],
            "gas_l": tucson_l, "tesla_kwh": tesla_kwh,
            "tucson_co2": tucson_l * assumptions["gasoline_co2_kg_per_litre"],
            "tesla_co2": tesla_kwh * assumptions["grid_co2_kg_per_kwh"][code],
            "price_date": price["collected_at"],
            "code": code,
            "dest": stop["name"],
        })
    return pd.DataFrame(rows)


def ferry_costs(econ):
    records = []
    for i, ferry in enumerate(econ["ferries"][:2]):
        tr = T["ferries"][i]
        vehicle_cost = ferry.get("indicative_vehicle_fare", 0)
        passenger_cost = ferry.get("passenger_fare", 0) + ferry.get("port_fee", 0)
        records.append({
            T["f_crossing"]: tr["name"],
            T["f_route"]: tr["route"],
            T["f_operator"]: tr["operator"],
            T["f_vehicle"]: T["yes"] if ferry.get("vehicle_included") else T["no"],
            T["f_vehicle_fare"]: money(vehicle_cost, "AR") if vehicle_cost else "—",
            T["f_passenger"]: usd_text(passenger_cost) if passenger_cost else "—",
            T["f_duration"]: f"{ferry['duration_minutes']} {T['minutes']}",
            T["f_status"]: tr["status"],
        })
    return pd.DataFrame(records)


def get_image_base64(path):
    candidate = APP_DIR / path
    try:
        if candidate.exists() and candidate.stat().st_size > 0:
            return base64.b64encode(candidate.read_bytes()).decode("utf-8")
    except OSError:
        pass
    return ""


img_tesla_front = f"data:image/png;base64,{get_image_base64('tesla_front.png')}"
img_tesla_back = f"data:image/png;base64,{get_image_base64('tesla_back.png')}"
img_tucson_front = f"data:image/png;base64,{get_image_base64('tucson_front.png')}"
img_tucson_back = f"data:image/png;base64,{get_image_base64('tucson_back.png')}"

segment_df = build_segment_costs(route_data, economics)
total_tucson_cost = float(segment_df["gas_cost"].sum())
total_tesla_cost = float(segment_df["ev_cost"].sum())
total_tucson_co2 = float(segment_df["tucson_co2"].sum())
total_tesla_co2 = float(segment_df["tesla_co2"].sum())
total_tesla_usd = sum(usd(v, c) for v, c in zip(segment_df["ev_cost"], segment_df["code"]))
total_tucson_usd = sum(usd(v, c) for v, c in zip(segment_df["gas_cost"], segment_df["code"]))
ratio = total_tucson_usd / total_tesla_usd if total_tesla_usd else 0.0

# ============================================================
# HERO
# ============================================================
FLAG_OF = {"BR": "🇧🇷", "AR": "🇦🇷", "CL": "🇨🇱", "UY": "🇺🇾"}
flags_txt = " ".join(FLAG_OF[c] for c in USED_CODES)
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-tag">{T['hero_tag']}</div>
    <div class="hero-title">{T['hero_title']}</div>
    <div class="hero-subtitle">{T['hero_subtitle']}</div>
    <div class="hero-badges">
        <span class="badge badge-highlight">{T['badge1']}</span>
        <span class="badge badge-highlight">{T['badge2']}</span>
        <span class="badge">{flags_txt} {T['badge_countries'].format(n=len(USED_CODES))}</span>
        <span class="badge">{T['badge_km'].format(km=numfmt(round(ROAD_KM_TOTAL, -1)))}</span>
        <span class="badge">{T['badge_points'].format(n=len(route_data))}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SEÇÃO 1: HOME ───────────────────────────────────────────
if nav_idx == 0:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-box"><div class="metric-val">~{numfmt(round(ROAD_KM_TOTAL, -1))} km</div><div class="metric-label">{T["m1"]}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-box success"><div class="metric-val">{usd_text(total_tesla_usd)}</div><div class="metric-label">{T["m2"]}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-box danger"><div class="metric-val">{usd_text(total_tucson_usd)}</div><div class="metric-label">{T["m3"]}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-box"><div class="metric-val">{numfmt(ratio, 1)}×</div><div class="metric-label">{T["m4"]}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.2, 1])
    with col_l:
        st.markdown(f'<div class="section-label">{T["context_label"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">{T["why_go_title"]}</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-card">
            <p style="line-height: 1.7; font-size: 0.98rem; color: #1d3557;">{T['why_go_text']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown(f'<div class="section-label">{T["route_label"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">{T["route_title"]}</div>', unsafe_allow_html=True)
        parts = []
        for i, s in enumerate(route_data):
            nm = s["name"]
            if i == 0:
                nm = f"<b>{T['route_start']}:</b> {nm}"
            elif i == IDX_END1:
                nm = f"<b>🏁 {T['route_end1']}:</b> {nm}"
            elif i == IDX_END2:
                nm = f"<i>({T['route_ferry']} ⛴️)</i> <b>🏁 {T['route_end2']}:</b> {nm}"
            parts.append(nm)
        st.markdown(f"""
        <div class="info-card" style="border-left-color: #218380;">
            <strong>{T['route_overview_title']}</strong><br><br>
            <p style="font-size: 0.9rem; color: #334155; line-height: 1.7;">{' → '.join(parts)}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f'<div class="section-label" style="margin-top:1rem">{T["ends_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["ends_title"]}</div>', unsafe_allow_html=True)
    e1, e2 = st.columns(2)
    with e1:
        st.markdown(f"""
        <div class="info-card" style="border-left-color: #e63946;">
            <h3>{T['end1_title']}</h3>
            <p style="line-height:1.65">{T['end1_text']}</p>
            <p style="font-size:.8rem;color:#64748b">-54.80°, -68.30°</p>
        </div>
        """, unsafe_allow_html=True)
    with e2:
        st.markdown(f"""
        <div class="info-card" style="border-left-color: #ffb703;">
            <h3>{T['end2_title']}</h3>
            <p style="line-height:1.65">{T['end2_text']}</p>
            <p style="font-size:.8rem;color:#64748b">-54.93°, -67.62°</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown(f'<div class="alert-box">{T["ferry_note"]}</div>', unsafe_allow_html=True)

# ── SEÇÃO 2: MODO AUTO-DRIVE COM PAUSE/PLAY ─────────────────
elif nav_idx == 1:
    st.markdown(f'<div class="section-label">{T["map_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["map_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="alert-box">{T["map_hint"]}</div>', unsafe_allow_html=True)

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        selected_car = st.selectbox(
            T["car_label"], options=["tesla", "tucson"], key="car_sel",
            format_func=lambda x: T["car_tesla"] if x == "tesla" else T["car_tucson"],
        )
    with col_c2:
        selected_direction = st.selectbox(
            T["dir_label"], options=["out", "back"], key="dir_sel",
            format_func=lambda x: T["dir_out"] if x == "out" else T["dir_back"],
        )

    is_tesla = selected_car == "tesla"
    is_outbound = selected_direction == "out"
    if is_tesla:
        car_img_data = img_tesla_front if is_outbound else img_tesla_back
    else:
        car_img_data = img_tucson_front if is_outbound else img_tucson_back

    points = [[c["lat"], c["lon"]] for c in route_data]
    modes = [0] * (len(points) - 2) + [1]  # 1 = travessia de balsa (Ushuaia ↔ Puerto Williams)
    if not is_outbound:
        points = list(reversed(points))
        modes = list(reversed(modes))

    try:
        carto_key = st.secrets.get("CARTO_API_KEY", "")
    except Exception:
        carto_key = ""

    m = folium.Map(location=[-42, -64], zoom_start=4, tiles=None, control_scale=True)
    if carto_key:
        folium.TileLayer(
            tiles=("https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png?key=" + carto_key),
            attr=('&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; '
                  '<a href="https://carto.com/attributions">CARTO</a>'),
            name="CARTO Voyager", subdomains="abcd", max_zoom=20, overlay=False, control=True,
        ).add_to(m)
    else:
        folium.TileLayer(
            "OpenStreetMap", name="OpenStreetMap",
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            control=True,
        ).add_to(m)

    # trecho rodoviário (SP → Ushuaia) e travessia de balsa (Ushuaia → Puerto Williams)
    road_pts = points[:-1] if is_outbound else points[1:]
    folium.PolyLine(points, color="#1b3b6f", weight=3, opacity=0.4, tooltip=T["route_tip"]).add_to(m)
    AntPath(
        road_pts, color="#218380" if is_outbound else "#e63946", weight=5, opacity=0.85,
        delay=1200, dash_array=[15, 25], pulse_color="#ffffff", tooltip=T["road_tip"],
    ).add_to(m)
    ferry_pts = [[route_data[IDX_END1]["lat"], route_data[IDX_END1]["lon"]],
                 [route_data[IDX_END2]["lat"], route_data[IDX_END2]["lon"]]]
    folium.PolyLine(ferry_pts, color="#0077b6", weight=4, opacity=0.95, dash_array="2 10",
                    tooltip=T["ferry_tip"]).add_to(m)

    rtl_css = "direction:rtl;text-align:right;" if RTL else ""
    for i, stop in enumerate(route_data):
        icon_name, icon_color, prefix_val = "info-sign", "blue", "glyphicon"
        if stop["type"] == "Start":
            icon_name, icon_color = "play", "green"
        elif "End" in stop["type"]:
            icon_name, icon_color = "flag", ("red" if i == IDX_END1 else "darkred")
        elif stop["type"] == "Ferry":
            icon_name, icon_color, prefix_val = "ship", "darkblue", "fa"
        elif "Tesla" in stop["type"] or "Grid" in stop["type"]:
            icon_name, icon_color = "flash", "cadetblue"
        elif "Gas" in stop["type"] or "Fuel" in stop["type"]:
            icon_name, icon_color, prefix_val = "gas-pump", "orange", "fa"

        badge = ""
        if i == IDX_END1:
            badge = f"<p style='margin:3px 0;font-size:12px;color:#e63946'><b>🏁 {T['route_end1']}</b></p>"
        elif i == IDX_END2:
            badge = f"<p style='margin:3px 0;font-size:12px;color:#c1121f'><b>🏁 {T['route_end2']}</b></p>"
        popup_html = f"""
        <div style="font-family:'Plus Jakarta Sans','Noto Sans',sans-serif;width:230px;padding:5px;{rtl_css}">
            <h4 style="margin:0 0 5px 0;color:#1b3b6f;">{stop['name']}</h4>
            {badge}
            <p style="margin:3px 0;font-size:12px;"><b>{T['popup_country']}:</b> {stop['country']}</p>
            <p style="margin:3px 0;font-size:12px;"><b>{T['popup_distance']}:</b> {numfmt(stop['km'])} km</p>
            <p style="margin:3px 0;font-size:12px;color:#218380;"><i>{stop['highlights']}</i></p>
        </div>
        """
        tip = f"#{stop['id']} - {stop['name']}"
        if i in (IDX_END1, IDX_END2):
            tip += " 🏁"
        folium.Marker(
            [stop["lat"], stop["lon"]], popup=folium.Popup(popup_html, max_width=260),
            tooltip=tip, icon=folium.Icon(color=icon_color, icon=icon_name, prefix=prefix_val),
        ).add_to(m)

    i18n_js = json.dumps({k: T[k] for k in ["btn_pause", "btn_resume", "btn_reset", "btn_replay",
                                            "st_moving", "st_driving", "st_paused", "st_arrived", "st_ferry"]},
                         ensure_ascii=False)
    car_animation_js = """
    <div id="autodrive-controls" style="margin-bottom:10px;display:flex;gap:10px;align-items:center;flex-wrap:wrap;background:#ffffff;padding:10px 15px;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,0.05);__DIR__">
        <span style="font-family:'JetBrains Mono','Noto Sans',monospace;font-size:12px;font-weight:700;color:#1b3b6f;">__CTL_TITLE__</span>
        <button id="btnPause" onclick="toggleDrive()" style="background:#e63946;color:white;border:none;padding:6px 14px;border-radius:6px;cursor:pointer;font-weight:600;font-size:12px;">__BTN_PAUSE__</button>
        <button id="btnReset" onclick="resetDrive()" style="background:#1b3b6f;color:white;border:none;padding:6px 14px;border-radius:6px;cursor:pointer;font-weight:600;font-size:12px;">__BTN_RESET__</button>
        <span id="driveStatus" style="font-size:12px;color:#2a9d8f;font-weight:600;">__ST_MOVING__</span>
    </div>

    <script>
    var I = __I18N__;
    var isDriving = true;
    var onWater = false;
    function statusDriving() { return onWater ? I.st_ferry : I.st_driving; }
    function toggleDrive() {
        isDriving = !isDriving;
        var btn = document.getElementById('btnPause');
        var status = document.getElementById('driveStatus');
        if (isDriving) {
            btn.style.background = '#e63946';
            btn.innerHTML = I.btn_pause;
            status.style.color = '#2a9d8f';
            status.innerHTML = statusDriving();
        } else {
            btn.style.background = '#2a9d8f';
            btn.innerHTML = I.btn_resume;
            status.style.color = '#e63946';
            status.innerHTML = I.st_paused;
        }
    }

    (function() {
        function initAutoDrive() {
            var mapContainer = null;
            var mapKeys = Object.keys(window).filter(function(k) { return k.indexOf('map_') === 0; });
            for (var i = 0; i < mapKeys.length; i++) {
                if (window[mapKeys[i]] && window[mapKeys[i]]._container) { mapContainer = window[mapKeys[i]]; }
            }
            if (!mapContainer) { setTimeout(initAutoDrive, 300); return; }

            var routePoints = __POINTS__;
            var segModes = __MODES__;
            var carIcon = L.divIcon({
                html: '<div style="background:rgba(255,255,255,0.95);padding:4px;border-radius:50%;box-shadow:0 4px 12px rgba(0,0,0,0.35);"><img src="__CAR__" style="width:55px;height:38px;object-fit:contain;transform:translate(-50%,-50%);display:block;" /></div>',
                className: 'custom-car-autodrive', iconSize: [55, 38], iconAnchor: [27, 19]
            });
            var carMarker = L.marker(routePoints[0], {icon: carIcon, zIndexOffset: 3000}).addTo(mapContainer);

            var segIndex = 0, steps = 150, stepCount = 0, finished = false;
            function lerp(a, b, t) { return a + (b - a) * t; }
            function setStatus(text, color) {
                var status = document.getElementById('driveStatus');
                status.innerHTML = text; status.style.color = color;
            }
            window.resetDrive = function() {
                segIndex = 0; stepCount = 0; finished = false; isDriving = true; onWater = false;
                carMarker.setLatLng(routePoints[0]);
                var btn = document.getElementById('btnPause');
                btn.style.background = '#e63946'; btn.innerHTML = I.btn_pause;
                setStatus(I.st_moving, '#2a9d8f');
            };
            function driveStep() {
                if (isDriving && !finished) {
                    var start = routePoints[segIndex], end = routePoints[segIndex + 1];
                    var progress = stepCount / steps;
                    var nowWater = segModes[segIndex] === 1;
                    if (nowWater !== onWater) { onWater = nowWater; setStatus(statusDriving(), onWater ? '#0077b6' : '#2a9d8f'); }
                    carMarker.setLatLng([lerp(start[0], end[0], progress), lerp(start[1], end[1], progress)]);
                    stepCount++;
                    if (stepCount > steps) {
                        stepCount = 0; segIndex++;
                        if (segIndex >= routePoints.length - 1) {
                            finished = true;
                            carMarker.setLatLng(routePoints[routePoints.length - 1]);
                            setStatus(I.st_arrived, '#1b3b6f');
                            document.getElementById('btnPause').innerHTML = I.btn_replay;
                        }
                    }
                }
                setTimeout(function() { requestAnimationFrame(driveStep); }, 75);
            }
            driveStep();
        }
        setTimeout(initAutoDrive, 600);
    })();
    </script>
    """
    for key, val in {
        "__I18N__": i18n_js, "__POINTS__": json.dumps(points), "__MODES__": json.dumps(modes),
        "__CAR__": car_img_data, "__CTL_TITLE__": T["ctl_title"], "__BTN_PAUSE__": T["btn_pause"],
        "__BTN_RESET__": T["btn_reset"], "__ST_MOVING__": T["st_moving"],
        "__DIR__": "direction:rtl;" if RTL else "",
    }.items():
        car_animation_js = car_animation_js.replace(key, val)
    m.get_root().html.add_child(folium.Element(car_animation_js))
    st_folium(m, width=1250, height=620, key=f"map_{LANG}_{selected_car}_{selected_direction}")

# ── SEÇÃO 3: PARADAS ───────────────────────────────────────
elif nav_idx == 2:
    st.markdown(f'<div class="section-label">{T["details_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["details_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="alert-box">{T["stops_alert"]}</div>', unsafe_allow_html=True)

    sel = st.selectbox(
        T["stop_select"], options=list(range(len(route_data))), key="stop_idx",
        format_func=lambda i: f"#{i + 1} · {route_data[i]['name']}" + (" 🏁" if i in (IDX_END1, IDX_END2) else ""),
    )
    stop_info = route_data[sel]
    code = stop_info["cc"]
    price = economics["prices"][code]
    seg_rows = segment_df[segment_df["dest_idx"] == sel]
    stop_row = seg_rows.iloc[0] if not seg_rows.empty else None

    col_a, col_b = st.columns([1.15, 1])
    with col_a:
        st.markdown(f"""
        <div class="info-card">
            <h3>📍 #{stop_info['id']} — {stop_info['name']}</h3>
            <p><b>{T['card_country']}:</b> {stop_info['country']} · {price['currency']}</p>
            <p><b>{T['card_distance']}:</b> {numfmt(stop_info['km'])} km</p>
            <p><b>{T['card_elevation']}:</b> {T['not_informed']}</p>
            <p><b>{T['card_climate']}:</b> {T['card_summer']} {T['variable']} · {T['card_winter']} {T['variable']}</p>
            <p><b>{T['card_charging']}:</b> {stop_info['charging_infra']}</p>
            <p><b>{T['card_fuel']}:</b> {stop_info['gas_infra']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="info-card" style="border-left-color: #ffb703;">
            <h3>{T['field_title']}</h3>
            <p>{stop_info['highlights']}</p>
            <p><b>{T['field_challenge']}:</b> {stop_info['logistics']}</p>
        </div>
        """, unsafe_allow_html=True)

    p1, p2, p3, p4 = st.columns(4)
    p1.metric(T["p_gasoline"], money(price["gasoline"], code) + "/L")
    p2.metric(T["p_diesel"], money(price["diesel"], code) + "/L")
    p3.metric(T["p_charge"], money(price["electricity_kwh"], code) + "/kWh")
    p4.metric(T["p_date"], price["collected_at"])

    if stop_row is not None:
        st.markdown(f"#### {T['seg_title']}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(T["seg_distance"], f"{numfmt(stop_row['km'])} km")
        c2.metric(T["seg_tucson"], money(stop_row["gas_cost"], code))
        c3.metric(T["seg_tesla"], money(stop_row["ev_cost"], code))
        c4.metric(T["seg_co2"], f"{numfmt(max(stop_row['tucson_co2'] - stop_row['tesla_co2'], 0))} kg")
    else:
        st.info(T["seg_origin"])

# ── SEÇÃO 4: SPECS & CUSTOS ────────────────────────────────
elif nav_idx == 3:
    st.markdown(f'<div class="section-label">{T["specs_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["specs_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="alert-box">{T["specs_alert"]}</div>', unsafe_allow_html=True)

    saving_usd = total_tucson_usd - total_tesla_usd
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(T["s_tesla_energy"], usd_text(total_tesla_usd))
    m2.metric(T["s_tucson_gas"], usd_text(total_tucson_usd))
    m3.metric(T["s_diff"], usd_text(saving_usd))
    m4.metric(T["s_co2"], f"{numfmt(max(total_tucson_co2 - total_tesla_co2, 0))} kg")

    a = economics["assumptions"]
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown(f"""
        <div class="info-card" style="border-left-color: #2a9d8f;">
            <h3>{T['tesla_card_title']}</h3>
            <p><b>{T['tesla_consumption']}:</b> {numfmt(a['tesla_kwh_per_100km'], 1)} kWh/100 km + {numfmt(a['tesla_charge_loss'] * 100)}% {T['tesla_losses']}.</p>
            <p><b>{T['tesla_energy']}:</b> {numfmt(segment_df['tesla_kwh'].sum())} kWh</p>
            <p><b>{T['tesla_co2']}:</b> {numfmt(total_tesla_co2)} kg</p>
            <p><b>{T['tesla_premise']}:</b> {T['tesla_premise_text']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_v2:
        st.markdown(f"""
        <div class="info-card" style="border-left-color: #e63946;">
            <h3>{T['tucson_card_title']}</h3>
            <p><b>{T['tesla_consumption']}:</b> {numfmt(a['tucson_km_per_litre'], 1)} km/L.</p>
            <p><b>{T['tucson_gas']}:</b> {numfmt(segment_df['gas_l'].sum())} L</p>
            <p><b>{T['tucson_co2']}:</b> {numfmt(total_tucson_co2)} kg</p>
            <p><b>{T['tucson_factor']}:</b> {numfmt(a['gasoline_co2_kg_per_litre'], 3)} kg CO₂/L, {T['tucson_factor_text']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"#### {T['seg_chart_title']}")
    chart_df = pd.DataFrame({
        "dest": segment_df["dest"],
        "tucson": [usd(v, c) for v, c in zip(segment_df["gas_cost"], segment_df["code"])],
        "tesla": [usd(v, c) for v, c in zip(segment_df["ev_cost"], segment_df["code"])],
    })
    fig = go.Figure(data=[
        go.Bar(name=T["chart_tesla"], x=chart_df["dest"], y=chart_df["tesla"], marker_color="#2a9d8f"),
        go.Bar(name=T["chart_tucson"], x=chart_df["dest"], y=chart_df["tucson"], marker_color="#e63946"),
    ])
    fig.update_layout(
        barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title=T["chart_y"], xaxis_title=T["chart_x"], height=460,
        font=dict(family="Plus Jakarta Sans, Noto Sans, Noto Sans SC, Noto Naskh Arabic"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    plot(fig)

    table = pd.DataFrame({
        T["tbl_route"]: segment_df["route"],
        T["tbl_country"]: segment_df["country"],
        T["tbl_mode"]: [T["mode_water"] if w else T["mode_road"] for w in segment_df["water"]],
        T["tbl_km_route"]: [numfmt(v) for v in segment_df["km"]],
        T["tbl_km_road"]: [numfmt(v) for v in segment_df["drive_km"]],
        T["tbl_gas_price"]: [numfmt(v, 2) for v in segment_df["gas_price"]],
        T["tbl_energy_price"]: [numfmt(v, 2) for v in segment_df["elec_price"]],
        T["tbl_tucson"]: [money(v, c) for v, c in zip(segment_df["gas_cost"], segment_df["code"])],
        T["tbl_tesla"]: [money(v, c) for v, c in zip(segment_df["ev_cost"], segment_df["code"])],
        T["tbl_date"]: segment_df["price_date"],
    })
    show_table(table)

    st.markdown(f"#### {T['ferry_title']}")
    show_table(ferry_costs(economics))
    f1, f2, f3 = st.columns(3)
    f1.metric(T["f1"], usd_text(economics["ferries"][0]["indicative_vehicle_fare"] / fx["AR"]))
    beagle = economics["ferries"][1]
    f2.metric(T["f2"], usd_text(beagle["passenger_fare"] + beagle["port_fee"]))
    f3.metric(T["f3"], T["f3v"])
    st.caption(T["ferry_caption"])

    st.markdown(f"#### {T['markets_title']}")
    market_rows = []
    for code, item in economics["prices"].items():
        market_rows.append({
            T["mk_country"]: T["countries"][code],
            T["mk_gas"]: f"{money(item['gasoline'], code)}/L",
            T["mk_diesel"]: f"{money(item['diesel'], code)}/L",
            T["mk_charge"]: f"{money(item['electricity_kwh'], code)}/kWh",
            T["mk_last"]: item["collected_at"],
            T["mk_freq"]: item.get("frequency", ""),
            T["mk_source"]: item["source"],
        })
    show_table(pd.DataFrame(market_rows))
    st.caption(T["mk_caption"].format(t=economics["runtime"]["loaded_at"], u=", ".join(economics["runtime"]["online_updates"]) or T["mk_none"]))

# ── SEÇÃO 5: METODOLOGIA ───────────────────────────────────
elif nav_idx == 4:
    st.markdown(f'<div class="section-label">{T["tech_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["tech_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f"<div class='info-card'>{T['tech_text']}</div>", unsafe_allow_html=True)

    a = economics["assumptions"]
    a1, a2 = st.columns(2)
    with a1:
        st.markdown(f"#### {T['assump_title']}")
        show_table(pd.DataFrame([
            {T["as_param"]: T["as_tesla_cons"], T["as_value"]: f"{numfmt(a['tesla_kwh_per_100km'], 1)} kWh/100 km"},
            {T["as_param"]: T["as_tesla_loss"], T["as_value"]: f"{numfmt(a['tesla_charge_loss'] * 100)}%"},
            {T["as_param"]: T["as_tucson_cons"], T["as_value"]: f"{numfmt(a['tucson_km_per_litre'], 1)} km/L"},
            {T["as_param"]: T["as_gas_co2"], T["as_value"]: f"{numfmt(a['gasoline_co2_kg_per_litre'], 3)} kg/L"},
            {T["as_param"]: T["as_diesel_co2"], T["as_value"]: f"{numfmt(a['diesel_co2_kg_per_litre'], 3)} kg/L"},
        ]))
    with a2:
        st.markdown(f"#### {T['grid_title']}")
        show_table(pd.DataFrame([
            {T["mk_country"]: T["countries"][c], T["grid_hyp"]: f"{numfmt(a['grid_co2_kg_per_kwh'][c], 2)} kg CO₂/kWh"}
            for c in a["grid_co2_kg_per_kwh"]
        ]))
        st.caption(T["assumption_note"])

    st.markdown(f"#### {T['sources_title']}")
    src_rows = []
    for name, url_idx, note_idx in SOURCES_USED:
        src_rows.append({T["src_name"]: name, T["src_note"]: T["sources_notes"][note_idx],
                         "URL": economics["sources"][url_idx]["url"]})
    show_table(pd.DataFrame(src_rows))
    st.markdown(f"#### {T['status_title']}")
    st.json(economics["runtime"])

# RODAPÉ
st.markdown(f"""
<div class="footer-wrap">
    <div class="footer-title">{T['footer_title']}</div>
    <p style="margin: 0.5rem 0; font-size: 0.92rem;">{T['footer_desc']}</p>
    <p style="margin: 1rem 0; font-size: 0.85rem;">{T['footer_links']} &nbsp;|&nbsp; 🌐 <a href="https://amaurialmeida.github.io/environmental-portfolio/" style="color:#ffb703">{T['portfolio_label']}</a></p>
</div>
""", unsafe_allow_html=True)
