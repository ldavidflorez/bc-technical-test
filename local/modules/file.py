import hashlib


# Get file content (for local test)
def get_file_content(file_path: str) -> list:
    with open(file_path, "r") as file:
        return file.read()


# Transform file content to md5 hash
def file_to_hash(file_content: str) -> str:
    md5 = hashlib.md5()
    lines = list(line for line in (l.strip() for l in file_content.split("\n")) if line)[:-1]
    string_to_hash = "~".join(list(map(lambda s: s.split("=")[1], lines)))
    md5.update(string_to_hash.encode())
    return md5.hexdigest()


# Get inner file hash
def get_file_hash(file_content: str) -> str:
    hash_line = list(line for line in (l.strip() for l in file_content.split("\n")) if line)[-1]
    file_hash = hash_line.split("=")[-1]
    return file_hash


# Compare two hashes
is_file_correct = lambda generated_hash, file_hash: generated_hash == file_hash


if __name__ == "__main__":
    # Set file path
    file_path = "../files/my-file.txt"

    # Check functions
    file_content = get_file_content(file_path)
    generated_hash = file_to_hash(file_content)
    file_hash = get_file_hash(file_content)
    are_equal = is_file_correct(generated_hash, file_hash)

    # Print results
    print(f"Generated hash: {generated_hash}")
    print(f"File hash: {file_hash}")
    print(f"Are equal? R\ {are_equal}")
