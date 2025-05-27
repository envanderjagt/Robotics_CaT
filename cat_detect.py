import torch
import clip
from PIL import Image
from picamera2 import Picamera2
import cv2


def get_cat_probability(cam):
    """
    This function captures an image from the camera, processes it using CLIP,
    and returns the probability that the image contains a cat.
    """
    # 0) Check if GPU is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # 1) Load CLIP
    model, preprocess = clip.load("ViT-B/32", device=device)

    # 2) Prepare your image
    frame = cam.capture_array()
    image = Image.fromarray(frame)
    img = preprocess(image).unsqueeze(0).to(device)

    # 3) Prepare the two candidate labels
    text = clip.tokenize(["a cat or part of a cat", "something else"]).to(device)

    # 4) Compute similarity
    with torch.no_grad():
        image_features = model.encode_image(img)
        text_features  = model.encode_text(text)
        logits = (image_features @ text_features.T).softmax(dim=-1)

    # logits[0,0] is confidence for “cat”
    cat_confidence = logits[0, 0].item()
    if cat_confidence >= 0.1:
        cv2.imwrite("catimage.png", frame)
    return cat_confidence
