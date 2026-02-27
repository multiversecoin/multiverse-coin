import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, MapPin, Sparkles } from 'lucide-react';
import { sendMessage, type ChatMessage } from '../lib/api';

interface MiaChatProps {
  userLat?: number;
  userLng?: number;
}

export default function MiaChat({ userLat, userLng }: MiaChatProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Welcome message
  useEffect(() => {
    setMessages([
      {
        role: 'assistant',
        content: 'Ola! Sou a MIA, sua concierge digital de Moema! Posso te ajudar com ofertas, restaurantes, historia do bairro, servicos e muito mais. O que voce precisa hoje?',
      },
    ]);
  }, []);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: ChatMessage = { role: 'user', content: input.trim() };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const response = await sendMessage(newMessages, userLat, userLng);
      setMessages([...newMessages, { role: 'assistant', content: response }]);
    } catch {
      setMessages([
        ...newMessages,
        { role: 'assistant', content: 'Ops, tive um probleminha. Tenta de novo?' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    { label: 'Ofertas perto', icon: MapPin, query: 'Quais ofertas estao perto de mim?' },
    { label: 'Restaurantes', icon: Sparkles, query: 'Me recomende restaurantes em Moema' },
    { label: 'Historia', icon: Bot, query: 'Conta a historia de Moema' },
  ];

  return (
    <div className="flex flex-col h-full bg-gray-950">
      {/* Header */}
      <div className="bg-gradient-to-r from-amber-600 to-amber-500 p-4 flex items-center gap-3 shadow-lg">
        <div className="w-10 h-10 rounded-full bg-gray-900 flex items-center justify-center">
          <Bot className="w-6 h-6 text-amber-400" />
        </div>
        <div>
          <h2 className="text-white font-bold text-lg">MIA</h2>
          <p className="text-amber-100 text-xs">Multiverse Intelligent Assistant</p>
        </div>
        {userLat && (
          <div className="ml-auto flex items-center gap-1 text-amber-100 text-xs">
            <MapPin className="w-3 h-3" />
            <span>Moema</span>
          </div>
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex gap-2 max-w-[85%] ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
              <div className={`w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center ${
                msg.role === 'user' ? 'bg-amber-600' : 'bg-gray-800 border border-amber-500/30'
              }`}>
                {msg.role === 'user' ? (
                  <User className="w-4 h-4 text-white" />
                ) : (
                  <Bot className="w-4 h-4 text-amber-400" />
                )}
              </div>
              <div className={`rounded-2xl px-4 py-3 ${
                msg.role === 'user'
                  ? 'bg-amber-600 text-white rounded-br-md'
                  : 'bg-gray-800 text-gray-100 border border-gray-700 rounded-bl-md'
              }`}>
                <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.content}</p>
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="flex gap-2 max-w-[85%]">
              <div className="w-8 h-8 rounded-full bg-gray-800 border border-amber-500/30 flex items-center justify-center">
                <Bot className="w-4 h-4 text-amber-400" />
              </div>
              <div className="bg-gray-800 border border-gray-700 rounded-2xl rounded-bl-md px-4 py-3">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-amber-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 bg-amber-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 bg-amber-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Actions */}
      {messages.length <= 1 && (
        <div className="px-4 pb-2 flex gap-2 overflow-x-auto">
          {quickActions.map((action) => (
            <button
              key={action.label}
              onClick={() => {
                setInput(action.query);
                setTimeout(() => inputRef.current?.focus(), 100);
              }}
              className="flex items-center gap-1.5 px-3 py-2 bg-gray-800 border border-amber-500/30 rounded-full text-xs text-amber-300 hover:bg-gray-700 transition whitespace-nowrap"
            >
              <action.icon className="w-3 h-3" />
              {action.label}
            </button>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="p-3 bg-gray-900 border-t border-gray-800">
        <div className="flex items-center gap-2">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Pergunte algo sobre Moema..."
            className="flex-1 bg-gray-800 text-white rounded-full px-4 py-3 text-sm border border-gray-700 focus:border-amber-500 focus:outline-none placeholder-gray-500"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || loading}
            className="w-10 h-10 rounded-full bg-amber-600 flex items-center justify-center hover:bg-amber-500 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-5 h-5 text-white" />
          </button>
        </div>
      </div>
    </div>
  );
}
