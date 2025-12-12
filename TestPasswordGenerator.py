import pytest
from PasswordGenerator import PasswordGenerator, GeneratorPolicy

def test_generate_length():
    gen = PasswordGenerator()
    pwd = gen.generate(16)
    assert len(pwd) == 16

def test_generate_invalid_length_raises():
    gen = PasswordGenerator(GeneratorPolicy(min_length=15, max_length=32))
    with pytest.raises(ValueError):
        gen.generate(10)

def test_generate_many_count():
    gen = PasswordGenerator()
    pwds = gen.generate_many(16, 5)
    assert len(pwds) == 5
    assert all(len(p) == 16 for p in pwds)

def test_entropy_estimation_positive():
    gen = PasswordGenerator()
    pwd = gen.generate(16)
    assert gen.estimate_entropy_bits(pwd) > 0
