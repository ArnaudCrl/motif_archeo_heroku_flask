import io
import torch
import torch.nn as nn
import torchvision.transforms as T
from PIL import Image
from torchvision import models
import dowload_model

# load model
net = models.resnet18(pretrained=True)
device = torch.device('cpu')
num_ftrs = net.fc.in_features
net.fc = nn.Linear(num_ftrs, 46)

PATH = "torch_resnet_model.pt"

net.load_state_dict(torch.load(PATH, map_location=device))
net.eval()


# image -> tensor
def transform_image(image_bytes):
    normalize = T.Normalize(mean=[0.5], std=[0.5])
    transform = T.Compose([  # T.Grayscale(num_output_channels=1),
        T.Resize((512, 512)),
        T.RandomHorizontalFlip(),
        T.RandomPerspective(distortion_scale=0.05, p=0.5),
        T.ToTensor(),
        normalize,
    ])

    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert("RGB")
    return transform(image).unsqueeze(0)


# predict
def get_prediction(image_tensor):
    # images = image_tensor.reshape(-1, 512 * 512)
    outputs = net(image_tensor)
    # max returns (value ,index)
    # _, predicted = torch.max(outputs.data, 1)
    return outputs
