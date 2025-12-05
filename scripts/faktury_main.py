"""Faktury (Invoices) main script."""

import time
import sys


def main():
    """Main function for the Faktury application."""
    print("=" * 50)
    print("Faktury Application Started")
    print("=" * 50)
    print()

    counter = 0
    try:
        while True:
            counter += 1
            print(f"[Faktury] Processing invoice batch #{counter}...")
            sys.stdout.flush()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[Faktury] Application stopped by user.")


if __name__ == "__main__":
    main()
