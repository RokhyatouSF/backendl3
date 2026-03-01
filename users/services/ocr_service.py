import pytesseract
import cv2
import re

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def extract_text(image_path: str) -> str:
    img = cv2.imread(image_path)

    if img is None:
        raise Exception("Image non lisible")

    # agrandir image
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    gray = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    config = "--oem 3 --psm 6"
    text = pytesseract.image_to_string(gray, lang="fra", config=config)

    print("\n===== OCR BRUT =====")
    print(text)

    text = clean_text(text)

    print("\n===== OCR CLEAN =====")
    print(text)

    return text
