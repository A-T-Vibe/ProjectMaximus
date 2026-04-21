from database.db import get_credits_used, increment_credits, reset_credits_if_new_month
from config import KLING_MONTHLY_CREDIT_LIMIT, HAILUO_MONTHLY_CREDIT_LIMIT, PIKA_MONTHLY_CREDIT_LIMIT
from generators import kling, hailuo, pika

GENERATORS = [
    {"name": "kling",   "module": kling,   "limit": KLING_MONTHLY_CREDIT_LIMIT},
    {"name": "hailuo",  "module": hailuo,  "limit": HAILUO_MONTHLY_CREDIT_LIMIT},
    {"name": "pika",    "module": pika,    "limit": PIKA_MONTHLY_CREDIT_LIMIT},
]


def pick_generator():
    """Return the generator with the most remaining free credits."""
    best = None
    best_remaining = -1

    for g in GENERATORS:
        reset_credits_if_new_month(g["name"])
        info = get_credits_used(g["name"])
        remaining = g["limit"] - info["credits_used"]
        if remaining > best_remaining:
            best_remaining = remaining
            best = g

    if best is None or best_remaining <= 0:
        raise RuntimeError("All generators have exhausted their free credits for this month.")

    return best


def generate_video(prompt):
    """
    Pick the best available generator, generate a video, record credit usage.
    Returns (generator_name, file_path).
    """
    gen = pick_generator()
    print(f"Using generator: {gen['name']}")

    file_path = gen["module"].generate(prompt)
    increment_credits(gen["name"], gen["module"].credits_cost())

    return gen["name"], file_path
