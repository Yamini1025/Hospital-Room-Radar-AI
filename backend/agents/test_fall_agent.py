from agents.fall_safety import analyze_fall_safety

image_url = "https://room-radar-images.s3.us-east-2.amazonaws.com/Gemini_Generated_Image_m5eu5ym5eu5ym5eu.jpeg"

result = analyze_fall_safety(image_url)
print(result)