import os
import cv2
import numpy as np
import torch
import pydicom
from django.core.files.base import ContentFile
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
        
        if img_path.lower().endswith('.dcm'):
            dicom_data = pydicom.dcmread(img_path)
            pixel_array = dicom_data.pixel_array
            if np.max(pixel_array) > 0:
                pixel_array = (pixel_array / np.max(pixel_array)) * 255.0
            
            img_cv_original = np.uint8(pixel_array)
            if len(img_cv_original.shape) == 2:
                img_cv_original = cv2.cvtColor(img_cv_original, cv2.COLOR_GRAY2RGB)
            img_pil = Image.fromarray(img_cv_original)
        else:
            img_pil = Image.open(img_path).convert('RGB')
            img_cv_original = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

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
        if np.max(heatmap) > 0:
            heatmap /= np.max(heatmap) # Normalize to [0, 1]

        # 5. Overlay on original image using OpenCV
        heatmap_resized = cv2.resize(heatmap, (img_cv_original.shape[1], img_cv_original.shape[0]))
        heatmap_uint8 = np.uint8(255 * heatmap_resized)
        heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
        
        # Superimpose: 60% original image + 40% heatmap
        diagnostic_result = cv2.addWeighted(img_cv_original, 0.6, heatmap_color, 0.4, 0)

        # 6. Save Heatmap to Database Field
        heatmap_name = f"heatmap_{record_id}.jpg"
        ret, buf = cv2.imencode('.jpg', diagnostic_result)
        if ret:
            content = ContentFile(buf.tobytes())
            record.heatmap_image.save(heatmap_name, content, save=False)
        
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
        # Update record with error so user is notified
        try:
            record.description += f"\n[AI Error]: Failed to process image. Reason: {str(e)}"
            record.save()
        except:
            pass
        return f"Error: {str(e)}"