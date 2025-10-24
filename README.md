# OptionsTrader

A comprehensive stock options analysis application that leverages free cloud resources and AI services to analyze market data and provide trading recommendations.

## Architecture

```mermaid
graph TD
    %% Users and Frontend
    User(User) --> Dashboard(Dashboard UI on Mochahost Node.js/React)
    
    %% Data Sources
    PolygonAPI[Polygon.io API] -->|News Data| NewsScript[run_analysis.py on Mochahost]
    PolygonAPI -->|Price History| PriceScript[fetch_price.py on Mochahost]
    
    %% Primary Database - Oracle Cloud
    NewsScript -->|Store News & Sentiment| OracleDB[(Oracle JSON DB)]
    PriceScript -->|Store Price Data| OracleDB
    
    %% AI Processing - Google Cloud
    NewsScript -->|Sentiment Analysis| GeminiAI[Google Gemini API]
    GeminiAI -->|Results| NewsScript
    NewsScript -.->|Backup Analysis| GoogleNL[Google Natural Language API]
    GoogleNL -.->|Sentiment Results| NewsScript
    
    %% AI Processing - Azure
    NewsScript -.->|Additional Analysis| AzureTxtAnal[Azure Text Analytics]
    AzureTxtAnal -.->|Sentiment Results| NewsScript
    
    %% AI Processing - AWS
    NewsScript -.->|Alternative Analysis| AWSComprehend[AWS Comprehend]
    AWSComprehend -.->|Sentiment Results| NewsScript
    
    %% Alert System - AWS
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
    
    %% Google Cloud Functions
    GCPBackup[GCP Function: backupData] -.->|Backup News| FirestoreDB[(Google Firestore)]
    GCPBackup -.->|Archive Data| GCS[(Google Cloud Storage)]
    GCPBackup -.->|Fetch Data| AzureGetNews
    
    %% AWS Additional Services
    AWSForecasting[AWS Lambda: priceForecast] -.->|Historical Prices| AzureGetPrice
    AWSForecasting -.->|ML Prediction| AWSSageMaker[AWS SageMaker]
    AWSSageMaker -.->|Store Model| S3
    AWSForecasting -.->|Store Predictions| DynamoDB[(AWS DynamoDB)]
    
    %% Azure ML Services
    AzureAutoML[Azure AutoML] -.->|Training Data| AzureGetPrice
    AzureAutoML -.->|Store Model| AzureBlobStorage[(Azure Blob Storage)]
    AzureGetDecision -.->|Validate Decision| AzureAutoML
    
    %% Oracle Additional Services
    OracleFunction[Oracle Cloud Function] -.->|DB Maintenance| OracleDB
    
    %% Dashboard Connections
    Dashboard -->|Fetch News| AzureGetNews
    Dashboard -->|Fetch Price Data| AzureGetPrice
    Dashboard -->|Get Trading Recommendation| AzureGetDecision
    Dashboard -.->|Optional: Direct Access| DynamoDB
    
    %% Automation
    MochaCron1[Mochahost Cron Job 1] -->|Daily Trigger| NewsScript
    MochaCron2[Mochahost Cron Job 2] -->|Daily Trigger| PriceScript
    GCPScheduler[Google Cloud Scheduler] -.->|Daily Trigger| GCPBackup
    
    %% Styling
    classDef aws fill:#FF9900,stroke:#232F3E,color:white
    classDef azure fill:#0089D6,stroke:#0072C6,color:white
    classDef gcp fill:#4285F4,stroke:#3367D6,color:white
    classDef oracle fill:#F80000,stroke:#D00000,color:white
    classDef mochahost fill:#76B900,stroke:#5B9600,color:white
    classDef api fill:#FF5722,stroke:#E64A19,color:white
    classDef user fill:#9C27B0,stroke:#7B1FA2,color:white
    
    class AWSLambda,S3,SNS,AmazonPolly,AWSComprehend,AWSSageMaker,AWSForecasting,DynamoDB aws
    class AzureGetNews,AzureGetPrice,AzureGetDecision,AzureTxtAnal,AzureAutoML,AzureBlobStorage azure
    class GeminiAI,GoogleNL,GCPBackup,FirestoreDB,GCS,GCPScheduler gcp
    class OracleDB,OracleFunction oracle
    class NewsScript,PriceScript,Dashboard,MochaCron1,MochaCron2 mochahost
    class PolygonAPI api
    class User user
```

## Overview

OptionsTrader is a multi-cloud stock options analysis application that leverages free tiers of AWS, Azure, Google Cloud, and Oracle Cloud to provide comprehensive market analysis and trading recommendations. The application collects news and price data, performs sentiment analysis using various AI services, and displays the results in an interactive dashboard.

## Key Features

- **Data Collection**: Automated collection of stock news and price history from Polygon.io API
- **AI-Powered Analysis**: Sentiment analysis using Google Gemini API, with backup options from AWS Comprehend and Azure Text Analytics
- **Multi-Cloud Storage**: Primary data storage in Oracle Cloud's Always Free JSON Database, with backups in Google Firestore and AWS DynamoDB
- **Serverless Computing**: API endpoints distributed across Azure Functions and AWS Lambda to stay within free tier limits
- **Automated Alerts**: Voice alerts for significant market movements using AWS Polly and SNS
- **Interactive Dashboard**: React-based frontend with Chart.js visualizations

## Cloud Resources Utilized

### AWS Free Tier
- Lambda for serverless functions
- S3 for media storage
- DynamoDB for backup/cache
- Comprehend for sentiment analysis
- Polly for voice alerts
- SNS for notifications
- CloudWatch for monitoring

### Azure Free Tier
- Azure Functions for API endpoints
- Cosmos DB for secondary database
- Blob Storage for backups
- Text Analytics for sentiment analysis
- Application Insights for monitoring

### Google Cloud Free Tier
- Cloud Functions for data processing
- Firestore for document storage
- Cloud Storage for archiving
- Natural Language API for sentiment analysis
- Cloud Scheduler for automation

### Oracle Cloud Free Tier
- Autonomous JSON Database for primary storage
- Cloud Functions for database maintenance

## Implementation Plan

The implementation is divided into several phases:

1. **Infrastructure Setup**: Setting up accounts and configuring free tier resources
2. **Data Collection**: Implementing scripts to gather news and price data
3. **Analysis Pipeline**: Setting up AI services for sentiment analysis
4. **API Layer**: Creating serverless functions to serve data
5. **Frontend**: Building the React-based dashboard
6. **Decision Engine**: Implementing the trading recommendation system
7. **Monitoring**: Setting up cross-cloud monitoring and alerting

For a detailed implementation plan, see [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md).

## Getting Started

To deploy this project, follow these steps:

1. Clone this repository
2. Set up accounts with AWS, Azure, Google Cloud, and Oracle Cloud
3. Follow the setup instructions in [SETUP.md](SETUP.md)
4. Deploy the application components as described in [DEPLOYMENT.md](DEPLOYMENT.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
