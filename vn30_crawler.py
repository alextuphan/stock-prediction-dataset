#!/usr/bin/env python3
"""
VN30 Stock Data Crawler
Crawls historical stock data for 30 VN30 stocks from VNDirect API
Data range: 2010-01-01 to present (excluding weekends)
"""

import json
import ssl
import os
import csv
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
import time

# Disable SSL verification for VNDirect API
ssl._create_default_https_context = ssl._create_unverified_context

# VN30 stock symbols (30 main stocks in Vietnam stock market)
VN30_SYMBOLS = [
    "ACB", "BID", "BVH", "CTG", "FPT", "GAS", "GVR", "HDB", "HPG", "MBB",
    "MSN", "MWG", "NVL", "PDR", "PLX", "POW", "SAB", "SSI", "STB", "TCB",
    "TPB", "VCB", "VHM", "VIC", "VJC", "VNM", "VPB", "VRE", "VPI", "VTP"
]

# Configuration
START_DATE = "2010-01-01"
DATA_DIR = "stock_data"
API_BASE_URL = "https://api-finfo.vndirect.com.vn/v4/stock_prices"

def get_end_date():
    """Get current date as end date"""
    return datetime.now().strftime("%Y-%m-%d")

def is_weekend(date_str):
    """Check if a date is weekend (Saturday or Sunday)"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.weekday() >= 5  # 5=Saturday, 6=Sunday

def create_folder_structure():
    """Create folders for each stock symbol"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    for symbol in VN30_SYMBOLS:
        symbol_dir = os.path.join(DATA_DIR, symbol)
        if not os.path.exists(symbol_dir):
            os.makedirs(symbol_dir)
            print(f"[INFO] Created folder: {symbol_dir}")
        else:
            print(f"[INFO] Folder exists: {symbol_dir}")

def fetch_stock_data(symbol, start_date, end_date):
    """
    Fetch stock data from VNDirect API
    
    Args:
        symbol: Stock symbol (e.g., 'VCB')
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        List of stock records
    """
    query_params = (
        f"sort=date&q=code:{symbol}"
        f"~date:gte:{start_date}~date:lte:{end_date}"
        f"&size=9990&page=1"
    )
    api_url = f"{API_BASE_URL}?{query_params}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        request = Request(api_url, headers=headers)
        response_data = urlopen(request, timeout=30).read()
        parsed_data = json.loads(response_data)
        
        if "data" in parsed_data and isinstance(parsed_data["data"], list):
            return parsed_data["data"]
        return []
    
    except Exception as e:
        print(f"[ERROR] Error fetching {symbol}: {str(e)}")
        return []

def save_to_csv(symbol, data):
    """
    Save stock data to CSV file with all available fields from API
    
    Args:
        symbol: Stock symbol
        data: List of stock records
    """
    if not data:
        print(f"  [WARN] No data to save for {symbol}")
        return
    
    # Filter out weekend data
    filtered_data = [record for record in data if not is_weekend(record.get("date", ""))]
    
    if not filtered_data:
        print(f"  [WARN] No weekday data for {symbol}")
        return
    
    csv_file = os.path.join(DATA_DIR, symbol, f"{symbol}_historical_data.csv")
    
    # CSV columns - all fields from VNDirect API
    fieldnames = [
        # Basic info
        "code", "date", "time", "floor", "type",
        # Price data
        "basicPrice", "ceilingPrice", "floorPrice",
        "open", "high", "low", "close", "average",
        # Adjusted price data
        "adOpen", "adHigh", "adLow", "adClose", "adAverage",
        # Volume data
        "nmVolume", "nmValue", "ptVolume", "ptValue",
        # Change data
        "change", "adChange", "pctChange"
    ]
    
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            
            for record in filtered_data:
                # Keep all fields from API response
                normalized_record = {
                    "code": record.get("code", symbol),
                    "date": record.get("date", ""),
                    "time": record.get("time", ""),
                    "floor": record.get("floor", ""),
                    "type": record.get("type", ""),
                    # Prices
                    "basicPrice": record.get("basicPrice", ""),
                    "ceilingPrice": record.get("ceilingPrice", ""),
                    "floorPrice": record.get("floorPrice", ""),
                    "open": record.get("open", ""),
                    "high": record.get("high", ""),
                    "low": record.get("low", ""),
                    "close": record.get("close", ""),
                    "average": record.get("average", ""),
                    # Adjusted prices
                    "adOpen": record.get("adOpen", ""),
                    "adHigh": record.get("adHigh", ""),
                    "adLow": record.get("adLow", ""),
                    "adClose": record.get("adClose", ""),
                    "adAverage": record.get("adAverage", ""),
                    # Volume
                    "nmVolume": record.get("nmVolume", ""),
                    "nmValue": record.get("nmValue", ""),
                    "ptVolume": record.get("ptVolume", ""),
                    "ptValue": record.get("ptValue", ""),
                    # Changes
                    "change": record.get("change", ""),
                    "adChange": record.get("adChange", ""),
                    "pctChange": record.get("pctChange", "")
                }
                writer.writerow(normalized_record)
        
        print(f"  [INFO] Saved {len(filtered_data)} records to {csv_file}")
    
    except Exception as e:
        print(f"  [ERROR] Error saving {symbol}: {str(e)}")

def crawl_stock(symbol, start_date, end_date):
    """
    Crawl data for a single stock
    
    Args:
        symbol: Stock symbol
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    """
    print(f"\n{'='*60}")
    print(f"Crawling {symbol} from {start_date} to {end_date}")
    print(f"{'='*60}")
    
    data = fetch_stock_data(symbol, start_date, end_date)
    
    if data:
        save_to_csv(symbol, data)
        print(f"[INFO] {symbol} completed successfully")
    else:
        print(f"[ERROR] {symbol} failed or no data available")
    
    # Rate limiting - be polite to the API
    time.sleep(1)

def main():
    """Main crawler function"""
    print("\n" + "="*60)
    print("VN30 STOCK DATA CRAWLER")
    print("="*60)
    print(f"Start Date: {START_DATE}")
    print(f"End Date: {get_end_date()}")
    print(f"Total Symbols: {len(VN30_SYMBOLS)}")
    print(f"Symbols: {', '.join(VN30_SYMBOLS)}")
    print("="*60 + "\n")
    
    # Step 1: Create folder structure
    print("Step 1: Creating folder structure...")
    create_folder_structure()
    
    # Step 2: Crawl data for each stock
    print("\nStep 2: Crawling stock data...")
    
    end_date = get_end_date()
    success_count = 0
    fail_count = 0
    
    for i, symbol in enumerate(VN30_SYMBOLS, 1):
        print(f"\nProgress: [{i}/{len(VN30_SYMBOLS)}]")
        try:
            crawl_stock(symbol, START_DATE, end_date)
            success_count += 1
        except Exception as e:
            print(f"[ERROR] Unexpected error for {symbol}: {str(e)}")
            fail_count += 1
    
    # Summary
    print("\n" + "="*60)
    print("CRAWLING SUMMARY")
    print("="*60)
    print(f"Total Stocks: {len(VN30_SYMBOLS)}")
    print(f"Success: {success_count}")
    print(f"Failed: {fail_count}")
    print("="*60)
    
    print(f"\n[INFO] All data saved to '{DATA_DIR}/' directory")
    print(f"[INFO] Each stock has its own folder with CSV file")
    print(f"[INFO] CSV format is ready for database import")

if __name__ == "__main__":
    main()

