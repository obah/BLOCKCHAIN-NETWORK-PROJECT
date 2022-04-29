from encodings import utf_8
import hashlib
import json

def crypto_hash(*args):
    """
    returns a SHA-256 hash of the given arguments.
    """
    stringified_args = sorted(map(lambda data: json.dumps(data), args))

    joined_data = ''.join(stringified_args)

    return hashlib.sha256(joined_data.encode('utf_8')).hexdigest()

def main():
    print(f"hash of 'one', 1, ['two', 3.5] is: {crypto_hash('one', 1, ['two', 3.5])}")
    print(f"hash of 1, ['two', 3.5], 'one' is: {crypto_hash(1, ['two', 3.5], 'one')}")

if __name__ == "__main__":
    main()
