import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_fabric_to_dress(dress_img_path, fabric_img_path, mask_img_path):
    # Load images
    dress_img = cv2.imread(dress_img_path)
    fabric_img = cv2.imread(fabric_img_path)
    mask_img = cv2.imread(mask_img_path, cv2.IMREAD_GRAYSCALE)  # Binary mask of the dress
    dress_img = cv2.resize(dress_img,(512, 512))
    fabric_img = cv2.resize(fabric_img,(512, 512))
    # Resize the fabric to the size of the dress image
    fabric_img = cv2.resize(fabric_img, (dress_img.shape[1], dress_img.shape[0]))

    # Create an inverse mask
    inverse_mask = cv2.bitwise_not(mask_img)
    # inverse_mask = mask_img


    # Use the mask to extract the dress region
    dress_region = cv2.bitwise_and(dress_img, dress_img, mask=mask_img)

    # Use the inverse mask to remove the dress region from the fabric
    fabric_region = cv2.bitwise_and(fabric_img, fabric_img, mask=mask_img)

    # Combine the dress region with the new fabric pattern
    combined_img = cv2.add(dress_region, fabric_region)
    # cv2.imshow('Image',combined_img)
    alpha = 0.2  # Adjust this value as needed

# Weight for the dress region
    beta = 1.0 - alpha

# Perform weighted addition
    bled_img = cv2.addWeighted(fabric_region, alpha, dress_region, beta, 0)
    # cv2.imshow('Image',bled_img)
    
    # Use the inverse mask to add the non-dress parts of the original image
    background = cv2.bitwise_and(dress_img, dress_img, mask=inverse_mask)
    final_img = cv2.add(combined_img, background)

    return final_img

# File paths (update these paths accordingly)
dress_img_path = 'uploads/person.jpg'
fabric_img_path = 'uploads/fabric.jpg'
mask_img_path = 'uploads/mask.png'

# Apply fabric to dress
result_img = apply_fabric_to_dress(dress_img_path, fabric_img_path, mask_img_path)

output_path = 'uploads/result.jpg'
cv2.imwrite(output_path, result_img)
# print(f"Result image saved at {output_path}")
# Display the result

