import argparse

__version__ = "0.1.0b0"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--version", help="show program version", action="store_true")
    parser.add_argument("-n", "--name", help="output Hello Name! or Hello World!", nargs='?', const='World', type=str)

    # Read arguments from the command line
    args = parser.parse_args()

    # Check for --version or -V
    if args.version:
        print(f"Version-{__version__}")
    if args.name:
        print(f'Hello {str(args.name).title()}!')

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do. Return values are exit codes.


if __name__ == "__main__":
    main()
