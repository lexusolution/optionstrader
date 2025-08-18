#!/usr/bin/env python3
"""
AAL Options Data Downloader
Automatically checks and installs required dependencies
"""

import sys
import subprocess
import importlib.util

def check_and_install_package(package_name, import_name=None):
    """Check if package is installed, install if not"""
    if import_name is None:
        import_name = package_name
    
    spec = importlib.util.find_spec(import_name)
    if spec is None:
        print(f"📦 Installing {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✅ {package_name} installed successfully")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package_name}")
            return False
    else:
        print(f"✅ {package_name} already installed")
        return True

def install_requirements():
    """Install all required packages"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        ("yfinance", "yfinance"),
        ("pandas", "pandas"),
        ("requests", "requests")
    ]
    
    all_installed = True
    for package, import_name in required_packages:
        if not check_and_install_package(package, import_name):
            all_installed = False
    
    if not all_installed:
        print("❌ Some packages failed to install. Please run: pip install yfinance pandas requests")
        sys.exit(1)
    
    print("✅ All dependencies ready!\n")

# Check dependencies first
install_requirements()

# Now import the packages
import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def download_aal_options():
    """Download AAL options data"""
    print("🚀 Starting AAL Options Download...")
    
    # Create AAL ticker
    aal = yf.Ticker("AAL")
    
    try:
        # Get current price
        hist = aal.history(period="1d")
        if not hist.empty:
            current_price = hist['Close'].iloc[-1]
            print(f"Current AAL Price: ${current_price:.2f}")
        
        # Get expiration dates
        expirations = aal.options
        print(f"Found {len(expirations)} expiration dates")
        
        if not expirations:
            print("❌ No options data available")
            return
        
        # Create data directory
        today = datetime.now().strftime("%Y-%m-%d")
        os.makedirs("options_data", exist_ok=True)
        
        # Download options for nearest expiration
        exp_date = expirations[0]
        print(f"Downloading options for: {exp_date}")
        
        options = aal.option_chain(exp_date)
        
        # Prepare data
        calls = options.calls.copy()
        puts = options.puts.copy()
        
        calls['type'] = 'CALL'
        calls['expiration'] = exp_date
        calls['download_time'] = datetime.now()
        
        puts['type'] = 'PUT'
        puts['expiration'] = exp_date
        puts['download_time'] = datetime.now()
        
        # Combine and save
        all_options = pd.concat([calls, puts], ignore_index=True)
        filename = f"options_data/AAL_options_{exp_date}_{today}.csv"
        all_options.to_csv(filename, index=False)
        
        print(f"✅ Saved {len(all_options)} options to: {filename}")
        
        # Show summary
        print(f"\n📊 Summary:")
        print(f"Calls: {len(calls)}")
        print(f"Puts: {len(puts)}")
        print(f"Total Volume: {all_options['volume'].sum():,.0f}")
        print(f"Total Open Interest: {all_options['openInterest'].sum():,.0f}")
        
        # Show top options by volume
        top_volume = all_options.nlargest(5, 'volume')[['strike', 'type', 'lastPrice', 'volume', 'openInterest']]
        print(f"\n🔥 Top 5 by Volume:")
        print(top_volume)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    download_aal_options()
