from modules.file import *
from modules.aws import *

if __name__ == "__main__":
    # Set variables
    credentials_file_path = "files/credentials.json"
    bucket_name = "ai-technical-test-luis-david"
    file_key = "my-file.txt"
    table_name = "ai-technical-test-luis-david"
    
    # Load credentials
    credentials = load_credentials(credentials_file_path)
    
    # Read file from S3
    file_content = read_file_from_s3(bucket_name, file_key, credentials)
    
    # Print readed file from S3
    print("S3 file content: ")
    print(f"{file_content}")
    
    # Get hashes and result comparation
    generated_hash = file_to_hash(file_content)
    file_hash = get_file_hash(file_content)
    are_equal = is_file_correct(generated_hash, file_hash)
    
    # Print results
    print(f"Generated hash: {generated_hash}")
    print(f"File hash: {file_hash}")
    print(f"Are equal? R\ {are_equal}\n")
    
    # Create PK (timestamp) for DynamoDB table
    timestamp = str(datetime.now().timestamp() * 1000)
    
    # Transform file content to dict format
    file_content_as_dict = file_to_dict(file_content)
    
    # Add PK, hashes and correct status
    file_content_as_dict["timestamp"] = timestamp
    file_content_as_dict["generatedHash"] = generated_hash
    file_content_as_dict["fileHash"] = file_hash
    file_content_as_dict["isFileCorrect"] = are_equal
    
    # Store the item in DynamoDB
    store_in_dynamodb(table_name, file_content_as_dict, credentials)