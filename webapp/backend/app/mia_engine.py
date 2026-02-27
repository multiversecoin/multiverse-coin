"""
MIA - Multiverse Intelligent Assistant
Motor de IA da MIA com prompt leve e tools sob demanda.
"""
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from app.moema_data import (
    search_moema_history,
    search_places,
    search_restaurants,
    search_offers,
    search_services,
    get_nearby_offers,
    get_moema_stats,
)

load_dotenv()

# ============================================================
# SYSTEM PROMPT LEVE (~15 linhas)
# ============================================================
MIA_SYSTEM_PROMPT = """Voce e a MIA (Multiverse Intelligent Assistant), a concierge digital do bairro de Moema, Sao Paulo.
Voce faz parte do ecossistema Multiverse Coin ($MVC), uma economia digital hiperlocal.

Personalidade: Calorosa, esperta, prestativa e orgulhosa de Moema. Fala de forma natural, como uma vizinha que conhece tudo do bairro.
Tom: Amigavel e informal, mas profissional. Use portugues brasileiro natural.

Regras:
- Sempre busque informacoes usando as tools disponiveis antes de responder sobre Moema.
- Quando recomendar comercios, mencione o cashback em MVC disponivel.
- Se o usuario estiver perto de uma oferta, avise proativamente.
- Para entregas, mencione que pode ir buscar no local (gratis) ou pagar taxa de entrega para receber em casa.
- Incentive o uso de $MVC e explique os beneficios do ecossistema.
- Seja concisa mas completa. Use emojis com moderacao.
- Quando falar de impacto social, mencione o programa de adocao virtual e o fundo social automatico.
- Adapte a linguagem conforme o perfil do usuario (jovem, idoso, familia, etc).
- Nunca invente informacoes. Use apenas dados das tools."""

# ============================================================
# TOOLS DEFINITIONS (OpenAI Function Calling)
# ============================================================
MIA_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "searchMoemaHistory",
            "description": "Busca informacoes sobre a historia do bairro de Moema. Use quando o usuario perguntar sobre historia, origens, evolucao ou fatos historicos do bairro.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Termo de busca sobre a historia de Moema (ex: 'origem do nome', 'parque ibirapuera', 'metro')"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "searchPlaces",
            "description": "Busca lugares e pontos de interesse em Moema como parques, pracas, museus, shoppings, estacoes de metro. Use quando o usuario perguntar sobre o que fazer, visitar ou conhecer no bairro.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "O que o usuario esta procurando (ex: 'parque', 'museu', 'shopping')"
                    },
                    "category": {
                        "type": "string",
                        "description": "Categoria opcional: parque, shopping, cultura, transporte, praca, feira, polo_gastronomico"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "searchRestaurants",
            "description": "Busca restaurantes, cafes, bares e opcoes gastronomicas em Moema. Use quando o usuario quiser comer, beber ou pedir recomendacao de lugar para refeicao.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "O que o usuario quer comer ou tipo de restaurante (ex: 'pizza', 'japones', 'cafe', 'hamburgueria')"
                    },
                    "cuisine": {
                        "type": "string",
                        "description": "Tipo de culinaria opcional: japonesa, italiana, brasileira, arabe, tailandesa, cafeteria, hamburgueria, chocolateria"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "searchOffers",
            "description": "Busca ofertas, promocoes e descontos disponiveis nos comercios parceiros de Moema. Todas as ofertas dao cashback em $MVC. Use quando o usuario perguntar sobre promocoes, descontos ou quiser economizar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Tipo de oferta ou produto procurado (ex: 'comida', 'servico', 'farmacia', 'pet')"
                    },
                    "category": {
                        "type": "string",
                        "description": "Categoria opcional: gastronomia, saude, servicos, compras, saudavel"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "searchServices",
            "description": "Busca servicos do bairro como hospitais, escolas, veterinarios, cartorios, auto escolas. Use quando o usuario precisar de um servico especifico no bairro.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Tipo de servico procurado (ex: 'hospital', 'veterinario', 'escola')"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "getNearbyOffers",
            "description": "Busca ofertas proximas baseado na localizacao do usuario. Use quando tiver a localizacao do usuario para sugerir ofertas pertinentes nas proximidades.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {
                        "type": "number",
                        "description": "Latitude do usuario"
                    },
                    "lng": {
                        "type": "number",
                        "description": "Longitude do usuario"
                    },
                    "radius_km": {
                        "type": "number",
                        "description": "Raio de busca em km (padrao: 1.0)"
                    }
                },
                "required": ["lat", "lng"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "getMoemaStats",
            "description": "Retorna dados demograficos e economicos de Moema como populacao, area, numero de comercios, IDH, etc. Use quando o usuario perguntar sobre dados do bairro.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


def execute_tool(tool_name: str, arguments: dict) -> str:
    """Executa uma tool e retorna o resultado como string JSON."""
    if tool_name == "searchMoemaHistory":
        result = search_moema_history(arguments.get("query", ""))
    elif tool_name == "searchPlaces":
        result = search_places(arguments.get("query", ""), arguments.get("category", ""))
    elif tool_name == "searchRestaurants":
        result = search_restaurants(arguments.get("query", ""), arguments.get("cuisine", ""))
    elif tool_name == "searchOffers":
        result = search_offers(arguments.get("query", ""), arguments.get("category", ""))
    elif tool_name == "searchServices":
        result = search_services(arguments.get("query", ""))
    elif tool_name == "getNearbyOffers":
        result = get_nearby_offers(
            arguments.get("lat", -23.5988),
            arguments.get("lng", -46.6635),
            arguments.get("radius_km", 1.0)
        )
    elif tool_name == "getMoemaStats":
        result = get_moema_stats()
    else:
        result = {"error": f"Tool {tool_name} nao encontrada"}
    return json.dumps(result, ensure_ascii=False, default=str)


def chat_with_mia(
    messages: list[dict],
    user_lat: float | None = None,
    user_lng: float | None = None,
) -> str:
    """
    Processa uma conversa com a MIA usando OpenAI com function calling.
    Mantem o prompt leve e busca dados sob demanda via tools.
    """
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return "Ola! Sou a MIA, sua assistente do bairro de Moema! No momento estou em manutencao, mas logo estarei de volta para ajudar voce a explorar tudo que Moema tem de melhor. 🏘️"

    client = OpenAI(api_key=api_key)

    # Build system message with optional location context
    system_msg = MIA_SYSTEM_PROMPT
    if user_lat is not None and user_lng is not None:
        system_msg += f"\n\nLocalizacao atual do usuario: lat={user_lat}, lng={user_lng}. Use getNearbyOffers para sugerir ofertas proximas quando relevante."

    # Prepare messages for API
    api_messages = [{"role": "system", "content": system_msg}]
    for msg in messages:
        api_messages.append({
            "role": msg.get("role", "user"),
            "content": msg.get("content", "")
        })

    try:
        # First call - may trigger tool use
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=api_messages,
            tools=MIA_TOOLS,
            tool_choice="auto",
            temperature=0.7,
            max_tokens=1000,
        )

        assistant_message = response.choices[0].message

        # If the model wants to call tools
        if assistant_message.tool_calls:
            # Add assistant message with tool calls
            api_messages.append({
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in assistant_message.tool_calls
                ]
            })

            # Execute each tool and add results
            for tool_call in assistant_message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)
                result = execute_tool(func_name, func_args)

                api_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })

            # Second call - generate final response with tool results
            response2 = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=api_messages,
                temperature=0.7,
                max_tokens=1000,
            )

            return response2.choices[0].message.content or "Desculpe, nao consegui processar sua mensagem."

        return assistant_message.content or "Desculpe, nao consegui processar sua mensagem."

    except Exception as e:
        print(f"MIA Error: {e}")
        return "Ops, tive um probleminha tecnico! Pode tentar novamente em alguns segundos? 😅"
