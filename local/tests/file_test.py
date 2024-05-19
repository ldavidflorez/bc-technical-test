import pytest
from ..modules.file import get_file_content, file_to_hash, get_file_hash, is_file_correct


@pytest.fixture
def sample_file_content():
    return "totalContactoClientes=250\nmotivoReclamo=25\nmotivoGarantia=10\nmotivoDuda=100\nmotivoCompra=100\nmotivoFelicitaciones=7\nmotivoCambio=8\nhash=2f941516446dce09bc2841da60bf811f\n"


def test_get_file_content(sample_file_content):
    # Test if get_file_content returns the correct content
    expected_content = sample_file_content
    file_content = get_file_content("files/my-file.txt")
    assert file_content == expected_content


def test_file_to_hash(sample_file_content):
    # Test if file_to_hash generates the correct hash
    expected_hash = "2f941516446dce09bc2841da60bf811f"
    generated_hash = file_to_hash(sample_file_content)
    assert generated_hash == expected_hash


def test_get_file_hash(sample_file_content):
    # Test if get_file_hash retrieves the correct hash
    expected_hash = "2f941516446dce09bc2841da60bf811f"
    file_hash = get_file_hash(sample_file_content)
    assert file_hash == expected_hash


def test_is_file_correct():
    # Test if is_file_correct correctly compares two hashes
    generated_hash = "2f941516446dce09bc2841da60bf811f"
    file_hash = "2f941516446dce09bc2841da60bf811f"
    assert is_file_correct(generated_hash, file_hash) is True

    generated_hash = "wrong_hash"
    file_hash = "abcdef1234567890"
    assert is_file_correct(generated_hash, file_hash) is False
