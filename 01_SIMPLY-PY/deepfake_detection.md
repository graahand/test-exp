# DEEPFAKE DETECTION

Deepfake is a technology dedicated to creating highly realistic facial images and videos under specific conditions, which has significant application potential in fields such as entertainment, movie production and digital human creation.  In addition to deepfake generation, corresponding deepfake detection technology continuously evolve to regulate the potential misuse of deepfakes, such as privacy invasion and phishing attacks.

As deepfakes become realistic and widespread around the social media, it becomes harder to identify the authenticity of all kind of information sources. The manipulation of content, such as photography or audio, also raises the ethical issues around the consent. 

## How are Deepfakes Made?

There are two different ways to create the deepfakes images, videos and audios. They are listed below: 

1. Generative Adversarial Networks
2. Diffusion Models

1. GAN (Generative Adversarial Networks) : GAN is composed of two models that play a game against each other. The first model, the generator either selects the image or video, or generate the fake one. The second model, the discriminator, decides whether the image or video is real or fake. The generator win the game if the discriminator, decides whether the image or video is real or fake. The generator wins the game if the discriminator can’t tell that a generate content is fake. Playing this game over and over trains the generator to generate the realistic content, whilst improving this game over discriminator’s ability to guess correctly whether the content is real. 
2. Diffusion Models: A diffusion model  is trained to restore an image or video to its original state after visual ‘noise’ had been added. Some diffusion models are trained with guidance such as text prompts encouraging them to generate particular images, whilst others try to decide what the likeliest output will be on their own. The resultant models can ‘inpaint’ missing patches in an image, filling the gaps with something plausible. Model such as Stable Diffusion and DALL-E 2 are both examples of diffusion models that take text prompts as part of their input. Diffusion models are newer than GANs and likely to become more prominent in deepfake generation as they are believed to be easier for train than GANs. 

### Deepfake Detection

Deepfakes are becoming increasingly hard to detect due to the advancement in the generative AI methods for creating deepfakes. There are several ways that the images, videos and audio can be classified as deepfake based on the spatial and visual inconsistencies contained by the deepfake contents. Video and audio deepfakes can be given away by time-based inconsistencies, such as mismatch between speech and mouth movements. Deepfake generation methods such as GANs and diffusion models can also leave detectable ‘fingerprints’ within the pixels of images or videos. 

Deep fake detection opensource projects

1. **Faceswap.dev**
2. https://github.com/shaoanlu/faceswap-GAN; Face tracking/alignment using MTCNN and kalman filter in video conversion

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/aee735a5-eac4-4d5e-b899-fc378944231e/image.png)

1. https://www.youtube.com/watch?v=x2g48Q2I2ZQ
2. https://github.com/Billy1900/Awesome-DeepFake-Learning?tab=readme-ov-file#3-curated-lists

**spatio-temporal action recognition**

https://www.creativebloq.com/features/deepfake-examples

https://github.com/jacobgil/pytorch-grad-cam

https://typeset.io/

# Classification Model Neural Architecture with PyTorch.

Recent evidence shows that the network The effect of depth on network performance is critical, and the main results on the challenging ImageNet dataset all employ very deep models, ranging from 16 to 30 layers deep (https://arxiv.org/pdf/2208.08231).

However,the first obstacle to this problem is the infamous gradient vanishing and gradient exploding problems, which hinder the convergence of the network. Later, researchers found that this problem can be alleviated by normalizing the input data and batch normalization, which is generally not a problem for a dozen-layer network.

Simply stacking the network to increase the depth of the network does not improve
the performance of the network. He et al. call this phenomenon the degradation problem,
which shows that not all systems are easy to optimize(He et al.).

## Inception-ResNetv1

The Inception-Resnet v1 is a hybrid network inspired by inception and the performance of resnet. There are two different versions of the Inception-Resnet, V1 and V2, where V2 being comparatively  producing higher computational cost. 

The Inception-Resnet incorporates the use of 3 different stem modules and reduction blocks. The output of Inception module is added to the input. 

![Schematic for Inception-ResNet v1 AND v2  Network](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/2ebf2ce2-dad3-44ff-8636-6a14f3106f02/image.png)

Schematic for Inception-ResNet v1 AND v2  Network

The dimension of the output from the inception module and the input from the previous layer must have same dimension without any alteration. Factorization of the convolutions filters become much more important to match these dimensions. However, further studies shows that the network dies when the convolutions filters exceeds 1000(https://iq.opengenus.org/inception-resnet-v1/). This  problem was later solved by introducing the concept called Activation Scaling. 

![    Inception-ResNetv1](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/b35538f6-71c4-4e6d-b27a-5487e8f42699/image.png)

    Inception-ResNetv1

![Inception-ResNetv2](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/477b6378-9d9e-410a-9571-75f7653e5e42/image.png)

Inception-ResNetv2

# LSTM (Long Short Term Memory)

## Video Vision Transformer for Video Classification

The VivitForVideoClassification class in Hugging Face Transformers library provides a PyTorch implementation of the Video Vision Transformer specifically designed for video classification. This class requires a VivitConfig object, which contains all the necessary parameters for the model’s architecture and operation. When initializing the model with the configuration, it only load the structural details of the models instead of the model’s weights. For loading the model’s weights, the **from_pretrained()** method need to be implemented. 

The ViViT model is a powerful architecture for video classification. It processes video frames as sequences of patches. Classification head is attached on top of  the model. It also supports the fine-tuning process by enabling **interpolate_pos_encoding,** which adjusts position embeddings for new resolutions. This allows leveraging pre-trained weights effectively on different datasets like **Kinetics-400.** 

The forward function contains the parameters such as **pixel_values, head_mask, output_attentions, output_hidden_states, interpolate_pos_encoding, return_dict, labels.** 

```python
import torch
from transformers import VivitModel, VivitImageProcessor

model = VivitModel.from_pretrained("google/vivit-base")
processor = VivitImageProcessor.from_pretrained("google/vivit-base")
images = ["image1.png", "image2.png"]  # Example images
inputs = processor(images, return_tensors="pt", padding=True)
head_mask = None  # No masking of attention heads
labels = torch.tensor([0, 1])  # Example ground truth labels
output_attentions = False
output_hidden_states = False
interpolate_pos_encoding = True
return_dict = True

#forward pass
outputs = model.forward(
    pixel_values=inputs.pixel_values,
    head_mask=head_mask,
    labels=labels,
    output_attentions=output_attentions,
    output_hidden_states=output_hidden_states,
    interpolate_pos_encoding=interpolate_pos_encoding,
    return_dict=return_dict,
)

if labels is not None:
    loss = outputs.loss  # Cross-entropy or MSE loss
logits = outputs.logits  # Classification scores

print("Model outputs:", logits)
if labels is not None:
    print("Loss:", loss)

```

### Logits in PyTorch

The raw outputs from the output layer of the neural network are called logits which are also known as activations. Deep learning networks at the core are made up of matrices multiplication and non-linearities like ReLU, these logits can range from **(-R,R)** where **R** represents real numbers. These logits can not be interpreted as model scores due to which activations are applied to them before getting the final score. 

### Init and Forward Method in PyTorch

```python
class MyNeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(MyNeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.sigmoid(out)
        return out
```

**init** is a constructor method used to initialize the parameters of the network. It is executed when an object of the class is created. For example, in PyTorch, this method is used to define the layers of the network, such as convolutional layers, linear layers, activation functions, etc. **forward** is a method that defines the forward pass of the neural network. This method takes the input data and passes it through the layers of the network to produce the output. This method is executed whenever the model is called to make prediction or to compute the loss during training. 

In other words, **init** sets up the network by defining the layers while forward specifies the data flows through the network. Both methods are required to create a neural network in PyTorch and serve different purposes. 

# Model Training on Celebs Dataset

```python
""" """
import os
import cv2
import torch
import numpy as np
from torch import nn
from torchvision import transforms
"""Transforms are common image transformations. They can be chained together using
		Compose. There is also a functional module for transform which provides the 
		fine-grained control over transformations."""
		
from torch.utils.data import Dataset, DataLoader
"""
"""
from facenet_pytorch import InceptionResnetV1
from PIL import Image

class VideoDataset(Dataset):
    def __init__(self, folder_paths, frame_count=20, transform=None):
        self.frame_count = frame_count
        self.transform = transform
        self.videos = []
        self.labels = []
       
        # Process real celebrity videos
        for video_file in os.listdir(folder_paths[0]):
            if video_file.endswith(('.mp4')):
                self.videos.append(os.path.join(folder_paths[0], video_file))
                self.labels.append(0)  # Real
               
        # Process fake celebrity videos
        for video_file in os.listdir(folder_paths[1]):
            if video_file.endswith(('.mp4')):
                self.videos.append(os.path.join(folder_paths[1], video_file))
                self.labels.append(1)  # Fake
               
        # Process YouTube real videos
        for video_file in os.listdir(folder_paths[2]):
            if video_file.endswith(('.mp4')):
                self.videos.append(os.path.join(folder_paths[2], video_file))
                self.labels.append(0)  # Real
   
    def extract_frames(self, video_path):
        frames = []
        cap = cv2.VideoCapture(video_path)
       
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        interval = max(total_frames // self.frame_count, 1)
       
        frame_counter = 0
        while len(frames) < self.frame_count and frame_counter < total_frames:
            ret, frame = cap.read()
            if not ret:
                break
               
            if frame_counter % interval == 0:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                if self.transform:
                    frame = self.transform(frame)
                frames.append(frame)
               
            frame_counter += 1
           
        cap.release()
       
        # Pad sequence if necessary
        while len(frames) < self.frame_count:
            frames.append(torch.zeros_like(frames[0]))
           
        return torch.stack(frames)
   
    def __len__(self):
        return len(self.videos)
   
    def __getitem__(self, idx):
        video_path = self.videos[idx]
        frames = self.extract_frames(video_path)
        label = self.labels[idx]
        return frames, torch.tensor(label, dtype=torch.float32)

class DeepFakeDetector(nn.Module):
    def __init__(self, frame_count=20, hidden_size=512):
        super(DeepFakeDetector, self).__init__()
       
        # Load pretrained InceptionResNetV1
        self.feature_extractor = InceptionResnetV1(pretrained='vggface2')
        # Freeze feature extractor parameters
        for param in self.feature_extractor.parameters():
            param.requires_grad = False
           
        # LSTM for sequence processing
        self.lstm = nn.LSTM(
            input_size=512,  # InceptionResNetV1 output size
            hidden_size=hidden_size,
            num_layers=2,
            batch_first=True,
            dropout=0.5
        )
       
        # Final classification layers
        self.classifier = nn.Sequential(
            nn.Linear(hidden_size, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )
       
    def forward(self, x):
        batch_size, seq_len, c, h, w = x.size()
       
        # Reshape for feature extraction
        x = x.view(-1, c, h, w)
       
        # Extract features
        features = self.feature_extractor(x)
       
        # Reshape for LSTM
        features = features.view(batch_size, seq_len, -1)
       
        # Process with LSTM
        lstm_out, _ = self.lstm(features)
       
        # Use last LSTM output
        lstm_out = lstm_out[:, -1, :]
       
        # Final classification
        output = self.classifier(lstm_out)
        return output

def train_model(model, train_loader, val_loader, epochs=50, device='cuda'):
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters())
   
    model = model.to(device)
    best_val_loss = float('inf')
   
    for epoch in range(epochs):
        # Training phase
        model.train()
        train_loss = 0
        for frames, labels in train_loader:
            frames, labels = frames.to(device), labels.to(device)
           
            optimizer.zero_grad()
            outputs = model(frames)
            loss = criterion(outputs.squeeze(), labels)
           
            loss.backward()
            optimizer.step()
           
            train_loss += loss.item()
           
        # Validation phase
        model.eval()
        val_loss = 0
        correct = 0
        total = 0
       
        with torch.no_grad():
            for frames, labels in val_loader:
                frames, labels = frames.to(device), labels.to(device)
                outputs = model(frames)
                loss = criterion(outputs.squeeze(), labels)
                val_loss += loss.item()
               
                predicted = (outputs.squeeze() > 0.5).float()
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
       
        train_loss /= len(train_loader)
        val_loss /= len(val_loader)
        accuracy = 100 * correct / total
       
        print(f'Epoch {epoch+1}/{epochs}:')
        print(f'Training Loss: {train_loss:.4f}')
        print(f'Validation Loss: {val_loss:.4f}')
        print(f'Validation Accuracy: {accuracy:.2f}%')
       
        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), 'best_model.pth')

# Example usage
def main():
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)
   
    # Define transforms
    transform = transforms.Compose([
        transforms.Resize((160, 160)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])
   
    # Create datasets
    folder_paths = [
        'datasets/Celeb-real',
        'datasets/Celeb-synthesis',
        'datasets/YouTube-real'
    ]
   
    # Create full dataset
    dataset = VideoDataset(folder_paths, frame_count=20, transform=transform)
   
    # Split dataset
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(
        dataset, [train_size, val_size]
    )
   
    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=8,
        shuffle=True,
        num_workers=4
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=8,
        shuffle=False,
        num_workers=4
    )
   
    # Create and train model
    model = DeepFakeDetector()
    train_model(model, train_loader, val_loader, epochs=50, device=device)

if __name__ == '__main__':
    main()
```

### Probability Distribution

A **probability distribution** is the mathematical function that gives the probabilities of occurrence of the possible outcomes for an experiment. It is a mathematical description of  a random phenomenon in terms of its sample space and probabilities of events. The sample space, often represented in  notation by **Ω** (omega) is the set of all possible outcomes of a random phenomenon being observed. The sample space may be any set: a set of real numbers, a set of vectors, a set of arbitrary non-numerical values etc. Sample space of coin flip would be **Ω =** {”heads”, “tails”}.

Defining the probability of the distribution depends on the type of random variables. **Discrete and absolutely continuous.** In the discrete case, it is sufficiently to specify a probability mass function *p*  assigning probability to each possible outcomes. In contrast when a random variable takes values from a continuum then by convention, any individual outcome is assigned probability zero. For such continuous random variables, only events that include infinitely many outcomes such as intervals have probability greater than zero.