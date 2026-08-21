import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Database, 
  AlertTriangle, 
  GitCommit, 
  Search, 
  Bot, 
  FileText, 
  ShieldCheck, 
  Menu, 
  X 
} from 'lucide-react';
import { NavigationTab, DatasetMeta, SystemHealth } from './types';
import { fetchHealth, fetchDatasets } from './services/api';
import { DashboardPage } from './pages/Dashboard';
import { DatasetPage } from './pages/Dataset';
import { AnomaliesPage } from './pages/Anomalies';
import { PatternsPage } from './pages/Patterns';
import { InvestigationPage } from './pages/Investigation';
import { AssistantPage } from './pages/Assistant';
import { ReportsPage } from './pages/Reports';

export default function App() {
  const [activeTab, setActiveTab] = useState<NavigationTab>('dashboard');
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [currentDataset, setCurrentDataset] = useState<DatasetMeta | null>(null);
  const [datasetsList, setDatasetsList] = useState<DatasetMeta[]>([]);

  const loadDatasets = () => {
    fetchDatasets()
      .then((datasets) => {
        if (datasets && datasets.length > 0) {
          setDatasetsList(datasets);
          setCurrentDataset((prev) => {
            if (!prev) return datasets[0];
            const exists = datasets.find((d) => d.id === prev.id);
            return exists || datasets[0];
          });
        }
      })
      .catch(console.error);
  };

  useEffect(() => {
    fetchHealth()
      .then(setHealth)
      .catch(() => setHealth(null));

    loadDatasets();
  }, []);

  const handleDatasetUploaded = (newMeta: DatasetMeta) => {
    setCurrentDataset(newMeta);
    loadDatasets();
  };


  const navItems = [
    { id: 'dashboard' as NavigationTab, label: 'Dashboard', icon: Activity },
    { id: 'datasets' as NavigationTab, label: 'Datasets', icon: Database },
    { id: 'anomalies' as NavigationTab, label: 'Anomaly Detection', icon: AlertTriangle },
    { id: 'patterns' as NavigationTab, label: 'Patterns & Correlations', icon: GitCommit },
    { id: 'investigation' as NavigationTab, label: 'Root-Cause Investigation', icon: Search },
    { id: 'assistant' as NavigationTab, label: 'AI Assistant', icon: Bot },
    { id: 'reports' as NavigationTab, label: 'Reports', icon: FileText },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex overflow-hidden">
      {/* Sidebar Navigation */}
      <aside
        className={`${
          sidebarOpen ? 'w-64' : 'w-20'
        } bg-slate-900 border-r border-slate-800 transition-all duration-300 flex flex-col z-20`}
      >
        {/* Brand Header */}
        <div className="h-16 flex items-center justify-between px-4 border-b border-slate-800">
          <div className="flex items-center gap-3 overflow-hidden">
            <div className="w-9 h-9 rounded-lg bg-indigo-600/20 border border-indigo-500/40 flex items-center justify-center text-indigo-400 flex-shrink-0">
              <Activity className="w-5 h-5 animate-pulse" />
            </div>
            {sidebarOpen && (
              <div className="leading-none">
                <h1 className="font-bold text-xs tracking-tight bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent truncate">
                  AI INVESTIGATOR
                </h1>
                <span className="text-[10px] text-slate-500 font-mono mt-0.5 block">v1.0 • Grounded ML</span>
              </div>
            )}
          </div>
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-slate-400 hover:text-white p-1 rounded-md hover:bg-slate-800 transition-colors"
          >
            {sidebarOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
          </button>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-indigo-600/15 text-indigo-400 border border-indigo-500/30 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-850'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-indigo-400' : 'text-slate-500'}`} />
                {sidebarOpen && <span className="truncate">{item.label}</span>}
              </button>
            );
          })}
        </nav>

        {/* Footer System Status */}
        {sidebarOpen && (
          <div className="p-4 border-t border-slate-800 bg-slate-950/40 text-[11px] text-slate-500 space-y-1 font-mono">
            <div className="flex justify-between items-center">
              <span>Engine Status</span>
              <span className="flex items-center gap-1 text-emerald-400 font-semibold">
                <ShieldCheck className="w-3 h-3" />
                {health?.status === 'healthy' ? 'Healthy' : 'Online'}
              </span>
            </div>
            <div className="flex justify-between items-center text-[10px] text-slate-600">
              <span>Provider</span>
              <span>{health?.details?.llm_provider || 'Fallback'}</span>
            </div>
          </div>
        )}
      </aside>

      {/* Main Workspace Layout */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top Navbar */}
        <header className="h-16 bg-slate-900/80 backdrop-blur border-b border-slate-800 px-6 flex items-center justify-between z-10">
          <div>
            <span className="text-xs text-slate-400">Section /</span>
            <h2 className="text-sm font-bold text-white uppercase tracking-wider capitalize">
              {activeTab.replace('_', ' ')}
            </h2>
          </div>

          <div className="flex items-center gap-4 text-xs">
            {datasetsList.length > 0 && (
              <div className="hidden sm:flex items-center gap-2 bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
                <Database className="w-3.5 h-3.5 text-indigo-400" />
                <span className="text-slate-400 hidden md:inline">Dataset:</span>
                <select
                  value={currentDataset?.id || ''}
                  onChange={(e) => {
                    const found = datasetsList.find((d) => d.id === e.target.value);
                    if (found) setCurrentDataset(found);
                  }}
                  className="bg-transparent text-slate-200 font-semibold font-mono text-xs focus:outline-none cursor-pointer max-w-[200px]"
                >
                  {datasetsList.map((ds) => (
                    <option key={ds.id} value={ds.id} className="bg-slate-900 text-slate-200">
                      {ds.filename} ({ds.row_count.toLocaleString()} rows)
                    </option>
                  ))}
                </select>
              </div>
            )}
            <div className="flex items-center gap-1.5 bg-emerald-500/10 border border-emerald-500/30 px-3 py-1.5 rounded-lg text-emerald-400 font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              Deterministic ML Active
            </div>
          </div>
        </header>

        {/* Dynamic Page Container */}
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto">
            {activeTab === 'dashboard' && (
              <DashboardPage currentDataset={currentDataset} onNavigate={setActiveTab} />
            )}
            {activeTab === 'datasets' && (
              <DatasetPage
                currentDataset={currentDataset}
                datasetsList={datasetsList}
                onSelectDataset={setCurrentDataset}
                onDatasetUploaded={handleDatasetUploaded}
              />
            )}
            {activeTab === 'anomalies' && <AnomaliesPage currentDataset={currentDataset} />}
            {activeTab === 'patterns' && <PatternsPage currentDataset={currentDataset} />}
            {activeTab === 'investigation' && <InvestigationPage currentDataset={currentDataset} />}
            {activeTab === 'assistant' && <AssistantPage currentDataset={currentDataset} />}
            {activeTab === 'reports' && <ReportsPage currentDataset={currentDataset} />}
          </div>
        </main>
      </div>
    </div>
  );
}
