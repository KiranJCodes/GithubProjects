# Coffee Production & Import Analysis

## Project Overview
Python data analysis of global coffee production and import trends. This script processes historical coffee data to identify top producers/importers and analyze recent market changes.

## Analysis Performed

### 1. Top Coffee Producers
- Identified top 10 coffee producing countries by total production
- Brazil leads with 75B units (40% of top 10 production)
- Vietnam (28.8B) and Colombia (21.6B) follow as major producers
- Visualized with bar charts showing production in billions

### 2. Production Trend Analysis
- Calculated average production changes between last 5 years vs previous 5 years
- **Top Increases**: Vietnam (+414M), Colombia (+280M), Brazil (+272M)
- **Top Decreases**: El Salvador (-30M), Peru (-27.98M), Venezuela (-26.98M)
- Generated side-by-side visualizations for increases (green) and decreases (red)

### 3. Top Coffee Importers  
- USA dominates imports with 42B units (30% of top 10 imports)
- Germany (31.4B) and Italy (13.2B) are major import markets
- Japan (12.4B) and France (11.9B) complete top 5

### 4. Import Trend Analysis
- Analyzed 5-year import trend changes
- **Top Increases**: Austria (+115M), Italy (+88.5M), Germany (+68.8M)
- **Top Decreases**: Various countries showing minor declines

## Technical Implementation

### Data Processing
- Loaded CSV datasets: `Coffee_production.csv` and `Coffee_import.csv`
- Automated column detection for year-based analysis
- Dynamic calculation of 5-year averages and changes
- Data normalization (conversion to billions/millions for readability)

### Visualization
- Seaborn bar plots with color coding:
  - Green: Positive trends
  - Red: Negative trends  
- Proper labeling with units (Billions/Millions)
- Comparative subplots for increases vs decreases

### Key Functions
- `ShowTopten()`: Universal function for both production and import top 10 analysis
- Automated year column processing for trend analysis
- Flexible data handling for different dataset structures

## Files Required
- `Coffee_report1.py` - Main analysis script
- `Coffee_production.csv` - Production data by country and year
- `Coffee_import.csv` - Import data by country and year

## Dependencies
- pandas
- matplotlib  
- seaborn

Run the script to regenerate all analysis and visualizations.