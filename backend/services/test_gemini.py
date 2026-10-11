from agents.coordinator import analyze_room
from services.gemini import generate_report


def main():
    image_url = "https://room-radar-images.s3.us-east-2.amazonaws.com/Gemini_Generated_Image_kqa43xkqa43xkqa4.jpeg"

    analysis = analyze_room(image_url)

    print("\n--- COORDINATOR ANALYSIS ---")
    print(analysis)

    if analysis["errors"]:
        print("\nAgents failed:")
        print(analysis["errors"])
        return

    report = generate_report(analysis)

    print("\n--- GEMINI FINAL REPORT ---")
    print(report)


if __name__ == "__main__":
    main()