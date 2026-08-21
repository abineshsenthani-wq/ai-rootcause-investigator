import { SystemHealth, DatasetMeta, ProfileSummary } from '../types';

const API_BASE = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL.replace(/\/$/, '')}/api` 
  : '/api';

export async function fetchHealth(): Promise<SystemHealth> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.statusText}`);
  return res.json();
}

export async function fetchDatasets(): Promise<DatasetMeta[]> {
  const res = await fetch(`${API_BASE}/datasets`);
  if (!res.ok) return [];
  return res.json();
}

export async function uploadDataset(file: File): Promise<DatasetMeta> {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/datasets/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Failed to upload dataset');
  }

  return res.json();
}

export async function fetchDatasetProfile(datasetId: string): Promise<ProfileSummary> {
  const res = await fetch(`${API_BASE}/datasets/${datasetId}/profile`);
  if (!res.ok) throw new Error(`Failed to fetch dataset profile: ${res.statusText}`);
  return res.json();
}

export async function fetchDatasetTrends(datasetId: string, metric?: string, granularity?: string): Promise<any> {
  let url = `${API_BASE}/datasets/${datasetId}/trends?`;
  if (metric) url += `metric=${encodeURIComponent(metric)}&`;
  if (granularity) url += `granularity=${encodeURIComponent(granularity)}`;

  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to fetch trends: ${res.statusText}`);
  return res.json();
}

export async function fetchDatasetEvents(datasetId: string, metric?: string): Promise<any[]> {
  let url = `${API_BASE}/datasets/${datasetId}/events?`;
  if (metric) url += `metric=${encodeURIComponent(metric)}`;

  const res = await fetch(url);
  if (!res.ok) return [];
  return res.json();
}

export async function fetchDatasetAnomalies(datasetId: string, metric?: string): Promise<any> {
  let url = `${API_BASE}/datasets/${datasetId}/anomalies?`;
  if (metric) url += `metric=${encodeURIComponent(metric)}`;

  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to fetch anomalies: ${res.statusText}`);
  return res.json();
}

export async function runInvestigation(datasetId: string, payload: { metric?: string; start_period?: string; end_period?: string; question?: string } = {}): Promise<any> {
  const res = await fetch(`${API_BASE}/datasets/${datasetId}/investigate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Investigation failed');
  }

  return res.json();
}

export async function simulateScenario(datasetId: string, targetMetric: string, driverAdjustments: Record<string, number>): Promise<any> {
  const res = await fetch(`${API_BASE}/datasets/${datasetId}/simulate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      target_metric: targetMetric,
      driver_adjustments: driverAdjustments,
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Simulation failed');
  }

  return res.json();
}

export async function fetchMetricForecast(datasetId: string, metric?: string, periods: number = 12): Promise<any> {
  let url = `${API_BASE}/datasets/${datasetId}/forecast?periods=${periods}`;
  if (metric) url += `&metric=${encodeURIComponent(metric)}`;

  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to fetch forecast: ${res.statusText}`);
  return res.json();
}

export async function sendChatQuestion(datasetId: string, question: string): Promise<any> {
  const res = await fetch(`${API_BASE}/datasets/${datasetId}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Chat request failed');
  }

  return res.json();
}

export async function fetchChatHistory(datasetId: string): Promise<any[]> {
  const res = await fetch(`${API_BASE}/datasets/${datasetId}/chat/history`);
  if (!res.ok) return [];
  const data = await res.json();
  return data.messages || [];
}

export async function clearChatHistory(datasetId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/datasets/${datasetId}/chat/history`, {
    method: 'DELETE',
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Failed to clear chat history');
  }
}

export function getReportDownloadUrl(datasetId: string): string {
  return `${API_BASE}/datasets/${datasetId}/report`;
}
