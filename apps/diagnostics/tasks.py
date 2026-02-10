from celery import shared_task
# REMOVED: from .models import MedicalRecord (This was causing the loop)
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
from PIL import Image
import os

# Initialize the model globally so it stays in RAM
weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)
model.eval()
preprocess = weights.transforms()

@shared_task(name='apps.diagnostics.tasks.process_medical_image')
def process_medical_image(record_id):
    # Import inside the function to break the Circular Import Loop
    from apps.diagnostics.models import MedicalRecord 
    
    try:
        record = MedicalRecord.objects.get(id=record_id)
        print(f"--- AI ANALYZING RECORD {record_id} ---")
        
        img_path = record.document.path
        img = Image.open(img_path).convert('RGB')
        
        batch = preprocess(img).unsqueeze(0)
        
        with torch.no_grad():
            prediction = model(batch).squeeze(0)
            confidences = torch.nn.functional.softmax(prediction, dim=0)
            
        score, class_id = torch.max(confidences, dim=0)
        
        record.is_analyzed = True
        record.description += f"\n[AI Insight]: Analysis complete. Confidence Score: {score.item():.2f}."
        
        if score.item() < 0.50:
            record.description += "\n[Warning]: Low confidence detection. Manual review highly recommended."
        
        record.save()
        return f"Record {record_id} processed with score {score.item()}"

    except Exception as e:
        print(f"AI Error: {str(e)}")
        return f"Error: {str(e)}"