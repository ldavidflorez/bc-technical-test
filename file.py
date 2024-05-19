import hashlib


def file_to_hash(file_path: str) -> str:
    md5 = hashlib.md5()

    with open(file_path, "r") as file:
        lines = list(line for line in (l.strip() for l in file) if line)[:-1]
        string_to_hash = "~".join(list(map(lambda s: s.split("=")[1], lines)))
        md5.update(string_to_hash.encode())

    return md5.hexdigest()


def get_file_hash(file_path: str) -> str:
    with open(file_path, "r") as file:
        hash_line = list(line for line in (l.strip() for l in file) if line)[-1]
        file_hash = hash_line.split("=")[-1]
        return file_hash


is_file_correct = lambda generated_hash, file_hash: generated_hash == file_hash


if __name__ == "__main__":
    file_path = "files/my-file.txt"

    generated_hash = file_to_hash(file_path)
    file_hash = get_file_hash(file_path)
    are_equal = is_file_correct(generated_hash, file_hash)

    print(f"Generated hash: {generated_hash}")
    print(f"File hash: {file_hash}")
    print(f"Are equal? R\ {are_equal}")
