from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.mia_engine import chat_with_mia
from app.moema_data import (
    MOEMA_OFFERS,
    MOEMA_RESTAURANTS,
    MOEMA_PLACES,
    MOEMA_HISTORY,
    MOEMA_SERVICES,
    MOEMA_STATS,
    search_offers,
    search_restaurants,
    search_places,
    get_nearby_offers,
)

app = FastAPI(title="Multiverse Coin API", version="1.0.0")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# ============================================================
# Models
# ============================================================
class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    user_lat: float | None = None
    user_lng: float | None = None


class ChatResponse(BaseModel):
    response: str


# ============================================================
# MIA Chat Endpoint
# ============================================================
@app.post("/api/mia/chat", response_model=ChatResponse)
def mia_chat(request: ChatRequest):
    """Endpoint principal do chat com a MIA."""
    messages = [{"role": m.role, "content": m.content} for m in request.messages]
    response = chat_with_mia(
        messages=messages,
        user_lat=request.user_lat,
        user_lng=request.user_lng,
    )
    return ChatResponse(response=response)


# ============================================================
# Offers Endpoints
# ============================================================
@app.get("/api/offers")
async def get_offers(category: str = "", query: str = ""):
    """Lista todas as ofertas ou filtra por categoria/query."""
    if category or query:
        return search_offers(query or category, category)
    return MOEMA_OFFERS


@app.get("/api/offers/nearby")
async def get_offers_nearby(lat: float = -23.5988, lng: float = -46.6635, radius: float = 1.0):
    """Ofertas proximas baseadas em geolocalizacao."""
    return get_nearby_offers(lat, lng, radius)


# ============================================================
# Restaurants Endpoints
# ============================================================
@app.get("/api/restaurants")
async def get_restaurants(cuisine: str = "", query: str = ""):
    """Lista restaurantes ou filtra por culinaria/query."""
    if cuisine or query:
        return search_restaurants(query or cuisine, cuisine)
    return MOEMA_RESTAURANTS


# ============================================================
# Places Endpoints
# ============================================================
@app.get("/api/places")
async def get_places(category: str = "", query: str = ""):
    """Lista lugares e pontos de interesse."""
    if category or query:
        return search_places(query or category, category)
    return MOEMA_PLACES


# ============================================================
# History Endpoints
# ============================================================
@app.get("/api/history")
async def get_history():
    """Retorna a linha do tempo historica de Moema."""
    return MOEMA_HISTORY


# ============================================================
# Services Endpoints
# ============================================================
@app.get("/api/services")
async def get_services():
    """Lista servicos do bairro."""
    return MOEMA_SERVICES


# ============================================================
# Stats Endpoint
# ============================================================
@app.get("/api/stats")
async def get_stats():
    """Dados demograficos e economicos de Moema."""
    return MOEMA_STATS


# ============================================================
# Wallet Mock Endpoints
# ============================================================
@app.get("/api/wallet")
async def get_wallet():
    """Retorna dados mock da carteira do usuario."""
    return {
        "balance_mvc": 2458.75,
        "balance_brl": 24587.50,
        "cashback_week": 125.50,
        "level": "Explorador",
        "social_impact": {
            "donations_brl": 342.18,
            "families_impacted": 5,
            "impact_level": 3,
            "adopted": {
                "name": "Familia Santos",
                "type": "familia",
                "progress": 72,
                "next_goal": "Material escolar para 2 criancas"
            }
        },
        "transactions": [
            {"id": "tx1", "type": "cashback", "amount": 12.50, "description": "Cashback - Cafe Moema", "date": "2025-06-15T10:30:00", "mvc": True},
            {"id": "tx2", "type": "payment", "amount": -85.00, "description": "Forneria San Paolo", "date": "2025-06-14T20:15:00", "mvc": True},
            {"id": "tx3", "type": "cashback", "amount": 8.50, "description": "Cashback - Farmacia", "date": "2025-06-14T15:00:00", "mvc": True},
            {"id": "tx4", "type": "social", "amount": -2.50, "description": "Fundo Social Automatico", "date": "2025-06-14T20:15:01", "mvc": True},
            {"id": "tx5", "type": "received", "amount": 500.00, "description": "Deposito via PIX", "date": "2025-06-13T09:00:00", "mvc": False},
            {"id": "tx6", "type": "cashback", "amount": 25.00, "description": "Cashback - Shopping Ibirapuera", "date": "2025-06-12T16:45:00", "mvc": True},
            {"id": "tx7", "type": "payment", "amount": -32.00, "description": "Acai da Terra Moema", "date": "2025-06-12T12:30:00", "mvc": True},
            {"id": "tx8", "type": "reward", "amount": 50.00, "description": "Desafio Semanal Completo!", "date": "2025-06-11T23:59:00", "mvc": True},
        ]
    }


# ============================================================
# Gamification Endpoints
# ============================================================
@app.get("/api/gamification")
async def get_gamification():
    """Dados de gamificacao do usuario."""
    return {
        "level": 7,
        "level_name": "Explorador de Moema",
        "xp": 2340,
        "xp_next_level": 3000,
        "badges": [
            {"name": "Primeiro Cafe", "icon": "coffee", "description": "Fez a primeira compra em uma cafeteria", "earned": True},
            {"name": "Vizinho Solidario", "icon": "heart", "description": "Contribuiu para o fundo social", "earned": True},
            {"name": "Explorador", "icon": "map", "description": "Visitou 10 comercios parceiros", "earned": True},
            {"name": "Gastronauta", "icon": "utensils", "description": "Experimentou 5 restaurantes diferentes", "earned": True},
            {"name": "Moema Lover", "icon": "star", "description": "100 transacoes no bairro", "earned": False},
        ],
        "challenges": [
            {"name": "Cafe da Semana", "description": "Visite 3 cafeterias diferentes esta semana", "progress": 2, "total": 3, "reward_mvc": 30},
            {"name": "Impacto Social", "description": "Contribua R$10 para o fundo social", "progress": 7, "total": 10, "reward_mvc": 50},
            {"name": "Desbravador", "description": "Visite um comercio que nunca visitou", "progress": 0, "total": 1, "reward_mvc": 20},
        ],
        "streak": {
            "days": 12,
            "description": "12 dias consecutivos usando MVC!",
            "bonus_multiplier": 1.5
        }
    }


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
