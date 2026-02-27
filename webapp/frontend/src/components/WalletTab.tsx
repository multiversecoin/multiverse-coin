import { useState, useEffect } from 'react';
import { Wallet, ArrowUpRight, ArrowDownLeft, Heart, Trophy, Flame, Target, Award, Plus, Send, History } from 'lucide-react';
import { getWallet, getGamification, type WalletData, type GamificationData } from '../lib/api';

export default function WalletTab() {
  const [wallet, setWallet] = useState<WalletData | null>(null);
  const [gamification, setGamification] = useState<GamificationData | null>(null);
  const [loading, setLoading] = useState(true);
  const [showTransactions, setShowTransactions] = useState(false);

  useEffect(() => {
    Promise.all([getWallet(), getGamification()])
      .then(([w, g]) => {
        setWallet(w);
        setGamification(g);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading || !wallet || !gamification) {
    return (
      <div className="flex items-center justify-center h-full bg-gray-950">
        <div className="w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const txIcon = (type: string) => {
    switch (type) {
      case 'cashback': return <ArrowDownLeft className="w-4 h-4 text-green-400" />;
      case 'payment': return <ArrowUpRight className="w-4 h-4 text-red-400" />;
      case 'social': return <Heart className="w-4 h-4 text-pink-400" />;
      case 'reward': return <Trophy className="w-4 h-4 text-amber-400" />;
      default: return <ArrowDownLeft className="w-4 h-4 text-blue-400" />;
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-950 overflow-y-auto">
      {/* Header with Balance */}
      <div className="bg-gradient-to-br from-amber-600 via-amber-500 to-yellow-500 p-6 pb-8 relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(255,255,255,0.1),transparent)]" />
        <div className="relative">
          <p className="text-amber-100 text-xs font-medium">Seu saldo</p>
          <h2 className="text-white text-3xl font-bold mt-1">
            {wallet.balance_mvc.toLocaleString('pt-BR', { minimumFractionDigits: 2 })} <span className="text-lg font-normal">MVC</span>
          </h2>
          <p className="text-amber-100 text-sm mt-0.5">
            R$ {wallet.balance_brl.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
          </p>
          <div className="mt-1 text-xs text-amber-100 bg-white/10 inline-flex px-2 py-0.5 rounded-full">
            + {wallet.cashback_week} MVC cashback esta semana
          </div>

          {/* Quick Actions */}
          <div className="flex gap-4 mt-4">
            {[
              { icon: Plus, label: 'Adicionar' },
              { icon: Send, label: 'Enviar' },
              { icon: History, label: 'Historico' },
            ].map((action) => (
              <button
                key={action.label}
                onClick={() => action.label === 'Historico' && setShowTransactions(!showTransactions)}
                className="flex flex-col items-center gap-1"
              >
                <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm">
                  <action.icon className="w-5 h-5 text-white" />
                </div>
                <span className="text-white text-xs">{action.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="px-4 -mt-4 space-y-4 pb-4">
        {/* Social Impact Card */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-3">
            <Heart className="w-4 h-4 text-pink-400" />
            <h3 className="text-white font-semibold text-sm">Seu Impacto Social</h3>
          </div>
          <div className="grid grid-cols-3 gap-3 mb-3">
            <div className="text-center">
              <p className="text-amber-400 font-bold text-lg">R$ {wallet.social_impact.donations_brl}</p>
              <p className="text-gray-500 text-xs">Doacoes</p>
            </div>
            <div className="text-center">
              <p className="text-amber-400 font-bold text-lg">{wallet.social_impact.families_impacted}</p>
              <p className="text-gray-500 text-xs">Familias</p>
            </div>
            <div className="text-center">
              <p className="text-amber-400 font-bold text-lg">Nivel {wallet.social_impact.impact_level}</p>
              <p className="text-gray-500 text-xs">Impacto</p>
            </div>
          </div>
          {/* Adopted family */}
          <div className="bg-gray-800 rounded-lg p-3">
            <div className="flex items-center justify-between mb-2">
              <span className="text-white text-xs font-medium">{wallet.social_impact.adopted.name}</span>
              <span className="text-amber-400 text-xs">{wallet.social_impact.adopted.progress}%</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div
                className="bg-gradient-to-r from-amber-500 to-amber-400 h-2 rounded-full transition-all"
                style={{ width: `${wallet.social_impact.adopted.progress}%` }}
              />
            </div>
            <p className="text-gray-400 text-xs mt-1">Proxima meta: {wallet.social_impact.adopted.next_goal}</p>
          </div>
        </div>

        {/* Gamification */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <Trophy className="w-4 h-4 text-amber-400" />
              <h3 className="text-white font-semibold text-sm">{gamification.level_name}</h3>
            </div>
            <span className="text-gray-400 text-xs">Nivel {gamification.level}</span>
          </div>
          {/* XP Bar */}
          <div className="mb-3">
            <div className="flex justify-between text-xs text-gray-500 mb-1">
              <span>{gamification.xp} XP</span>
              <span>{gamification.xp_next_level} XP</span>
            </div>
            <div className="w-full bg-gray-800 rounded-full h-2">
              <div
                className="bg-gradient-to-r from-amber-600 to-amber-400 h-2 rounded-full"
                style={{ width: `${(gamification.xp / gamification.xp_next_level) * 100}%` }}
              />
            </div>
          </div>

          {/* Streak */}
          <div className="bg-amber-600/10 border border-amber-500/20 rounded-lg p-3 mb-3 flex items-center gap-3">
            <Flame className="w-8 h-8 text-amber-400" />
            <div>
              <p className="text-white text-sm font-semibold">{gamification.streak.days} dias de streak!</p>
              <p className="text-amber-400 text-xs">Bonus {gamification.streak.bonus_multiplier}x nos cashbacks</p>
            </div>
          </div>

          {/* Challenges */}
          <h4 className="text-gray-400 text-xs font-medium mb-2 flex items-center gap-1">
            <Target className="w-3 h-3" /> DESAFIOS ATIVOS
          </h4>
          <div className="space-y-2">
            {gamification.challenges.map((challenge, i) => (
              <div key={i} className="bg-gray-800 rounded-lg p-3">
                <div className="flex justify-between items-start mb-1">
                  <span className="text-white text-xs font-medium">{challenge.name}</span>
                  <span className="text-amber-400 text-xs">+{challenge.reward_mvc} MVC</span>
                </div>
                <p className="text-gray-500 text-xs mb-2">{challenge.description}</p>
                <div className="flex items-center gap-2">
                  <div className="flex-1 bg-gray-700 rounded-full h-1.5">
                    <div
                      className="bg-amber-500 h-1.5 rounded-full"
                      style={{ width: `${(challenge.progress / challenge.total) * 100}%` }}
                    />
                  </div>
                  <span className="text-gray-500 text-xs">{challenge.progress}/{challenge.total}</span>
                </div>
              </div>
            ))}
          </div>

          {/* Badges */}
          <h4 className="text-gray-400 text-xs font-medium mt-4 mb-2 flex items-center gap-1">
            <Award className="w-3 h-3" /> CONQUISTAS
          </h4>
          <div className="flex gap-2 flex-wrap">
            {gamification.badges.map((badge, i) => (
              <div
                key={i}
                className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-full text-xs ${
                  badge.earned
                    ? 'bg-amber-600/20 text-amber-400 border border-amber-500/30'
                    : 'bg-gray-800 text-gray-600 border border-gray-700'
                }`}
                title={badge.description}
              >
                <Wallet className="w-3 h-3" />
                {badge.name}
              </div>
            ))}
          </div>
        </div>

        {/* Transactions */}
        {showTransactions && (
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
            <h3 className="text-white font-semibold text-sm mb-3">Transacoes Recentes</h3>
            <div className="space-y-3">
              {wallet.transactions.map((tx) => (
                <div key={tx.id} className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-gray-800 rounded-full flex items-center justify-center flex-shrink-0">
                    {txIcon(tx.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-white text-xs font-medium truncate">{tx.description}</p>
                    <p className="text-gray-500 text-xs">
                      {new Date(tx.date).toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                  <span className={`text-sm font-semibold ${tx.amount >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {tx.amount >= 0 ? '+' : ''}{tx.amount.toFixed(2)} {tx.mvc ? 'MVC' : 'BRL'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
