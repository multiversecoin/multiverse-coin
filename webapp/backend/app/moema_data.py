"""
Base de conhecimento completa sobre o bairro de Moema, Sao Paulo.
Organizada em modulos para consulta sob demanda pela MIA.
"""

# ============================================================
# HISTORIA DE MOEMA
# ============================================================
MOEMA_HISTORY = [
    {
        "year": "1500s",
        "title": "Origens Indigenas",
        "content": "O territorio onde hoje fica Moema era habitado pelos povos indigenas Tupi-Guarani. O nome 'Moema' vem do tupi e significa 'a que faz doer', 'a que adormece' ou 'falsa'. E tambem o nome de uma personagem do poema epico 'Caramuru' de Santa Rita Durao, uma jovem indigena apaixonada pelo naufrago portugues Diogo Alvares Correia."
    },
    {
        "year": "1890s",
        "title": "Primeiros Loteamentos",
        "content": "No final do seculo XIX, a regiao comecou a ser loteada. Era uma area rural, com chácaras e fazendas nos arredores da cidade de Sao Paulo. O bairro fazia parte do antigo distrito de Indianopolis."
    },
    {
        "year": "1920s",
        "title": "Desenvolvimento Inicial",
        "content": "Na decada de 1920, Moema comecou a se desenvolver com a chegada do bonde eletrico e a abertura de novas ruas. A Avenida Ibirapuera (hoje Avenida Brigadeiro Luis Antonio na regiao) e a proximidade com o centro impulsionaram o crescimento."
    },
    {
        "year": "1930s-1940s",
        "title": "Aeroporto de Congonhas",
        "content": "Em 1936, foi inaugurado o Aeroporto de Congonhas, na fronteira de Moema. Isso trouxe grande valorizacao ao bairro e mudou completamente sua dinamica urbana. Hoteis, restaurantes e servicos surgiram para atender viajantes."
    },
    {
        "year": "1954",
        "title": "Parque Ibirapuera",
        "content": "A inauguracao do Parque Ibirapuera em 1954, projetado por Oscar Niemeyer para o IV Centenario de Sao Paulo, transformou a regiao. Moema ganhou um dos maiores parques urbanos da America Latina como vizinho, atraindo moradores de classe media e alta."
    },
    {
        "year": "1960s-1970s",
        "title": "Verticalizacao",
        "content": "Moema passou por intensa verticalizacao, com a construcao de edificios residenciais de alto padrao. O bairro consolidou-se como uma das regioes mais valorizadas de Sao Paulo, com excelente infraestrutura e qualidade de vida."
    },
    {
        "year": "1980s",
        "title": "Boom Comercial",
        "content": "A decada de 1980 trouxe o Shopping Ibirapuera (1976, nas proximidades) e uma explosao do comercio de rua. A Avenida Moema e ruas adjacentes se tornaram polos gastronomicos e de compras, com restaurantes, bares e boutiques."
    },
    {
        "year": "1990s",
        "title": "Consolidacao como Bairro Nobre",
        "content": "Moema se consolidou como um dos bairros mais desejados de SP. O metro chegou com as estacoes Moema e Eucaliptos (Linha 5-Lilas), melhorando a acessibilidade. O bairro ganhou fama pela qualidade de vida, seguranca e oferta de servicos."
    },
    {
        "year": "2000s",
        "title": "Polo Gastronomico",
        "content": "Moema se tornou um dos principais polos gastronomicos de Sao Paulo, com centenas de restaurantes de diversas culinarias. A regiao da Alameda dos Arapanes e Avenida Moema concentram opcoes que vao de culinaria japonesa a italiana, passando por hamburguerias artesanais e confeitarias."
    },
    {
        "year": "2010s",
        "title": "Metro Linha 5 Lilas Expandida",
        "content": "A expansao da Linha 5-Lilas do metro conectou Moema ao centro de SP e a outras linhas. As estacoes Moema (2018) e Eucaliptos trouxeram nova onda de valorizacao e acessibilidade ao bairro."
    },
    {
        "year": "2020s",
        "title": "Moema Digital e Sustentavel",
        "content": "Moema se destaca por iniciativas de sustentabilidade e digitalizacao. O bairro abraca tecnologia com alta penetracao de apps de delivery, pagamentos digitais e servicos sob demanda. A comunidade e engajada em questoes ambientais, com feiras organicas e iniciativas verdes."
    },
    {
        "year": "2025",
        "title": "Multiverse Coin nasce em Moema",
        "content": "O projeto Multiverse Coin escolhe Moema como laboratorio para a primeira economia digital hiperlocal do Brasil. Com ~100 mil moradores, +10 mil CNPJs ativos e 3.500 estabelecimentos, o bairro e o cenario ideal para provar que economia circular, tecnologica e com proposito e possivel."
    }
]

# ============================================================
# LUGARES E PONTOS DE INTERESSE
# ============================================================
MOEMA_PLACES = [
    {
        "name": "Parque Ibirapuera",
        "category": "parque",
        "description": "Um dos maiores e mais importantes parques urbanos da America Latina, com 158 hectares. Projetado por Oscar Niemeyer, abriga museus (MAM, MAC, Afro Brasil), o Auditorio Ibirapuera, pistas de corrida, ciclovia, quadras e areas verdes exuberantes. E o coracao verde de Moema.",
        "address": "Av. Pedro Alvares Cabral - Vila Mariana",
        "lat": -23.5874,
        "lng": -46.6576,
        "rating": 4.8,
        "cashback_mvc": 0,
        "tags": ["parque", "lazer", "cultura", "esporte", "familia"]
    },
    {
        "name": "Shopping Ibirapuera",
        "category": "shopping",
        "description": "Um dos shoppings mais tradicionais de Sao Paulo, com mais de 400 lojas, cinema, praca de alimentacao e eventos culturais. Localizado na Av. Ibirapuera, e referencia de compras na regiao.",
        "address": "Av. Ibirapuera, 3103 - Moema",
        "lat": -23.6095,
        "lng": -46.6658,
        "rating": 4.5,
        "cashback_mvc": 3,
        "tags": ["compras", "lazer", "gastronomia", "cinema"]
    },
    {
        "name": "Aeroporto de Congonhas",
        "category": "transporte",
        "description": "O segundo aeroporto mais movimentado do Brasil, na fronteira de Moema. Opera voos domesticos e e fundamental para a economia do bairro, trazendo executivos e turistas.",
        "address": "Av. Washington Luis, s/n - Campo Belo",
        "lat": -23.6261,
        "lng": -46.6564,
        "rating": 4.0,
        "cashback_mvc": 0,
        "tags": ["transporte", "viagem", "negocios"]
    },
    {
        "name": "Praca Perola Byington",
        "category": "praca",
        "description": "Praca charmosa no coracao de Moema, cercada por restaurantes e cafes. E um ponto de encontro dos moradores, especialmente nos finais de semana. Homenageia Perola Byington, pioneira do servico social no Brasil.",
        "address": "R. Canario - Moema",
        "lat": -23.5977,
        "lng": -46.6621,
        "rating": 4.3,
        "cashback_mvc": 0,
        "tags": ["praca", "lazer", "encontro", "pet-friendly"]
    },
    {
        "name": "Estacao Moema (Metro)",
        "category": "transporte",
        "description": "Estacao da Linha 5-Lilas do metro, inaugurada em 2018. Conecta Moema ao centro de SP e outras regioes, facilitando o acesso ao bairro.",
        "address": "R. dos Jurubatubas - Moema",
        "lat": -23.6002,
        "lng": -46.6656,
        "rating": 4.2,
        "cashback_mvc": 0,
        "tags": ["transporte", "metro"]
    },
    {
        "name": "Estacao Eucaliptos (Metro)",
        "category": "transporte",
        "description": "Estacao da Linha 5-Lilas do metro na regiao de Moema/Indianopolis.",
        "address": "R. Sena Madureira - Vila Mariana",
        "lat": -23.5939,
        "lng": -46.6601,
        "rating": 4.1,
        "cashback_mvc": 0,
        "tags": ["transporte", "metro"]
    },
    {
        "name": "MAM - Museu de Arte Moderna",
        "category": "cultura",
        "description": "Localizado dentro do Parque Ibirapuera, o MAM abriga acervo de mais de 5 mil obras de arte moderna e contemporanea. Tem programacao cultural intensa com exposicoes, oficinas e eventos.",
        "address": "Parque Ibirapuera, Portao 3 - Moema",
        "lat": -23.5871,
        "lng": -46.6554,
        "rating": 4.6,
        "cashback_mvc": 5,
        "tags": ["cultura", "museu", "arte", "exposicao"]
    },
    {
        "name": "Museu Afro Brasil Emanoel Araujo",
        "category": "cultura",
        "description": "Museu dedicado a cultura afro-brasileira dentro do Parque Ibirapuera. Acervo com mais de 6 mil obras sobre a influencia africana na formacao da identidade brasileira.",
        "address": "Parque Ibirapuera, Portao 10",
        "lat": -23.5858,
        "lng": -46.6574,
        "rating": 4.5,
        "cashback_mvc": 5,
        "tags": ["cultura", "museu", "historia", "afro-brasileiro"]
    },
    {
        "name": "Feira de Moema",
        "category": "feira",
        "description": "Feira livre tradicional que acontece semanalmente nas ruas de Moema. Oferece frutas, verduras, queijos, flores e produtos artesanais. E um ritual do bairro, onde moradores se encontram e fazem compras frescas.",
        "address": "Ruas de Moema (itinerante)",
        "lat": -23.5990,
        "lng": -46.6630,
        "rating": 4.7,
        "cashback_mvc": 8,
        "tags": ["feira", "alimentacao", "organico", "comunidade"]
    },
    {
        "name": "Alameda dos Arapanes",
        "category": "polo_gastronomico",
        "description": "Uma das ruas mais charmosas de Moema, repleta de restaurantes, bares e cafes. E o coracao gastronomico do bairro, perfeita para um passeio a pe experimentando diferentes culinarias.",
        "address": "Al. dos Arapanes - Moema",
        "lat": -23.5985,
        "lng": -46.6640,
        "rating": 4.6,
        "cashback_mvc": 0,
        "tags": ["gastronomia", "passeio", "restaurantes", "bares"]
    }
]

# ============================================================
# RESTAURANTES E GASTRONOMIA
# ============================================================
MOEMA_RESTAURANTS = [
    {
        "name": "Outback Steakhouse Moema",
        "cuisine": "Australiana/Steakhouse",
        "description": "Rede de restaurantes com ambiente descontraido e pratos generosos. Famoso pelas costelas, blooming onion e drinks.",
        "address": "Av. Moema, 401",
        "lat": -23.6008,
        "lng": -46.6635,
        "rating": 4.4,
        "price_range": "$$",
        "cashback_mvc": 8,
        "phone": "(11) 5051-0001",
        "hours": "11:30-23:00",
        "tags": ["steakhouse", "casual", "familia"]
    },
    {
        "name": "Sushi Leblon",
        "cuisine": "Japonesa",
        "description": "Restaurante japones sofisticado com sushis e sashimis premium. Ambiente elegante e atendimento impecavel.",
        "address": "Al. dos Arapanes, 60",
        "lat": -23.5988,
        "lng": -46.6645,
        "rating": 4.7,
        "price_range": "$$$",
        "cashback_mvc": 10,
        "phone": "(11) 5052-1234",
        "hours": "12:00-15:00, 19:00-23:00",
        "tags": ["japones", "sushi", "premium", "romantico"]
    },
    {
        "name": "Forneria San Paolo",
        "cuisine": "Italiana/Pizza",
        "description": "Pizzaria artesanal com forno a lenha e ingredientes importados da Italia. Massas frescas feitas diariamente.",
        "address": "R. Normandia, 240",
        "lat": -23.5995,
        "lng": -46.6620,
        "rating": 4.6,
        "price_range": "$$",
        "cashback_mvc": 12,
        "phone": "(11) 5055-3456",
        "hours": "18:00-00:00",
        "tags": ["pizza", "italiano", "artesanal", "familia"]
    },
    {
        "name": "Cafe Moema",
        "cuisine": "Cafeteria/Brunch",
        "description": "Cafeteria acolhedora com graos especiais torrados artesanalmente. Opcoes de brunch, bolos caseiros e sanduiches gourmet. Wifi rapido e ambiente perfeito para trabalhar.",
        "address": "R. Canario, 315",
        "lat": -23.5975,
        "lng": -46.6618,
        "rating": 4.8,
        "price_range": "$",
        "cashback_mvc": 15,
        "phone": "(11) 5053-7890",
        "hours": "07:00-20:00",
        "tags": ["cafe", "brunch", "trabalho", "wifi", "artesanal"]
    },
    {
        "name": "Hamburgueria Moema Burger",
        "cuisine": "Hamburgueria Artesanal",
        "description": "Hamburgueria craft com blend proprio de carnes nobres. Paes feitos na casa e molhos autorais. Opcoes veganas disponiveis.",
        "address": "R. Gaivota, 180",
        "lat": -23.6012,
        "lng": -46.6650,
        "rating": 4.5,
        "price_range": "$$",
        "cashback_mvc": 10,
        "phone": "(11) 5054-5678",
        "hours": "11:30-23:30",
        "tags": ["hamburgueria", "artesanal", "craft", "vegano"]
    },
    {
        "name": "Padaria Real Moema",
        "cuisine": "Padaria/Confeitaria",
        "description": "Padaria tradicional do bairro ha mais de 30 anos. Paes artesanais, doces finos, salgados e cafe fresquinho. Ponto de encontro dos moradores pela manha.",
        "address": "Av. Juriti, 521",
        "lat": -23.5968,
        "lng": -46.6625,
        "rating": 4.6,
        "price_range": "$",
        "cashback_mvc": 12,
        "phone": "(11) 5051-9012",
        "hours": "06:00-22:00",
        "tags": ["padaria", "cafe", "tradicion", "bairro", "manha"]
    },
    {
        "name": "Emporio Moema Gourmet",
        "cuisine": "Emporio/Gourmet",
        "description": "Emporio com produtos importados, vinhos selecionados, queijos artesanais e azeites premium. Oferece degustacoes nos finais de semana.",
        "address": "R. Canario, 450",
        "lat": -23.5982,
        "lng": -46.6615,
        "rating": 4.7,
        "price_range": "$$$",
        "cashback_mvc": 8,
        "phone": "(11) 5056-3421",
        "hours": "09:00-21:00",
        "tags": ["emporio", "gourmet", "vinho", "queijo", "importados"]
    },
    {
        "name": "Acai da Terra Moema",
        "cuisine": "Acaiteria/Saudavel",
        "description": "Acai puro do Para com toppings frescos. Opcoes de bowls proteicos, smoothies e sucos naturais. Ideal para pos-treino.",
        "address": "Al. dos Arapanes, 150",
        "lat": -23.5992,
        "lng": -46.6648,
        "rating": 4.4,
        "price_range": "$",
        "cashback_mvc": 15,
        "phone": "(11) 5057-6543",
        "hours": "08:00-22:00",
        "tags": ["acai", "saudavel", "fitness", "smoothie"]
    },
    {
        "name": "Churrascaria Moema Grill",
        "cuisine": "Churrascaria",
        "description": "Churrascaria premium com cortes nobres, rodizio completo e buffet de saladas. Ambiente familiar com espaco kids.",
        "address": "Av. Moema, 520",
        "lat": -23.6020,
        "lng": -46.6638,
        "rating": 4.5,
        "price_range": "$$$",
        "cashback_mvc": 7,
        "phone": "(11) 5058-8765",
        "hours": "11:30-16:00, 18:30-23:00",
        "tags": ["churrasco", "rodizio", "familia", "premium"]
    },
    {
        "name": "Loja de Chocolates Moema",
        "cuisine": "Chocolateria",
        "description": "Chocolateria artesanal com cacau brasileiro de origem unica. Trufas, bombons, barras bean-to-bar e chocolate quente especial. Perfeito para presentear.",
        "address": "R. Normandia, 95",
        "lat": -23.5998,
        "lng": -46.6628,
        "rating": 4.9,
        "price_range": "$$",
        "cashback_mvc": 12,
        "phone": "(11) 5059-1098",
        "hours": "10:00-20:00",
        "tags": ["chocolate", "artesanal", "presente", "doce", "bean-to-bar"]
    },
    {
        "name": "Restaurante Arabe Moema",
        "cuisine": "Arabe/Libanesa",
        "description": "Culinaria arabe autentica com esfihas, kibes, homus e pratos tipicos libaneses. Ambiente decorado com elementos do Oriente Medio.",
        "address": "R. Gaivota, 340",
        "lat": -23.6025,
        "lng": -46.6655,
        "rating": 4.6,
        "price_range": "$$",
        "cashback_mvc": 10,
        "phone": "(11) 5060-2109",
        "hours": "11:00-23:00",
        "tags": ["arabe", "libanes", "esfiha", "kibe"]
    },
    {
        "name": "Thai Garden Moema",
        "cuisine": "Tailandesa",
        "description": "Culinaria tailandesa autentica com ingredientes frescos. Pad Thai, curries, sopas e pratos wok. Ambiente zen e acolhedor.",
        "address": "Al. dos Arapanes, 220",
        "lat": -23.5990,
        "lng": -46.6642,
        "rating": 4.5,
        "price_range": "$$",
        "cashback_mvc": 10,
        "phone": "(11) 5061-3210",
        "hours": "12:00-15:00, 19:00-23:00",
        "tags": ["tailandes", "asiatico", "pad-thai", "curry"]
    }
]

# ============================================================
# OFERTAS E PROMOCOES
# ============================================================
MOEMA_OFFERS = [
    {
        "id": "offer_001",
        "business": "Loja de Chocolates Moema",
        "title": "Trufa Artesanal - Compre 3, Leve 4",
        "description": "Trufas premiadas de cacau brasileiro. Na compra de 3, ganhe 1 trufa extra + 12% cashback em MVC!",
        "original_price": 45.00,
        "offer_price": 33.75,
        "cashback_mvc": 12,
        "category": "gastronomia",
        "image_emoji": "🍫",
        "valid_until": "2025-12-31",
        "lat": -23.5998,
        "lng": -46.6628,
        "distance_text": "350m",
        "tags": ["chocolate", "presente", "doce"]
    },
    {
        "id": "offer_002",
        "business": "Cafe Moema",
        "title": "Combo Brunch Especial",
        "description": "Cafe especial + tosta de abacate + suco natural. Perfeito para comecar o dia! 15% de cashback em MVC.",
        "original_price": 38.00,
        "offer_price": 29.90,
        "cashback_mvc": 15,
        "category": "gastronomia",
        "image_emoji": "☕",
        "valid_until": "2025-12-31",
        "lat": -23.5975,
        "lng": -46.6618,
        "distance_text": "200m",
        "tags": ["cafe", "brunch", "manha"]
    },
    {
        "id": "offer_003",
        "business": "Forneria San Paolo",
        "title": "Pizza Margherita Artesanal",
        "description": "Pizza no forno a lenha com mozzarella de bufala e manjericao fresco. 12% cashback em MVC!",
        "original_price": 65.00,
        "offer_price": 49.90,
        "cashback_mvc": 12,
        "category": "gastronomia",
        "image_emoji": "🍕",
        "valid_until": "2025-12-31",
        "lat": -23.5995,
        "lng": -46.6620,
        "distance_text": "400m",
        "tags": ["pizza", "italiano", "jantar"]
    },
    {
        "id": "offer_004",
        "business": "Acai da Terra Moema",
        "title": "Bowl Proteico Pos-Treino",
        "description": "Acai 500ml + granola + banana + whey protein. Ideal para depois do treino! 15% cashback MVC.",
        "original_price": 32.00,
        "offer_price": 24.90,
        "cashback_mvc": 15,
        "category": "saudavel",
        "image_emoji": "🥤",
        "valid_until": "2025-12-31",
        "lat": -23.5992,
        "lng": -46.6648,
        "distance_text": "300m",
        "tags": ["acai", "fitness", "saudavel"]
    },
    {
        "id": "offer_005",
        "business": "Pet Shop Moema",
        "title": "Banho + Tosa com 20% OFF",
        "description": "Cuide do seu pet com qualidade! Banho e tosa com produtos premium + 10% cashback em MVC.",
        "original_price": 120.00,
        "offer_price": 96.00,
        "cashback_mvc": 10,
        "category": "servicos",
        "image_emoji": "🐾",
        "valid_until": "2025-12-31",
        "lat": -23.5970,
        "lng": -46.6610,
        "distance_text": "500m",
        "tags": ["pet", "animal", "servico"]
    },
    {
        "id": "offer_006",
        "business": "Academia FitMoema",
        "title": "Plano Mensal com 30% OFF",
        "description": "Musculacao + aulas coletivas + area funcional. Primeiro mes com desconto especial para usuarios MVC!",
        "original_price": 250.00,
        "offer_price": 175.00,
        "cashback_mvc": 8,
        "category": "saude",
        "image_emoji": "💪",
        "valid_until": "2025-12-31",
        "lat": -23.6005,
        "lng": -46.6660,
        "distance_text": "450m",
        "tags": ["academia", "fitness", "saude"]
    },
    {
        "id": "offer_007",
        "business": "Farmacia Sao Paulo Moema",
        "title": "Vitaminas com 25% OFF",
        "description": "Linha completa de vitaminas e suplementos com desconto exclusivo para usuarios Multiverse Coin!",
        "original_price": 89.90,
        "offer_price": 67.43,
        "cashback_mvc": 8,
        "category": "saude",
        "image_emoji": "💊",
        "valid_until": "2025-12-31",
        "lat": -23.6015,
        "lng": -46.6632,
        "distance_text": "600m",
        "tags": ["farmacia", "saude", "vitamina"]
    },
    {
        "id": "offer_008",
        "business": "Lavanderia Express Moema",
        "title": "Lavagem de Edredom por R$39,90",
        "description": "Lavagem profissional de edredom com amaciante premium. Entrega em 48h! 10% cashback MVC.",
        "original_price": 59.90,
        "offer_price": 39.90,
        "cashback_mvc": 10,
        "category": "servicos",
        "image_emoji": "👔",
        "valid_until": "2025-12-31",
        "lat": -23.5960,
        "lng": -46.6605,
        "distance_text": "550m",
        "tags": ["lavanderia", "servico", "casa"]
    },
    {
        "id": "offer_009",
        "business": "Floricultura Moema Garden",
        "title": "Buque de Rosas - De R$89 por R$59",
        "description": "Buque com 12 rosas vermelhas colombianas. Entrega no mesmo dia para Moema! 10% cashback MVC.",
        "original_price": 89.00,
        "offer_price": 59.00,
        "cashback_mvc": 10,
        "category": "compras",
        "image_emoji": "🌹",
        "valid_until": "2025-12-31",
        "lat": -23.5985,
        "lng": -46.6622,
        "distance_text": "250m",
        "tags": ["flores", "presente", "entrega"]
    },
    {
        "id": "offer_010",
        "business": "Mecanico Moema Auto",
        "title": "Revisao Completa por R$199",
        "description": "Revisao de 30 itens + troca de oleo + check-up eletronico. 5% cashback em MVC!",
        "original_price": 350.00,
        "offer_price": 199.00,
        "cashback_mvc": 5,
        "category": "servicos",
        "image_emoji": "🚗",
        "valid_until": "2025-12-31",
        "lat": -23.6030,
        "lng": -46.6665,
        "distance_text": "700m",
        "tags": ["automovel", "servico", "revisao"]
    }
]

# ============================================================
# SERVICOS DO BAIRRO
# ============================================================
MOEMA_SERVICES = [
    {
        "name": "Hospital Santa Cruz",
        "category": "saude",
        "description": "Hospital de referencia em Moema com pronto-socorro 24h, diversas especialidades medicas e tecnologia de ponta.",
        "address": "R. Santa Cruz, 398",
        "phone": "(11) 5080-2000",
        "cashback_mvc": 3,
        "tags": ["hospital", "emergencia", "saude"]
    },
    {
        "name": "UBS Moema",
        "category": "saude",
        "description": "Unidade Basica de Saude do bairro de Moema. Atendimento pelo SUS com consultas, vacinas e programas de prevencao.",
        "address": "R. Inhambupe, 100",
        "phone": "(11) 5055-1234",
        "cashback_mvc": 0,
        "tags": ["saude", "sus", "publico"]
    },
    {
        "name": "Colegio Moema Internacional",
        "category": "educacao",
        "description": "Escola bilingue de alto padrao com educacao infantil ao ensino medio. Metodologia moderna e infraestrutura completa.",
        "address": "R. Maracatins, 450",
        "phone": "(11) 5053-5678",
        "cashback_mvc": 5,
        "tags": ["escola", "educacao", "bilingue"]
    },
    {
        "name": "Veterinaria Pet Care Moema",
        "category": "pet",
        "description": "Clinica veterinaria completa com emergencia 24h, internacao, cirurgia e especialidades. Parceira Multiverse Coin.",
        "address": "R. Canario, 200",
        "phone": "(11) 5054-9012",
        "cashback_mvc": 8,
        "tags": ["veterinario", "pet", "emergencia"]
    },
    {
        "name": "Cartorio Moema",
        "category": "servico_publico",
        "description": "Cartorio de registro civil e notas de Moema. Servicos de autenticacao, reconhecimento de firma e registro de documentos.",
        "address": "Av. Juriti, 320",
        "phone": "(11) 5051-3456",
        "cashback_mvc": 0,
        "tags": ["cartorio", "documentos", "publico"]
    },
    {
        "name": "Auto Escola Moema",
        "category": "servicos",
        "description": "Auto escola com alta taxa de aprovacao. Aulas praticas e teoricas, simulador e flexibilidade de horarios.",
        "address": "R. Gaivota, 250",
        "phone": "(11) 5052-7890",
        "cashback_mvc": 5,
        "tags": ["autoescola", "cnh", "habilitacao"]
    }
]

# ============================================================
# DADOS DEMOGRAFICOS E ECONOMICOS
# ============================================================
MOEMA_STATS = {
    "populacao": "~100.000 moradores",
    "area": "~4 km²",
    "cnpjs_ativos": "+10.000",
    "estabelecimentos_porta_aberta": "~3.500",
    "renda_media": "Alta (Classe A/B predominante)",
    "idh": "0.957 (um dos maiores de SP)",
    "estacoes_metro": "Moema e Eucaliptos (Linha 5-Lilas)",
    "cep_range": "04077 a 04086",
    "subprefeitura": "Vila Mariana",
    "distrito": "Moema",
    "principais_vias": [
        "Avenida Moema",
        "Avenida Ibirapuera",
        "Avenida Juriti",
        "Avenida Macuco",
        "Alameda dos Arapanes",
        "Rua Canario",
        "Rua Gaivota",
        "Rua Normandia"
    ],
    "caracteristicas": [
        "Bairro nobre e residencial",
        "Forte comercio de rua",
        "Polo gastronomico",
        "Alta seguranca",
        "Pet-friendly",
        "Proximo ao Parque Ibirapuera",
        "Excelente transporte publico",
        "Comunidade ativa e engajada"
    ]
}


def search_moema_history(query: str) -> list[dict]:
    """Busca na historia de Moema por palavra-chave."""
    query_lower = query.lower()
    results = []
    for entry in MOEMA_HISTORY:
        text = f"{entry['title']} {entry['content']} {entry['year']}".lower()
        if any(word in text for word in query_lower.split()):
            results.append(entry)
    return results if results else MOEMA_HISTORY[:3]


def search_places(query: str, category: str = "") -> list[dict]:
    """Busca lugares e pontos de interesse em Moema."""
    query_lower = query.lower()
    results = []
    for place in MOEMA_PLACES:
        text = f"{place['name']} {place['description']} {place['category']} {' '.join(place['tags'])}".lower()
        if category and category.lower() in text:
            results.append(place)
        elif any(word in text for word in query_lower.split()):
            results.append(place)
    return results if results else MOEMA_PLACES[:5]


def search_restaurants(query: str, cuisine: str = "") -> list[dict]:
    """Busca restaurantes em Moema."""
    query_lower = query.lower()
    results = []
    for restaurant in MOEMA_RESTAURANTS:
        text = f"{restaurant['name']} {restaurant['cuisine']} {restaurant['description']} {' '.join(restaurant['tags'])}".lower()
        if cuisine and cuisine.lower() in text:
            results.append(restaurant)
        elif any(word in text for word in query_lower.split()):
            results.append(restaurant)
    return results if results else MOEMA_RESTAURANTS[:5]


def search_offers(query: str, category: str = "") -> list[dict]:
    """Busca ofertas e promocoes em Moema."""
    query_lower = query.lower()
    results = []
    for offer in MOEMA_OFFERS:
        text = f"{offer['business']} {offer['title']} {offer['description']} {offer['category']} {' '.join(offer['tags'])}".lower()
        if category and category.lower() in text:
            results.append(offer)
        elif any(word in text for word in query_lower.split()):
            results.append(offer)
    return results if results else MOEMA_OFFERS[:5]


def search_services(query: str) -> list[dict]:
    """Busca servicos do bairro."""
    query_lower = query.lower()
    results = []
    for service in MOEMA_SERVICES:
        text = f"{service['name']} {service['description']} {service['category']} {' '.join(service['tags'])}".lower()
        if any(word in text for word in query_lower.split()):
            results.append(service)
    return results if results else MOEMA_SERVICES[:3]


def get_nearby_offers(lat: float, lng: float, radius_km: float = 1.0) -> list[dict]:
    """Retorna ofertas proximas baseado em geolocalizacao."""
    import math
    results = []
    for offer in MOEMA_OFFERS:
        dist = math.sqrt((offer["lat"] - lat)**2 + (offer["lng"] - lng)**2) * 111  # aprox km
        if dist <= radius_km:
            offer_copy = dict(offer)
            offer_copy["distance_km"] = round(dist, 2)
            results.append(offer_copy)
    results.sort(key=lambda x: x["distance_km"])
    return results


def get_moema_stats() -> dict:
    """Retorna dados demograficos e economicos de Moema."""
    return MOEMA_STATS
