# MoneyTalks

Get predictions of future stock prices. Have those predictions explained to you in natural language and with a degree of confidence. 

Read [report](report.pdf) for more info.

## Running

In the project root folder:

```
docker-compose up --build
```

Website available at ```http://localhost:5173/```

## Features

### See at a glance how the stock market will fare!

![recommendations_page](https://github.com/user-attachments/assets/e994d064-4261-40d3-9e6e-30b9024e62f2)

Each prediction is based on past stock prices (retrieved from the Macrotrends website) and financial data (from the SEC's EDGAR API).

### Get a detailed explanaition for a predicition

![prediction_page](https://github.com/user-attachments/assets/f6811a35-8da7-40b3-b561-7d73f9ad07dd)

For each prediction it makes, our model returns the datapoints that most influenced its decision. We provide these datapoints, to the ChatGPT AI in the form of a prompt engineered. ChatGPT then represents our data in the form of natural language. 
