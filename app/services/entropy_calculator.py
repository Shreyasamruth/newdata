import math

def calculate_pool_size(password: str) -> int:
    """Determines character pool size (N) based on character types present."""
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    pool = 0
    if has_lower:
        pool += 26
    if has_upper:
        pool += 26
    if has_digit:
        pool += 10
    if has_symbol:
        pool += 33
    
    return max(pool, 1)

def format_crack_time(seconds: float) -> str:
    """Formats raw seconds into human-readable duration strings."""
    if seconds < 0.001:
        return "Instant (< 1 ms)"
    elif seconds < 1:
        return f"{round(seconds * 1000, 1)} ms"
    elif seconds < 60:
        return f"{round(seconds, 1)} seconds"
    elif seconds < 3600:
        return f"{round(seconds / 60, 1)} minutes"
    elif seconds < 86400:
        return f"{round(seconds / 3600, 1)} hours"
    elif seconds < 31536000:
        return f"{round(seconds / 86400, 1)} days"
    elif seconds < 31536000 * 100:
        return f"{round(seconds / 31536000, 1)} years"
    elif seconds < 31536000 * 1000000:
        return f"{round(seconds / (31536000 * 100), 1)} centuries"
    else:
        return "Millions of centuries"

def estimate_crack_times(password: str) -> dict:
    """
    Estimates resistance against various attack vectors based on combinations count (N^L / 2).
    Returns formatted crack times for 4 attack scenarios.
    """
    length = len(password)
    pool_size = calculate_pool_size(password)
    
    if length == 0:
        return {
            "online_attack": "Instant",
            "slow_hash": "Instant",
            "fast_hash": "Instant",
            "gpu_cluster": "Instant",
            "combinations_log10": 0
        }

    # Total combinations = N^L
    combinations = pool_size ** length
    avg_attempts = combinations / 2.0
    
    # Speed benchmarks (attempts per second)
    SPEEDS = {
        "online_attack": 100.0,              # 100 reqs/sec (Web API)
        "slow_hash": 10000.0,                # 10 kH/s (bcrypt/Argon2)
        "fast_hash": 10000000000.0,          # 10 GH/s (MD5/NTLM)
        "gpu_cluster": 1000000000000.0       # 1 TH/s (GPU cluster)
    }

    results = {}
    for key, speed in SPEEDS.items():
        secs = avg_attempts / speed
        results[key] = format_crack_time(secs)
        
    results["combinations_log10"] = round(math.log10(max(combinations, 1)), 2)
    return results

def compute_health_score(password: str, features: dict) -> dict:
    """
    Calculates a 0-100 Password Health Score with detailed breakdown.
    Score breakdown:
    - Length: up to 30 pts
    - Character Diversity: up to 25 pts
    - Entropy: up to 25 pts
    - Uniqueness & Pattern Penalties: up to -40 pts
    """
    length = len(password)
    if length == 0:
        return {"score": 0, "category": "Very Weak", "color": "#ff0844", "breakdown": {}}

    # 1. Length Score (0 to 30)
    length_score = min(length * 2.5, 30.0)

    # 2. Diversity Score (0 to 25)
    char_sets = (features.get('num_uppercase', 0) > 0) + \
               (features.get('num_lowercase', 0) > 0) + \
               (features.get('num_digits', 0) > 0) + \
               (features.get('num_symbols', 0) > 0)
    diversity_score = char_sets * 6.25

    # 3. Entropy Score (0 to 25)
    entropy = features.get('shannon_entropy', 0.0)
    entropy_score = min((entropy / 80.0) * 25.0, 25.0)

    # 4. Uniqueness Bonus (0 to 20)
    unique_score = features.get('unique_char_ratio', 1.0) * 20.0

    raw_score = length_score + diversity_score + entropy_score + unique_score

    # 5. Penalties
    penalties = 0.0
    if features.get('dictionary_matches', 0) > 0:
        penalties += 20.0
    if features.get('keyboard_pattern_score', 0) > 0:
        penalties += 15.0
    if features.get('consecutive_repeats', 0) > 0:
        penalties += 10.0
    if features.get('sequential_chars', 0) > 0:
        penalties += 10.0

    final_score = int(max(0, min(100, round(raw_score - penalties))))

    if final_score < 30:
        category = "Weak"
        color = "#ff4d4d"
    elif final_score < 60:
        category = "Medium"
        color = "#ffaa00"
    elif final_score < 85:
        category = "Strong"
        color = "#00cc66"
    else:
        category = "Very Strong"
        color = "#00f2fe"

    return {
        "score": final_score,
        "category": category,
        "color": color,
        "breakdown": {
            "length_score": round(length_score, 1),
            "diversity_score": round(diversity_score, 1),
            "entropy_score": round(entropy_score, 1),
            "unique_score": round(unique_score, 1),
            "penalties": round(penalties, 1)
        }
    }
