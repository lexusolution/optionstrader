# OptionsTrader

A stock options analysis app that leverages free cloud resources and AI to analyze market data.

## Architecture
```mermaid
graph TD
    %% Define the main components
    User(User) --> Dashboard(Dashboard UI on Mochahost Node.js)
    
    %% Data Collection
    PolygonAPI[Polygon.io API] -->|News Data| NewsScript[run_analysis.py on Mochahost]
    PolygonAPI -->|Price History| PriceScript[fetch_price.py on Mochahost]
    
    %% AI Processing
    NewsScript -->|Sentiment Analysis| GeminiAI[Google Gemini API]
    GeminiAI -->|Results| NewsScript
    
    %% Data Storage
    NewsScript -->|Store News & Sentiment| OracleDB[(Oracle JSON DB)]
    PriceScript -->|Store Price Data| OracleDB
    
    %% Alert System
    NewsScript -->|High/Low Sentiment| AWSLambda[AWS Lambda]
    AWSLambda -->|Generate Audio| AmazonPolly[Amazon Polly]
    AmazonPolly -->|Store MP3| S3[AWS S3 Bucket]
    AWSLambda -->|Send Alert| SNS[AWS SNS]
    SNS -->|Email Alert| User
    
    %% Azure API Functions
    AzureGetNews[Azure Function: getNews] -->|Query| OracleDB
    AzureGetPrice[Azure Function: getPriceHistory] -->|Query| OracleDB
    AzureGetDecision[Azure Function: getDecision] -->|Query News| AzureGetNews
    AzureGetDecision -->|Query Price| AzureGetPrice
    AzureGetDecision -->|Generate Decision| AzureGetDecision
    
    %% Dashboard Connections
    Dashboard -->|Fetch News| AzureGetNews
    Dashboard -->|Fetch Price Data| AzureGetPrice
    Dashboard -->|Get Trading Recommendation| AzureGetDecision
    
    %% Automation
    MochaCron1[Mochahost Cron Job 1] -->|Daily Trigger| NewsScript
    MochaCron2[Mochahost Cron Job 2] -->|Daily Trigger| PriceScript
    
    %% Styling
    classDef aws fill:#FF9900,stroke:#232F3E,color:white
    classDef azure fill:#0089D6,stroke:#0072C6,color:white
    classDef gcp fill:#4285F4,stroke:#3367D6,color:white
    classDef oracle fill:#F80000,stroke:#D00000,color:white
    classDef mochahost fill:#76B900,stroke:#5B9600,color:white
    classDef api fill:#FF5722,stroke:#E64A19,color:white
    classDef user fill:#9C27B0,stroke:#7B1FA2,color:white
    
    class AWSLambda,S3,SNS,AmazonPolly aws
    class AzureGetNews,AzureGetPrice,AzureGetDecision azure
    class GeminiAI gcp
    class OracleDB oracle
    class NewsScript,PriceScript,Dashboard,MochaCron1,MochaCron2 mochahost
    class PolygonAPI api
    class User user
```

2. You can also add the implementation plan and timeline as separate markdown files in your repository:
   - Create a file called `IMPLEMENTATION_PLAN.md`
   - Create a file called `TIMELINE.md`
   - Copy the contents from the files I generated into these new files

3. To commit these files to your GitHub repository:
```bash
   git clone https://github.com/lexusolution/optionstrader.git
   cd optionstrader
   # Create the README.md file with the Mermaid diagram
   # Create the IMPLEMENTATION_PLAN.md file
   # Create the TIMELINE.md file
   git add .
   git commit -m "Add architecture diagram, implementation plan, and timeline"
   git push
```

GitHub now supports Mermaid diagrams natively in markdown, so the diagram will automatically render in your README.md file when viewed on GitHub.

Would you like me to help you with creating the other files for your repository or making any adjustments to the plan?
