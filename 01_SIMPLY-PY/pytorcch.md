# PyTorch 

Deep learning is inspired by how human brain learns where neuron of brain resembles neural networks.

PyTorch is a deep learning framework. Meta AI originally developed, later moved under Linux Foundation. 

Fundamental datastructure in PyTorch is tensor which is similar to array. created using python list or array

Deep learning perform addition and multiplication to process data and learn patterns. 

1. torch.tensor for creating tensor from python list.
2. torch.dtype for finding the datatype of the tensor
3. torch.shape for finding the shape of the tensor. 
4. torch.nn module is used for creating neural networks
5. number of input neurons is equals to the features from the [datase](http://datase.tr)t
6. number of neurons in output layers is equals to the number of classes. 
7. nn.Linear creates linear layer which makes the predictions. it takes two arguments. input features and desired size of output features/classes.  when input is passed through linear layer, linear operations is performed to include weight and biases. each linear have associated weight and biases. they are the key quantities that defines a neuron.  weights reflects the importance of  different features. whereas the bias is independent to the weight of the neuron 
8. stacking the layers in sequence is nn. Sequential(), this network takes input, passes it to each linear layer in sequence and output. layers inside the Sequential() are hidden layers. 
9. increasing the number of hidden layers increases the number of model parameters leading to higher model capacity. 
10. .numel() method returns the number of elements in the tensor. 
11. number of parameters is calculated by adding the weights and bias per output. Linear(9,4): weights=9x4=36, bias = 4 (one bias per output i.e. 4 in this case) total layer in this layer: 40. 
12. non-linearity is added to the network using activation function.sigmoid is used for binary classification and softmax is used for multi-class classification. 
13. pre-activation output is passed to activation function. nn.Sigmod() creates the layer and the layer itself takes the input_tensor as a input parameter. activation function is added as the last layer of the Sequential model. sigmoid layer is equivalent to logistic regression in classical machine learning. adding more layers and activations unlocks the true power of deep learning. 
14. activation function generates the output of the same shape of the input it takes. (dimension). nn.Softmax is used for creating the softmax activation layer with the input of dimension which means which part of tensor is passed with activation function.  it provides the probabilities for all the input tensor which sums to one.  
15. the purpose of the forward pass is to pass ipnut data through the network and produce predictions or output based on the model’s learned parameters or weights and biases.