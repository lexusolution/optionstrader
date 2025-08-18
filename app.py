from flask import Flask, render_template, jsonify
import sys

app = Flask(__name__)

# Add dependency check
try:
    import yfinance as yf
    import pandas as pd
    DEPENDENCIES_OK = True
except ImportError as e:
    DEPENDENCIES_OK = False
    IMPORT_ERROR = str(e)

from datetime import datetime

@app.route('/')
def index():
    """Main page with JavaScript frontend"""
    return render_template('index.html')

@app.route('/test')
def simple_test():
    """Simple test page to verify Flask is working"""
    return "<h1>Flask is working!</h1><p>Routes are being processed correctly.</p>"

@app.route('/api/options/<symbol>')
def get_options(symbol):
    """API endpoint that returns JSON data for JavaScript to consume"""
    
    # Check dependencies first
    if not DEPENDENCIES_OK:
        return jsonify({
            "error": f"Missing dependencies: {IMPORT_ERROR}",
            "fix": "Run: pip install yfinance pandas"
        }), 500
    
    try:
        # Add debug logging
        print(f"Getting options for symbol: {symbol}")
        
        ticker = yf.Ticker(symbol.upper())
        
        # Get current price
        print("Getting price history...")
        hist = ticker.history(period="1d")
        current_price = hist['Close'].iloc[-1] if not hist.empty else 0
        print(f"Current price: {current_price}")
        
        # Get options data
        print("Getting options expirations...")
        expirations = ticker.options
        print(f"Found {len(expirations)} expirations")
        
        if not expirations:
            return jsonify({"error": "No options data available"})
        
        # Get options for nearest expiration
        exp_date = expirations[0]
        print(f"Getting options for expiration: {exp_date}")
        options = ticker.option_chain(exp_date)
        
        # Convert to JSON-friendly format
        print("Converting to JSON...")
        calls_data = options.calls.to_dict('records')
        puts_data = options.puts.to_dict('records')
        
        result = {
            "symbol": symbol.upper(),
            "current_price": round(current_price, 2),
            "expiration": exp_date,
            "calls": calls_data[:10],  # Limit to top 10
            "puts": puts_data[:10],
            "timestamp": datetime.now().isoformat()
        }
        
        print("Success - returning JSON data")
        return jsonify(result)
        
    except Exception as e:
        print(f"ERROR in get_options: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/test')
def test_api():
    """Simple test endpoint"""
    return jsonify({"status": "working", "message": "API is functional"})

@app.route('/api/price/<symbol>')
def get_price(symbol):
    """Quick API to get just the current price"""
    try:
        ticker = yf.Ticker(symbol.upper())
        hist = ticker.history(period="1d")
        current_price = hist['Close'].iloc[-1] if not hist.empty else 0
        
        return jsonify({
            "symbol": symbol.upper(),
            "price": round(current_price, 2),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
