import json
import pytest
import boto3
from datetime import datetime
from ..modules.aws import (
    file_to_dict,
    read_file_from_s3,
    store_in_dynamodb,
    delete_file_from_s3   
)

@pytest.fixture
def load_credentials():
    with open("files/credentials.json", "r") as f:
        return json.load(f)
    
    
@pytest.fixture
def sample_file_content():
    return "totalContactoClientes=250\nmotivoReclamo=25\nmotivoGarantia=10\nmotivoDuda=100\nmotivoCompra=100\nmotivoFelicitaciones=7\nmotivoCambio=8\nhash=2f941516446dce09bc2841da60bf811f\n"

    
def test_file_to_dict(sample_file_content):
    expected_dict = {
        "totalContactoClientes": "250",
        "motivoReclamo": "25",
        "motivoGarantia": "10",
        "motivoDuda": "100",
        "motivoCompra": "100",
        "motivoFelicitaciones": "7",
        "motivoCambio": "8",
        "hash": "2f941516446dce09bc2841da60bf811f"
    }
    result_dict = file_to_dict(sample_file_content)
    assert result_dict == expected_dict


def test_read_file_from_s3(load_credentials, sample_file_content):
    bucket_name = "ai-technical-test-luis-david"
    file_key = "my-file.txt"

    file_content = read_file_from_s3(bucket_name, file_key, load_credentials)
    assert file_content == sample_file_content


def test_delete_file_from_s3_success(load_credentials):
    bucket_name = "ai-technical-test-luis-david"
    file_key = "my-file.txt"
    response = delete_file_from_s3(bucket_name, file_key, load_credentials)
    assert response == "ok"
    
    
def test_delete_file_from_s3_error(load_credentials):
    bucket_name = "ai-technical-test-luis-david"
    file_key = "my-file.txt"
    response = delete_file_from_s3(bucket_name, file_key, load_credentials)
    assert response == "ko"
    
         
def test_store_in_dynamodb(load_credentials):
    table_name = "ai-technical-test-luis-david"
    
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=load_credentials["aws_access_key_id"],
        aws_secret_access_key=load_credentials["aws_secret_access_key"],
        region_name=load_credentials["region_name"]
    )
    
    table = dynamodb.Table(table_name)
    
    item = {
        "timestamp": str(datetime.now().timestamp() * 1000),
        "totalContactoClientes": "250",
        "motivoReclamo": "25",
        "motivoGarantia": "10",
        "motivoDuda": "100",
        "motivoCompra": "100",
        "motivoFelicitaciones": "7",
        "motivoCambio": "8",
        "hash": "2f941516446dce09bc2841da60bf811f"
    }
    store_in_dynamodb(table_name, item, load_credentials)
    
    response = table.get_item(Key={"timestamp": item["timestamp"]})
    assert "Item" in response
    assert response["Item"] == item

if __name__ == "__main__":
    pytest.main()
