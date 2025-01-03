import base64
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def create_signature(
    jwt_header_encoded: str, jwt_payload_encoded: str, private_key: str
) -> str:
    signing_input = f"{jwt_header_encoded}.{jwt_payload_encoded}"
    private_key_obj = load_pem_private_key(private_key.encode(), password=None)
    signature = private_key_obj.sign(
        signing_input.encode(),
        padding.PKCS1v15(),
        hashes.SHA256(),
    )

    return base64.urlsafe_b64encode(signature).decode().strip("=")
