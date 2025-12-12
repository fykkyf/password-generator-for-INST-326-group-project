# A dict of all chars typically allowed in passwords
PASSWORD_CHARS = {
    "uppercase": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    "lowercase": list("abcdefghijklmnopqrstuvwxyz"),
    "digits": list("0123456789"),
    "symbols": list("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
}

# list of all chars for convenience
ALL_CHARS = (
    PASSWORD_CHARS["uppercase"]
    + PASSWORD_CHARS["lowercase"]
    + PASSWORD_CHARS["digits"]
    + PASSWORD_CHARS["symbols"]
)
