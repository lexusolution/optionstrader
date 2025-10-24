# OptionsTrader - Stock Options Analysis App Implementation Plan

## Overview
This comprehensive implementation plan outlines the step-by-step approach to build the OptionsTrader application by leveraging:
- Free tiers of cloud services (Google Cloud, AWS, Azure, Oracle Cloud)
- Existing hosting (Mochahost with PHP, Node.js, Python)
- Modern frameworks and libraries (React, Chart.js)
- Efficient data storage strategies to minimize API calls

## Phase 1: Data Collection and Storage Infrastructure

### Task #44: Get News and Store in Database

#### Subtask 44.1: Setup Backend Environment (Mochahost)
- [ ] Create "Python App" in cPanel for the analysis script
- [ ] Note the virtual environment source command for future use

#### Subtask 44.2: Develop News Analysis Script (run_analysis.py)
- [ ] Install required packages in virtual environment:
  ```
  pip install requests google-generativeai oracledb
  ```
- [ ] Write Python function to fetch news from Polygon.io API
- [ ] Write Python function to call Google Gemini API with a sentiment prompt
- [ ] Write Python function to parse the JSON response from Gemini

#### Subtask 44.3: Setup Data Storage (Oracle Cloud Free Tier)
- [ ] Provision a free Oracle Autonomous JSON Database
- [ ] Download the Oracle Wallet for secure connection
- [ ] Upload wallet files to the Mochahost Python App folder
- [ ] Add save_to_database function in run_analysis.py to save:
  - Headline
  - URL
  - Sentiment score
  - Summary
  - Reasoning

#### Subtask 44.4: Automate the News Pipeline (Mochahost)
- [ ] Create a cPanel "Cron Job"
- [ ] Set the cron command to activate the Python App's virtual env and run script:
  ```
  source .../bin/activate && python .../run_analysis.py
  ```

#### Subtask 44.5: Build AI Alerter (AWS Free Tier)
- [ ] Create an S3 bucket for public MP3 hosting
- [ ] Create an SNS topic and subscribe your email
- [ ] Create an AWS Lambda function (Python)
- [ ] Configure IAM permissions for Lambda:
  - Amazon Polly access
  - S3 PutObject permissions
  - SNS Publish permissions
- [ ] Write Lambda code to:
  - Receive headline and reason from the request
  - Call Amazon Polly (AI) to generate an MP3 of the alert
  - Save the MP3 to the S3 bucket (publicly readable)
  - Call SNS to email a link to the S3 audio file
- [ ] Enable the Lambda's Function URL for HTTP access
- [ ] Add check_alert function to run_analysis.py to POST to the Lambda URL if sentiment is high/low

### Task #43: Create a Script to Get Price History and Store in the Database

#### Subtask 43.1: Develop Price History Script
- [ ] Create a new Python script (fetch_price.py) in the Mochahost Python App
- [ ] Write a function to call the Polygon.io "Aggregates" (OHLCV) API for the last 30 days of data
- [ ] Write a function to connect to the Oracle DB

#### Subtask 43.2: Store Price Data (Oracle Cloud)
- [ ] In fetch_price.py, write a function to save the price data
- [ ] Create a new JSON collection (stock_prices) in Oracle DB
- [ ] Ensure the script saves for each day:
  - Ticker symbol
  - Date
  - Open price
  - High price
  - Low price
  - Close price

#### Subtask 43.3: Automate the Price Pipeline (Mochahost)
- [ ] Create a second cPanel "Cron Job"
- [ ] Set it to run once per day (e.g., at 1 AM)
- [ ] Use the same command structure:
  ```
  source .../bin/activate && python .../fetch_price.py
  ```

## Phase 2: User Interface and Visualization

### Task #42: Create a Chart Under the Symbol Price

#### Subtask 42.1: Setup Frontend Environment (Mochahost)
- [ ] Create "Node.js App" in cPanel for the dashboard
- [ ] Assign it a URL (e.g., dashboard.yourdomain.com)
- [ ] Set the startup file to app.js

#### Subtask 42.2: Build Data API (Azure Free Tier)
- [ ] Create an Azure Function App (Python/Consumption Plan)
- [ ] Create an HTTP-triggered function getNews
- [ ] Add Oracle Wallet and oracledb to the function
- [ ] Write code for getNews to query the stock_news collection and return the latest 20 articles as JSON
- [ ] Create a second HTTP-triggered function getPriceHistory
- [ ] Write code for getPriceHistory to query the stock_prices collection and return the last 30 days of data as JSON

#### Subtask 42.3: Build Node.js Server (app.js)
- [ ] In the Node.js app folder, run:
  ```
  npm install express
  ```
- [ ] Create app.js to serve a static index.html file on the root route (/)

#### Subtask 42.4: Build Dashboard UI (index.html)
- [ ] Create index.html in the Node.js app folder
- [ ] Add a `<canvas>` element for the chart and a `<table>` for the news
- [ ] Include the Chart.js library via CDN
- [ ] Write client-side JavaScript (inside `<script>` tags):
  - On page load, fetch data from your Azure getPriceHistory API
  - Use the data to create a new Chart.js line chart
  - On page load, fetch data from your Azure getNews API
  - Use the data to populate the HTML table with the news, summary, and reasoning
- [ ] Restart the Node.js App from cPanel to go live

## Phase 3: Decision Analysis and Recommendations

### Task #10: Create Decision Tree

#### Subtask 10.1: Create Decision API (Azure Free Tier)
- [ ] Create a third Azure Function (getDecision)
- [ ] In this function, fetch data from both your getNews and getPriceHistory functions
- [ ] Write analysis logic:
  - Calculate the average sentiment from the last 5 news articles
  - Calculate the price trend (e.g., is the price today higher than 3 days ago?)
- [ ] Create a "decision" JSON based on this logic:
  ```javascript
  IF avg_sentiment > 0.5 AND price_trend is "UP", 
    THEN {"suggestion": "Strong Bullish", "reason": "Positive news and rising price."}
  IF avg_sentiment < -0.5 AND price_trend is "DOWN", 
    THEN {"suggestion": "Strong Bearish", "reason": "Negative news and falling price."}
  ELSE {"suggestion": "Neutral/Hold", "reason": "Mixed signals."}
  ```
- [ ] Make the function return this "decision" JSON

#### Subtask 10.2: Display Decision on Dashboard
- [ ] In your index.html (Node.js App), add a new div for the decision:
  ```html
  <div id="decision-box">
    <h2>AI Suggestion: <span id="suggestion">...</span></h2>
    <p id="reason">...</p>
  </div>
  ```
- [ ] In your client-side JavaScript, add a new fetch to call your Azure getDecision API
- [ ] Use the result to populate the suggestion and reason spans
- [ ] Restart the Node.js App to deploy the new feature

## Phase 4: Integration and Enhancement (Additional Free Cloud Resources)

### Google Cloud Free Tier Integration
- [ ] Set up Google Cloud Functions for additional data processing (2M invocations/month)
- [ ] Configure Firestore for backup document storage (1GB storage + 50K reads, 20K writes daily)
- [ ] Implement Cloud Scheduler for additional automated tasks (3 free jobs)
- [ ] Use Google Natural Language API free tier (5,000 requests/month) for additional sentiment analysis

### AWS Free Tier Enhancements
- [ ] Use AWS Lambda for additional serverless functions (1M free requests/month)
- [ ] Implement S3 (5GB free storage) for long-term data archiving
- [ ] Configure CloudWatch for monitoring (10 custom metrics free)

### Azure Free Tier Expansion
- [ ] Deploy additional Azure Functions for expanded processing
- [ ] Set up Azure Blob Storage (5GB free storage) for backup
- [ ] Implement Azure Logic Apps for workflow automation (750 action executions/month)

## Phase 5: Performance Optimization and Scalability

### Caching Strategy
- [ ] Implement browser-side caching for UI elements
- [ ] Set up Redis caching (using free tier from Redis Labs) for frequently accessed data
- [ ] Configure proper cache invalidation strategies

### Database Optimization
- [ ] Create appropriate indexes in Oracle JSON DB
- [ ] Implement query optimization for faster retrieval
- [ ] Set up data archiving strategy for historical data

### Bandwidth and Resource Management
- [ ] Implement compression for API responses
- [ ] Optimize image and asset sizes for dashboard
- [ ] Set up monitoring to ensure staying within free tier limits

## Implementation Notes

### Free Tier Usage Monitoring
- [ ] Create a simple monitoring dashboard to track usage of free resources
- [ ] Set up alerts when approaching 80% of free tier limits
- [ ] Implement fallback strategies if any service nears its limit

### Authentication and Security
- [ ] Implement basic authentication for the dashboard
- [ ] Secure API endpoints with API keys
- [ ] Ensure proper encryption for sensitive data

### Deployment and Testing
- [ ] Create a CI/CD pipeline using GitHub Actions (free tier)
- [ ] Implement unit tests for critical components
- [ ] Create an end-to-end testing strategy

---

This plan maximizes free tier usage across multiple cloud providers while leveraging your existing Mochahost environment for both backend processing and frontend display. The architecture distributes workloads efficiently to stay within free tier limits while providing robust functionality.
