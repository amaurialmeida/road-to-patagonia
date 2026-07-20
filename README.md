# 🏔️ Road to Patagonia — Electric vs. Combustion Expedition

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B?logo=streamlit&logoColor=white)](https://road-to-patagonia.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

🌐 **Languages:** English | [Português](README.pt-BR.md) | [Español](README.es.md)

**Independent Field Research — Applied Automotive & Energy Case Study**
Route: São Paulo (Mooca), Brazil → Ushuaia, Argentina & Puerto Williams, Chile
**Author:** Amauri Almeida de Souza Junior

---

## ❓ Research Question

> "Over a real ~5,000 km road trip from São Paulo to the southern tip of South America, crossing Brazil, Uruguay, Argentina, and Chile — how does a fully electric vehicle compare to a combustion vehicle in terms of estimated trip cost and range logistics?"

**Answer:** Across the same route, the electric vehicle (Tesla Model 3 Long Range) shows a substantially lower estimated energy cost than the combustion vehicle (Hyundai Tucson), at the expense of range per stop and dependency on charging infrastructure availability along a corridor where fast chargers are far less common than gas stations — a trade-off this project quantifies and visualizes stop by stop.

---

## 📊 Data Summary

| Indicator | Value |
|---|---|
| Route | São Paulo (BR) → Ushuaia (AR) → Puerto Williams (CL) |
| Countries crossed | 🇧🇷 Brazil · 🇺🇾 Uruguay · 🇦🇷 Argentina · 🇨🇱 Chile |
| Approx. total distance | ~5,000 km |
| Mapped stop points | 12 (start, waypoints, dual endpoint) |
| Vehicles compared | Tesla Model 3 (2024, electric) vs. Hyundai Tucson (2024, combustion) |
| Estimated cost — Tesla Model 3 | ≈ $450 USD (charging) |
| Estimated cost — Hyundai Tucson | ≈ $1,200 USD (gasoline) |

*Cost figures are trip-level estimates based on vehicle specs and regional energy/fuel prices, not metered real-world billing — see [Methodology](#-methodology).*

---

## 🔵 Key Findings

- **~2.7× lower estimated energy cost for the EV** — the Tesla Model 3's estimated charging cost (~$450) is roughly a third of the Tucson's estimated fuel cost (~$1,200) over the same route.
- **Range trade-off** — the Tesla's estimated range (550 km) is shorter than the Tucson's (750 km), meaning more frequent stops are required despite the lower running cost.
- **Infrastructure asymmetry** — gas stations (Ipiranga, YPF, Copec) are ubiquitous along the route, while CCS2 fast-charging infrastructure is comparatively sparse — especially south of Bahía Blanca, Argentina.
- **A genuinely international corridor** — the route crosses four countries and ends at two possible "southernmost point" destinations, Ushuaia (AR) and Puerto Williams (CL), reflecting real regional debate over which city is the true end of the road.

---

## 🗺️ Route Overview

```
Start        → São Paulo (Mooca), BR
Waypoints    → Curitiba → Florianópolis → Porto Alegre → Chuí (BR/UY border)
             → Punta del Este → Buenos Aires → Bahía Blanca
             → Puerto Madryn → Comodoro Rivadavia → Río Gallegos
End (AR)     → Ushuaia, Argentina
End (CL)     → Puerto Williams, Chile (via short crossing from Ushuaia)
```

The interactive map plots the full trajectory with dynamic markers — charging points, gas stations, and dual-fuel stops — rendered from geocoded route data.

---

## 🔬 Methodology

```
Route data       →  12 waypoints geocoded (lat/lon) and stored in route_data.json,
                     each tagged by stop type (Start / Tesla-Gas / End)

Mapping          →  Folium + CartoDB Positron tiles; polyline trajectory;
                     dynamic icon assignment per stop type (charger, gas pump, flag)

Vehicle specs    →  Tesla Model 3 Long Range (2024): 550 km range, 78.1 kWh battery,
                     CCS2 charging network
                     Hyundai Tucson (2024): 750 km range, 54 L fuel tank,
                     regional gas station networks

Cost comparison  →  Grouped bar chart (Plotly) contrasting estimated total trip cost
                     in USD for each vehicle across the same route

Trilingual UX    →  Full PT / EN / ES interface via a unified translation dictionary,
                     selectable from the sidebar
```

---

## 🛠️ Tech Stack

| Technology | Use |
|---|---|
| Python 3.11 | Core language |
| Streamlit | Interactive dashboard & multi-tab UI |
| Folium + streamlit-folium | Interactive route mapping |
| Plotly | Cost comparison charts |
| Pandas | Route data handling |
| JSON | Route waypoint storage |

---

## 📁 Repository Structure

```
road-to-patagonia/
├── app.py                  # Main Streamlit dashboard
├── route_data.json          # Geocoded route waypoints (lat/lon/type)
├── requirements.txt         # Python dependencies
├── README.md                 # This file (English)
├── README.pt-BR.md           # Portuguese version
└── README.es.md              # Spanish version
```

---

## 🚀 Run Locally

```bash
# Clone the repository
git clone https://github.com/amaurialmeida/road-to-patagonia.git
cd road-to-patagonia

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
```

---

## 🌐 Live App

🔗 **[road-to-patagonia.streamlit.app](https://road-to-patagonia.streamlit.app/)**

Available in 🇧🇷 Portuguese, 🇺🇸 English, and 🇪🇸 Spanish via the in-app language selector.

---

## 🔗 Academic / Professional Links

| Platform | Link |
|---|---|
| Lattes | http://lattes.cnpq.br/9545242042800090 |
| Escavador | https://www.escavador.com/sobre/8577779/amauri-almeida-de-souza-junior |

---

## 🌿 Environmental Portfolio

This project is part of the author's environmental research and data science portfolio.
🔗 [amaurialmeida.github.io/environmental-portfolio](https://amaurialmeida.github.io/environmental-portfolio)

---

© 2024–2026 · Amauri Almeida de Souza Junior · Independent Research · Portfolio Project
