import hashlib
import json

def creează_hash(*argumente):

    """
    Returnează sha-256 hash a informațiilor
    """

    argumente_ = sorted(map(lambda informații: json.dumps(informații),argumente))

    argumente_împreună = ''.join(argumente_)

    return hashlib.sha256(argumente_împreună.encode('utf-8')).hexdigest()


def main():
    pass


if __name__ == '__main__':
    main()
