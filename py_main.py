import sys
import pickle
import re
import Levenshtein
import pandas as pd

# Leet speak dictionary
leet_dict = {
    'a': ['4', '@', '/\\', '^', 'a'],
    'b': ['8', '6', '13', '|3', 'b'],
    'c': ['(', '<', '{', '[', 'c'],
    'd': ['|)', '|]', 'd'],
    'e': ['3', '&', '€', 'e'],
    'f': ['|=', 'ph', 'f'],
    'g': ['6', '9', 'g'],
    'h': ['#', '|-|', '[-]', 'h'],
    'i': ['1', '!', '|', 'i'],
    'j': ['_|', '_/', 'j'],
    'k': ['|<', '|{', 'k'],
    'l': ['1', '|_', '|', 'l'],
    'm': ['|\\/|', '/\\/\\', '(V)', 'm'],
    'n': ['|\\|', '/\\/', '(\\)', 'n'],
    'o': ['0', '()', '[]', '<>', '*', 'o'],
    'p': ['|*', '|>', 'p'],
    'q': ['9', 'q'],
    'r': ['|2', '12', 'r'],
    's': ['5', '$', 'z', 's'],
    't': ['7', '+', '†', 't'],
    'u': ['|_|', 'µ', 'u'],
    'v': ['\\/','<','>', 'v'],
    'w': ['\\/\\/', 'vv', '\\^/', 'w'],
    'x': ['><', ')(', '][' ,'}{', 'x'],
    'y': ['`/', 'y'],
    'z': ['2', 'z'],
}

def check_password_strength(password):
    # Function to normalize leet speak
    def normalize_leet_speak(password):
        normalized_password = password.lower()
        for char, replacements in leet_dict.items():
            for replacement in replacements:
                normalized_password = re.sub(re.escape(replacement), char, normalized_password, flags=re.IGNORECASE)
        normalized_password = re.sub(r'\s+', '_', normalized_password)
        return normalized_password

    # Analyze password features
    def analyze_password(password):
        normalized_password = normalize_leet_speak(password)
        contains_year = bool(re.search(r'(1[0-9]{3}|20[0-2][0-9]|[0-9]{4})', password))

        total_length = len(password)
        
        upper_count_original = sum(1 for char in password if char.isupper())
        lower_count_original = sum(1 for char in password if char.islower())
        digit_count_original = sum(1 for char in password if char.isdigit())
        special_count_original = len(password) - (upper_count_original + lower_count_original + digit_count_original)

        upper_count_normalized = sum(1 for char in normalized_password if char.isupper())
        lower_count_normalized = sum(1 for char in normalized_password if char.islower())
        digit_count_normalized = sum(1 for char in normalized_password if char.isdigit())
        special_count_normalized = len(normalized_password) - (upper_count_normalized + lower_count_normalized + digit_count_normalized)

        return [
            password,
            normalized_password,
            total_length,
            upper_count_original,
            lower_count_original,
            digit_count_original,
            special_count_original,
            upper_count_normalized,
            lower_count_normalized,
            digit_count_normalized,
            special_count_normalized,
            contains_year
        ]

    def calculate_similarity(password, normalized_password):
        # Calculate Levenshtein distance
        distance = Levenshtein.distance(password, normalized_password)
        
        # Determine the length of the longer string
        max_len = max(len(password), len(normalized_password))
        
        # Handle the case where both strings are empty
        if max_len == 0:
            return 1.0
        
        # Normalize the distance to get the similarity score
        similarity_score = 1 - (distance / max_len)
        return similarity_score

    # Load the trained model
    with open('C:\\Users\\Dell\\Desktop\\HC\\mit_thing\\random_forest_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

    # Analyze password features
    password_features = analyze_password(password)
    sim = calculate_similarity(password_features[0], password_features[1])

    # Prepare the feature list
    input_features = [
        password_features[2],  # total_length
        password_features[3],  # upper_count_original
        password_features[4],  # lower_count_original
        password_features[5],  # digit_count_original
        password_features[6],  # special_count_original
        password_features[7],  # upper_count_normalized
        password_features[8],  # lower_count_normalized
        password_features[9],  # digit_count_normalized
        password_features[10],  # special_count_normalized
        password_features[11],  # contains_year
        sim  # password_similarity
    ]

    # Correct order of feature names as per the model
    feature_names = [
        'total_length', 
        'upper_count_original', 
        'lower_count_original', 
        'digit_count_original', 
        'special_count_original', 
        'upper_count_normalized', 
        'lower_count_normalized', 
        'digit_count_normalized', 
        'special_count_normalized', 
        'contains_year', 
        'password_similarity'
    ]

    # Convert the input features into a DataFrame
    input_df = pd.DataFrame([input_features], columns=feature_names)

    # Predict strength using the model
    score = model.predict(input_df)[0]

    # Convert score to human-readable format
    def score_to_strength(score):
        if score == 0:
            return "weak"
        elif score == 1:
            return "medium"
        elif score == 2:
            return "strong"
        else:
            return "unknown"

    # Output the strength
    strength = score_to_strength(score)

    # Return the strength
    return strength

# Check for password input and call the function
if __name__ == "__main__":
    if len(sys.argv) > 1:
        password = sys.argv[1]
        print(check_password_strength(password))
    else:
        raise ValueError("No password received.")