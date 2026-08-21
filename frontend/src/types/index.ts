export type NavigationTab = 
  | 'dashboard' 
  | 'datasets' 
  | 'anomalies' 
  | 'patterns' 
  | 'investigation' 
  | 'assistant' 
  | 'reports';

export interface SystemHealth {
  status: 'healthy' | 'degraded' | 'error';
  version: string;
  environment: string;
  database_connected: boolean;
  storage_directory_writable: boolean;
  details: {
    llm_provider: string;
    data_storage_dir: string;
  };
}

export interface DatasetMeta {
  id: string;
  filename: string;
  upload_timestamp: string;
  file_size_bytes: number;
  row_count: number;
  column_count: number;
  date_min?: string;
  date_max?: string;
  primary_metric?: string;
  date_column?: string;
  anomaly_count?: number;
}

export interface ProfileSummary {
  classification?: {
    numerical_columns: string[];
    categorical_columns: string[];
    date_columns: string[];
    boolean_columns: string[];
    identifier_columns: string[];
  };
  numerical_columns?: string[];
  categorical_columns?: string[];
  date_columns?: string[];
  identifier_columns?: string[];
  column_stats?: Record<string, any>;
}
