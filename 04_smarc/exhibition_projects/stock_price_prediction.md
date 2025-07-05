# STOCK PRICE PREDICTION (PREDICTION AND ANALYSIS)


### model prediction 
    Next day’s Close price (Predicting the exact closing price for next day) (prediction)
    Price movement direction (up/down) (classification)

With Open, High, Low, Close, Percent Change, and Volume is sufficient to compute a wide range of technical indicators like MACD, Bollinger Bands, RSI, Momentum, and more. Adding these derived features will enrich model’s input space and likely enhance prediction performance.


LSTM/DECISION TREE, DATA AUGMENTATION (if possible)

VERY SMALL LLM FOR ANALYSIS AND DESCRITION (OPTIONAL)


chrono-bolts model requires dataset in following format: 

1. item_id (name of company alternatively [symbol])
2. timestamp (date in this format [yyyy-mm-dd], iso format)
3. target (closing price) (opening, high, low is not required)

need to merge the dataset of all companies into single dataset where the item_id will be the unique identifier for each stock's prices. 

chrono-bolts models are provided by amazon and have been pre-trained with around 100 billions time-series data and very good at zero-shot prediction as well. 

prophet(facebook ai research), time series forecasting [for forecasting time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects]
    

    process:

    rename the timestamp as ds
    rename the closing price as y

    code:
    

    (ai_env) (base) graahand@transformer:~/stock-price$ /home/graahand/miniconda3/envs/ai_env/bin/python /home/graahand/stock-price/train_bank.py
    17:29:26 - cmdstanpy - INFO - Chain [1] start processing
    17:29:26 - cmdstanpy - INFO - Chain [1] done processing
                ds        yhat  yhat_lower  yhat_upper
    1173 2025-07-04  330.130748  311.546719  348.559135
    1174 2025-07-05  346.993727  328.633787  365.069220
    1175 2025-07-06  337.967802  319.021428  357.471327
    1176 2025-07-07  339.004586  321.843562  355.282978
    1177 2025-07-08  341.688903  324.074562  360.082234