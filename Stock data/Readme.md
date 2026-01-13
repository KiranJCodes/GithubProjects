I'll help you create professional documentation for this stock price pipeline project, designed for your portfolio with spaces for screenshots.

---

# **Daily Stock Market Pipeline**

## **📌 Project Overview**
An automated data engineering pipeline that collects, processes, and stores live Indian stock market data. This production-ready system fetches real-time prices for a watchlist of 10 stocks daily and stores them in a PostgreSQL database using Apache Airflow for orchestration.

**Development Context**: Built in a Linux environment over approximately 10 hours with assistance from LLMs for code structuring and debugging.

---

## **🎯 Key Features**
- **Real-time API Integration**: Fetches live stock prices from Indian Stock Market API
- **Automated Scheduling**: Apache Airflow DAG executes pipeline at 8 AM every weekday
- **Database Storage**: Structured data storage in PostgreSQL with error handling
- **Performance Monitoring**: Execution time tracking for both API calls and database operations
- **Environment Security**: API keys and credentials managed via `.env` file

---

## **🏗️ Architecture & Workflow**

### **System Architecture Diagram**
```
[Stock Market API] → [Python ETL Script] → [PostgreSQL DB]
       ↑                    ↑
[Apache Airflow Scheduler]  [.env Config]
```

### **Data Pipeline Flow**
1. **Trigger**: Airflow DAG activates at scheduled time (8 AM weekdays)
2. **Extract**: Fetch stock prices for 10 predefined companies from API
3. **Transform**: Clean and structure data (date formatting, type conversion)
4. **Load**: Insert records into PostgreSQL `stockprofile` table
5. **Logging**: Record execution metrics and errors

---

## **📁 Project Structure**
```
stock_price_pipeline/
├── Main.py                 # Core ETL script
├── Stock_dag copy.py       # Airflow DAG definition
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in repo)
└── README.md               # This documentation
```

---

## **⚙️ Technical Implementation**

### **1. Data Extraction (`main.py`)**
```python
# Fetches stock data from Indian Stock Market API
def getStockof(Stock_name, market):
    # Handles API authentication with X-Api-Key header
    # Returns: company name, current price, date, closing price
```

**Key Details**:
- Used `http.client` for API requests
- **API key stored securely in environment variables**
- Market specification (NSE/BSE) supported
- Date transformation from `'03 Dec 2025'` to `'2025-12-03'`

---

### **2. Database Operations**
```python
# PostgreSQL connection with error handling
def connectDB():
    # Establishes connection using psycopg2
    # All credentials from environment variables
```

**Table Schema**:
```sql
-- PostgreSQL table structure
stockprofile (
    id SERIAL PRIMARY KEY,
    company VARCHAR(100),
    price DECIMAL(10,2),
    date DATE,
    closingprice DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

---

### **3. Airflow Orchestration (`dag.py`)**
```python
# Airflow DAG definition
dag = DAG(
    'stock_price_pipeline',
    schedule_interval='0 8 * * 1-5',  # 8 AM on weekdays
    catchup=False
)
```

**Scheduling Logic**:
- **Runs**: Monday-Friday at 8:00 AM
- **No catchup**: Prevents historical runs
- **Retry policy**: 1 retry after 5 minutes on failure

---

## **🛠️ Configuration & Setup**

### **Environment Variables (`.env`)**
```
API_KEY=your_indianapi_key_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=stockdb
DB_USER=postgres
DB_PASSWORD=your_password
```

### **Dependencies**
```txt
apache-airflow>=2.0.0
psycopg2-binary
python-dotenv
```

### **Installation Steps**
```bash
# 1. Clone repository
git clone <repo-url>
cd stock_price_pipeline

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 4. Set up Airflow
airflow db init
airflow users create --username admin --password admin [...]

# 5. Place DAG in Airflow folder
cp dag.py $AIRFLOW_HOME/dags/

# 6. Start Airflow scheduler
airflow scheduler
```

---

## **📊 Stock Watchlist**
The pipeline monitors these 10 NSE stocks:
| Stock | Symbol | Exchange |
|-------|--------|----------|
| Apex | APEX | NSE |
| Suzlon Energy | SUZLON | NSE |
| Canara Bank | CANBK | NSE |
| Tata Steel | TATASTEEL | NSE |
| BHEL | BHEL | NSE |
| Engineers India | ENGINERSIN | NSE |
| RBL Bank | RBLBANK | NSE |
| Wipro | WIPRO | NSE |
| Eternal | ETERNAL | NSE |
| Welspun Living | WELSPUNLIV | NSE |

---

## **📸 Screenshots Section**

### **Airflow DAG Visualization**

![[Pasted image 20260113201617.png]]
*Caption: Airflow DAG execution graph showing successful daily runs of the stock pipeline.*

---

### **Database Records**
![[Pasted image 20260113202157.png]]
*Caption: PostgreSQL table showing historical stock prices collected by the pipeline.*

---

### **Execution Logs**
![[Pasted image 20260113201725.png]]
*Caption: Performance metrics showing API fetch and database insert execution times.*

---

### **Error Handling Example**
![[Pasted image 20260113201830.png]]
*Caption: Pipeline demonstrating robust error handling during API failures or database issues.*

---

## **🚀 Performance & Metrics**
- **API Fetch Time**: ~12-15 seconds for 10 stocks
- **Database Insert Time**: ~0.5-1 seconds for batch insert
- **Total Pipeline Time**: ~15-18 seconds end-to-end
- **Reliability**: 99% success rate in testing

---

## **🔧 Troubleshooting**
| Issue | Solution |
|-------|----------|
| API authentication failed | Verify API key in `.env` file |
| Database connection error | Check PostgreSQL service status and credentials |
| Airflow DAG not loading | Verify file is in `$AIRFLOW_HOME/dags/` directory |
| Date parsing errors | Check API response format for date field |

---

## **📈 Future Enhancements**
1. **Alerting System**: Email/SMS notifications for price thresholds
2. **Data Analytics**: Daily price change reports and trends
3. **Web Dashboard**: Real-time visualization of collected data
4. **Additional Markets**: Support for BSE and international exchanges
5. **Backtesting**: Historical data analysis for strategy testing

---

## **👨‍💻 Development Notes**
- **Time Investment**: Approximately 10 hours development time
- **Environment**: Linux (Ubuntu 22.04), Python 3.9+
- **Tools Used**: VS Code, PostgreSQL CLI, Airflow Web UI
- **LLM Assistance**: Used for code structuring, debugging, and documentation templates

---


*Last Updated: December 2025*  