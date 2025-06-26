# TRANSFORMER FROM SCRATCH

## 1. INPUT EMBEDDINGS IN TRANSFORMER ( FIRST LAYER)

The input to transformers is essentially a sequence of tokens, each represented as one-hot-vectors. These vectors are subsequently multiplied by an embedding matrix (E) **Embedding matrix is an learned parameter during the training process,** Mathematically, this process can be represented as X = E * I where I stands for input one-hot vectors. 

## Data Flow of Transformer

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/97e68fe9-f6fb-4133-98df-906b051c49b4/image.png)

 A string (Input) is passed to a tokenizer which converts it to a numerical sequence that we call in the context of the transformers library **input_ids**. These are passed tot he embedding layer of the respective model to retrieve the **token_embedding** that are afterward used inside the attention layers to retrieve the **contextualized token embeddings**. 

Therefore, while the token embedding layer itself might simply be a lookup table, the combination of positional encoding and the attention mechanism allows contextual variations in word representations within a single sentence. This enables the model to capture the nuanced meaning of words based on their specific usage.

The Embedding layers takes two different arguments, vocab_size and d_model. The vocab_size refers to the number of unique tokens in the dataset whereas the d_model represents the dimension of the vector used for representing the word. 

E.g. d_model = 512, vocab_size = 20000

---

## 2. Positional Encoding

Embedding layers does creates the d_model-dimensional vector representation for each input token provided to it whose position needs to be conveyed to the model for getting the order of the tokens in an sentence after embedding process. Positional Encoding adds additional positional vector to solve the problem of orders of tokens in a sequence. Exponential decay is applied during positional encoding to scale them based on model dimension along with drop out for regularizing the positional encoding to prevent over fitting. Sine/Cosine functions ( sin for even positions and cos for odd position)  are used in transformer architecture but implementation of learnable positional encoding and no positional encoding in vision tasks due to convolution-like operations happens in that kind of deep learning task. 

### Buffer

Buffers are tensors, which are registered in the module and will thus be inside the state_dict.
These tensors do not require gradients and are thus not registered as parameters.
This is useful e.g. to track the mean and std in batchnorm layers etc. which should be stored and loaded using the state_dict of the module.One can still assign a Tensor as explicitly by using the **register_buffer()** function.

---

## 3. Layer Normalization

Layer Normalization is a method to normalize the inputs to a layer across its features (the last dimension of a tensor). This process helps in making the model’s training stable, efficient, and less sensitive to the choice of hyperparameters. The job of layer normalization is to treat **each row individually** and normalize the values within that row to have a **mean of 0** and a **standard deviation of 1**. 

The goal of the layer normalization is to standardize the input features to a layer so they have the **mean of zero and standard deviation of 1**. Features with large value and very smaller value will cause no conflict during the optimization process of learning for the architecture. In transformer the input to a layer is a tensor of shape **(batch_size, seq_len, d_model)** where 

- batch_size : Numbers of examples in a batch
- seq_len: Length of each sequence (no of tokens in a sentence)
- d_model: Feature dimension (embedding size of 512, 1024)

The last dimension contains the features of each token which are the learned representations of the token (embeddings). Three different values (eps, alpha and bias) are also introduced to the layer normalization for introducing the normalization to the learned input embeddings. Formula for layer normalization is given as, 

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/52898546-53e9-4b4f-8d59-843bd012414b/image.png)

---

## 4. Feed Forward Block

The feed forward block is the component of transformer architecture which introduce the concepts such as fully connected layers, expansion and compression of feature space and non-linearity for learning complex transformations. 

```python
class FeedForwardBlock(nn.Module):
    def __init__(self, d_model: int, d_ff: int, dropout: float) -> None:
        super().__init__()
        self.linear_1 = nn.Linear(d_model, d_ff) # W1 and B1
        self.dropout = nn.Dropout(dropout)
        self.linear_2 = nn.Linear(d_ff, d_model) # W2 and B2

    def forward(self, x):
        # (Batch, Seq_len, d_model) ---> (Batch, seq_len, d_ff) --> ( Batch, seq_len, d_model)
        return self.linear_2(self.dropout(torch.relu(self.linear_1(x))))
```

The first fully connected layer expands the feature dimension from **d_model** to **d_ff (intermediate size)** whereas the second fully connected layer in this block compresses the expanded features back to **d_model.** 

**d_ff** is higher-dimension space than the **d_model,** the larger space allow the model to capture the richer and more complex relationships among features. The compression occurs for maintaining the consistency in the size of the token representations throughout the Transformer layers. 

---

## Multi-Head Attention & Attention Mechanism

Multi-Head Attention is the most interesting and important part of transformer architecture, this is used in both encoder and decoder part of the transformer for attention mechanism.  Positional Encoding is used as the input for the multi-head attention layer and used for three times (query, key, values), its like a duplication of input for three times. 

Multi-head attention takes the input sequence (seq_len, d_model) and transforms it to three matrices [Q, K, V] of dimension (seq_len, d_model). These matrices are exactly the same as the input for encoder and slightly different for decoder. These three matrices are respectively multiplied by matrices of dimension (d_model, d_model).  [Wq, Wk, Wv] is the matrices used for multiplication. The multiplication results in new matrix [Q’, K’, V’] of dimension (seq_len, d_model), which are then split into H matrices where H means number of heads.**They are splitted across the embedding dimension not along the sequence dimension.**  

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/41fb8e9e-8304-4e10-81af-57c3ce2d7791/image.png)

Attention is applied to the smaller matrices which provides smaller molar  matrices as the result then those matrices are concatenated (combined) and then finally multiplied by **Wo** to get multi-head attention output which again is a matrix with the same dimension as the input matrix.   

---

## 5. Residual Connection

---

---

---

## How Transformers Works?

 Word Embedding is used for converting words into numbers for neural network architecture. It is relatively simple neural network that has one input for every word and symbol in the vocabulary that you want to use. The text is fragmented using special characters like <EOS> which stands for end of sequence. 

![image.png](attachment:fdec2708-7645-4680-97e0-7d6c1ca94604:image.png)

The vocabulary can be mix of words, word fragments and those fragments are called tokens. Inputs are connected to activation functions and each connection multiplies the input value by weight. The weights are multiplied with the input value for the each individual words and passed through activation function to provide the output (numbers) which is the representation of that words in embedding space. 

In practice, often hundreds and thousands of embedding values are used per word. 

Each weights in neural network is randomly generated/used which is tweaked by back propagation through an iterative correction process. This results in final weights which can be used for prediction.

The process of optimizing the weights is called Training.

For dealing with order of the words in sentence for correct meaning positional encoding set the numbers that correspond to word order to the embedding values for each word. 

![image.png](attachment:c474df30-068e-448b-a913-d2bb1e87a168:image.png)

The numbers that represents the word order comes from a sequence of **alternating Sine and Cosine squiggles.**

![image.png](attachment:6014152e-8fa2-4343-ab22-3f0378138426:image.png)

Each squiggle gives specific position values for each word’s embeddings. Because the Sine and Cosine squiggles are repetitive, it’s  possible that two words might get the same position, or y-axis value.  

The more embedding values we have, the squiggles get proportionately wider. Due to this even with a repetitive value here and there, we obtain unique sequence of position values for each word.

Finally the embedding values are summed with the encoding values to create a whole sentence. 

![image.png](attachment:232f686e-3e8c-4478-983f-ed5d7101e948:image.png)

### How Transformer Keeps Track of Relationship Among Words?

Example: 

![image.png](attachment:fd38f800-7864-4b5c-98f0-7624a3ce8b7f:image.png)

Transformer have self-attention,which is a mechanism to correctly associate the word ‘it’ with the word ‘pizza’.

Self-Attention works by seeing how similar each word is to all of the words in the sentence, including itself.  

For example: Self-Attention calculates the similarity between the first word, **The,** and all of the words in the sentence. 

![image.png](attachment:ff798917-416d-4918-822f-e90f4fdc9ebc:image.png)

Self-Attention calculates these similarities for every word in the sentence. 

![image.png](attachment:4db227c6-a6e9-4032-bd28-bc39d34f7d3e:image.png)

Once the similarities are calculated, they are used to determine how the Transformer encodes each word.

### How Transformer Encodes the Text?

The positional-encoding + embedding values and produce **Query Value** for each words and calculates the similarity between itself and the respective word. 

How does the similarity calculated?

![image.png](attachment:be510fca-894a-480e-8567-d35b7160a0d8:image.png)

The key value ( the same query value but for the different words) called Key Value. Then the similarity between the **query** and **keys** by calculating the **Dot Product** between them. 

![Dot Product calculation for word Let’s](attachment:31595dc0-1a1e-4a6f-80b8-cda901fd7858:image.png)

Dot Product calculation for word Let’s

The values are first multiplied in pair and then added together. The higher the value better the similarity exist between the words. 

Having greater similarity score will have more influence on its encoding as compared to lesser word with less similarity score. This is done by passing the similarity scores through **SoftMax** function. 

The main idea of softmax function is that it preserves the order of the input values, from low to high, and translates them into numbers between zero and 1 that add up to 1. 

Output of the SoftMax determine what percentage of each input word we should use to encode the word. 

The softmax function is critical in determining the significance of input words, ensuring that more relevant words have greater influence on the resulting encoding.

Transformers utilize shared weights for calculating self-attention across different inputs, which enhances efficiency and simplifies the computation process. This method allows for parallel processing of queries, keys, and values.

**Process for Calculating Self-Attention for a Target Word (e.g., "Word A"):**

1. **Similarity & Scaling:**
    - For the target word ("Word A"), calculate its similarity to *every* word in the sequence (including itself).
    - Retrieve the "value" representation/vector associated with *each* word in the sequence.
    - Scale the "value" vector of each word based on its calculated similarity *to the target word ("Word A")*.
        - *Result:* Words more similar to "Word A" will have their "value" vectors scaled higher; less similar words will have theirs scaled lower.
2. **Summing:**
    - Sum (add together) all the *scaled* "value" vectors from every word in the sequence.
        - `SelfAttention(Word A) = Sum [ ScaledValue(Word_i) ] for all words i in the sequence.`
    - This final sum is the self-attention value (the updated, context-aware representation) specifically for "Word A".

**Process for Other Words in the Sequence (e.g., "Word B", "Word C", ...):**

1. **Repeat:**
    - The entire process (Steps 1 & 2) is repeated independently for *each* word in the input sequence.
    - When calculating for "Word B," the similarities are calculated *relative to Word B*, new scaling factors are determined based on those similarities, and the scaled values are summed to get the self-attention value for "Word B."
    - This continues until every word has its own updated self-attention representation.

**Key Takeaway:** Self-attention allows the model to weigh the influence of different words in a sequence when representing a specific word, based purely on the relationships learned from the data (captured as similarities). This creates richer, context-dependent word representations.

The paper “Attention is all you need’ stacked 8 Self-Attention cells and called it Multi-Head Attention. 

The position encoded value is added with self-attention value to get the final encoding of the input from Transformer. 

Residual Connection are the bypasses and allow the self-attention layer to establish relationship among input words without having to also preserve Word Embedding and Position Encoding information. 

These four features allow the Transformer to encode words into numbers, encode the positions of the words, encode the relationship among the words and relatively easily and quickly train in parallel.

- Word Embedding
- Positional Encoding
- Self-Attention
- Residual Connections

![image.png](attachment:c2caf10e-08b9-4c7c-9e77-61de30d84bcf:image.png)

Transformer consists of two parts Encoder and Decoder. Above notes explain the  working mechanism of it, the decoder in the other hand create embedding values for output vocabulary which consists of output words. 

The <EOS> token is used first to start the decoding because that is a common way to initialize the process of decoding the encoded input sentence. Same steps happens for output data in decoder of the transformer. 

The sets of Weights we used to calculate the Decoder’s Self-Attention Query, Key and Value are different from the sets we used in Encoder. 

The main idea of Encoder-Decoder Attention is to allow the Decoder to keep track of significant words in the input. 

![image.png](attachment:4daf01eb-93f6-4ea7-9942-35cf7537e65f:image.png)

The similarity between the token from Decoder and the Encoder are calculated using the dot product just like before then the similarities are ran through a SoftMax function which tells us which word should be used as the next word. 

Encoder-Decoder Attention Values are calculated in same way they are calculated in Encoder.