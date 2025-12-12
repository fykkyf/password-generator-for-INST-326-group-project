from __future__ import annotations
import secrets
import math
from dataclasses import dataclass
from typing import Dict, List, Optional
from password_dictionary import PASSWORD_CHARS


@dataclass
class GeneratorPolicy:
    # basic policy for password
    min_length: int = 15
    max_length: int = 32
    require_upper: bool = True
    require_lower: bool = True
    require_digit: bool = True
    require_symbol: bool = True

class PasswordGenerator:

    def __init__(self, policy: Optional[GeneratorPolicy] = None, pools: Optional[Dict[str, str]] = None):
        self.policy = policy or GeneratorPolicy()
        self.pools = pools or PASSWORD_CHARS
        self._allowed_chars = self._build_allowed_chars()

    # build the allowed character pool based on current policy
    def _build_allowed_chars(self) -> str:
        """Build the allowed character pool based on current policy."""

        def flatten(pool) -> list[str]:
            # pool can be list[str] or str
            if pool is None:
                return []
            if isinstance(pool, str):
                return list(pool)
            return list(pool)  # handles list/tuple/set

        chars: list[str] = []

        if self.policy.require_upper:
            chars.extend(flatten(self.pools.get("uppercase")))
        if self.policy.require_lower:
            chars.extend(flatten(self.pools.get("lowercase")))
        if self.policy.require_digit:
            chars.extend(flatten(self.pools.get("digits", "0123456789")))
        if self.policy.require_symbol:
            chars.extend(flatten(self.pools.get("symbols")))

        return "".join(chars)

    # Update policy fields
    def set_policy(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if hasattr(self.policy, k):
                setattr(self.policy, k, v)
        self._allowed_chars = self._build_allowed_chars()

    # Raise ValueError if length violates policy bounds
    def validate_length(self, length: int) -> None:
        if length < self.policy.min_length or length > self.policy.max_length:
            raise ValueError(f"length must be in [{self.policy.min_length}, {self.policy.max_length}]")

    # Return one required char per enabled category
    def required_characters(self) -> List[str]:
        required = []
        if self.policy.require_upper:
            required.append(secrets.choice(self.pools["uppercase"]))
        if self.policy.require_lower:
            required.append(secrets.choice(self.pools["lowercase"]))
        if self.policy.require_digit:
            required.append(secrets.choice(self.pools.get("digits", "0123456789")))
        if self.policy.require_symbol:
            required.append(secrets.choice(self.pools["symbols"]))
        return required

    # Generate a single password
    def generate(self, length: int) -> str:
        self.validate_length(length)
        if not self._allowed_chars:
            raise ValueError("No allowed characters available. Check policy settings.")

        chars = self.required_characters()
        while len(chars) < length:
            chars.append(secrets.choice(self._allowed_chars))

        secrets.SystemRandom().shuffle(chars)
        return "".join(chars)

    # Generate multiple passwords
    def generate_many(self, length: int, count: int) -> List[str]:
        if count <= 0:
            raise ValueError("count must be > 0")
        return [self.generate(length) for _ in range(count)]
    # Rough entropy estimate: log2(pool_size^len) = len * log2(pool_size)
    def estimate_entropy_bits(self, password: str) -> float:
        pool_size = max(len(self._allowed_chars), 1)
        return len(password) * math.log2(pool_size)

    # Return a description
    def explain_policy(self) -> str:
        flags = []
        if self.policy.require_upper: flags.append("upper")
        if self.policy.require_lower: flags.append("lower")
        if self.policy.require_digit: flags.append("digit")
        if self.policy.require_symbol: flags.append("symbol")
        return (
            f"Length: {self.policy.min_length}-{self.policy.max_length}, "
            f"Required: {', '.join(flags) if flags else 'none'}"
        )

