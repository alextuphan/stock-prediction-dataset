# VN30 Stock Data Crawler

A simple tool to crawl historical stock trading data for Vietnam's VN30 index (30 major stocks) from VNDirect API.

**GitHub Repository**: https://github.com/alextuphan/stock-prediction-dataset

## Quick Start

```bash
python3 vn30_crawler.py
```

## Overview

- **Number of stocks**: 30 VN30 stocks
- **Time range**: January 1, 2010 to present
- **Data format**: CSV files
- **API source**: VNDirect Financial API
- **Weekend handling**: Automatically excluded (Saturday & Sunday)

## VN30 Stock Symbols

```
ACB, BID, BVH, CTG, FPT, GAS, GVR, HDB, HPG, MBB,
MSN, MWG, NVL, PDR, PLX, POW, SAB, SSI, STB, TCB,
TPB, VCB, VHM, VIC, VJC, VNM, VPB, VRE, VPI, VTP
```

## Project Structure

```
stock-prediction-dataset/
├── stock_data/                      # Created after running crawler
│   ├── ACB/
│   │   └── ACB_historical_data.csv
│   ├── BID/
│   │   └── BID_historical_data.csv
│   └── ... (28 more folders)
├── vn30_crawler.py                  # Main crawler script
├── .gitignore                       # Git ignore config
└── README.md                        # This file
```

## CSV Data Structure

Each CSV file contains 23 fields from VNDirect API:

### Basic Information
- code: Stock symbol
- date: Trading date (YYYY-MM-DD)
- time: Trading time
- floor: Exchange (HOSE, HNX, UPCOM)
- type: Security type

### Reference Prices
- basicPrice: Reference price
- ceilingPrice: Price ceiling (maximum allowed price)
- floorPrice: Price floor (minimum allowed price)

### Trading Prices
- open: Opening price
- high: Highest price
- low: Lowest price
- close: Closing price
- average: Average price

### Adjusted Prices
- adOpen: Adjusted opening price
- adHigh: Adjusted highest price
- adLow: Adjusted lowest price
- adClose: Adjusted closing price
- adAverage: Adjusted average price

### Volume Data
- nmVolume: Matched volume
- nmValue: Matched value
- ptVolume: Put-through volume
- ptValue: Put-through value

### Price Changes
- change: Price change (+/-)
- adChange: Adjusted price change
- pctChange: Percentage change

### Sample Data

```csv
code,date,time,floor,type,basicPrice,ceilingPrice,floorPrice,open,high,low,close,average,adOpen,adHigh,adLow,adClose,adAverage,nmVolume,nmValue,ptVolume,ptValue,change,adChange,pctChange
FPT,2025-10-31,15:10:03,HOSE,STOCK,102.7,109.8,95.6,102.6,103.9,101.0,103.9,102.917,102.6,103.9,101.0,103.9,102.917,1.48271E7,1.52595542E12,2447615.0,2.60069674E11,1.2,1.2,1.1685
FPT,2025-10-30,15:10:05,HOSE,STOCK,101.7,108.8,94.6,102.1,103.5,101.6,102.7,102.696,102.1,103.5,101.6,102.7,102.696,9730600.0,9.9929254E11,20004.0,2.0363784E9,1.0,1.0,0.9833
```

## Features

- Automatic folder creation for each stock
- Crawls data from 2010-01-01 to current date
- Automatically excludes weekends
- Saves all 23 fields from VNDirect API
- CSV format ready for database import
- Rate limiting (1 second delay between requests)
- Error handling and logging
- No external dependencies (uses Python built-in libraries only)

## System Requirements

- Python 3.6 or higher
- Internet connection
- Approximately 500MB storage for full historical data

## Important Notes

1. **Internet Connection**: Required to access VNDirect API
2. **Crawl Time**: Takes approximately 5-15 minutes for all 30 stocks from 2010
3. **Weekend Data**: Automatically excluded from results
4. **Rate Limiting**: 1-second delay between requests to avoid API spam
5. **Data Updates**: Re-run the script to fetch the latest data

## Troubleshooting

### Connection Errors
Check your internet connection. VNDirect API may be temporarily unavailable.

### SSL Errors
The script automatically handles SSL verification. If issues persist, check your Python SSL configuration.

### API Rate Limiting
Current delay is 1 second per request. If you encounter rate limiting, increase the delay in the code.

### Missing Data
Some stocks may not have data from 2010 if they were listed later. This is normal.

## Data Output

After running the crawler, you will have:
- 30 folders in `stock_data/` directory
- Each folder contains one CSV file
- CSV files include all historical data from 2010-01-01 to present
- All weekends are excluded
- All 23 fields from VNDirect API are included

## License

Free to use for personal, educational, and commercial purposes.

## Data Source

VNDirect Financial API: https://api-finfo.vndirect.com.vn/
