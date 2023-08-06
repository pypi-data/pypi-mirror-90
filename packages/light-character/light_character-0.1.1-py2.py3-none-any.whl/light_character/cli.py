"""Console script for light_character."""
import argparse
import sys
from light_character.light_character import save_characteristic_as_image


def main():
    """Console script for tartan."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'characteristic',
        help='A light characteristic pattern'
    )
    parser.add_argument('--width', default=512, type=int)
    parser.add_argument('--height', default=512, type=int)
    parser.add_argument('--img')
    args = parser.parse_args()
    save_characteristic_as_image(
        args.characteristic, (args.width, args.height),
        sys.stdout.buffer, args.img
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
