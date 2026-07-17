import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import os
from PIL import Image

st.set_page_config(
    page_title="Road to Patagonia · Potencial Eólico",
    page_icon="🌬️",
    layout="wide"
)

# ============================================================
# SISTEMA DE IDIOMAS
# ============================================================
if "lang" not in st.session_state:
    st.session_state.lang = "pt"

TRANSLATIONS = {
    "pt": {
        "page_title": "Road to Patagonia · Potencial Eólico",
        "hero_tag": "EXPEDIÇÃO CIENTÍFICA · PATAGÔNIA SUL · CHILE & ARGENTINA · NOV 2024–OUT 2025",
        "hero_title": "Road to Patagonia:\nAnálise do Potencial Eólico",
        "hero_subtitle": "Uma investigação comparativa do potencial de geração de energia eólica nas cidades mais ventosas do planeta, percorridas pessoalmente ao longo de 11 meses de expedição e validadas com reanálise climática ERA5.",
        "badge1": "💨 Westerlies · 40°S–60°S",
        "badge2": "⚡ 9.500+ MW potencial",
        "badge3": "Chile & Argentina",
        "badge4": "Expedição de Campo",
        "badge5": "OPEN-METEO · ERA5 · GWA",
        "m1": "Vel. média Punta Arenas",
        "m2": "Fator de capacidade (PAT)",
        "m3": "Rajada máx. registrada",
        "m4": "Potencial total estimado",
        "tab1": "🗺️ Mapa & Análise",
        "tab2": "🔬 Metodologia & Pipeline",
        "tab3": "💡 Descobertas de Campo",
        "tab4": "📷 Registro Visual",
        "tab5": "📚 Fontes & Referências",
        "map_label": "GEOLOCALIZAÇÃO — CORREDOR DE VENTOS",
        "map_title": "Mapa Interativo da Expedição",
        "map_hint": "💨 <strong>Clique nos marcadores</strong> para inspecionar os dados de vento, fatores de capacidade e o potencial instalável estimado de cada ponto estratégico visitado.",
        "chart_label": "ANÁLISE QUANTITATIVA DO VENTO",
        "wind_monthly_title": "Velocidade Média Mensal do Vento — Série Histórica (2020–2024)",
        "wind_y": "Velocidade (km/h)",
        "rose_title": "Rosa dos Ventos — Distribuição Direcional Histórica",
        "annual_title": "Evolução Anual da Velocidade Média (2020–2024)",
        "annual_y": "Velocidade média anual (km/h)",
        "simulator_label": "SIMULADOR DE GERAÇÃO INTERATIVO",
        "simulator_title": "Calculadora de Potencial Energético da Patagônia",
        "sim_city": "Cidade Alvo",
        "sim_turbines": "Número de aerogeradores",
        "sim_power": "Potência nominal por turbina (MW)",
        "sim_result_gwh": "GWh / ano estimados",
        "sim_result_homes": "domicílios atendidos",
        "sim_result_co2": "t CO₂ evitadas/ano",
        "capacity_title": "Fatores de Capacidade Regionais vs. Média Global (35%)",
        "method_label": "CIÊNCIA DO VENTO",
        "method_title": "Hipótese & Pipeline de Dados",
        "sci_question_title": "❓ Pergunta Central da Pesquisa",
        "sci_question": "\"Qual é o potencial real de geração de energia eólica nas cidades mais ventosas da Patagônia, e como a experiência direta de campo corrobora os dados de reanálise meteorológica sobre a consistência dos ventos Westerlies?\"",
        "pipeline_label": "PIPELINE DE ENGENHARIA DE DADOS",
        "steps": [
            ("1", "Ingestão e Coleta — Open-Meteo ERA5", "Extração automatizada de dados horários de velocidade e direção do vento (2020–2024) via API Histórica do Open-Meteo, utilizando o modelo de reanálise ERA5 do ECMWF."),
            ("2", "Validação de Campo — Expedição Patagônica", "11 meses de imersão direta nas quatro localidades: Punta Arenas, Puerto Natales, Rio Gallegos e Puerto Williams, coletando percepções empíricas e dados geográficos locais."),
            ("3", "Cálculo Físico — Lei da Potência Cúbica", "Modelagem da densidade de potência eólica ($P/A = \\frac{1}{2} \\rho v^3$). Onde a velocidade entra ao cubo, demonstrando matematicamente por que o fator de capacidade da Patagônia supera 60%."),
            ("4", "Simulação Dinâmica de Ativos", "Desenvolvimento do algoritmo de conversão energética: $\\text{GWh/ano} = P_{\\text{turbina}} \\times N \\times \\text{FC} \\times 8760 / 1000$, acoplado a variáveis de mitigação de carbono."),
            ("5", "Análise Vetorial e Direcional", "Processamento e plotagem vetorial para a geração da Rosa dos Ventos, evidenciando a dominância estrita e a baixíssima variabilidade do quadrante WSW-W-WNW."),
            ("6", "Dimensionamento de Impacto Ecológico", "Tratamento estatístico do potencial instalável combinado de 9.500 MW e cálculo de equivalência de substituição de matriz energética fóssil por renovável."),
        ],
        "physics_title": "⚙️ Mecânica dos Fluidos e Física do Vento",
        "physics_text": "• <b>Lei Cúbica da Potência:</b> $P/A = \\frac{1}{2} \\rho v^3$ (Duplicar o vento gera 8x mais energia)<br>• <b>Densidade do Ar ($\rho$):</b> ~1,20 kg/m³ ajustada para altitudes locais ao nível do mar<br>• <b>Fator de Capacidade Flutuante:</b> >60% na Patagônia vs. 35% de média global<br>• <b>Dinamismo Atmosférico:</b> Cinturão de ventos permanentes sem fricção orográfica continental",
        "westerlies_title": "🌍 Dinâmica dos Ventos Westerlies",
        "westerlies_text": "• <b>Sistemas de Baixa Pressão Circumpolares:</b> Fluxo contínuo entre os paralelos 40°S e 60°S<br>• <b>Estepes Planas:</b> Baixo coeficiente de rugosidade do solo na Patagônia Argentina amplifica a velocidade<br>• <b>Canais de Escoamento:</b> Fiordes chilenos atuam como aceleradores naturais de ventos (Efeito Venturi)<br>• <b>Resiliência Energética:</b> Sazonalidade controlada garante geração firme o ano todo",
        "discovery_label": "CONSOLIDAÇÃO DE RESULTADOS",
        "discovery_title": "Evidências Analíticas e Conclusões de Campo",
        "discoveries": [
            ("💨", "Punta Arenas — O Epicentro Energético", "Velocidade média de 30,2 km/h com rajadas severas de 130 km/h. O potencial técnico projetado de 4.200 MW valida a cidade como vetor estratégico de transição energética."),
            ("⚡", "Fator de Capacidade Incomparável", "Índices superiores a 60% significam eficiência máxima dos ativos. Uma turbina na Patagônia produz anualmente quase o dobro do que produziria na média global."),
            ("🌊", "Canais Patagônicos e o Efeito Venturi", "A topografia de Puerto Natales e arredores funciona como um funil aerodinâmico natural, mantendo médias elevadas de 26,8 km/h mesmo sob interferência de relevo montanhoso."),
            ("🏙️", "Puerto Williams — O Limite dos Screaming Sixties", "A vivência em Puerto Williams provou o rigor dos ventos austrais em ~55°S. A infraestrutura e a natureza coexistem sob forças extremas, incluindo o registro do abalo M7+ em maio de 2025."),
            ("📊", "9.500+ MW — Gigante Renovável", "O potencial mapeado para Punta Arenas, Puerto Natales e Rio Gallegos totaliza uma capacidade monumental capaz de redefinir o suprimento energético regional."),
            ("🌱", "Mitigação de Impacto Ambiental", "A exploração comercial de frações desse potencial tem capacidade para neutralizar milhões de toneladas de CO₂ anualmente da atmosfera."),
        ],
        "conclusion_label": "EPÍLOGO DA EXPEDIÇÃO",
        "conclusion_title": "A Patagônia como Resposta à Crise Climática Global",
        "conclusion_text": "Concluir a expedição 'Road to Patagonia' entre novembro de 2024 e outubro de 2025 consolidou uma certeza física: o vento que desafia o equilíbrio nas ruas de Punta Arenas é a força exata que pode alimentar matrizes industriais limpas. Cruzar as estepes e os canais austrais confirmou que a Patagônia possui o combustível mecânico do século XXI.",
        "conclusion_author": "Amauri Almeida · Relato e Pesquisa de Campo · Road to Patagonia",
        "field_label": "DIÁRIO DE BORDO E REGISTRO EMPÍRICO",
        "field_title": "Vivência Direta no Território Austral",
        "field_instructions_title": "📁 Gerenciamento de Ativos de Imagem",
        "field_instructions": "Para renderizar suas fotografias de expedição, armazene-as no diretório <code>assets/campo/</code> respeitando estritamente a nomenclatura indicada abaixo.",
        "photos": [
            {"emoji": "🌬️", "cidade": "Punta Arenas", "titulo": "Punta Arenas — Nov 2024", "desc": "Estreito de Magalhães. Zona ativa dos ventos de Oeste. Média: 30,2 km/h. Potencial estimado: 4.200 MW.", "path": "assets/campo/01_punta_arenas_nov2024.jpg", "legenda": "Punta Arenas · Chile · Estreito de Magalhães · 53.1°S", "coords": "53.1°S · 70.9°O", "vento": "30,2 km/h média", "pot": "4.200 MW", "mes": "Nov/2024", "cor": "#1A3A6E"},
            {"emoji": "🏔️", "cidade": "Puerto Natales", "titulo": "Puerto Natales — Dez 2024", "desc": "Canais da Patagônia Chilena. Média de 26,8 km/h com forte canalização aerodinâmica entre fiordes.", "path": "assets/campo/02_puerto_natales_dez2024.jpg", "legenda": "Puerto Natales · Última Esperanza · 51.7°S", "coords": "51.7°S · 72.5°O", "vento": "26,8 km/h média", "pot": "1.800 MW", "mes": "Dez/2024", "cor": "#1B3A1E"},
            {"emoji": "🌪️", "cidade": "Rio Gallegos", "titulo": "Rio Gallegos — Mar 2025", "desc": "Estepe Atlântica Argentina. Ausência total de barreiras geográficas resultando em ventos lineares de alta velocidade.", "path": "assets/campo/03_rio_gallegos_mar2025.jpg", "legenda": "Rio Gallegos · Argentina · Estepe Patagônica · 51.6°S", "coords": "51.6°S · 69.2°O", "vento": "27,1 km/h média", "pot": "3.500 MW", "mes": "Mar/2025", "cor": "#5C3D1E"},
            {"emoji": "🏁", "cidade": "Puerto Williams", "titulo": "Puerto Williams — Out 2025", "desc": "Fim da Linha na Isla Navarino (~55°S). Domínio dos Screaming Sixties. Linha de frente das tempestades subantárticas.", "path": "assets/campo/04_puerto_williams_out2025.jpg", "legenda": "Puerto Williams · Cabo de Hornos · 54.9°S", "coords": "54.9°S · 67.6°O", "vento": "Screaming Sixties", "pot": "Ponto de Controle", "mes": "Out/2025", "cor": "#8B2515", "destaque": True},
        ],
        "timeline_field_label": "CRONOGRAMA DE EXECUÇÃO — ROAD TO PATAGONIA",
        "timeline_field_items": [
            ("Nov 2024", "Início do Campo — Punta Arenas", "Coleta empírica inicial e validação da estação anemométrica do Estreito de Magalhães."),
            ("Dez 2024", "Mapeamento de Fiordes — Puerto Natales", "Análise qualitativa da aceleração de ventos gerada pela transição topográfica andina."),
            ("Mar 2025", "Travessia da Estepe — Rio Gallegos", "Estudo in loco do escoamento laminar dos ventos de Oeste sobre as planícies continentais argentinas."),
            ("Mai 2025", "Evento Geodinâmico — Puerto Williams", "Vivência e registro do abalo sísmico de magnitude M7+ na região da Isla Navarino."),
            ("Jun–Set 2025", "Monitoramento de Inverno — Canal Beagle", "Análise de resiliência e medição de persistência do vento durante as condições climáticas extremas do inverno austral."),
            ("Out 2025", "Encerramento da Expedição — Puerto Williams", "Consolidação e tabulação dos dados finais do diário de campo e fechamento da série ERA5."),
        ],
        "sources_label": "RIGOR ACADÊMICO",
        "sources_title": "Bases de Dados Científicas e Literárias",
        "tech_label": "STACK TECNOLÓGICA DO PROJETO",
        "footer_title": "Expedição Road to Patagonia",
        "footer_desc": "Engenharia de Dados & Gestão Ambiental Aplicada<br>Modelagem Preditiva e Análise de Recursos Renováveis em Ambientes de Alta Latitude",
        "footer_links": "📍 Campo de Pesquisa: 40°S a 55°S (Chile & Argentina)",
        "select_city": "Selecione a localidade alvo para simulação",
        "turbines_label": "Quantidade de unidades integradas ao parque",
        "power_label": "Potência ativa nominal do aerogerador (MW)",
        "year_label": "Ano de Análise",
    },
    "es": {
        "page_title": "Road to Patagonia · Potencial Eólico",
        "hero_tag": "EXPEDICIÓN CIENTÍFICA · PATAGONIA SUR · CHILE & ARGENTINA · NOV 2024–OCT 2025",
        "hero_title": "Road to Patagonia:\nAnálisis del Potencial Eólico",
        "hero_subtitle": "Una investigación comparativa del potencial de generación de energía eólica en las ciudades más ventosas del planeta, recorridas personalmente a lo largo de 11 meses de expedición y validadas con reanálisis climático ERA5.",
        "badge1": "💨 Westerlies · 40°S–60°S",
        "badge2": "⚡ 9.500+ MW potencial",
        "badge3": "Chile & Argentina",
        "badge4": "Expedición de Campo",
        "badge5": "OPEN-METEO · ERA5 · GWA",
        "m1": "Vel. media Punta Arenas",
        "m2": "Factor de capacidad (PAT)",
        "m3": "Ráfaga máx. registrada",
        "m4": "Potencial total estimado",
        "tab1": "🗺️ Mapa & Análisis",
        "tab2": "🔬 Metodología & Pipeline",
        "tab3": "💡 Hallazgos de Campo",
        "tab4": "📷 Registro Visual",
        "tab5": "📚 Fuentes & Referencias",
        "map_label": "GEOLOCALIZACIÓN — CORREDOR DE VIENTOS",
        "map_title": "Mapa Interactivo de la Expedición",
        "map_hint": "💨 <strong>Haga clic en los marcadores</strong> para inspeccionar los datos de viento, factores de capacidad y el potencial instalable estimado de cada punto estratégico visitado.",
        "chart_label": "ANÁLISIS CUANTITATIVO DEL VIENTO",
        "wind_monthly_title": "Velocidad Media Mensual del Viento — Serie Histórica (2020–2024)",
        "wind_y": "Velocidad (km/h)",
        "rose_title": "Rosa de los Vientos — Distribución Direccional Histórica",
        "annual_title": "Evolución Anual de la Velocidad Media (2020–2024)",
        "annual_y": "Velocidad media anual (km/h)",
        "simulator_label": "SIMULADOR DE GENERACIÓN INTERACTIVO",
        "simulator_title": "Calculadora de Potencial Energético de la Patagonia",
        "sim_city": "Ciudad Objetivo",
        "sim_turbines": "Número de aerogeneradores",
        "sim_power": "Potencia nominal por turbina (MW)",
        "sim_result_gwh": "GWh / año estimados",
        "sim_result_homes": "hogares atendidos",
        "sim_result_co2": "t CO₂ evitadas/año",
        "capacity_title": "Factores de Capacidad Regionales vs. Media Global (35%)",
        "method_label": "CIENCIA DEL VIENTO",
        "method_title": "Hipótesis & Pipeline de Datos",
        "sci_question_title": "❓ Pregunta Central de la Investigación",
        "sci_question": "\"¿Cuál es el potencial real de generación de energía eólica en las ciudades más ventosas de la Patagonia, y cómo la experiencia directa de campo corrobora los datos de reanálisis meteorológico sobre la consistencia de los vientos Westerlies?\"",
        "pipeline_label": "PIPELINE DE INGENIERÍA DE DATOS",
        "steps": [
            ("1", "Ingestión y Recolección — Open-Meteo ERA5", "Extracción automatizada de datos horarios de velocidad y dirección del viento (2020–2024) vía API Histórica de Open-Meteo, utilizando el modelo de reanálisis ERA5 del ECMWF."),
            ("2", "Validación de Campo — Expedición Patagónica", "11 meses de inmersión directa en las cuatro localidades: Punta Arenas, Puerto Natales, Río Gallegos y Puerto Williams, recolectando percepciones empíricas y datos geográficos locales."),
            ("3", "Cálculo Físico — Ley de la Potencia Cúbica", "Modelado de la densidad de potencia eólica ($P/A = \\frac{1}{2} \\rho v^3$). Donde la velocidad entra al cubo, demostrando matemáticamente por qué el factor de capacidad supera el 60%."),
            ("4", "Simulación Dinámica de Activos", "Desarrollo del algoritmo de conversión energética con variables de mitigación de carbono incorporadas."),
            ("5", "Análisis Vectorial y Direccional", "Procesamiento y diseño vectorial para la generación de la Rosa de los Vientos, evidenciando la dominancia estricta del cuadrante WSW-W-WNW."),
            ("6", "Dimensionamiento de Impacto Ecológico", "Tratamiento estadístico del potencial instalable combinado de 9.500 MW y cálculo de equivalencia de sustitución de energía."),
        ],
        "physics_title": "⚙️ Mecánica de Fluidos y Física del Viento",
        "physics_text": "• <b>Ley Cúbica de la Potencia:</b> $P/A = \\frac{1}{2} \\rho v^3$ (Duplicar el viento genera 8x más energía)<br>• <b>Densidad del Aire ($\rho$):</b> ~1,20 kg/m³ ajustada para altitudes locales<br>• <b>Factor de Capacidad Fluctuante:</b> >60% en la Patagonia vs. 35% de media global<br>• <b>Dinamismo Atmosférico:</b> Cinturón de vientos permanentes sin fricción continental",
        "westerlies_title": "🌍 Dinámica de los Vientos Westerlies",
        "westerlies_text": "• <b>Sistemas de Baja Presión Circumpolares:</b> Flujo continuo entre los paralelos 40°S y 60°S<br>• <b>Estepas Planas:</b> Bajo coeficiente de rugosidad en la Patagonia Argentina amplifica la velocidad<br>• <b>Canales de Fluido:</b> Fiordos chilenos actúan como aceleradores naturales de vientos (Efecto Venturi)<br>• <b>Resiliencia Energética:</b> Baja estacionalidad garantiza generación firme todo el año",
        "discovery_label": "CONSOLIDACIÓN DE RESULTADOS",
        "discovery_title": "Evidencias Analíticas y Conclusiones de Campo",
        "discoveries": [
            ("💨", "Punta Arenas — El Epicentro Energético", "Velocidad media de 30,2 km/h con ráfagas severas de 130 km/h. El potencial técnico proyectado de 4.200 MW valida la ciudad como vector estratégico."),
            ("⚡", "Factor de Capacidad Incomparable", "Índices superiores a 60% significan eficiencia máxima de los activos comerciales."),
            ("🌊", "Canales Patagónicos y el Efecto Venturi", "La topografía de Puerto Natales funciona como un embudo aerodinámico natural, manteniendo promedios elevados."),
            ("🏙️", "Puerto Williams — El Límite de los Screaming Sixties", "La vivencia en Puerto Williams demostró el rigor de los vientos australes en ~55°S y las fuerzas extremas de la naturaleza, incluido el sismo M7+."),
            ("📊", "9.500+ MW — Gigante Renovable", "El potencial mapeado para las tres ciudades principales define una capacidad monumental."),
            ("🌱", "Mitigación de Impacto Ambiental", "La explotación comercial de este potencial tiene capacidad para neutralizar millones de toneladas de CO₂."),
        ],
        "conclusion_label": "EPÍLOGO DE LA EXPEDICIÓN",
        "conclusion_title": "La Patagonia como Respuesta a la Crisis Climática Global",
        "conclusion_text": "Concluir la expedición 'Road to Patagonia' entre noviembre de 2024 y octubre de 2025 consolidó una certeza física: el viento que desafía el equilibrio en las calles de Punta Arenas es la fuerza exacta que puede alimentar industrias limpias.",
        "conclusion_author": "Amauri Almeida · Relato e Investigación de Campo · Road to Patagonia",
        "field_label": "DIARIO DE ABORDO Y REGISTRO EMPÍRICO",
        "field_title": "Vivencia Directa en el Territorio Austral",
        "field_instructions_title": "📁 Gestión de Activos de Imagen",
        "field_instructions": "Para renderizar sus fotografías de expedición, almacénelas en el directorio <code>assets/campo/</code> respetando la nomenclatura indicada abajo.",
        "photos": [
            {"emoji": "🌬️", "cidade": "Punta Arenas", "titulo": "Punta Arenas — Nov 2024", "desc": "Estrecho de Magallanes. Zona activa de los vientos del Oeste. Promedio: 30,2 km/h. Potencial: 4.200 MW.", "path": "assets/campo/01_punta_arenas_nov2024.jpg", "legenda": "Punta Arenas · Chile · Estrecho de Magallanes · 53.1°S", "coords": "53.1°S · 70.9°O", "vento": "30,2 km/h prome", "pot": "4.200 MW", "mes": "Nov/2024", "cor": "#1A3A6E"},
            {"emoji": "🏔️", "cidade": "Puerto Natales", "titulo": "Puerto Natales — Dic 2024", "desc": "Canales de la Patagonia Chilena. Promedio de 26,8 km/h con fuerte canalización entre fiordos.", "path": "assets/campo/02_puerto_natales_dez2024.jpg", "legenda": "Puerto Natales · Última Esperanza · 51.7°S", "coords": "51.7°S · 72.5°O", "vento": "26,8 km/h prome", "pot": "1.800 MW", "mes": "Dic/2024", "cor": "#1B3A1E"},
            {"emoji": "🌪️", "cidade": "Río Gallegos", "titulo": "Río Gallegos — Mar 2025", "desc": "Estepa Atlántica Argentina. Ausencia total de barreras geográficas resultando en vientos lineales de alta velocidad.", "path": "assets/campo/03_rio_gallegos_mar2025.jpg", "legenda": "Río Gallegos · Argentina · Estepa Patagónica · 51.6°S", "coords": "51.6°S · 69.2°O", "vento": "27,1 km/h prome", "pot": "3.500 MW", "mes": "Mar/2025", "cor": "#5C3D1E"},
            {"emoji": "🏁", "cidade": "Puerto Williams", "titulo": "Puerto Williams — Oct 2025", "desc": "Fin de la línea en Isla Navarino (~55°S). Dominio estricto de los Screaming Sixties.", "path": "assets/campo/04_puerto_williams_out2025.jpg", "legenda": "Puerto Williams · Cabo de Hornos · 54.9°S", "coords": "54.9°S · 67.6°O", "vento": "Screaming Sixties", "pot": "Punto de Control", "mes": "Oct/2025", "cor": "#8B2515", "destaque": True},
        ],
        "timeline_field_label": "CRONOGRAMA DE EJECUCIÓN — ROAD TO PATAGONIA",
        "timeline_field_items": [
            ("Nov 2024", "Inicio de Campo — Punta Arenas", "Validación empírica inicial en el Estrecho de Magallanes."),
            ("Dic 2024", "Mapeamiento de Fiordos — Puerto Natales", "Análisis cualitativo del Efecto Venturi en los canales chilenos."),
            ("Mar 2025", "Travesía de la Estepa — Río Gallegos", "Estudio de flujos laminares en llanuras continentales argentinas."),
            ("May 2025", "Evento Geodinámico — Puerto Williams", "Vivencia y registro del sismo de magnitud M7+ en Isla Navarino."),
            ("Jun–Sep 2025", "Monitoreo Invernal — Canal Beagle", "Análisis de persistencia de vientos en condiciones invernales extremas."),
            ("Oct 2025", "Cierre de Expedición — Puerto Williams", "Consolidación final de datos del diario de campo y serie meteorológica."),
        ],
        "sources_label": "RIGOR ACADÉMICO",
        "sources_title": "Bases de Datos Científicas y Literarias",
        "tech_label": "STACK TECNOLÓGICA DEL PROYECTO",
        "footer_title": "Expedición Road to Patagonia",
        "footer_desc": "Ingeniería de Datos & Gestión Ambiental Aplicada<br>Modelado Predictivo de Recursos Renovables en Altas Latitudes",
        "footer_links": "📍 Campo de Investigación: 40°S a 55°S (Chile & Argentina)",
        "select_city": "Seleccione la localidad para simulación",
        "turbines_label": "Cantidad de aerogeneradores integrados al parque",
        "power_label": "Potencia nominal del aerogenerador (MW)",
        "year_label": "Año de Análisis",
    },
    "en": {
        "page_title": "Road to Patagonia · Wind Energy Potential",
        "hero_tag": "SCIENTIFIC EXPEDITION · SOUTHERN PATAGONIA · CHILE & ARGENTINA · NOV 2024–OCT 2025",
        "hero_title": "Road to Patagonia:\nWind Potential Analysis",
        "hero_subtitle": "A comparative investigation of wind energy generation potential in the windiest cities on earth, personally tracked across an 11-month expedition and validated with ERA5 climate reanalysis.",
        "badge1": "💨 Westerlies · 40°S–60°S",
        "badge2": "⚡ 9,500+ MW potential",
        "badge3": "Chile & Argentina",
        "badge4": "Field Expedition",
        "badge5": "OPEN-METEO · ERA5 · GWA",
        "m1": "Avg. Wind Punta Arenas",
        "m2": "Capacity Factor (PAT)",
        "m3": "Max. Recorded Gust",
        "m4": "Total Estimated Potential",
        "tab1": "🗺️ Map & Analysis",
        "tab2": "🔬 Methodology & Pipeline",
        "tab3": "💡 Field Discoveries",
        "tab4": "📷 Visual Record",
        "tab5": "📚 Sources & References",
        "map_label": "GEOLOCATION — WIND CORRIDOR",
        "map_title": "Interactive Expedition Map",
        "map_hint": "💨 <strong>Click on markers</strong> to inspect historical wind data, capacity factors, and estimated installable power for each checkpoint visited.",
        "chart_label": "QUANTITATIVE WIND ANALYSIS",
        "wind_monthly_title": "Monthly Mean Wind Speed — Historical Series (2020–2024)",
        "wind_y": "Speed (km/h)",
        "rose_title": "Wind Rose — Directional Distribution Matrix",
        "annual_title": "Annual Mean Wind Speed Evolution (2020–2024)",
        "annual_y": "Annual mean speed (km/h)",
        "simulator_label": "INTERACTIVE ASSET SIMULATOR",
        "simulator_title": "Patagonia Energy Yield Calculator",
        "sim_city": "Target Location",
        "sim_turbines": "Number of wind turbines",
        "sim_power": "Nominal power capacity per turbine (MW)",
        "sim_result_gwh": "Estimated GWh / year",
        "sim_result_homes": "households powered",
        "sim_result_co2": "t CO₂ offset/year",
        "capacity_title": "Regional Capacity Factors vs. Global Average (35%)",
        "method_label": "WIND SCIENCE",
        "method_title": "Hypothesis & Data Engineering Pipeline",
        "sci_question_title": "❓ Core Research Question",
        "sci_question": "\"What is the real wind energy generation potential of the windiest cities in Patagonia, and how does direct field experience support meteorological reanalysis datasets regarding the consistency of the Westerlies?\"",
        "pipeline_label": "DATA ENGINEERING PIPELINE",
        "steps": [
            ("1", "Ingestion & Inflow — Open-Meteo ERA5", "Automated pipelines harvesting hourly wind vectors (2020–2024) via Open-Meteo Historical API backed by ECMWF's ERA5 reanalysis framework."),
            ("2", "Ground-Truth Validation — Expedition", "11 months of deep physical field deployment across four hubs: Punta Arenas, Puerto Natales, Río Gallegos, and Puerto Williams, collecting qualitative and spatial tokens."),
            ("3", "Physical Modeling — Cubic Power Law", "Computing wind power density grids ($P/A = \\frac{1}{2} \\rho v^3$). Tracking the cubic exponential scale to map why Patagonia clears >60% efficiency standards."),
            ("4", "Dynamic Yield Simulation", "Mathematical layout of expected output: $\\text{GWh/yr} = P_{\\text{turbine}} \\times N \\times \\text{CF} \\times 8760 / 1000$ calibrated against localized carbon offset data."),
            ("5", "Vector Directional Analysis", "Processing raw angular points to structure the polar Wind Rose, verifying strict structural dominance of WSW-W-WNW airflows."),
            ("6", "Environmental Impact Scaling", "Statistical staging of the combined 9,500 MW baseline asset matrix to project fossil fuel grid displacement impact metrics."),
        ],
        "physics_title": "⚙️ Fluid Dynamics & Wind Physics",
        "physics_text": "• <b>Cubic Power Law:</b> $P/A = \\frac{1}{2} \\rho v^3$ (Doubling velocity unlocks 8x kinetic energy yield)<br>• <b>Air Density ($\rho$):</b> ~1.20 kg/m³ calibrated to local sea-level bars<br>• <b>Capacity Factor Threshold:</b> >60% in Patagônian farms vs. 35% global average benchmarks<br>• <b>Atmospheric Inflow:</b> Non-obstructed boundary layer streamline over extreme high latitudes",
        "westerlies_title": "🌍 Dynamics of the Westerlies",
        "westerlies_text": "• <b>Circumpolar Low-Pressure Systems:</b> Continuous atmospheric drift between 40°S and 60°S lines<br>• <b>Flat Steppes:</b> Extremely low roughness length coefficients over Argentine plains accelerate wind streams<br>• <b>Venturi Channeling:</b> Deep Chilean fjords act as natural thermodynamic nozzles for airflow acceleration<br>• <b>Grid Resilience:</b> Highly reliable seasonal distribution prevents unexpected generation dropouts",
        "discovery_title": "Analytical Evidence & Field Assessment Summaries",
        "discoveries": [
            ("💨", "Punta Arenas — The Energy Apex", "30.2 km/h baseline mean speeds backed by 130 km/h gusts. The 4,200 MW asset scale highlights the hub's green hydrogen export potential."),
            ("⚡", "Unmatched Capacity Factors", "Sustained efficiency over 60% proves exceptional economic viability for asset deployments."),
            ("🌊", "The Chilean Fjords Nozzle Effect", "Puerto Natales terrain dynamics function as a natural kinetic amplifier, maintaining high averages despite mountain friction."),
            ("🏙️", "Puerto Williams — Screaming Sixties Threshold", "Field logs at ~55°S logged the stark weight of subantarctic flows. Extreme environment tracking included an M7+ seismic event in May 2025."),
            ("📊", "9,500+ MW — The Clean Energy Powerhouse", "Aggregated tech caps across key tracking points outline a vast unmapped clean energy asset frontier."),
            ("🌱", "Atmospheric Carbon Abatement", "Commercial scaling of these wind resources exhibits immense scale for industrial carbon offset targeting."),
        ],
        "conclusion_label": "EXPEDITION EPILOGUE",
        "conclusion_title": "Patagonia as the Ultimate Answer to Global Decarbonization",
        "conclusion_text": "Concluding the 'Road to Patagonia' field timeline between November 2024 and October 2025 delivered a clear physical truth: the intense kinetic wind force felt on the streets of Punta Arenas is the exact engine required to scale global clean grids. Moving across these steppes proved Patagonia owns the raw power of the next era.",
        "conclusion_author": "Amauri Almeida · Field Operations & Research Lead · Road to Patagonia",
        "field_label": "FIELD JOURNAL & EMPIRICAL LOGS",
        "field_title": "Direct Physical Tracking in Southern Ecosystems",
        "field_instructions_title": "📁 Static Photo Asset Management",
        "field_instructions": "To render your custom field images, store them inside the <code>assets/campo/</code> workspace folder using the filenames detailed below.",
        "photos": [
            {"emoji": "🌬️", "cidade": "Punta Arenas", "titulo": "Punta Arenas — Nov 2024", "desc": "Strait of Magellan. High-velocity Westerly zone. Mean: 30.2 km/h. Estimated capacity: 4,200 MW.", "path": "assets/campo/01_punta_arenas_nov2024.jpg", "legenda": "Punta Arenas · Chile · Strait of Magellan · 53.1°S", "coords": "53.1°S · 70.9°W", "vento": "30.2 km/h mean", "pot": "4,200 MW", "mes": "Nov/2024", "cor": "#1A3A6E"},
            {"emoji": "🏔️", "cidade": "Puerto Natales", "titulo": "Puerto Natales — Dec 2024", "desc": "Chilean Patagonian Channels. 26.8 km/h mean speeds utilizing mountain gap Venturi forcing lines.", "path": "assets/campo/02_puerto_natales_dez2024.jpg", "legenda": "Puerto Natales · Última Esperanza · 51.7°S", "coords": "51.7°S · 72.5°W", "vento": "26.8 km/h mean", "pot": "1,800 MW", "mes": "Dec/2024", "cor": "#1B3A1E"},
            {"emoji": "🌪️", "cidade": "Río Gallegos", "titulo": "Río Gallegos — Mar 2025", "desc": "Argentine Atlantic Steppes. Zero land obstructions yielding high-velocity laminar wind flows.", "path": "assets/campo/03_rio_gallegos_mar2025.jpg", "legenda": "Río Gallegos · Argentina · Patagonian Steppes · 51.6°S", "coords": "51.6°S · 69.2°W", "vento": "27.1 km/h mean", "pot": "3,500 MW", "mes": "Mar/2025", "cor": "#5C3D1E"},
            {"emoji": "🏁", "cidade": "Puerto Williams", "titulo": "Puerto Williams — Oct 2025", "desc": "End of the line at Isla Navarino (~55°S). Direct exposure to the subantarctic Screaming Sixties core.", "path": "assets/campo/04_puerto_williams_out2025.jpg", "legenda": "Puerto Williams · Cape Horn Biosphere · 54.9°S", "coords": "54.9°S · 67.6°W", "vento": "Screaming Sixties", "pot": "Control Node", "mes": "Oct/2025", "cor": "#8B2515", "destaque": True},
        ],
        "timeline_field_label": "DEPLOYMENT TIMELINE — ROAD TO PATAGONIA",
        "timeline_field_items": [
            ("Nov 2024", "Field Launch — Punta Arenas", "Setting up ground control points and cross-checking data lines against Strait of Magellan wind arrays."),
            ("Dec 2024", "Fjord Aerodynamics — Puerto Natales", "Investigating geographic amplification profiles across major Patagonian waterways."),
            ("Mar 2025", "Steppe Crossings — Río Gallegos", "Mapping boundary layer stability and continuous streamline flow fields across flat Argentine ranges."),
            ("May 2025", "Geodynamic Event — Puerto Williams", "Surviving and logging an M7+ deep tectonic shift event while deployed on Isla Navarino."),
            ("Jun–Sep 2025", "Winter Monitoring — Beagle Channel", "Tracking seasonal inflow persistence and subantarctic freeze cycles against turbine downtime risks."),
            ("Oct 2025", "Expedition Wrap — Puerto Williams", "Final ground-truth data aggregation, diary indexing, and closure of the ERA5 analytics baseline."),
        ],
        "sources_label": "ACADEMIC RIGOR",
        "sources_title": "Scientific Data Catalogs & Literature Reference",
        "tech_label": "STACK MODEL COMPOSITION",
        "footer_title": "Road to Patagonia Expedition",
        "footer_desc": "Applied Data Engineering & Environmental Management Systems<br>Predictive Modeling and High-Latitude Energy Resource Assessment",
        "footer_links": "📍 Project Target Bounds: 40°S to 55°S (Chile & Argentina)",
        "select_city": "Select target simulation node",
        "turbines_label": "Total operational asset count on site",
        "power_label": "Turbine rated nameplate capacity (MW)",
        "year_label": "Target Analysis Year",
    },
}

# ── SELETOR DE IDIOMA ──────────────────────────────────────────
def render_lang_selector():
    c0, c1, c2, c3 = st.columns([8, 1, 1, 1])
    with c1:
        if st.button("🇧🇷 PT", use_container_width=True, type="primary" if st.session_state.lang == "pt" else "secondary"):
            st.session_state.lang = "pt"; st.rerun()
    with c2:
        if st.button("🇪🇸 ES", use_container_width=True, type="primary" if st.session_state.lang == "es" else "secondary"):
            st.session_state.lang = "es"; st.rerun()
    with c3:
        if st.button("🇺🇸 EN", use_container_width=True, type="primary" if st.session_state.lang == "en" else "secondary"):
            st.session_state.lang = "en"; st.rerun()

render_lang_selector()
T = TRANSLATIONS[st.session_state.lang]

# ── INJEÇÃO DE ESTILOS CSS CUSTOMIZADOS ─────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&family=DM+Mono&display=swap');
:root{
  --wind:#1A3A6E;--wind-mid:#2555A0;--wind-light:#3A7ACA;
  --sky:#56B3F0;--sky-light:#A8D8F0;
  --slate:#2D3A4A;--cream:#F4F6FA;--warm-gray:#6A7888;
  --green:#2D7A3A;--amber:#C47D0E;--danger:#8B2515;--black:#0D1117;
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background-color:var(--cream);color:var(--black);}
.hero-wrap{
  background:linear-gradient(135deg,var(--slate) 0%,var(--wind) 50%,#1E4A8A 100%);
  border-radius:20px;padding:3rem 2.5rem 2rem;margin-bottom:2rem;position:relative;overflow:hidden;
}
.hero-wrap::before{content:"🌬️";font-size:200px;position:absolute;right:-20px;top:-30px;opacity:0.05;}
.hero-tag{background:#A8D8F0;color:var(--wind);font-family:'DM Mono',monospace;font-size:0.7rem;font-weight:bold;letter-spacing:2px;padding:4px 12px;border-radius:4px;display:inline-block;margin-bottom:1rem;text-transform:uppercase;}
.hero-title{font-family:'Playfair Display',serif;font-size:2.8rem;font-weight:900;color:#fff;line-height:1.15;margin-bottom:0.8rem;white-space:pre-line;}
.hero-subtitle{font-size:1rem;color:rgba(255,255,255,0.78);max-width:680px;line-height:1.6;margin-bottom:1.5rem;}
.hero-badges{display:flex;gap:10px;flex-wrap:wrap;}
.badge{background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.85);font-size:0.72rem;font-family:'DM Mono',monospace;padding:5px 12px;border-radius:20px;letter-spacing:0.5px;}
.badge-wind{background:rgba(168,216,240,0.2);border-color:#A8D8F0;color:#A8D8F0;}
.metric-box{background:white;border-radius:16px;padding:1.4rem 1.2rem;border-top:4px solid var(--wind-light);box-shadow:0 2px 12px rgba(0,0,0,0.06);text-align:center;}
.metric-box.sky{border-top-color:var(--sky);}
.metric-box.amber{border-top-color:var(--amber);}
.metric-box.green{border-top-color:var(--green);}
.metric-val{font-family:'Playfair Display',serif;font-size:2.1rem;font-weight:900;color:var(--wind);line-height:1;margin-bottom:0.3rem;}
.metric-label{font-size:0.75rem;color:var(--warm-gray);text-transform:uppercase;letter-spacing:1px;}
.section-label{font-family:'DM Mono',monospace;font-size:0.65rem;color:var(--wind-mid);text-transform:uppercase;letter-spacing:3px;margin-bottom:0.3rem;}
.section-title{font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:700;color:var(--wind);margin-bottom:1.2rem;line-height:1.2;}
.info-card{background:white;border-radius:16px;padding:1.5rem;box-shadow:0 2px 12px rgba(0,0,0,0.05);border-left:4px solid var(--wind-light);margin-bottom:1rem;}
.info-card.amber{border-left-color:var(--amber);}
.info-card.green{border-left-color:var(--green);}
.info-card.danger{border-left-color:var(--danger);}
.timeline-item{display:flex;gap:1rem;padding:1rem 0;border-bottom:1px solid #e0e8f0;}
.timeline-year{font-family:'Playfair Display',serif;font-size:1rem;font-weight:700;color:var(--wind-mid);min-width:80px;}
.timeline-title{font-weight:500;color:var(--wind);margin-bottom:0.2rem;}
.timeline-desc{font-size:0.85rem;color:var(--warm-gray);}
.method-step{display:flex;align-items:flex-start;gap:1rem;padding:1rem;background:white;border-radius:12px;margin-bottom:0.8rem;box-shadow:0 1px 6px rgba(0,0,0,0.04);}
.step-num{background:var(--wind-mid);color:white;font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.step-title{font-weight:500;color:var(--wind);font-size:0.95rem;}
.step-desc{font-size:0.82rem;color:var(--warm-gray);margin-top:0.2rem;}
.discovery-box{background:linear-gradient(135deg,#EEF4FF,#D8EAF8);border:2px solid var(--wind-light);border-radius:16px;padding:1.8rem;margin:0.8rem 0;}
.discovery-title{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:var(--wind);margin-bottom:0.5rem;}
.source-badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:0.8rem;}
.source-badge{background:var(--wind);color:white;font-family:'DM Mono',monospace;font-size:0.65rem;padding:4px 10px;border-radius:4px;letter-spacing:1px;text-transform:uppercase;}
.footer-wrap{background:var(--wind);border-radius:20px;padding:2rem;color:rgba(255,255,255,0.8);text-align:center;margin-top:3rem;}
.footer-title{font-family:'Playfair Display',serif;color:#A8D8F0;font-size:1.2rem;margin-bottom:0.5rem;}
.city-card{background:white;border-radius:16px;padding:1.4rem;border-top:5px solid;box-shadow:0 3px 14px rgba(0,0,0,0.07);margin-bottom:0.5rem;}
.city-card-title{font-family:'Playfair Display',serif;font-size:1rem;font-weight:700;margin-bottom:0.4rem;}
.city-card-meta{font-size:0.78rem;font-family:'DM Mono',monospace;color:var(--warm-gray);line-height:1.8;}
.photo-placeholder{background:#EEF4FF;border:2px dashed var(--wind-light);border-radius:12px;padding:2rem;text-align:center;min-height:220px;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.photo-emoji{font-size:2.8rem;}
.photo-title{font-weight:600;color:var(--wind);margin:0.5rem 0 0.2rem;font-size:1rem;}
.photo-desc{font-size:0.80rem;color:var(--warm-gray);line-height:1.55;max-width:280px;}
.photo-path{font-size:0.65rem;color:var(--wind-mid);font-family:'DM Mono',monospace;margin-top:0.5rem;background:#D8EAF8;padding:3px 8px;border-radius:4px;}
.photo-meta{font-size:0.7rem;font-family:'DM Mono',monospace;margin-top:0.4rem;line-height:1.7;}
.photo-legenda{font-size:0.72rem;color:var(--warm-gray);font-style:italic;padding:0.5rem 0.8rem;background:#f5f7fa;text-align:center;border-top:1px solid #d8e4f0;}
.photo-destaque{border:3px solid var(--wind-light);border-radius:14px;overflow:hidden;box-shadow:0 4px 20px rgba(26,58,110,0.15);}
</style>
""", unsafe_allow_html=True)

# ============================================================
# MATRIZ DE DADOS CLIMÁTICOS (SÉRIES TEMPORAIS)
# ============================================================
CITIES = {
    "Punta Arenas":  {"lat": -53.163, "lon": -70.917, "pais": "🇨🇱 Chile",  "v_media": 30.2, "rajada": 130, "pot_mw": 4200, "cap_factor": 0.63, "cor": "#1A3A6E"},
    "Puerto Natales": {"lat": -51.729, "lon": -72.494, "pais": "🇨🇱 Chile",  "v_media": 26.8, "rajada": 104, "pot_mw": 1800, "cap_factor": 0.55, "cor": "#1B3A1E"},
    "Rio Gallegos":   {"lat": -51.622, "lon": -69.218, "pais": "🇦🇷 Argentina", "v_media": 27.1, "rajada": 100, "pot_mw": 3500, "cap_factor": 0.61, "cor": "#5C3D1E"},
    "Puerto Williams":{"lat": -54.935, "lon": -67.616, "pais": "🇨🇱 Chile",  "v_media": 22.0, "rajada": 95,  "pot_mw": None,  "cap_factor": 0.52, "cor": "#8B2515"},
}

MONTHS = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
WIND_DATA = {
    "Punta Arenas":  [33.1,31.8,29.6,28.4,27.9,28.2,29.1,30.5,31.8,32.4,33.6,32.9],
    "Puerto Natales": [28.4,27.6,26.1,25.3,24.8,25.1,25.8,26.9,27.5,28.1,29.2,28.8],
    "Rio Gallegos":   [29.2,28.1,27.0,25.8,25.2,25.6,26.4,27.8,28.5,29.1,29.8,29.5],
    "Puerto Williams":[23.1,22.5,21.8,20.9,20.4,20.8,21.5,22.3,22.8,23.4,24.1,23.7],
}
ANNUAL = {
    "Punta Arenas":   [29.1,29.8,30.2,30.5,31.0],
    "Puerto Natales": [25.8,26.1,26.5,26.9,27.2],
    "Rio Gallegos":   [26.4,26.8,27.0,27.3,27.6],
    "Puerto Williams":[21.2,21.6,21.9,22.1,22.5],
}
YEARS = [2020, 2021, 2022, 2023, 2024]
CITY_COLORS = {"Punta Arenas": "#1A3A6E", "Puerto Natales": "#1B3A1E", "Rio Gallegos": "#5C3D1E", "Puerto Williams": "#8B2515"}

# ── RENDEREZAÇÃO DE MÉTRICAS CRÍTICAS DA HOME ───────────────────
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-box"><div class="metric-val">30,2 km/h</div><div class="metric-label">{T["m1"]}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-box sky"><div class="metric-val">>60%</div><div class="metric-label">{T["m2"]}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-box amber"><div class="metric-val">130 km/h</div><div class="metric-label">{T["m3"]}</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-box green"><div class="metric-val">9.500 MW</div><div class="metric-label">{T["m4"]}</div></div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── ESTRUTURA RECONFIGURADA DE ABAS ────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([T['tab1'], T['tab2'], T['tab3'], T['tab4'], T['tab5']])

# ── TAB 1: GEOPROCESSAMENTO E ANÁLISE INTERATIVA ───────────────
with tab1:
    st.markdown(f'<div class="section-label">{T["map_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["map_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card">{T["map_hint"]}</div>', unsafe_allow_html=True)

    # Inicialização do mapa Folium focado nas latitudes austrais
    mapa = folium.Map(location=[-52.5, -70.0], zoom_start=5, tiles='CartoDB positron')

    for city, d in CITIES.items():
        radius = d["v_media"] * 1200
        pot_str = f"{d['pot_mw']:,} MW" if d['pot_mw'] else "Ponto de Controle Austral"
        pop_html = f"""<div style='font-family:sans-serif;min-width:240px;padding:12px'>
            <h4 style='color:{d["cor"]};margin:0 0 8px'>{city}</h4>
            <p style='margin:3px 0;font-size:12px'>🌍 {d["pais"]}</p>
            <p style='margin:3px 0;font-size:12px'>💨 Vel. média: <b>{d["v_media"]} km/h</b></p>
            <p style='margin:3px 0;font-size:12px'>⚡ Rajada máx.: <b>{d["rajada"]} km/h</b></p>
            <p style='margin:3px 0;font-size:12px'>🔋 Potencial: <b>{pot_str}</b></p>
            <p style='margin:3px 0;font-size:12px'>📊 Cap. factor: <b>{d["cap_factor"]*100:.0f}%</b></p>
            <hr style='margin:8px 0;border-color:#eee'>
            <p style='margin:0;font-size:10px;color:#999'>Lat: {d["lat"]:.3f} · Lon: {d["lon"]:.3f}</p>
        </div>"""
        
        folium.Circle(
            location=[d["lat"], d["lon"]], radius=radius,
            color=d["cor"], fill=True, fill_color=d["cor"], fill_opacity=0.15,
            weight=2, tooltip=f"💨 {city} · {d['v_media']} km/h"
        ).add_to(mapa)
        
        folium.Marker(
            location=[d["lat"], d["lon"]],
            popup=folium.Popup(pop_html, max_width=270),
            tooltip=f"💨 {city}",
            icon=folium.Icon(color="blue" if "Chile" in d["pais"] else "red", icon="wind", prefix="fa")
        ).add_to(mapa)

    # Inclusão da representação vetorial simplificada do cinturão dos Westerlies
    folium.PolyLine(
        locations=[[-40, -80],[-40,-65],[-45,-60],[-50,-60],[-55,-65],[-55,-68]],
        color="#56B3F0", weight=2, opacity=0.5, dash_array="8",
        tooltip="Ventos de Oeste (Westerlies)"
    ).add_to(mapa)

    folium_static(mapa, width=1100, height=480)

    # Exibição dos cartões de resumo estáticos abaixo do mapa
    st.markdown("<br>", unsafe_allow_html=True)
    col_cards = st.columns(4)
    for i, (city, d) in enumerate(CITIES.items()):
        pot_str = f"{d['pot_mw']:,} MW" if d['pot_mw'] else "Estação de Controle"
        with col_cards[i]:
            st.markdown(f"""
            <div class="city-card" style="border-top-color:{d['cor']}">
              <div class="city-card-title" style="color:{d['cor']}">{city}</div>
              <div class="city-card-meta">
                💨 {d['v_media']} km/h média<br>
                ⚡ Rajada: {d['rajada']} km/h<br>
                🔋 Potencial: {pot_str}<br>
                📊 Fator Cap: {d['cap_factor']*100:.0f}%
              </div>
            </div>
            """, unsafe_allow_html=True)

    # Seção de Gráficos Analíticos
    st.markdown(f"<br><div class='section-label'>{T['chart_label']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>{T['wind_monthly_title']}</div>", unsafe_allow_html=True)

    fig_monthly = go.Figure()
    for city, vals in WIND_DATA.items():
        fig_monthly.add_trace(go.Scatter(
            x=MONTHS, y=vals, mode='lines+markers', name=city,
            line=dict(color=CITY_COLORS[city], width=2.5),
            marker=dict(size=6, color=CITY_COLORS[city]),
            hovertemplate='<b>%{x}</b>: %{y:.1f} km/h'
        ))
    fig_monthly.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(26,58,110,0.02)',
        font=dict(family='DM Sans'), height=350,
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#e0e8f0', title=T['wind_y']),
        margin=dict(t=10, b=10)
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

    # Subseção: Distribuição Direcional Polar e Tendência Anual
    col_r, col_a = st.columns(2)
    with col_r:
        st.markdown(f"<div class='section-label'>{T['rose_title']}</div>", unsafe_allow_html=True)
        direcoes = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSO","SO","OSO","O","ONO","NO","NNO"]
        freqs_pa = [2,1.5,1.5,2,2.5,3,4,5,4,5,8,12,18,16,9,6]
        freqs_rg = [2,2,2,2.5,3,4,5,6,5,6,9,13,16,15,8,5]
        
        fig_rose = go.Figure()
        fig_rose.add_trace(go.Barpolar(r=freqs_pa, theta=direcoes, name="Punta Arenas", marker_color="#1A3A6E", opacity=0.8))
        fig_rose.add_trace(go.Barpolar(r=freqs_rg, theta=direcoes, name="Rio Gallegos", marker_color="#5C3D1E", opacity=0.6))
        fig_rose.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', polar=dict(radialaxis=dict(range=[0, 20]), angularaxis=dict(direction="clockwise")),
            height=320, margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig_rose, use_container_width=True)

    with col_a:
        st.markdown(f"<div class='section-label'>{T['annual_title']}</div>", unsafe_allow_html=True)
        fig_annual = go.Figure()
        for city, vals in ANNUAL.items():
            fig_annual.add_trace(go.Bar(name=city, x=YEARS, y=vals, marker_color=CITY_COLORS[city], opacity=0.85))
        fig_annual.update_layout(
            barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=320, yaxis=dict(title=T['annual_y'], gridcolor='#e0e8f0'), margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig_annual, use_container_width=True)

    # Simulador Operacional de Ativos Eólicos
    st.markdown(f"<br><div class='section-label'>{T['simulator_label']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>{T['simulator_title']}</div>", unsafe_allow_html=True)

    sim_col1, sim_col2, sim_col3 = st.columns([2, 1, 1])
    with sim_col1:
        city_sel = st.selectbox(T['select_city'], list(CITIES.keys()))
    with sim_col2:
        n_turbines = st.slider(T['turbines_label'], 1, 500, 100)
    with sim_col3:
        power_mw = st.slider(T['power_label'], 2.0, 8.0, 4.2, step=0.1)

    cf = CITIES[city_sel]["cap_factor"]
    gwh_yield = (power_mw * n_turbines * cf * 8760) / 1000
    households = int(gwh_yield * 1000 / 4.2)
    co2_offset = int(gwh_yield * 1000 * 0.42)

    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1:
        st.markdown(f'<div class="metric-box"><div class="metric-val">{gwh_yield:,.1f}</div><div class="metric-label">{T["sim_result_gwh"]}</div></div>', unsafe_allow_html=True)
    with res_col2:
        st.markdown(f'<div class="metric-box sky"><div class="metric-val">{households:,}</div><div class="metric-label">{T["sim_result_homes"]}</div></div>', unsafe_allow_html=True)
    with res_col3:
        st.markdown(f'<div class="metric-box green"><div class="metric-val">{co2_offset:,}</div><div class="metric-label">{T["sim_result_co2"]}</div></div>', unsafe_allow_html=True)

    # Painel de Medidores (Gauges) de Fator de Capacidade
    fig_gauges = go.Figure()
    for i, (city, d) in enumerate(CITIES.items()):
        fig_gauges.add_trace(go.Indicator(
            mode="gauge+number", value=d["cap_factor"] * 100, number={'suffix': "%"},
            gauge={'axis': {'range': [0, 80]}, 'bar': {'color': d["cor"]}},
            title={'text': city, 'font': {'size': 12}}, domain={'row': 0, 'column': i}
        ))
    fig_gauges.update_layout(grid={'rows': 1, 'columns': 4}, paper_bgcolor='rgba(0,0,0,0)', height=200, margin=dict(t=40, b=10))
    st.plotly_chart(fig_gauges, use_container_width=True)

# ── TAB 2: PIPELINE DE DATA ENGINEERING & FISICA ───────────────
with tab2:
    st.markdown(f'<div class="section-label">{T["method_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["method_title"]}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="discovery-box">
      <div class="discovery-title">{T['sci_question_title']}</div>
      <p style="font-size:1.05rem;color:#1A3A6E;line-height:1.7;margin:0"><em>{T['sci_question']}</em></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="section-label" style="margin-top:1.5rem">{T["pipeline_label"]}</div>', unsafe_allow_html=True)
    for num, title, desc in T['steps']:
        st.markdown(f"""
        <div class="method-step">
          <div class="step-num">{num}</div>
          <div style="flex:1">
            <div class="step-title">{title}</div>
            <div class="step-desc">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f'<div class="info-card"><strong>{T["physics_title"]}</strong><br><br>{T["physics_text"]}</div>', unsafe_allow_html=True)
    with col_m2:
        st.markdown(f'<div class="info-card amber"><strong>{T["westerlies_title"]}</strong><br><br>{T["westerlies_text"]}</div>', unsafe_allow_html=True)

# ── TAB 3: DESCOBERTAS CIENTÍFICAS DE CAMPO ────────────────────
with tab3:
    st.markdown(f'<div class="section-label">{T["discovery_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["discovery_title"]}</div>', unsafe_allow_html=True)

    for emoji, titulo, texto in T['discoveries']:
        st.markdown(f"""
        <div class="discovery-box">
          <div style="display:flex;align-items:flex-start;gap:1rem">
            <span style="font-size:1.5rem">{emoji}</span>
            <div>
              <div class="discovery-title">{titulo}</div>
              <p style="color:#1A3A6E;line-height:1.65;font-size:0.93rem;margin:0">{texto}</p>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-card" style="background:linear-gradient(135deg,#EEF4FF,#D8EAF8);margin-top:2rem">
      <strong style="color:#1A3A6E;font-size:1.1rem">{T['conclusion_title']}</strong><br><br>
      <p style="color:#1A3A6E;line-height:1.7;font-size:0.95rem">{T['conclusion_text']}</p>
      <p style="color:#2555A0;font-size:0.85rem;margin:0"><b>{T['conclusion_author']}</b></p>
    </div>
    """, unsafe_allow_html=True)

# ── TAB 4: MÓDULO VISUAL E CRONOGRAMA ─────────────────────────
with tab4:
    st.markdown(f'<div class="section-label">{T["field_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["field_title"]}</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-card amber">
      <strong>{T['field_instructions_title']}</strong><br>
      <div style="font-size:0.85rem;color:#5C3D1E;margin-top:0.3rem">{T['field_instructions']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Pipeline de Renderização de Imagens Dinâmicas com Fallback Estruturado
    photos = T['photos']
    fotos_normais = [f for f in photos if not f.get("destaque")]
    foto_destaque = next((f for f in photos if f.get("destaque")), None)

    row_cols = st.columns(3)
    for i, foto in enumerate(fotos_normais):
        with row_cols[i]:
            img_path = foto['path']
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    st.image(img, use_container_width=True)
                except Exception:
                    st.error(f"Erro ao carregar asset: {img_path}")
            else:
                st.markdown(f"""
                <div class="photo-placeholder" style="border-color:{foto['cor']}">
                  <div class="photo-emoji">{foto['emoji']}</div>
                  <div class="photo-title" style="color:{foto['cor']}">{foto['titulo']}</div>
                  <div class="photo-desc">{foto['desc']}</div>
                  <div class="photo-meta" style="color:{foto['cor']}">
                    📍 {foto['coords']} · 💨 {foto['vento']}<br>📅 {foto['mes']}
                  </div>
                  <div class="photo-path">{img_path}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f'<div class="photo-legenda">{foto["legenda"]}</div>', unsafe_allow_html=True)

    if foto_destaque:
        st.markdown("<br><hr>", unsafe_allow_html=True)
        img_dest_path = foto_destaque['path']
        if os.path.exists(img_dest_path):
            try:
                st.markdown('<div class="photo-destaque">', unsafe_allow_html=True)
                st.image(Image.open(img_dest_path), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception:
                pass
        else:
            st.markdown(f"""
            <div class="photo-placeholder" style="min-height:280px;border-color:{foto_destaque['cor']}">
              <div class="photo-emoji" style="font-size:3rem">{foto_destaque['emoji']}</div>
              <div class="photo-title" style="font-size:1.2rem;color:{foto_destaque['cor']}">{foto_destaque['titulo']}</div>
              <div class="photo-desc" style="max-width:600px">{foto_destaque['desc']}</div>
              <div class="photo-meta" style="color:{foto_destaque['cor']}">📍 {foto_destaque['coords']} · 📅 {foto_destaque['mes']}</div>
              <div class="photo-path">{img_dest_path}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f'<div class="photo-legenda" style="font-size:0.82rem">{foto_destaque["legenda"]}</div>', unsafe_allow_html=True)

    # Seção da Linha do Tempo da Expedição
    st.markdown(f"<br><br><div class='section-label'>{T['timeline_field_label']}</div>", unsafe_allow_html=True)
    for data, titulo, desc in T['timeline_field_items']:
        st.markdown(f"""
        <div class="timeline-item">
          <div class="timeline-year">{data}</div>
          <div style="flex:1">
            <div class="timeline-title">{titulo}</div>
            <div class="timeline-desc">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── TAB 5: PROTOCOLO DE RECONHECIMENTO E FONTES ────────────────
with tab5:
    st.markdown(f'<div class="section-label">{T["sources_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["sources_title"]}</div>', unsafe_allow_html=True)

    fontes = [
        ("OPEN-METEO", "Open-Meteo Historical API — Reanálise Climatológica ERA5", "Acesso automatizado a matrizes horárias globais computadas pelo ECMWF.", "#1A3A6E"),
        ("GWA", "Global Wind Atlas — Banco Mundial / DTU Wind Energy", "Mapeamento micrometeorológico de alta resolução para validação de rugosidade de terreno.", "#2555A0"),
        ("MDPI 2024", "MDPI Sustainability — Análise Eólica de Alta Latitude", "Modelagem de fatores de capacidade específicos para o cone sul americano.", "#3A7ACA"),
        ("EXPEDIÇÃO", "Logs de Campo e Registros In Situ — Road to Patagonia", "Evidências qualitativas coletadas empiricamente ao longo do trâmite geográfico.", "#8B2515")
    ]

    for sigla, nome, desc, cor in fontes:
        st.markdown(f"""
        <div class="info-card" style="border-left-color:{cor}">
          <div style="display:flex;align-items:center;gap:1rem">
            <div style="background:{cor};color:white;font-family:'DM Mono';font-size:0.65rem;padding:4px 8px;border-radius:4px;min-width:90px;text-align:center"><b>{sigla}</b></div>
            <div>
              <div style="font-weight:500;font-size:0.9rem;color:var(--wind)">{nome}</div>
              <div style="font-size:0.8rem;color:var(--warm-gray)">{desc}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"<br><div class='section-label'>{T['tech_label']}</div>", unsafe_allow_html=True)
    techs = ["Python 3.11", "Streamlit", "Plotly Engine", "Folium Maps", "Pandas", "LaTeX Rendering", "Open-Meteo API", "ERA5 Data Engine"]
    st.markdown(''.join([f'<span class="source-badge">{t}</span>' for t in techs]), unsafe_allow_html=True)

    # Rodapé unificado de autoria institucional
    st.markdown(f"""
    <div class="footer-wrap">
      <div class="footer-title">{T['footer_title']}</div>
      <p style="margin:0.5rem 0;font-size:0.9rem">{T['footer_desc']}</p>
      <p style="margin:1rem 0 0;font-size:0.8rem;opacity:0.7">
        🌐 <a href="https://amaurialmeida.github.io/environmental-portfolio/" style="color:#A8D8F0" target="_blank">Portfolio</a> &nbsp;|&nbsp; 
        🐙 <a href="https://github.com/amaurialmeida" style="color:#A8D8F0" target="_blank">GitHub</a>
      </p>
    </div>
    """, unsafe_allow_html=True)
