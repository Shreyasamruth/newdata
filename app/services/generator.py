import random
import string

WORD_LIST = [
    "alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel",
    "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "papa",
    "quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey", "xray",
    "yankee", "zulu", "anchor", "beacon", "castle", "dragon", "eagle", "falcon",
    "glacier", "harbor", "island", "jungle", "knight", "legend", "matrix", "nexus",
    "orbit", "phoenix", "quantum", "rocket", "shadow", "titan", "vertex", "zenith"
]

def generate_password(category: str = "custom", length: int = 16, include_upper: bool = True,
                      include_digits: bool = True, include_symbols: bool = True) -> str:
    """
    Generates strong, entropy-maximized passwords based on context/use-case.
    """
    if category == "passphrase":
        num_words = max(3, length // 5)
        chosen = [random.choice(WORD_LIST).capitalize() for _ in range(num_words)]
        sep = random.choice(["-", "_", "!", "@", "#", "$", "."])
        num_suffix = str(random.randint(10, 99)) if include_digits else ""
        return sep.join(chosen) + num_suffix

    elif category == "banking":
        # Strict high security: 16+ chars, all sets included
        chars = string.ascii_lowercase
        if include_upper: chars += string.ascii_uppercase
        if include_digits: chars += string.digits
        if include_symbols: chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Ensure at least one character from each set
        pwd = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase) if include_upper else random.choice(string.ascii_lowercase),
            random.choice(string.digits) if include_digits else random.choice(string.ascii_lowercase),
            random.choice("!@#$%^&*") if include_symbols else random.choice(string.ascii_lowercase)
        ]
        
        for _ in range(length - len(pwd)):
            pwd.append(random.choice(chars))
            
        random.shuffle(pwd)
        return "".join(pwd)

    elif category == "memorable":
        # Alternating consonant-vowel pairs with symbols and digits
        consonants = "bcdfghjklmnpqrstvwxyz"
        vowels = "aeiou"
        pwd_chars = []
        for i in range(length - 4):
            if i % 2 == 0:
                pwd_chars.append(random.choice(consonants).upper() if i == 0 else random.choice(consonants))
            else:
                pwd_chars.append(random.choice(vowels))
        
        pwd_chars.append(random.choice("!@#$%^&*"))
        pwd_chars.append(str(random.randint(100, 999)))
        return "".join(pwd_chars)

    else: # Custom / Social Media / Email / Gaming
        chars = string.ascii_lowercase
        if include_upper: chars += string.ascii_uppercase
        if include_digits: chars += string.digits
        if include_symbols: chars += "!@#$%^&*()_+-=[]?"
        
        return "".join(random.choice(chars) for _ in range(length))
