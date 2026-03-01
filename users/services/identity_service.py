import re
import unicodedata


def normalize_text(text):
    if not text:
        return ""

    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def check_identity(user, ocr_text, numero_attendu):

    print("===== OCR CLEAN =====")
    ocr_clean = normalize_text(ocr_text)
    print(ocr_clean)

    ocr_words = ocr_clean.split()
    print("OCR WORDS:", ocr_words)

    # ======================
    # NUMERO
    # ======================
    numero_match = numero_attendu.replace(" ", "") in ocr_clean.replace(" ", "")
    print("NUMERO MATCH:", numero_match)

    # ======================
    # PRENOM (multi-mots)
    # ======================
    expected_firstname = normalize_text(user.first_name)
    expected_words = expected_firstname.split()

    firstname_match = all(word in ocr_words for word in expected_words)

    print("PRENOM ATTENDU:", expected_firstname)
    print("PRENOM MATCH:", firstname_match)

    # ======================
    # NOM
    # ======================
    expected_lastname = normalize_text(user.last_name)

    nom_match = expected_lastname in ocr_words

    print("NOM ATTENDU:", expected_lastname)
    print("NOM MATCH:", nom_match)

    # ======================
    # DATE
    # ======================
    date_input = user.date_naissance  # format YYYY-MM-DD
    date_match = False

    if date_input:
        try:
            year, month, day = date_input.split("-")
            date_carte = f"{day} {month} {year}"

            print("DATE ATTENDUE (FORMAT CARTE):", date_carte)

            if date_carte in ocr_clean:
                date_match = True

        except:
            print("Erreur format date")

    print("DATE MATCH:", date_match)

    # ======================
    # SCORE
    # ======================
    score = 0
    if numero_match:
        score += 10
    if firstname_match:
        score += 10
    if nom_match:
        score += 10
    if date_match:
        score += 10

    print("SCORE FINAL:", score, "/40")

    verified = score >= 30
    status = "approved" if verified else "rejected"

    return verified, status, score