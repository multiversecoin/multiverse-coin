const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface Offer {
  id: string;
  business: string;
  title: string;
  description: string;
  original_price: number;
  offer_price: number;
  cashback_mvc: number;
  category: string;
  image_emoji: string;
  valid_until: string;
  lat: number;
  lng: number;
  distance_text: string;
  tags: string[];
}

export interface Restaurant {
  name: string;
  cuisine: string;
  description: string;
  address: string;
  lat: number;
  lng: number;
  rating: number;
  price_range: string;
  cashback_mvc: number;
  phone: string;
  hours: string;
  tags: string[];
}

export interface Place {
  name: string;
  category: string;
  description: string;
  address: string;
  lat: number;
  lng: number;
  rating: number;
  cashback_mvc: number;
  tags: string[];
}

export interface HistoryEntry {
  year: string;
  title: string;
  content: string;
}

export interface WalletData {
  balance_mvc: number;
  balance_brl: number;
  cashback_week: number;
  level: string;
  social_impact: {
    donations_brl: number;
    families_impacted: number;
    impact_level: number;
    adopted: {
      name: string;
      type: string;
      progress: number;
      next_goal: string;
    };
  };
  transactions: {
    id: string;
    type: string;
    amount: number;
    description: string;
    date: string;
    mvc: boolean;
  }[];
}

export interface GamificationData {
  level: number;
  level_name: string;
  xp: number;
  xp_next_level: number;
  badges: { name: string; icon: string; description: string; earned: boolean }[];
  challenges: { name: string; description: string; progress: number; total: number; reward_mvc: number }[];
  streak: { days: number; description: string; bonus_multiplier: number };
}

export async function sendMessage(messages: ChatMessage[], userLat?: number, userLng?: number): Promise<string> {
  const res = await fetch(`${API_URL}/api/mia/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      messages,
      user_lat: userLat,
      user_lng: userLng,
    }),
  });
  const data = await res.json();
  return data.response;
}

export async function getOffers(category?: string): Promise<Offer[]> {
  const params = category ? `?category=${category}` : '';
  const res = await fetch(`${API_URL}/api/offers${params}`);
  return res.json();
}

export async function getRestaurants(): Promise<Restaurant[]> {
  const res = await fetch(`${API_URL}/api/restaurants`);
  return res.json();
}

export async function getPlaces(): Promise<Place[]> {
  const res = await fetch(`${API_URL}/api/places`);
  return res.json();
}

export async function getHistory(): Promise<HistoryEntry[]> {
  const res = await fetch(`${API_URL}/api/history`);
  return res.json();
}

export async function getWallet(): Promise<WalletData> {
  const res = await fetch(`${API_URL}/api/wallet`);
  return res.json();
}

export async function getGamification(): Promise<GamificationData> {
  const res = await fetch(`${API_URL}/api/gamification`);
  return res.json();
}

export async function getStats(): Promise<Record<string, unknown>> {
  const res = await fetch(`${API_URL}/api/stats`);
  return res.json();
}
