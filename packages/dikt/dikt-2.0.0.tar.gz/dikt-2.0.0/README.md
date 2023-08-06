# Dictionary read on disk

Query items out-of-memory from a dictionary that would take to long to open, or one that doesn't fit in RAM, with Dikt.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


### Installing

You can install the method by typing:
```
pip install dikt
```

### Basic usage

```python
import dikt
import random


# generate a dictionary with 1 million entries
N = 1000000
data = {
    # key can be anything you want
    # values will be "eval"-ed by Python
    "key_" + str(i): list(range(i, i + 100)) for i in range(N)
}

# persist to dictionary using dikt
dikt.dump(data, "data.dikt")
del data

# load file
data = dikt.Dikt("data.dikt")

# get item without loading the whole file in RAM
print(data["key_125"])

# or get multiple items at once (here 10k)
keys = [f"key_" + str(random.randint(0, N - 1)) for i in range(10000)]
print(data[keys][0])
```

## Authors

Maixent Chenebaux