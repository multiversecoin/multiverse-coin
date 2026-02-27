import { useState, useEffect } from 'react';
import { Clock, MapPin, Star, ChevronDown, ChevronUp, Landmark, UtensilsCrossed, Building2, Info } from 'lucide-react';
import { getHistory, getPlaces, getRestaurants, type HistoryEntry, type Place, type Restaurant } from '../lib/api';

type SubTab = 'history' | 'places' | 'restaurants';

export default function ExploreTab() {
  const [subTab, setSubTab] = useState<SubTab>('history');
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [places, setPlaces] = useState<Place[]>([]);
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedHistory, setExpandedHistory] = useState<number | null>(null);

  useEffect(() => {
    setLoading(true);
    if (subTab === 'history') {
      getHistory().then(setHistory).finally(() => setLoading(false));
    } else if (subTab === 'places') {
      getPlaces().then(setPlaces).finally(() => setLoading(false));
    } else {
      getRestaurants().then(setRestaurants).finally(() => setLoading(false));
    }
  }, [subTab]);

  const tabs = [
    { id: 'history' as SubTab, label: 'Historia', icon: Clock },
    { id: 'places' as SubTab, label: 'Lugares', icon: Landmark },
    { id: 'restaurants' as SubTab, label: 'Gastronomia', icon: UtensilsCrossed },
  ];

  return (
    <div className="flex flex-col h-full bg-gray-950">
      {/* Header */}
      <div className="bg-gradient-to-r from-amber-600 to-amber-500 p-4 shadow-lg">
        <h2 className="text-white font-bold text-lg">Explorar Moema</h2>
        <p className="text-amber-100 text-xs mt-0.5">Descubra tudo sobre o bairro</p>
      </div>

      {/* Sub Tabs */}
      <div className="flex border-b border-gray-800">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setSubTab(tab.id)}
            className={`flex-1 flex items-center justify-center gap-1.5 py-3 text-xs font-medium transition ${
              subTab === tab.id
                ? 'text-amber-400 border-b-2 border-amber-400'
                : 'text-gray-500 hover:text-gray-300'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : subTab === 'history' ? (
          <div className="space-y-0">
            <div className="text-center mb-6">
              <h3 className="text-amber-400 font-bold text-lg">Linha do Tempo de Moema</h3>
              <p className="text-gray-500 text-xs">Dos povos indigenas ate a era digital</p>
            </div>
            {history.map((entry, i) => (
              <div key={i} className="flex gap-3">
                {/* Timeline line */}
                <div className="flex flex-col items-center">
                  <div className={`w-3 h-3 rounded-full flex-shrink-0 ${
                    i === history.length - 1 ? 'bg-amber-400 ring-4 ring-amber-400/20' : 'bg-gray-600'
                  }`} />
                  {i < history.length - 1 && <div className="w-0.5 flex-1 bg-gray-800" />}
                </div>
                {/* Content */}
                <div className="pb-6 flex-1">
                  <button
                    onClick={() => setExpandedHistory(expandedHistory === i ? null : i)}
                    className="w-full text-left"
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-amber-400 font-mono text-xs font-bold">{entry.year}</span>
                      <span className="text-white font-semibold text-sm">{entry.title}</span>
                      {expandedHistory === i ? (
                        <ChevronUp className="w-4 h-4 text-gray-500 ml-auto flex-shrink-0" />
                      ) : (
                        <ChevronDown className="w-4 h-4 text-gray-500 ml-auto flex-shrink-0" />
                      )}
                    </div>
                  </button>
                  {expandedHistory === i && (
                    <p className="text-gray-400 text-xs mt-2 leading-relaxed bg-gray-900 rounded-lg p-3 border border-gray-800">
                      {entry.content}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : subTab === 'places' ? (
          <div className="space-y-3">
            {places.map((place, i) => (
              <div key={i} className="bg-gray-900 border border-gray-800 rounded-xl p-4 hover:border-amber-500/30 transition">
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 bg-amber-600/20 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Building2 className="w-5 h-5 text-amber-400" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h3 className="text-white font-semibold text-sm">{place.name}</h3>
                      {place.rating > 0 && (
                        <div className="flex items-center gap-0.5">
                          <Star className="w-3 h-3 text-amber-400 fill-amber-400" />
                          <span className="text-amber-400 text-xs">{place.rating}</span>
                        </div>
                      )}
                    </div>
                    <span className="text-amber-500/70 text-xs capitalize">{place.category.replace('_', ' ')}</span>
                    <p className="text-gray-400 text-xs mt-1 leading-relaxed">{place.description}</p>
                    <div className="flex items-center gap-1 mt-2 text-gray-500 text-xs">
                      <MapPin className="w-3 h-3" />
                      {place.address}
                    </div>
                    {place.cashback_mvc > 0 && (
                      <div className="mt-2 inline-flex items-center gap-1 bg-amber-600/20 text-amber-400 text-xs px-2 py-0.5 rounded-full">
                        {place.cashback_mvc}% cashback MVC
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="space-y-3">
            {restaurants.map((restaurant, i) => (
              <div key={i} className="bg-gray-900 border border-gray-800 rounded-xl p-4 hover:border-amber-500/30 transition">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <h3 className="text-white font-semibold text-sm">{restaurant.name}</h3>
                    <span className="text-amber-500/70 text-xs">{restaurant.cuisine}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Star className="w-3 h-3 text-amber-400 fill-amber-400" />
                    <span className="text-amber-400 text-xs font-medium">{restaurant.rating}</span>
                  </div>
                </div>
                <p className="text-gray-400 text-xs leading-relaxed">{restaurant.description}</p>
                <div className="flex items-center gap-4 mt-3">
                  <div className="flex items-center gap-1 text-gray-500 text-xs">
                    <MapPin className="w-3 h-3" />
                    {restaurant.address}
                  </div>
                  <span className="text-gray-600 text-xs">{restaurant.price_range}</span>
                </div>
                <div className="flex items-center gap-2 mt-2">
                  <span className="bg-amber-600/20 text-amber-400 text-xs px-2 py-0.5 rounded-full">
                    {restaurant.cashback_mvc}% cashback MVC
                  </span>
                  <span className="text-gray-500 text-xs flex items-center gap-1">
                    <Info className="w-3 h-3" />
                    {restaurant.hours}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
