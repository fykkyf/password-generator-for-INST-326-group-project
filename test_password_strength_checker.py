import pytest
from PasswordStrengthChecker import PasswordStrengthChecker

@pytest.fixture
def checker():
    return PasswordStrengthChecker()

def test_length_check(checker):
    assert checker.check_length("abc12345") is True
    assert checker.check_length("aB3!") is False

def test_character_variety_check(checker):
    assert checker.check_character_variety("abcD123") == 3
    assert checker.check_character_variety("abcdef12") == 2
    assert checker.check_character_variety("ABC123!!") == 3

def test_common_patterns_check(checker):
    assert checker.contains_common_patterns("password") is True
    assert checker.contains_common_patterns("mypassword123") is True
    assert checker.contains_common_patterns("UniqPW!23") is False

def test_strength_score(checker):
    assert checker.calculate_strength_score("A7f!k2Lp") == 3
    assert checker.calculate_strength_score("password") == 1
    assert checker.calculate_strength_score("1234") == 0
    assert checker.calculate_strength_score("Pass123") == 2

def test_strength_label(checker):
    assert checker.get_strength_label("A7f!k2Lp") == "Strong"
    assert checker.get_strength_label("password") == "Weak"
    assert checker.get_strength_label("1234") == "You serious?"
    assert checker.get_strength_label("Pass123") == "Medium"

def test_detailed_report(checker):
    report = checker.get_detailed_report("A7f!k2Lp")
    assert report["length_ok"] is True
    assert report["variety_count"] == 4
    assert report["contains_common_patterns"] is False
    assert report["score"] == 3
    assert report["label"] == "Strong"

def test_evaluate(checker):
    result = checker.evaluate("A7f!k2Lp")
    assert result["password"] == "A7f!k2Lp"
    assert result["strength"] == "Strong"
    assert "details" in result