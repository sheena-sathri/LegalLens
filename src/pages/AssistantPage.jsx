import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, BookOpen, Loader2, MessageSquare, Mail, Monitor, AlertCircle } from 'lucide-react';
import { Badge } from '../components/Badge';
import { sampleChat, suggestedQueries } from '../data/mockData';
import { searchAsk } from '../services/api';

export default function AssistantPage() {
  const [messages, setMessages] = useState(() =>
    sampleChat.map((msg, i) => ({ id: i, ...msg }))
  );
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const question = input.trim();
    if (!question || loading) return;

    setError(null);
    setInput('');

    const userMsg = { id: Date.now(), role: 'user', content: question };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const result = await searchAsk(question);
      const botMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        content: result.answer,
        sources: result.sources || [],
        confidence: result.confidence,
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to get a response. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (query) => {
    setInput(query);
    inputRef.current?.focus();
  };

  const channels = [
    { name: 'Web', icon: Monitor, current: true },
    { name: 'Slack', icon: MessageSquare, current: false },
    { name: 'Email', icon: Mail, current: false },
    { name: 'Teams', icon: MessageSquare, current: false },
  ];

  return (
    <div className="flex gap-6 h-[calc(100vh-7rem)]">
      <div className="flex-1 flex flex-col bg-white rounded-lg border border-gray-200 shadow-sm">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-indigo-100 flex items-center justify-center">
              <Bot className="w-5 h-5 text-indigo-600" />
            </div>
            <div>
              <h1 className="text-xl font-semibold text-gray-900">AI Legal Assistant</h1>
              <p className="text-sm text-gray-500">Ask questions about policies, contracts, and legal matters</p>
            </div>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.map((msg) => (
            <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`flex gap-3 max-w-[80%] ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                  msg.role === 'user' ? 'bg-indigo-100' : 'bg-gray-100'
                }`}>
                  {msg.role === 'user' ? (
                    <User className="w-4 h-4 text-indigo-600" />
                  ) : (
                    <Bot className="w-4 h-4 text-gray-600" />
                  )}
                </div>
                <div className={`rounded-lg p-4 ${
                  msg.role === 'user'
                    ? 'bg-indigo-50 text-gray-900'
                    : 'bg-white border border-gray-200'
                }`}>
                  <div className="text-sm whitespace-pre-wrap">{msg.content}</div>
                  {msg.role === 'assistant' && msg.sources && msg.sources.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-gray-100">
                      <div className="flex items-center gap-1.5 text-xs text-gray-500 mb-2">
                        <BookOpen className="w-3 h-3" />
                        <span>Sources</span>
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {msg.sources.map((src, i) => (
                          <Badge key={i} color="blue">{src}</Badge>
                        ))}
                      </div>
                    </div>
                  )}
                  {msg.role === 'assistant' && msg.confidence != null && (
                    <div className="mt-2 flex items-center gap-2">
                      <div className="h-1.5 flex-1 bg-gray-100 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-emerald-500 rounded-full"
                          style={{ width: `${msg.confidence}%` }}
                        />
                      </div>
                      <span className="text-xs text-gray-500">{msg.confidence}% confidence</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="flex gap-3 max-w-[80%]">
                <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center flex-shrink-0">
                  <Bot className="w-4 h-4 text-gray-600" />
                </div>
                <div className="bg-white border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center gap-2 text-sm text-gray-500">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Thinking...</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="flex justify-center">
              <div className="flex items-center gap-2 bg-rose-50 text-rose-700 rounded-lg px-4 py-3 text-sm max-w-[80%]">
                <AlertCircle className="w-4 h-4 flex-shrink-0" />
                <span>{error}</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className="p-4 border-t border-gray-200">
          <form onSubmit={handleSubmit} className="flex gap-3">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a legal question..."
              className="flex-1 px-4 py-2.5 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="px-4 py-2.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
          <p className="mt-2 text-xs text-gray-400 text-center">
            AI responses are for guidance only. Always consult with your legal team for final decisions.
          </p>
        </div>
      </div>

      <div className="w-80 flex-shrink-0 space-y-6">
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
          <h3 className="text-sm font-semibold text-gray-900 mb-4">Available on</h3>
          <div className="space-y-3">
            {channels.map((ch) => (
              <div
                key={ch.name}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm ${
                  ch.current ? 'bg-indigo-50 text-indigo-700 font-medium' : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <ch.icon className="w-4 h-4" />
                <span>{ch.name}</span>
                {ch.current && <Badge color="indigo">Current</Badge>}
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
          <h3 className="text-sm font-semibold text-gray-900 mb-4">Suggested Queries</h3>
          <div className="space-y-2">
            {suggestedQueries.map((q, i) => (
              <button
                key={i}
                onClick={() => handleSuggestionClick(q)}
                className="w-full text-left px-3 py-2.5 rounded-lg border border-gray-200 text-sm text-gray-700 hover:bg-indigo-50 hover:border-indigo-200 hover:text-indigo-700 transition-colors"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
