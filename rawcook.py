"""Rawcookfood utility functions and CLI"""

import argparse
from typing import Dict

def cooked_weight_from_raw(raw_portion: float, raw_total: float, cooked_total: float) -> float:
    """Return cooked weight equivalent for a given raw portion."""
    if raw_total == 0:
        raise ValueError("raw_total must be non-zero")
    return raw_portion * cooked_total / raw_total


def per_ingredient_portion(
    raw_weights: Dict[str, float],
    cooked_total: float,
    portion_weight: float,
) -> Dict[str, float]:
    """Return weight of each ingredient in a cooked portion."""
    total_raw = sum(raw_weights.values())
    if total_raw == 0:
        raise ValueError("Total raw weight must be non-zero")
    ratio_cooked_to_raw = cooked_total / total_raw
    cooked_weights = {
        name: weight * ratio_cooked_to_raw for name, weight in raw_weights.items()
    }
    portion_ratio = portion_weight / cooked_total
    return {name: weight * portion_ratio for name, weight in cooked_weights.items()}


def parse_ingredients(pairs):
    result = {}
    for pair in pairs:
        if ':' not in pair:
            raise argparse.ArgumentTypeError(
                f"Ingredient '{pair}' must be in name:weight format"
            )
        name, weight = pair.split(':', 1)
        try:
            result[name] = float(weight)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(
                f"Invalid weight for ingredient '{name}'"
            ) from exc
    return result


def main():
    parser = argparse.ArgumentParser(description="Calculate raw/cooked food weights")
    subparsers = parser.add_subparsers(dest="command", required=True)

    single = subparsers.add_parser("single", help="Single ingredient conversions")
    single.add_argument("raw_total", type=float, help="Total raw weight cooked")
    single.add_argument("cooked_total", type=float, help="Total cooked weight")
    group = single.add_mutually_exclusive_group(required=True)
    group.add_argument("--raw", type=float, help="Raw portion to convert to cooked")
    group.add_argument("--cooked", type=float, help="Cooked portion to convert to raw")

    multi = subparsers.add_parser("multi", help="Multiple ingredient portions")
    multi.add_argument(
        "--ingredient",
        "-i",
        action="append",
        required=True,
        help="Ingredient as name:weight",
    )
    multi.add_argument(
        "cooked_total",
        type=float,
        help="Total cooked weight of the mixed dish",
    )
    multi.add_argument(
        "portion_weight",
        type=float,
        help="Portion weight of cooked dish",
    )

    args = parser.parse_args()
    if args.command == "single":
        if args.raw is not None:
            cooked = cooked_weight_from_raw(args.raw, args.raw_total, args.cooked_total)
            print(f"{args.raw}g raw -> {cooked:.2f}g cooked")
        else:
            raw = cooked_weight_from_raw(args.cooked, args.cooked_total, args.raw_total)
            print(f"{args.cooked}g cooked -> {raw:.2f}g raw")
    elif args.command == "multi":
        ingredients = parse_ingredients(args.ingredient)
        portion = per_ingredient_portion(
            ingredients, args.cooked_total, args.portion_weight
        )
        for name, weight in portion.items():
            print(f"{name}: {weight:.2f}g")


if __name__ == "__main__":
    main()
