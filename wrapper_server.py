import base64
import json
import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

app = FastAPI()

AES_KEY = b'12345678901234567890123456789012'
AES_IV = b'abcdefghijklmnop'

def aes_encrypt(plain_text: str) -> str:
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plain_text.encode('utf-8')) + padder.finalize()

    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    return base64.b64encode(encrypted).decode('utf-8')

def aes_decrypt(encrypted_b64: str) -> str:
    encrypted_data = base64.b64decode(encrypted_b64)

    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext.decode('utf-8')

class EncryptedPayload(BaseModel):
    data: str

@app.post("/news")
async def fetch_news(payload: EncryptedPayload):
    try:
        decrypted_json = aes_decrypt(payload.data)
        print("🔹 NewsAPI Request:", decrypted_json)
        params = json.loads(decrypted_json)

        print(params)

        url = "https://newsapi.org/v2/everything"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10)

        print("🔹 NewsAPI Response:", response.text)

        encrypted_response = aes_encrypt(response.text)
        return JSONResponse(
            content={"data": encrypted_response},
            status_code=response.status_code
        )

    except Exception as e:
        print("❌ Exception occurred:", str(e))
        return JSONResponse(
            content={"data": aes_encrypt(str(e))},
            status_code=500
        )