import re

class PasswordStrengthChecker:
    "(1) Initialize the checker with minimum length of 8"
    def __init__(self, min_length=8):

        self.min_length = min_length
        self.common_patterns = ["1234", "password", "abcd", "qwerty"]
        self.score_map = {
            0: "Very Weak",
            1: "Weak",
            2: "Medium",
            3: "Strong",
            4: "Very Strong"
        }

    "(2) method to check the length"
    def check_length(self, password):
        "compare password length and minimum length and return boolean if it is greater or equal"
        return len(password) >= self.min_length

    "(3) method to check if the password contain all kinds of characters"
    def check_character_variety(self, password):
        "use any() and .is to check each char"
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)
        "return a list of boolean to see the result and add together for score to use"
        return sum([has_upper, has_lower, has_digit, has_symbol])

    "(4) method to check if password has a common pattern "
    def contains_common_patterns(self, password):
        "use for loop to check if password contains all common patterns "
        return any(pattern in password.lower() for pattern in self.common_patterns)

    "(5) method to the password a score based on the previous methods"
    def calculate_strength_score(self, password):
        "initialize the score"
        score = 0
        "use each method of boolean result to calculate"
        if self.check_length(password):
            score += 1

        if self.check_character_variety(password) >= 3:
            score += 1
        "use not because of it contains common patterns means it is weak"
        if not self.contains_common_patterns(password):
            score += 1
        "use min to make sure the score stays in the range"
        return min(score, 3)

    "(6) method to get the score and compare to score map to get the score report"
    def get_strength_label(self, password):
        "use .get() to get the score and the value"
        return self.score_map.get(self.calculate_strength_score(password), "no score")

    "(7) method to get each method's result for test"
    def get_detailed_report(self, password):

        return {
            "length_ok": self.check_length(password),
            "variety_count": self.check_character_variety(password),
            "contains_common_patterns": self.contains_common_patterns(password),
            "score": self.calculate_strength_score(password),
            "label": self.get_strength_label(password)
        }
    "(8) method to get all information to show in the terminal"
    def evaluate(self, password):
        return {
            "password": password,
            "strength": self.get_strength_label(password),
            "details": self.get_detailed_report(password)
        }
