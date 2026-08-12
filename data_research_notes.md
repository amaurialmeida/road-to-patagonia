# Pesquisa de dados — Road to Patagonia

## 12 de agosto de 2026

### Brasil
A ANP mantém um painel Power BI de preços de combustíveis, localizado em https://app.powerbi.com/view?r=eyJrIjoiMGM0NDhhMTUtMjQwZi00N2RlLTk1M2UtYjkxZTlkNzM1YzE5IiwidCI6IjQ0OTlmNGZmLTI0YTYtNGI0Mi1iN2VmLTEyNGFmY2FkYzkxMyJ9. O resultado de busca indicou atualização dos dados em 07/08/2026. O painel é dinâmico e, na sessão de pesquisa, não expôs imediatamente as tabelas no texto; deve ser tratado como fonte de consulta/validação, não como endpoint simples.

Também foi localizado o painel de preços médios de diesel da Petrobras em https://precos.petrobras.com.br/precos-diesel, com referência baseada em dados da ANP. O resultado de busca indicou preço médio do Brasil de R$ 6,95 para diesel, publicado em agosto de 2026; o valor precisa ser rechecado no momento da integração e acompanhado da data de coleta.

### Diretriz de arquitetura
O aplicativo não deve afirmar "preço atualizado diariamente" sem registrar timestamp e fonte por observação. O modelo de dados deverá guardar país, cidade/parada, combustível, preço, moeda, preço convertido, data de coleta, URL da fonte e nível de confiabilidade. Para fontes sem API pública, usar um adaptador manual/CSV ou uma fonte pública alternativa e expor claramente a data da última atualização.

### Itens a pesquisar
1. Preços regionais de gasolina/nafta e diesel/gasoil no Uruguai, Argentina e Chile.
2. Tarifas e regras de travessias por balsa/ferry, especialmente Estreito de Magalhães e travessias entre Ushuaia e Puerto Williams.
3. Tarifas de recarga elétrica por país/rede e distinção entre preço residencial, público por kWh, taxa de conexão e estacionamento.
4. Fatores de emissão e método de cálculo para combustível fóssil, eletricidade e travessias.
5. Necessidade de indicar estimativas quando a tarifa depende de veículo, temporada, câmbio, disponibilidade ou cotação comercial.

## Fontes preliminares
- ANP — painel de preços de combustíveis: https://app.powerbi.com/view?r=eyJrIjoiMGM0NDhhMTUtMjQwZi00N2RlLTk1M2UtYjkxZTlkNzM1YzE5IiwidCI6IjQ0OTlmNGZmLTI0YTYtNGI0Mi1iN2VmLTEyNGFmY2FkYzkxMyJ9
- Petrobras — preços médios de diesel: https://precos.petrobras.com.br/precos-diesel
- Resultado de pesquisa GlobalPetrolPrices — Argentina: https://es.globalpetrolprices.com/Argentina/diesel_prices/
- Resultado de pesquisa GlobalPetrolPrices — preços globais de gasolina: https://es.globalpetrolprices.com/gasoline_prices/

## Observação metodológica
As cifras previamente presentes no app (~US$ 460 para Tesla e ~US$ 1.250 para Tucson) são estimativas de simulação. A nova versão deverá recalculá-las a partir dos valores por trecho, combustível/energia, consumo, câmbio e tarifas de travessia, exibindo também uma faixa de incerteza.

### Uruguai — ANCAP
A página oficial de histórico da ANCAP, https://www.ancap.com.uy/10564/1/historico-precios-combustibles.html, expõe uma tabela por data. Para 01/08/2026, os valores publicados são: Nafta Súper 95 30S = 88,67 UYU/L; Nafta Premium 97 30S = 91,19 UYU/L; Gasoil 50S = 58,68 UYU/L; Gasoil 10S = 67,33 UYU/L; querosene = 67,50 UYU/L; Supergás = 93,56 UYU/kg. O app deve usar a data de vigência e mostrar moeda local, conversão opcional e fonte.

### Argentina — consulta por estação
A Secretaria de Energia da Argentina mantém a página oficial de consulta em http://res1104.se.gob.ar/consultaprecios.eess.php. A página permite consultar preços públicos por estação, província, localidade e produto, além de mínimos e máximos. A navegação automatizada não renderizou o conteúdo no navegador, mas a página HTML foi salva para inspeção técnica. Essa fonte é adequada para alimentar uma rotina de coleta, desde que o formato/endpoint seja confirmado e que a aplicação respeite a data de atualização de cada registro.

### Decisão provisória
Para o Uruguai, usar ANCAP como referência nacional e permitir ajuste por localidade. Para a Argentina, preferir preço por estação/localidade para Buenos Aires, Bahía Blanca, Puerto Madryn, Comodoro Rivadavia, Río Gallegos e Ushuaia, em vez de um único preço nacional. Caso a coleta automática da página não seja estável, expor importação de CSV/JSON e marcar o dado como "última coleta".

### Chile — API CNE
A Comisión Nacional de Energía disponibiliza um catálogo público em https://api.cne.cl/ e uma documentação em https://apidocs.cne.cl/. A documentação lista o endpoint GET `/api/v4/estaciones`, além de listas de distribuidores e tipos de combustível. Também há endpoint de fatores de emissão. A documentação indica uso de token Bearer e login para obtê-lo; portanto, a integração automática precisa tratar credencial/configuração separadamente, sem embutir token no repositório público.

### Travessia preliminar — Estreito de Magalhães
A pesquisa localizou notícias recentes sobre tarifas do cruce Primera Angostura, mas os resultados não são a fonte primária final. Como o valor é alterado e depende do tipo de veículo, o app deverá modelar a travessia como item logístico próprio: empresa/operador, origem, destino, veículo, moeda, tarifa, data de vigência, duração aproximada, frequência e status operacional. Para a versão publicada, a tarifa deve ser carregada de fonte oficial do operador ou apresentada como estimativa com data e link.

### Próximos passos de dados
- Confirmar a página oficial do operador da balsa Primera Angostura/TABSA e tarifas vigentes.
- Confirmar a operação e preço do ferry de passageiros/veículos entre Ushuaia e Puerto Williams; a viagem pode exigir transporte separado do carro, dependendo do serviço e das regras de embarque.
- Pesquisar preços de eletricidade/recarga pública e fatores de emissão por país.
- Implementar fallback por arquivo de dados versionado quando APIs exigirem token ou não forem estáveis.

### Travessia do Estreito de Magalhães — TABSA
A TABSA é o operador oficial localizado em https://www.tabsa.cl/rutas/primera-angostura e mantém um portal de reservas em https://reservas.tabsa.cl/. A página da rota é uma aplicação JavaScript e não expôs a tabela de tarifas no texto extraído; o portal de reservas confirma que a compra depende de origem, destino, data e número de passageiros. A integração deve consultar a tarifa por data/veículo ou manter uma tabela de referência versionada, sempre com status "a confirmar" quando o preço não puder ser obtido automaticamente.

### Ushuaia ↔ Puerto Williams — diferença logística importante
A página comercial https://www.ushuaiapuertowilliams.com/cruce-canal-beagle/ apresenta o serviço como "Cruce Ushuaia a Puerto Williams — Tickets y Reserva". O resultado de pesquisa associado indica preço a partir de US$ 235 por pessoa e trecho para 2026–2027, com taxa portuária de Ushuaia de US$ 10, mas o valor deve ser tratado como cotação comercial/indicativa, não como tarifa oficial universal. A interface deve deixar explícito que este cruce é normalmente um serviço de passageiros e que o Tesla/Tucson não deve ser presumido como embarcável. Para simular a viagem completa com carro, o app precisa oferecer dois cenários: (a) veículo permanece na rota terrestre e o trecho Puerto Williams é explorado sem o carro; (b) logística especial de transporte do veículo, com cotação separada e confirmação do operador.

### Regra para custos de água
Toda travessia deve aparecer como um evento da rota com campos: tipo (balsa/ferry), trecho, veículo embarcado (sim/não), passageiro, tarifa base, taxa portuária, moeda, câmbio usado, data de vigência, duração, frequência, risco climático e link de reserva. Isso evita somar incorretamente uma passagem de passageiro como se fosse uma tarifa para automóvel.

### Emissões — EPA/IPCC
A EPA documenta 8.887 g CO2 por galão de gasolina e 10.180 g CO2 por galão de diesel, assumindo conversão do carbono em CO2 e citando o IPCC 2006. Fonte: https://www.epa.gov/energy/greenhouse-gas-equivalencies-calculator-calculations-and-references. Convertendo por galão americano, isso equivale aproximadamente a 2,348 kg CO2/L de gasolina e 2,689 kg CO2/L de diesel. O app deve separar emissões diretas do escapamento das emissões associadas à geração da eletricidade; para a eletricidade, usar um fator por país/região quando disponível e deixar explícita a hipótese.

### Modelo ambiental recomendado
- Tucson: distância rodoviária × consumo em L/100 km × fator de emissão do combustível.
- Tesla: distância rodoviária × consumo em kWh/100 km × preço da energia e fator de emissão da eletricidade.
- Travessias: adicionar tarifa financeira e, opcionalmente, emissões do ferry como item separado, sem atribuí-las automaticamente ao veículo.
- Exibir CO2 direto, CO2 da energia e CO2 total estimado em abas distintas para evitar falsa precisão.

### Argentina — referência atual
A página https://www.globalpetrolprices.com/Argentina/gasoline_prices/ informa, em 10/08/2026, gasolina Octane-95 a ARS 2.055,00/L (US$ 1,38/L), com fonte indicada como Secretaría de Energía da Argentina e frequência semanal. A mesma página informa que a série é obtida de fontes oficiais/regulatórias e atualizada semanalmente. Para o app, este número é uma referência nacional; a versão detalhada por parada deve preferir a consulta oficial por estação/localidade, pois Río Gallegos, Comodoro Rivadavia e Ushuaia podem divergir.

### Observação de atualização
O requisito do usuário de atualização diária deve ser apresentado de forma honesta: algumas fontes publicam diariamente, outras semanalmente ou por vigência mensal. O painel deverá exibir a data e a frequência real de cada fonte, em vez de afirmar que todos os preços mudam diariamente.

### Validação da interface — 12/08/2026
O Streamlit abre corretamente, a barra lateral, os controles de atualização diária, câmbio e a página inicial foram renderizados. Na primeira carga com atualização online habilitada, a lateral aparece antes do conteúdo principal, indicando que as requisições externas podem atrasar a primeira renderização. A arquitetura deve manter o snapshot local como caminho rápido e fazer a tentativa online de forma mais curta/segura, para não bloquear a experiência visual.

O dossiê renderizado antes da correção mostrou que o custo por trecho estava calculado e que o trecho Ushuaia → Puerto Williams aparecia como 80 km. Foi corrigido para modal "Água / ferry" e `drive_km = 0`, evitando tratar o canal como rodovia; o custo da travessia continua na tabela própria de ferries.
