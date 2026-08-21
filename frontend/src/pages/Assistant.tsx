import React, { useState, useEffect } from 'react';
import { Bot, Send, User, Sparkles, Trash2 } from 'lucide-react';
import { DatasetMeta } from '../types';
import { sendChatQuestion, fetchChatHistory, clearChatHistory } from '../services/api';

interface Message {
  id?: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: string;
  intent?: string;
}

const DEFAULT_WELCOME_MESSAGE: Message = {
  sender: 'assistant',
  text: 'Hello! I am your AI Root-Cause Analyst. Ask me evidence-grounded questions about your dataset such as:\n• "Why did the metric decrease?"\n• "Which category performed worst?"\n• "What are the top anomalies?"\n• "What should management do next?"',
  timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
};

export const AssistantPage: React.FC<{ currentDataset: DatasetMeta | null }> = ({ currentDataset }) => {
  const [input, setInput] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [messages, setMessages] = useState<Message[]>([DEFAULT_WELCOME_MESSAGE]);

  useEffect(() => {
    if (!currentDataset?.id) {
      setMessages([DEFAULT_WELCOME_MESSAGE]);
      return;
    }

    const loadHistory = async () => {
      setIsLoadingHistory(true);
      try {
        const history = await fetchChatHistory(currentDataset.id);
        if (history && history.length > 0) {
          const formattedHistory: Message[] = history.map((m: any) => ({
            id: m.id,
            sender: m.sender as 'user' | 'assistant',
            text: m.text,
            intent: m.intent,
            timestamp: m.timestamp ? new Date(m.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }));
          setMessages(formattedHistory);
        } else {
          setMessages([DEFAULT_WELCOME_MESSAGE]);
        }
      } catch (err) {
        console.error('Failed to load chat history:', err);
        setMessages([DEFAULT_WELCOME_MESSAGE]);
      } finally {
        setIsLoadingHistory(false);
      }
    };

    loadHistory();
  }, [currentDataset?.id]);

  const handleSend = async () => {
    if (!input.trim()) return;

    if (!currentDataset?.id) {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'assistant',
          text: '⚠️ Please upload a dataset first in the Datasets tab before asking questions.',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
      return;
    }

    const userQuery = input;
    const userMsg: Message = {
      sender: 'user',
      text: userQuery,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsSending(true);

    try {
      const res = await sendChatQuestion(currentDataset.id, userQuery);
      const botMsg: Message = {
        sender: 'assistant',
        text: res.ai_explanation || res.evidence?.summary || 'Analysis complete.',
        intent: res.intent,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'assistant',
          text: `⚠️ Analysis engine notice: ${err.message || 'Unable to process question.'}`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setIsSending(false);
    }
  };

  const handleClearHistory = async () => {
    if (!currentDataset?.id) return;
    try {
      await clearChatHistory(currentDataset.id);
      setMessages([DEFAULT_WELCOME_MESSAGE]);
    } catch (err: any) {
      console.error('Failed to clear history:', err);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl flex flex-col h-[calc(100vh-12rem)]">
      {/* Header */}
      <div className="p-4 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Bot className="w-5 h-5 text-indigo-400" />
          <h2 className="text-sm font-semibold text-white">AI Evidence Assistant</h2>
          {currentDataset && (
            <span className="text-xs text-slate-500 font-mono hidden sm:inline">
              ({currentDataset.filename})
            </span>
          )}
        </div>
        <div className="flex items-center gap-3">
          {currentDataset && messages.length > 1 && (
            <button
              onClick={handleClearHistory}
              title="Clear dataset chat history"
              className="text-xs px-2.5 py-1 bg-rose-500/10 border border-rose-500/30 hover:bg-rose-500/20 text-rose-400 rounded-lg flex items-center gap-1 transition-colors"
            >
              <Trash2 className="w-3.5 h-3.5" /> Clear History
            </button>
          )}
          <span className="text-xs px-2.5 py-1 bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 rounded-full flex items-center gap-1 font-mono">
            <Sparkles className="w-3 h-3" /> Grounded Evidence Engine Active
          </span>
        </div>
      </div>

      {/* Chat Messages Log */}
      <div className="flex-1 p-4 overflow-y-auto space-y-4 text-xs">
        {isLoadingHistory ? (
          <div className="flex gap-3 justify-center items-center text-slate-500 text-xs italic font-mono py-8">
            <span className="w-4 h-4 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin"></span>
            Loading Chat History...
          </div>
        ) : (
          messages.map((m, idx) => (
            <div
              key={m.id || idx}
              className={`flex gap-3 ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {m.sender === 'assistant' && (
                <div className="w-7 h-7 rounded-full bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center text-indigo-400 flex-shrink-0">
                  <Bot className="w-4 h-4" />
                </div>
              )}
              <div
                className={`max-w-xl p-4 rounded-xl leading-relaxed whitespace-pre-wrap ${
                  m.sender === 'user'
                    ? 'bg-indigo-600 text-white rounded-br-none font-sans text-xs'
                    : 'bg-slate-950 border border-slate-850 text-slate-200 rounded-bl-none font-mono text-[11px]'
                }`}
              >
                {m.intent && (
                  <span className="inline-block mb-2 px-2 py-0.5 bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 rounded text-[9px] font-bold uppercase">
                    Intent: {m.intent}
                  </span>
                )}
                <p>{m.text}</p>
                <span className="block mt-2 text-[9px] opacity-60 text-right">{m.timestamp}</span>
              </div>
              {m.sender === 'user' && (
                <div className="w-7 h-7 rounded-full bg-slate-800 flex items-center justify-center text-slate-400 flex-shrink-0">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))
        )}
        {isSending && (
          <div className="flex gap-3 justify-start items-center text-slate-500 text-xs italic font-mono">
            <span className="w-4 h-4 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin"></span>
            Executing Question Router & Python Analytical Engine...
          </div>
        )}
      </div>

      {/* Input Form */}
      <div className="p-4 border-t border-slate-800 bg-slate-950/60 flex items-center gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder={currentDataset ? "Ask a question about metric changes, anomalies, or segments..." : "Please upload a dataset first..."}
          className="flex-1 bg-slate-900 border border-slate-800 rounded-lg px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
        />
        <button
          onClick={handleSend}
          disabled={isSending}
          className="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg transition-colors flex items-center gap-1 text-xs font-medium"
        >
          <Send className="w-3.5 h-3.5" />
          Send
        </button>
      </div>
    </div>
  );
};

