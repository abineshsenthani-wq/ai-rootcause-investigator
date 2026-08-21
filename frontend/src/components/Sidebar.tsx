import React from 'react';
import {
  LayoutDashboard,
  Database,
  AlertCircle,
  GitGraph,
  Sparkles,
  Bot,
  FileText,
  Settings
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'dataset', label: 'Datasets', icon: Database },
    { id: 'anomalies', label: 'Anomalies', icon: AlertCircle },
    { id: 'patterns', label: 'Patterns', icon: GitGraph },
    { id: 'investigation', label: 'Investigation', icon: Sparkles },
    { id: 'assistant', label: 'AI Assistant', icon: Bot },
    { id: 'reports', label: 'Reports', icon: FileText },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between flex-shrink-0 min-h-screen">
      <div>
        {/* Brand Logo */}
        <div className="p-6 flex items-center gap-3 border-b border-slate-800/80">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-cyan-400 flex items-center justify-center text-white shadow-lg shadow-indigo-500/20">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-sm font-bold text-white tracking-wide">Root-Cause</h1>
            <p className="text-[10px] text-indigo-400 font-mono tracking-wider uppercase font-semibold">
              AI Investigator
            </p>
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="p-4 space-y-1.5">
          <div className="px-3 py-2 text-[10px] font-semibold text-slate-500 font-mono uppercase tracking-wider">
            Workspace Nav
          </div>
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-xs font-medium transition-all duration-150 ${
                  isActive
                    ? 'bg-indigo-600/15 border border-indigo-500/30 text-indigo-300 font-semibold shadow-sm shadow-indigo-500/10'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border border-transparent'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-indigo-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer / System Settings */}
      <div className="p-4 border-t border-slate-800/80">
        <div className="px-3 py-2 bg-slate-950/60 border border-slate-800/60 rounded-xl flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Settings className="w-4 h-4 text-slate-400" />
            <span className="text-[11px] font-mono text-slate-400">Settings</span>
          </div>
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        </div>
      </div>
    </aside>
  );
};
