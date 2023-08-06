
import pandas as pd

# cache
import pkg_resources
DEATHS = pkg_resources.resource_filename(__name__, "data/deaths.csv")
x = None


def read_deaths():
    """Read cache."""
    global x
    if x is None:
        x = pd.read_csv(DEATHS)
    return x

def write_deaths(deaths):
    """Write cache."""
    global x
    deaths.to_csv(DEATHS, index = False)
    x = deaths

__all__ = ["read_deaths","write_deaths"]