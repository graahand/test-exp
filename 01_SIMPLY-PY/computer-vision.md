# COMPUTER VISION

```python
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
```

First tuple is mean for the RGB color channel whereas the second tuple is standard deviation, each values ranges from (0,1) and (-1,1). This ensure the pixel values are centered around 0 and have a standard deviation of 1 after normalization. Improves training stability and model learning convergence. 

**Formula**

```python
normalized_value = (original_value - mean) / std
```

**Before Normalization**

```python
[[[0.0, 0.5, 1.0],
  [0.2, 0.7, 0.9]],
 [[0.1, 0.6, 0.8],
  [0.3, 0.4, 0.5]]]
```

**After Normalization**

```python
[[[-1.0, 0.0, 1.0],
  [-0.6, 0.4, 0.8]],
 [[-0.8, 0.2, 0.6],
  [-0.4, -0.2, 0.0]]]
```

---

---

---

# Image Captioning

***https://readmedium.com/image-caption-model-from-scratch-vit-gpt-94afaae30fb7***

1. patch_size: This variable determines the patch size used in the ViT component. The patch size is the size of the small image patches that are used as input to the ViT model. Here, the patch size is 16x16 pixels.
2. d_model_vit: This variable determines the dimensionality of the output embedding from the ViT component. It is calculated as the product of the patch size and the number of color channels.
3. num_patches: This variable determines the number of patches in the input image. It is calculated by dividing the image size by the patch size.
4. softmax_denom_eps: This variable determines a small value added to the denominator of the softmax function to prevent division by zero.

## Patch Embeddings

Patch Embedding is a technique used in computer vision to convert an image into a format that can be fed into a neural network.

Imagine an image is made up of small, non-overlapping squares called patches. Each patch is a small portion of the image, and it can be thought of as a tiny, independent image.

The Patch Embedding process involves:

- **Dividing the image into patches:** The image is divided into a grid of patches, where each patch is a small square portion of the image.
- **Representing each patch as a vector**: Each patch is represented as a vector, which is a list of numbers that describe the patch's color and texture.
- **Flattening the patch vectors:** The patch vectors are flattened into a long, one-dimensional list of numbers.

In Vision Transformers (ViT), Patch Embedding is used to convert the input image into a sequence of patch embeddings, which are then fed into the transformer network. The transformer network processes the patch embeddings in parallel, allowing it to learn global features and relationships in the image.

**PatchEmbeddings class**

The `PatchEmbeddings` class is responsible for creating the patches of an image using a convolutional layer. Here's a step-by-step explanation:

1. **Convolutional layer**: The class uses a convolutional layer (`nn.Conv2d`) to create the patches of the image. The convolutional layer takes the input image and applies a filter to it, resulting in a feature map.
2. **Flatten**: The feature map is then flattened using the `nn.Flatten` layer, which converts the 3D feature map into a 2D tensor.
3. **Permute**: The flattened tensor is then permuted using the `permute` method, which rearranges the dimensions of the tensor. The resulting tensor has shape `(B, N, D_MODEL)`, where `B` is the batch size, `N` is the number of patches, and `D_MODEL` is the dimensionality of the patch embeddings.

```jsx
self.conv_patch_layer = nn.Conv2d(in_channels=config['channels'],
                                  out_channels=config['d_model'],
                                  kernel_size=config['patch_size'],
                                  stride=config['patch_size'])
```

**ViTEmbedding class**

The `ViTEmbedding` class creates the input embeddings for the ViT model by combining both patch and positional embeddings. Here's how it works:

1. **Class token embedding**: The class token embedding is a learnable parameter that represents the class token. The class token is a special token that is used to represent the entire image.
    1. **Positional embedding**: The positional embedding is a learnable parameter that represents the position of each patch in the image. The positional embedding is used to capture the spatial relationships between patches.
    2. **Patch embeddings layer**: The `PatchEmbeddings` class is used to create the patch embeddings from the input image.
    3. **Dropout**: The patch embeddings are then passed through a dropout layer, which randomly sets a fraction of the output elements to zero during training.
    4. **Add positional embedding**: The patch embeddings with class token are then added to the positional embedding, resulting in the final input embeddings for the ViT model.

## Creating Patch Embeddings using Convolutional Layers

Patch embeddings are created using a two-dimensional convolutional layer. This might seem surprising, as many people think that patch embeddings are created by simply dividing an image into patches and flattening them.

### Why Convolutional Layers?

However, using convolutional layers to create patch embeddings has several advantages:

1. Computational Efficiency: Convolutional layers are highly optimized and come pre-built with deep learning libraries like PyTorch and TensorFlow. This means that they can be used efficiently and effectively, without the need to implement custom patch embedding code.
2. Capturing Different Information: Convolutional layers can capture different types of information from the image, such as edges, textures, and patterns. This is because they are designed to extract features from images, which is exactly what we need to create patch embeddings.

**How it Works**

Here's a step-by-step explanation of how patch embeddings are created using convolutional layers:

1. **Convolutional Layer**: A 2D convolutional layer is applied to the input image. This layer extracts features from the image, such as edges and textures.
2. **Feature Maps**: The convolutional layer produces a feature map, which is a 2D array of values that represent the features extracted from the image.
3. **Flattening**: The feature map is then flattened into a 1D array, which represents the patch embeddings.
4. **Classification Token**: The classification token is appended to the front of the patch embeddings, which represents the entire image.

## Normalization

In reality, the mean of 0 and a standard deviation of 1 are mathematical concepts that are used to normalize the input data. Here's what it means in simple terms:

**Mean of 0**

Imagine you have a dataset of exam scores, and the average score is 80. If you subtract 80 from each score, you get a new set of scores that have a mean of 0. This means that the scores are centered around 0, and there is no longer an overall bias or shift in the data.

In the context of neural networks, normalizing the input data to have a mean of 0 helps to:

- Reduce the effect of outliers or extreme values
- Improve the stability of the model
- Enhance the accuracy of the model

**Standard Deviation of 1**

The standard deviation is a measure of how spread out the data is. If the standard deviation is 1, it means that the data points are relatively close to the mean, and there is not a lot of variation in the data.

In the context of neural networks, normalizing the input data to have a standard deviation of 1 helps to:

- Improve the convergence of the model during training
- Enhance the interpretability of the model
- Reduce the risk of overfitting