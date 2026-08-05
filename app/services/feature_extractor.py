import math
import re

# QWERTY physical keyboard row mapping for pattern detection
QWERTY_ROWS = [
    "`1234567890-=",
    "qwertyuiop[]\\",
    "asdfghjkl;'",
    "zxcvbnm,./"
]

# Common dictionary words and popular password fragments
COMMON_WORDS = {
    "password", "admin", "welcome", "login", "master", "shadow", "dragon",
    "football", "baseball", "monkey", "sunshine", "princess", "superman",
    "trustno1", "freedom", "whatever", "starwars", "pokemon", "jordan",
    "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december", "monday", "tuesday",
    "wednesday", "thursday", "friday", "saturday", "sunday", "google",
    "microsoft", "apple", "amazon", "facebook", "twitter", "instagram"
}

LEET_MAP = {
    '@': 'a', '4': 'a', '3': 'e', '1': 'i', '!': 'i',
    '0': 'o', '5': 's', '$': 's', '7': 't', '+': 't', '8': 'b'
}

def decode_leetspeak(text: str) -> str:
    """Converts common leetspeak characters to standard lowercase letters."""
    lowered = text.lower()
    for leet, orig in LEET_MAP.items():
        lowered = lowered.replace(leet, orig)
    return lowered

def calculate_shannon_entropy(password: str) -> float:
    """Calculates Shannon Entropy in bits for a given password."""
    if not password:
        return 0.0
    
    length = len(password)
    char_counts = {}
    for char in password:
        char_counts[char] = char_counts.get(char, 0) + 1
    
    entropy = 0.0
    for count in char_counts.values():
        p = count / length
        entropy -= p * math.log2(p)
    
    # Scale total entropy by length
    return round(entropy * length, 2)

def detect_sequential_characters(password: str) -> int:
    """Counts sequential character runs (e.g. 'abc', '123', 'zyx')."""
    if len(password) < 2:
        return 0
    
    seq_count = 0
    lowered = password.lower()
    for i in range(len(lowered) - 1):
        diff = ord(lowered[i + 1]) - ord(lowered[i])
        if diff == 1 or diff == -1:
            seq_count += 1
    return seq_count

def detect_consecutive_repeats(password: str) -> int:
    """Counts adjacent duplicate characters (e.g., 'aa', '11')."""
    repeat_count = 0
    for i in range(len(password) - 1):
        if password[i] == password[i + 1]:
            repeat_count += 1
    return repeat_count

def detect_keyboard_patterns(password: str) -> int:
    """Detects physical QWERTY keyboard adjacency walks."""
    lowered = password.lower()
    pattern_matches = 0
    
    for row in QWERTY_ROWS:
        for i in range(len(lowered) - 2):
            sub = lowered[i:i + 3]
            if sub in row or sub in row[::-1]:
                pattern_matches += 1
    return pattern_matches

def detect_dictionary_words(password: str) -> int:
    """Detects embedded dictionary words and leetspeak equivalents."""
    lowered = password.lower()
    decoded = decode_leetspeak(password)
    
    match_count = 0
    for word in COMMON_WORDS:
        if len(word) >= 4 and (word in lowered or word in decoded):
            match_count += 1
    return match_count

def extract_features(password: str) -> dict:
    """
    Extracts 15 numerical features from raw password text.
    Returns a dictionary of named features.
    """
    length = len(password)
    if length == 0:
        return {
            'length': 0, 'num_uppercase': 0, 'num_lowercase': 0,
            'num_digits': 0, 'num_symbols': 0, 'uppercase_ratio': 0.0,
            'digit_ratio': 0.0, 'symbol_ratio': 0.0, 'shannon_entropy': 0.0,
            'unique_char_ratio': 0.0, 'consecutive_repeats': 0,
            'sequential_chars': 0, 'keyboard_pattern_score': 0,
            'dictionary_matches': 0, 'has_leetspeak': 0
        }

    num_upper = sum(1 for c in password if c.isupper())
    num_lower = sum(1 for c in password if c.islower())
    num_digits = sum(1 for c in password if c.isdigit())
    num_symbols = sum(1 for c in password if not c.isalnum())

    decoded = decode_leetspeak(password)
    has_leet = 1 if decoded != password.lower() and any(c in LEET_MAP for c in password) else 0

    return {
        'length': length,
        'num_uppercase': num_upper,
        'num_lowercase': num_lower,
        'num_digits': num_digits,
        'num_symbols': num_symbols,
        'uppercase_ratio': round(num_upper / length, 4),
        'digit_ratio': round(num_digits / length, 4),
        'symbol_ratio': round(num_symbols / length, 4),
        'shannon_entropy': calculate_shannon_entropy(password),
        'unique_char_ratio': round(len(set(password)) / length, 4),
        'consecutive_repeats': detect_consecutive_repeats(password),
        'sequential_chars': detect_sequential_characters(password),
        'keyboard_pattern_score': detect_keyboard_patterns(password),
        'dictionary_matches': detect_dictionary_words(password),
        'has_leetspeak': has_leet
    }
