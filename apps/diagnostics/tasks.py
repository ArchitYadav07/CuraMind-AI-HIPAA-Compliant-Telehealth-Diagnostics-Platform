import os
import cv2
import numpy as np
import torch
from celery import shared_task
from PIL import Image
from torchvision.models import resnet50, ResNet50_Weights

# Initialize the model globally (Efficient for your ₹1 Lakh lab setup)
weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)
model.eval()
preprocess = weights.transforms()

@shared_task(name='apps.diagnostics.tasks.process_medical_image')
def process_medical_image(record_id):
    from apps.diagnostics.models import MedicalRecord 
    
    try:
        record = MedicalRecord.objects.get(id=record_id)
        print(f"--- AI ANALYZING RECORD {record_id} ---")
        
        # 1. Prepare Image
        img_path = record.document.path
        img_pil = Image.open(img_path).convert('RGB')
        input_tensor = preprocess(img_pil).unsqueeze(0)
        
        # 2. Hook into the last convolutional layer (layer4) for Heatmap
        features = []
        def hook_fn(module, input, output):
            features.append(output)
        
        hook = model.layer4.register_forward_hook(hook_fn)
        
        # 3. Run Inference
        with torch.no_grad():
            output = model(input_tensor)
            confidences = torch.nn.functional.softmax(output[0], dim=0)
        
        hook.remove() # Clean up the hook
        score, class_id = torch.max(confidences, dim=0)

        # 4. Generate Heatmap logic
        feature_map = features[0].detach().cpu().numpy()[0] # Shape: (2048, 7, 7)
        heatmap = np.mean(feature_map, axis=0) # Average across channels
        heatmap = np.maximum(heatmap, 0) # ReLU
        heatmap /= np.max(heatmap) # Normalize to [0, 1]

        # 5. Overlay on original image using OpenCV
        img_cv = cv2.imread(img_path)
        heatmap_resized = cv2.resize(heatmap, (img_cv.shape[1], img_cv.shape[0]))
        heatmap_uint8 = np.uint8(255 * heatmap_resized)
        heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
        
        # Superimpose: 60% original image + 40% heatmap
        diagnostic_result = cv2.addWeighted(img_cv, 0.6, heatmap_color, 0.4, 0)

        # 6. Save Heatmap to the same directory
        heatmap_name = f"heatmap_{record_id}.jpg"
        # Using record.document.path to find the directory
        heatmap_path = os.path.join(os.path.dirname(img_path), heatmap_name)
        cv2.imwrite(heatmap_path, diagnostic_result)
        
        # 7. Update Database
        record.is_analyzed = True
        record.description += f"\n[AI Insight]: Confidence: {score.item():.2f}."
        record.description += f"\n[AI Visualizer]: Heatmap generated for diagnostic review."
        
        if score.item() < 0.50:
            record.description += "\n[Warning]: Low confidence. Manual review required."
        
        record.save()
        return f"Record {record_id} processed with Heatmap at {heatmap_name}"

    except Exception as e:
        print(f"AI Error: {str(e)}")
        return f"Error: {str(e)}"