import torch
import torchvision.transforms as T
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Load the pre-trained DeepLabV3 model
model = torch.hub.load('pytorch/vision:v0.10.0', 'deeplabv3_resnet101', pretrained=True)
model.eval()

# Define the transformation
transform = T.Compose([
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def create_mask(image_path, output_mask_path):
    # Load the image
    input_image = Image.open(image_path).convert("RGB")
    
    input_image = input_image.resize((512, 512))
    
    # Apply the transformation
    input_tensor = transform(input_image)
    input_batch = input_tensor.unsqueeze(0)  # Create a mini-batch as expected by the model

    with torch.no_grad():
        output = model(input_batch)['out'][0]
    output_predictions = output.argmax(0)

    # Convert the output to a binary mask
    mask = (output_predictions == 15).byte().cpu().numpy()  # Class 15 is the 'person' class in COCO dataset

    # Save the mask as an image
    mask_img = Image.fromarray(mask * 255).convert("L")
    mask_img.save(output_mask_path)

    # Display the original image and the mask
    

# Paths to the images (update these paths accordingly)
person_image_path = 'uploads/person.jpg'
mask_image_path = 'uploads/mask.png'

# Create and save the mask image
create_mask(person_image_path, mask_image_path)
