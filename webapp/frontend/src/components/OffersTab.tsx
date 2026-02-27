import { useState, useEffect } from 'react';
import { Tag, MapPin, Percent, ChevronRight } from 'lucide-react';
import { getOffers, type Offer } from '../lib/api';

const CATEGORIES = [
  { id: '', label: 'Todas', icon: Tag },
  { id: 'gastronomia', label: 'Gastronomia', icon: Tag },
  { id: 'saude', label: 'Saude', icon: Tag },
  { id: 'servicos', label: 'Servicos', icon: Tag },
  { id: 'compras', label: 'Compras', icon: Tag },
  { id: 'saudavel', label: 'Saudavel', icon: Tag },
];

export default function OffersTab() {
  const [offers, setOffers] = useState<Offer[]>([]);
  const [category, setCategory] = useState('');
  const [loading, setLoading] = useState(true);
  const [selectedOffer, setSelectedOffer] = useState<Offer | null>(null);

  useEffect(() => {
    setLoading(true);
    getOffers(category).then((data) => {
      setOffers(data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, [category]);

  return (
    <div className="flex flex-col h-full bg-gray-950">
      {/* Header */}
      <div className="bg-gradient-to-r from-amber-600 to-amber-500 p-4 shadow-lg">
        <h2 className="text-white font-bold text-lg">Ofertas em Moema</h2>
        <p className="text-amber-100 text-xs mt-0.5">Cashback em $MVC em todas as compras</p>
      </div>

      {/* Category Filter */}
      <div className="px-4 py-3 flex gap-2 overflow-x-auto no-scrollbar">
        {CATEGORIES.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setCategory(cat.id)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition ${
              category === cat.id
                ? 'bg-amber-600 text-white'
                : 'bg-gray-800 text-gray-300 border border-gray-700 hover:border-amber-500/50'
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Offers List */}
      <div className="flex-1 overflow-y-auto px-4 pb-4 space-y-3">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : (
          offers.map((offer) => (
            <div
              key={offer.id}
              onClick={() => setSelectedOffer(offer)}
              className="bg-gray-900 border border-gray-800 rounded-xl p-4 hover:border-amber-500/30 transition cursor-pointer"
            >
              <div className="flex items-start gap-3">
                <div className="w-14 h-14 bg-gray-800 rounded-xl flex items-center justify-center text-2xl flex-shrink-0">
                  {offer.image_emoji}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2">
                    <h3 className="text-white font-semibold text-sm leading-tight">{offer.title}</h3>
                    <div className="flex items-center gap-1 text-amber-400 text-xs whitespace-nowrap">
                      <MapPin className="w-3 h-3" />
                      {offer.distance_text}
                    </div>
                  </div>
                  <p className="text-gray-400 text-xs mt-0.5">{offer.business}</p>
                  <div className="flex items-center gap-3 mt-2">
                    <span className="text-gray-500 text-xs line-through">
                      R$ {offer.original_price.toFixed(2)}
                    </span>
                    <span className="text-amber-400 font-bold text-sm">
                      R$ {offer.offer_price.toFixed(2)}
                    </span>
                    <span className="bg-amber-600/20 text-amber-400 text-xs px-2 py-0.5 rounded-full flex items-center gap-1">
                      <Percent className="w-3 h-3" />
                      {offer.cashback_mvc}% MVC
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Offer Detail Modal */}
      {selectedOffer && (
        <div className="fixed inset-0 bg-black/80 z-50 flex items-end" onClick={() => setSelectedOffer(null)}>
          <div
            className="bg-gray-900 w-full rounded-t-3xl p-6 max-h-[80vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="w-10 h-1 bg-gray-700 rounded-full mx-auto mb-4" />
            <div className="text-center mb-4">
              <div className="w-20 h-20 bg-gray-800 rounded-2xl flex items-center justify-center text-4xl mx-auto mb-3">
                {selectedOffer.image_emoji}
              </div>
              <h3 className="text-white font-bold text-lg">{selectedOffer.title}</h3>
              <p className="text-amber-400 text-sm">{selectedOffer.business}</p>
            </div>
            <p className="text-gray-300 text-sm mb-4">{selectedOffer.description}</p>
            <div className="bg-gray-800 rounded-xl p-4 mb-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-400 text-sm">Preco original</span>
                <span className="text-gray-500 line-through">R$ {selectedOffer.original_price.toFixed(2)}</span>
              </div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-400 text-sm">Preco com MVC</span>
                <span className="text-amber-400 font-bold text-lg">R$ {selectedOffer.offer_price.toFixed(2)}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400 text-sm">Cashback</span>
                <span className="text-green-400 font-semibold">{selectedOffer.cashback_mvc}% em $MVC</span>
              </div>
            </div>
            <div className="flex items-center gap-2 text-gray-400 text-xs mb-4">
              <MapPin className="w-4 h-4" />
              <span>{selectedOffer.distance_text} de voce</span>
            </div>
            <div className="space-y-2">
              <button className="w-full bg-amber-600 text-white py-3 rounded-xl font-semibold hover:bg-amber-500 transition flex items-center justify-center gap-2">
                Ir ao Local <ChevronRight className="w-4 h-4" />
              </button>
              <button className="w-full bg-gray-800 text-amber-400 py-3 rounded-xl font-semibold hover:bg-gray-700 transition border border-amber-500/30">
                Pedir Entrega (+taxa)
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
