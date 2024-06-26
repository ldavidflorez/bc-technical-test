import json
import boto3


# Load AWS credentials from a JSON file
def load_credentials(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return json.load(f)


# Function to convert S3 file to dict
def file_to_dict(file_as_string: str) -> dict:
    lines = file_as_string.split("\n")
    preprocessed_lines = list(line for line in (l.strip() for l in lines) if line)
    keys = [kv.split("=")[0] for kv in preprocessed_lines]
    values = [kv.split("=")[1] for kv in preprocessed_lines]
    return {k:v for (k,v) in zip(keys, values)}


# Connect to S3 and read the file
def read_file_from_s3(bucket_name: str, file_key: str, credentials: str) -> str:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=credentials["aws_access_key_id"],
        aws_secret_access_key=credentials["aws_secret_access_key"],
        region_name=credentials["region_name"]
    )
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response["Body"].read().decode("utf-8")
        return file_content
    except Exception as e:
        print(f"Error reading file from S3: {e}")
        return None


# Delete S3 file
def delete_file_from_s3(bucket_name: str, file_key: str, credentials: str):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=credentials["aws_access_key_id"],
        aws_secret_access_key=credentials["aws_secret_access_key"],
        region_name=credentials["region_name"]
    )

    try:
        s3.delete_object(Bucket=bucket_name, Key=file_key)
        return "ok"
    except Exception as e:
        return "ko"
        
        
# Store data in DynamoDB
def store_in_dynamodb(table_name: str, item: dict, credentials: dict):
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=credentials["aws_access_key_id"],
        aws_secret_access_key=credentials["aws_secret_access_key"],
        region_name=credentials["region_name"]
    )
    table = dynamodb.Table(table_name)
    try:
        table.put_item(Item=item)
        print("Item successfully stored in DynamoDB.")
    except Exception as e:
        print(f"Error storing item in DynamoDB: {e}")


# if __name__ == "__main__":
#     # File paths and names
#     credentials_file_path = "../files/credentials.json"
#     bucket_name = "ai-technical-test-luis-david"
#     file_key = "my-file.txt"
#     table_name = "ai-technical-test-luis-david"
#     function_name = "ai-technical-test-luis-david"

#     # Load credentials
#     credentials = load_credentials(credentials_file_path)
    
#     # Read file from S3
#     file_content = read_file_from_s3(bucket_name, file_key, credentials)
    
#     # Create PK (timestamp) for DynamoDB table
#     timestamp = datetime.now().timestamp() * 1000
    
#     # Transform file content to dict format
#     file_content_as_dict = file_to_dict(file_content)
    
#     # Add PK
#     file_content_as_dict["timestamp"] = str(timestamp)
    
#     # Store the item in DynamoDB
#     store_in_dynamodb(table_name, file_content_as_dict, credentials)
    
#     # Delete S3 file
#     result = delete_file_from_s3(bucket_name, file_key, credentials)
