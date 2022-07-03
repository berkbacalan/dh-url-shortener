import random
import string


def generate_short_url():
    short_url = ''.join(random.choice(string.ascii_lowercase) for i in range(6))

    return short_url