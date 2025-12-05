"""Zlecenia (Orders) main script."""

import time
import sys


def main():
    """Main function for the Zlecenia application."""
    print("=" * 50)
    print("Zlecenia Application Started")
    print("=" * 50)
    print()

    counter = 0
    try:
        while True:
            counter += 1
            print(f"[Zlecenia] Processing order batch #{counter}...")
            sys.stdout.flush()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[Zlecenia] Application stopped by user.")


if __name__ == "__main__":
    main()
