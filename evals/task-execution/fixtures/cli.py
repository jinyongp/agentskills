"""Public fixture contract: total nonnegative integer quantities from JSON stdin."""
import json
import sys


def main():
    try:
        values = json.load(sys.stdin)
        if not isinstance(values, list) or any(
            type(value) is not int or value < 0 for value in values
        ):
            raise ValueError('expected an array of nonnegative integers')
        print(json.dumps({'total': sum(values)}))
        return 0
    except (ValueError, TypeError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
