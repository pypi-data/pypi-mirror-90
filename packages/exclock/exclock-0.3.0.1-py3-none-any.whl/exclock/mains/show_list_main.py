from exclock.util import get_clock_basenames


def main() -> None:
    for basename in get_clock_basenames():
        print(basename)
