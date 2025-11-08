# FIFA 21 Data Cleaning Tutorial

## Project Overview
A comprehensive data cleaning pipeline for FIFA 21 player dataset, demonstrating practical data preprocessing techniques for real-world messy data.

## Data Cleaning Steps Performed

### 1. Column Management
- **Removed Non-Essential Columns**: Dropped irrelevant fields including `Name`, `photoUrl`, `playerUrl`, `Joined`, `Loan Date End`, `Club`, `Positions`, `LongName`, `Nationality`
- **Column Selection**: Limited dataset to first 18 columns for focused analysis

### 2. Data Type Conversion & Standardization

#### Height Conversion
- Converted mixed format heights (`5'11"` and `180cm`) to consistent centimeters
- Handled both imperial (feet'inches") and metric (cm) formats
- **Process**: Split feet/inches, calculated total inches, converted to cm

#### Weight Conversion  
- Standardized weight data from mixed `lbs` and `kg` formats to kilograms
- **Process**: Extracted numeric values, applied conversion factor for pounds (0.453592)

#### Financial Data Cleaning
- **Value, Wage, Release Clause**: Removed '€' symbol and converted K/M suffixes to numeric values
- **Conversion Logic**: 
  - 'M' = ×1,000,000
  - 'K' = ×1,000
  - Default cases handled with fallback values

### 3. Categorical Data Encoding

#### Preferred Foot
- Mapped to binary values: `{'Left': 0, 'Right': 1}`

#### Best Position  
- Encoded 15 player positions to numeric codes:
  - `ST:1, CF:2, LW:3, RW:4, CAM:5, CDM:6, CM:7, LM:8, RM:9, GK:0, CB:10, LB:11, RB:12, RWB:13, LWB:14`

### 4. Contract Data Processing
- **Complex String Parsing**: Handled multiple contract formats:
  - Range format: `"2018~2022"`
  - Loan format: `"On Loan 2021~2023"`
  - Single year: `"2021"`
  - Free agents: `"Free"`
- **Created New Columns**:
  - `start`: Contract start year
  - `end`: Contract end year  
  - `loan`: Binary indicator for loan status (1=on loan, 0=not)
- **Dropped Original**: Removed raw `Contract` column after extraction

## Technical Implementation

### Libraries Used
- **pandas**: Data manipulation and cleaning
- **numpy**: Numerical operations and NaN handling

### Data Quality Improvements
- Standardized measurement units across all records
- Converted categorical data to machine-readable formats
- Extracted structured information from complex text fields
- Maintained data integrity through systematic processing

## Result
**Clean Dataset**: 2000 players × 20 columns with consistent numeric data types, ready for analysis, visualization, or machine learning applications.

## Files Required
- `Cleaning Tutorial.ipynb` - Jupyter notebook with complete cleaning pipeline
- `FIFA21.csv` - Raw FIFA 21 player dataset

Run the notebook sequentially to reproduce the entire data cleaning process.