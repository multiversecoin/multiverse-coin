import { useState, useEffect } from 'react';
import { MessageCircle, Gift, Compass, Wallet, Bell } from 'lucide-react';
import MiaChat from './components/MiaChat';
import OffersTab from './components/OffersTab';
import ExploreTab from './components/ExploreTab';
import WalletTab from './components/WalletTab';

type Tab = 'mia' | 'offers' | 'explore' | 'wallet';

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('mia');
  const [userLat, setUserLat] = useState<number | undefined>();
  const [userLng, setUserLng] = useState<number | undefined>();
  const [notification, setNotification] = useState<string | null>(null);

  // Get user geolocation
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setUserLat(pos.coords.latitude);
          setUserLng(pos.coords.longitude);
        },
        () => {
          // Default to center of Moema if denied
          setUserLat(-23.5988);
          setUserLng(-46.6635);
        }
      );
    } else {
      setUserLat(-23.5988);
      setUserLng(-46.6635);
    }
  }, []);

  // Simulate geolocation notification
  useEffect(() => {
    const timer = setTimeout(() => {
      setNotification('Voce esta perto da Loja de Chocolates Moema! Trufas com 12% cashback MVC');
      setTimeout(() => setNotification(null), 6000);
    }, 8000);
    return () => clearTimeout(timer);
  }, []);

  const tabs = [
    { id: 'mia' as Tab, label: 'MIA', icon: MessageCircle },
    { id: 'offers' as Tab, label: 'Ofertas', icon: Gift },
    { id: 'explore' as Tab, label: 'Explorar', icon: Compass },
    { id: 'wallet' as Tab, label: 'Carteira', icon: Wallet },
  ];

  return (
    <div className="h-full flex flex-col bg-gray-950 max-w-md mx-auto relative">
      {/* Geolocation Notification Banner */}
      {notification && (
        <div className="absolute top-0 left-0 right-0 z-50 animate-slide-down">
          <div className="mx-3 mt-3 bg-gradient-to-r from-amber-600 to-amber-500 rounded-xl p-3 shadow-2xl shadow-amber-500/20 flex items-start gap-3">
            <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center flex-shrink-0">
              <Bell className="w-4 h-4 text-white" />
            </div>
            <div className="flex-1">
              <p className="text-white text-xs font-semibold">MIA - Oferta Proxima!</p>
              <p className="text-amber-100 text-xs mt-0.5">{notification}</p>
            </div>
            <button
              onClick={() => setNotification(null)}
              className="text-white/70 hover:text-white text-xs"
            >
              X
            </button>
          </div>
        </div>
      )}

      {/* Content Area */}
      <div className="flex-1 overflow-hidden">
        {activeTab === 'mia' && <MiaChat userLat={userLat} userLng={userLng} />}
        {activeTab === 'offers' && <OffersTab />}
        {activeTab === 'explore' && <ExploreTab />}
        {activeTab === 'wallet' && <WalletTab />}
      </div>

      {/* Bottom Navigation */}
      <div className="bg-gray-900 border-t border-gray-800 px-2 pb-safe">
        <div className="flex justify-around">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex flex-col items-center py-2 px-4 transition-all ${
                activeTab === tab.id ? 'text-amber-400' : 'text-gray-500 hover:text-gray-300'
              }`}
            >
              <div className={`relative ${activeTab === tab.id ? 'scale-110' : ''} transition-transform`}>
                <tab.icon className="w-5 h-5" />
                {tab.id === 'mia' && activeTab !== 'mia' && (
                  <div className="absolute -top-1 -right-1 w-2 h-2 bg-amber-400 rounded-full" />
                )}
              </div>
              <span className="text-xs mt-1 font-medium">{tab.label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
