# Problem 10: Tokenizer for Clinical NLP
# Prompt: Build a simple tokenizer for clinical notes that handles common abbreviations and keeps hyphenated terms together.

# Rules:
# Split on whitespace and punctuation EXCEPT hyphens within words
# Keep abbreviations intact: “pt.”, “dx.”, “tx.”, “hx.”
# Lowercase everything
# Remove standalone punctuation tokens

note = "Pt. reports moderate-to-severe anxiety. Dx. is GAD; tx. plan includes CBT."

# tokenize(note)
# # → ["pt.", "reports", "moderate-to-severe", "anxiety", "dx.", "is",
# #     "gad", "tx.", "plan", "includes", "cbt"]

# Expected signature:
# def tokenize(note: str) -> list[str]:

# Follow-ups:
# How would you extend this to handle negation? (“no anxiety” vs “anxiety”)
# Build a vocabulary index from a corpus of notes
# How does this compare to what a real NLP tokenizer (spaCy, BERT) does?


ABBREVIATIONS = {"pt.", "dx.", "tx.", "hx.", "rx.", "sx.", "fx.", "bx."}


def tokenize(note: str) -> list[str]:
    raw_tokens = note.lower().split()
    tokens = []

    for raw in raw_tokens:
        # Check abbreviations first (strip trailing ; or ,)
        stripped = raw.rstrip(";,")
        if stripped in ABBREVIATIONS:
            tokens.append(stripped)
            continue

        # Build token character by character
        # Keep letters and hyphens between letters, strip everything else
        current = []
        for i, char in enumerate(raw):
            if char.isalpha():
                current.append(char)
            elif char == "-":
                # Only keep hyphen if it's between letters
                has_before = i > 0 and raw[i - 1].isalpha()
                has_after = i < len(raw) - 1 and raw[i + 1].isalpha()
                if has_before and has_after:
                    current.append(char)
                else:
                    # Hyphen at edge — treat as separator
                    if current:
                        tokens.append("".join(current))
                        current = []
            else:
                # Any other character is a separator
                if current:
                    tokens.append("".join(current))
                    current = []

        if current:
            tokens.append("".join(current))

    return tokens


print(tokenize(note))
# # → ["pt.", "reports", "moderate-to-severe", "anxiety", "dx.", "is",
# #     "gad", "tx.", "plan", "includes", "cbt"]
