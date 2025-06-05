# Rawcookfood

Utility to convert raw food weights to cooked weights and calculate ingredient amounts in a portion of a mixed dish.

## Usage

Install Python 3.12 or later. Run the `rawcook.py` script with one of the subcommands below.

### Single ingredient conversion

```
python3 rawcook.py single RAW_TOTAL COOKED_TOTAL --raw RAW_PORTION
```

Outputs the weight of the cooked portion equivalent to `RAW_PORTION` grams of raw ingredient. Use `--cooked` instead of `--raw` to convert a cooked weight back to raw.

Example:

```
python3 rawcook.py single 500 732 --raw 60
```

prints

```
60.0g raw -> 87.84g cooked
```

### Mixed dish portions

Provide each ingredient in `name:weight` format with `-i`/`--ingredient`. Specify the total cooked weight of the finished dish and the desired portion weight.

```
python3 rawcook.py multi -i mushrooms:300 -i chicken:189 -i oil:10 -i milk:200 -i onion:100 640 250
```

This prints the amount of each ingredient in a 250 g cooked portion.
