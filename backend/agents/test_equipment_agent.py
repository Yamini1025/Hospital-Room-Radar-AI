from agents.equipment_safety import analyze_equipment_safety

image_url = "https://room-radar-images.s3.us-east-2.amazonaws.com/Gemini_Generated_Image_kqa43xkqa43xkqa4.jpeg"

result = analyze_equipment_safety(image_url)

print(result)