# STOCK PRICE PREDICTION: V2

**Stock Price Prediction Pitch (Simplest Form)**

- Stock Price Prediction is the project based on deep learning and transformer architecture for the prediction of the stock’s prices of various companies based on the historical price’s data of those companies from 2019 to October 2024.
- This system utilizes the historical data of the stock’s prices of 9 different banks of Nepal for the training of the AI model for the prediction.
- The dataset for this project was created by merging the dataset of all different companies' data used along with the differentiation between them using the appropriate symbol.
- The deep learning model used for this project is trained for 80 epochs with large volume of stock’s data.
- The accuracy obtained for the trained model is about 70 percent.
- The model can predict the stock prices of the companies based on the last 30 day’s stock data.
- The Stock Price Prediction system can be accessed using following link: [StockPricePrediction.](https://stock-price-prediction.skillmuseum.org/)
- Additionally, this project utilizes the intuitive user interface for selecting appropriate bank for the prediction, dropping the CSV file as the input for the prediction along with the analysis and tweaking of the predicted stock’s graph.
- The user/student can easily access the Stock Price Prediction system using the above link and select the appropriate bank for the prediction process followed by selection of the CSV file containing the stock’s price of last 30 days. Click on the Submit button after selecting the bank’s name and the CSV file, the prediction page with the stock’s prices in the graph along with the table for each day will be displayed.
- This project unleashes the power of transformer architecture to capture the dependency and the trend of the stock’s prices using the concept called attention mechanism and residual connection for the prediction of stock’s prices.
- This project can be further improved by implementing Genetic Algorithm with DEAP programming for fine-tuning the hyperparameters of Transformer architecture.

**Project Specification**

Stock Price Prediction utilizes the Django framework for back-end development along with some intuitive user interface using the Django templates available for front-end. The back-end of this project merges the **Prediction Model** efficiently to allow the users to predict the stock’s prices correctly. The model takes the name of the company and the 30 days' worth stock’s prices in CSV format as the parameters and predict the stock prices based on the training samples and learned weights by the model during its intensive training to provide the predicted 14 day (about 2 weeks)’s stock’s prices as the output.

## Reference Papers & Links

https://blog.bbelyakov.com/stock-price-forecasting-with-lag-llama-transformers-2d6ada22a088

[lag_llama.pdf](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/1e51b9a0-5c2e-4991-9ec9-7acce97be769/lag_llama.pdf)

Understanding RNN and LSTM

Humans don’t start their thinking from scratch every second. As you read this essay, you understand each word based on your understanding of previous words. You don’t throw everything away and start thinking from scratch again(https://colah.github.io/posts/2015-08-Understanding-LSTMs/). 

Traditional Neural Network can not do this which is the major shortcoming for the sequential and temporal data. RNN addresses this issue by integrating loops in the networks allowing the information to persist. 

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/e2fc9aff-7599-4c43-98f4-46590afb37ea/image.png)

The chain-like structure of RNNs made possible to capture the sequential and temporal dependencies for the tasks like speech recognition, speech recognition, language modelling, image captioning and so on. RNNs are effective for such cases where the gap between the relevant information and the place that it’s needed is small, RNNs can learn to use the past information. For example, completing the sentence “THE CLOUDS ARE IN THE *SKY”.* 

For the cases where we need more context, RNNs become unable to learn to connect the information due to which LSTM networks are used. Long Short Term  Memory are explicitly designed to avoid the long-term dependency problem. Remembering information for long periods of time is practically their default behavior, not something they struggle to learn. 

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/d0323ff8-3649-46dd-9e66-5c9cfd94efde/image.png)

**The repeating module in an LSTM contains four interacting layers.** 

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/707ef6b6-50d3-43b0-8d2c-9aaa8c869aab/image.png)

**Layers of LSTM networks**

The key to LSTM  is the cell state, the horizontal line running the top of the diagram. The cell state is like a conveyor belt. It runs down the entire chain, with only some minor linear interactions. It’s very easy for information to just flow along it unchanged. 

The LSTM does have the ability to remove or add information to the cell state, carefully regulated by structures called **gates.** Gates are the way to optimally let information through. They are composed out of sigmoid activation layer and point-wise multiplication operation(multiplying corresponding elements of two vectors or matrices).

The sigmoid layer outputs numbers between zero and one, describing how much of each component should be let through. An LSTM has three gates (forget gate, input gate, output gate), to protect and control the cell state. 

### Analogy to understand the LSTM working mechanism

Let’s say you’re looking at reviews online to determine if you want to buy Mac-book (don’t ask me why). You’ll first read the review then determine if someone thought it was good or if it was bad.

When you read the review, your brain subconsciously only remembers important keywords. You pick up words like “good battery”, “high performance”, and “worth buying”. You don’t care much for words like “this”, “gave“, “all”, “should”, etc. If a friend asks you the next day what the review said, you probably wouldn’t remember it word for word. You might remember the main points though like “worth buying”. If you’re a lot like me, the other words will fade away from memory.

And that is essentially what an  LSTM does. It can learn to keep only relevant information to make predictions, and forget non relevant data. In this case, the words you remembered made you judge that it was good.

### Summary of LSTM Working Mechanism

### Step-by-Step Mechanism of LSTM

**1. Forget Gate**

The first step in an LSTM is to decide what information to discard from the cell state. This is done using a sigmoid layer called the “forget gate,” which takes ht−1h_{t-1} (previous hidden state) and xtx_t (current input). It outputs a value between 0 and 1 for each element in Ct−1C_{t-1} (previous cell state), where 1 means “keep completely” and 0 means “forget entirely.” For example, in a language model, this step might forget the gender of a previous subject when encountering a new subject.

**2. Input Gate**

Next, we determine what new information to store in the cell state. A sigmoid layer (input gate) decides which values to update, while a tanh layer generates new candidate values C~t\tilde{C}_t. These are combined to create the update. For instance, the gender of the new subject might be added to replace the old one.

**3. Cell State Update**

The old cell state Ct−1C_{t-1} is updated to CtC_t. First, the old state is multiplied by ftf_t (forget gate output) to forget selected information. Then, it⋅C~ti_t \cdot \tilde{C}_t (input gate scaled candidates) is added. This step finalizes forgetting the old subject’s gender and incorporating the new one.

**4. Output Gate**

Finally, the output is computed based on the updated cell state CtC_t. A sigmoid layer decides which parts of CtC_t to output. The cell state is passed through tanh to scale values between −1 and 1, and the result is multiplied by the sigmoid gate output. For a language model, this output might include information like singular/plural, to help predict the next word correctly.

### RNN Cell

![1_WMnFSJHzOloFlJHU6fVN-g.gif](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/8bc25a44-cb17-44f7-9d10-e1010c8818d2/1_WMnFSJHzOloFlJHU6fVN-g.gif)

### Vector Transformation without Hyperbolic Tangent (tanh) and with tanh