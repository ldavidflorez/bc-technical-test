import urllib.parse
import boto3
from datetime import datetime
import hashlib

print("Loading function")

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")


# Transform file content to md5 hash
def file_to_hash(file_content):
    md5 = hashlib.md5()
    lines = list(line for line in (l.strip() for l in file_content.split("\n")) if line)[:-1]
    string_to_hash = "~".join(list(map(lambda s: s.split("=")[1], lines)))
    md5.update(string_to_hash.encode())
    return md5.hexdigest()


# Get inner file hash
def get_file_hash(file_content):
    hash_line = list(line for line in (l.strip() for l in file_content.split("\n")) if line)[-1]
    file_hash = hash_line.split("=")[-1]
    return file_hash


# Compare two hashes
is_file_correct = lambda generated_hash, file_hash: generated_hash == file_hash


# Function to convert S3 file to dict
def file_to_dict(file_as_string: str) -> dict:
    lines = file_as_string.split("\n")
    preprocessed_lines = list(line for line in (l.strip() for l in lines) if line)
    keys = [kv.split("=")[0] for kv in preprocessed_lines]
    values = [kv.split("=")[1] for kv in preprocessed_lines]
    return {k:v for (k,v) in zip(keys, values)}


# Connect to S3 and read the file
def read_file_from_s3(bucket_name, file_key):
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    file_content = response["Body"].read().decode("utf-8")
    return file_content
    

# Store data in DynamoDB
def store_in_dynamodb(table_name, item):
    table = dynamodb.Table(table_name)
    table.put_item(Item=item)
        
        
def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    # Define table name (can be stored as enviroment variables)
    table_name = "ai-technical-test-luis-david"

    # Get bucket and key
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")
    
    # Get file content
    file_content = read_file_from_s3(bucket, key)
    
    # Get hashes and result comparation
    generated_hash = file_to_hash(file_content)
    file_hash = get_file_hash(file_content)
    are_equal = is_file_correct(generated_hash, file_hash)
    
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
    store_in_dynamodb(table_name, file_content_as_dict)
    
    # Return
    return {"response": "ok"}
              