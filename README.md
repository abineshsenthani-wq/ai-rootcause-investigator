# AI ROOT-CAUSE INVESTIGATOR

> **AI-Powered Business Anomaly Detection & Root-Cause Analysis**
> *"Find what changed. Understand why. Act with evidence."*

---

## 🔍 Executive Problem & Overview

Traditional business intelligence dashboards (PowerBI, Tableau, Looker) excel at showing **what** happened:
> *"Revenue decreased by 24.1% in July."*

However, traditional dashboards rarely explain **why** it happened or automatically isolate contributing factors.

**AI ROOT-CAUSE INVESTIGATOR** acts as an automated data science investigator. When an anomaly or metric shift occurs, the system automatically analyzes the dataset to determine:
1. **When** did the anomaly begin?
2. **Which** dimension slices (region, product category, customer segment, sales channel) contributed most?
3. **What** operational variables co-varied or spiked during the same period?
4. **Which** anomalies occurred across transaction records?
5. **What** evidence score supports each potential root cause?

---

## 📐 Architecture & Principles

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 DATA SCIENCE ENGINE (Python)                           │
│                                                                                        │
│  [CSV / Excel Upload] ──> Data Profiling & Validation ──> Time Trend Engine            │
│                                                                   │                    │
│  ┌────────────────────────────────────────────────────────────────┴─────────────────┐  │
│  │                                                                                  │  │
│  ▼                                   ▼                                              ▼  │
│ Multi-Method Anomaly        Segment Contribution %                   Pearson / Spearman│ │
│ (IQR, Z-Score, I-Forest)   (Drop / Total Drop * 100)               Correlations     │ │
│  │                                   │                                              │  │
│  └───────────────────────────────────┼──────────────────────────────────────────────┘  │
│                                      ▼                                                 │
│                        Root-Cause Multi-Factor Ranking Engine                           │
│                        (Contribution 40%, Correlation 20%,                             │
│                         Temporal 20%, Anomaly 10%, Coverage 10%)                       │
│                                      │                                                 │
└──────────────────────────────────────┼─────────────────────────────────────────────────┘
                                       ▼
                       ┌──────────────────────────────┐
                       │  STRUCTURED JSON EVIDENCE    │
                       └──────────────┬───────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │    LLM EXPLANATION LAYER     │
                       │ (Grounded Prompt Enforcement)│
                       └──────────────┬───────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │      REACT UI WORKSPACE      │
                       │ (Evidence Graph, PDF Report) │
                       └──────────────────────────────┘
```

### Critical Principle: Data Science First, AI Second
The LLM does **not** analyze raw data directly or guess statistical figures. Python (Pandas, SciPy, Scikit-Learn) computes all statistics, anomalies, correlations, and segment contributions deterministically. The LLM receives structured JSON evidence purely to draft articulate executive summaries.

### Strict Separation: Fact vs. Hypothesis vs. Recommendation
- **FACT**: Directly calculated from the dataset (e.g., *"Revenue decreased by 24.1%. West region dropped -41.8%, contributing 42% of total loss."*).
- **HYPOTHESIS**: A statistical association supported by evidence (e.g., *"Delivery time increased by +31% in the West region during the same window, scoring 82/100 on evidence alignment."*).
- **RECOMMENDATION**: Next steps for investigation (e.g., *"Audit West region fulfillment carrier performance and Product C stock levels."*).

---

## 🛠️ Tech Stack

- **Backend**: Python 3.13, FastAPI, Pydantic v2, Pandas, NumPy, SciPy, Scikit-learn, SQLAlchemy, SQLite, ReportLab
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Recharts, Lucide Icons
- **AI Integration**: Provider Abstraction (OpenAI GPT-4o-mini, Anthropic Claude, or Deterministic Template Fallback Engine)
- **Deployment**: Docker, Docker Compose

---

## 🚀 Quick Start & Local Execution

### 1. Backend Setup
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
- API Health Check: `http://localhost:8000/api/health`
- Swagger OpenAPI Docs: `http://localhost:8000/docs`

### 2. Frontend Setup
```powershell
cd frontend
npm install
npm run dev
```
- Web Application UI: `http://localhost:5173`

### 3. Generate 100,000-Row Benchmark Dataset
```powershell
python data/sample/generate_synthetic_data.py
```

### 4. Run Automated Test Suite
```powershell
cd backend
.\venv\Scripts\pytest
```

---

## 🎤 3-Minute Technical Interview Explanation

> *"Traditional dashboards tell business leaders **what** happened — for example, that revenue dropped by 24%. My system automatically investigates **why** it happened.*
>
> *When an anomaly occurs, the application ingests the dataset and runs an automated analytical pipeline. First, Python computes time-series trends and period-over-period shifts. Next, a multi-method anomaly detection engine runs IQR, Z-Score, and Isolation Forest ML models to isolate outlier transactions.*
>
> *Then, a dimension contribution engine calculates the exact mathematical percentage share of the decline contributed by each product, region, or customer segment. At the same time, Pearson and Spearman correlation algorithms scan numerical variables to detect co-varying operational indicators — such as a 31% delivery delay spike.*
>
> *These signals are aggregated into a transparent multi-factor evidence score out of 100. Crucially, the LLM does not calculate the numbers. Python and machine learning generate structured evidence first, and the LLM acts purely as an articulation layer to turn that evidence into natural language summaries.*
>
> *Finally, the system enforces a strict separation between **FACTS**, **HYPOTHESES**, and **RECOMMENDATIONS** so that observational correlation is never presented as unproven causation."*
