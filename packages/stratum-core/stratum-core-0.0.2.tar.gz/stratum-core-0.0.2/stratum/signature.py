import time
import ecdsa
from ecdsa import curves
import base64
import hashlib
import json
from exceptions import SignatureVerificationFailed, UnknownSignatureAlgorithm, UnknownSignatureId

_p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
_r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
_b = 0x0000000000000000000000000000000000000000000000000000000000000007
_a = 0x0000000000000000000000000000000000000000000000000000000000000000
_Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
_Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

curve_secp256k1 = ecdsa.ellipticcurve.CurveFp(_p, _a, _b)
generator_secp256k1 = ecdsa.ellipticcurve.Point(curve_secp256k1, _Gx, _Gy, _r)
oid_secp256k1 = (1, 3, 132, 0, 10)
SECP256k1 = ecdsa.curves.Curve("SECP256k1", curve_secp256k1, generator_secp256k1, oid_secp256k1)

# Register SECP256k1 to ecdsa library
curves.curves.append(SECP256k1)


def generate_keypair():
    private_key = ecdsa.SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()

    return private_key, public_key


def load_private_key_pem(filename):
    return ecdsa.SigningKey.from_pem(open(filename, "r").read().strip())


def sign(private_key, data):
    hash = hashlib.sha256(data).digest()
    signature = private_key.sign_digest(hash, sigencode=ecdsa.util.sigdecode_der)
    return base64.b64encode(signature)


def verify(public_key, signature, data):
    hash = hashlib.sha256(data).digest()
    sign = base64.b64decode(signature)
    try:
        return public_key.verify_digest(sign, hash, sigdecode=ecdsa.util.sigdecode_der)
    except:
        return False


def jsonrpc_dumps_sign(private_key, private_key_id, is_request, message_id, method="", params=[], result=None,
                       error=None):
    """Creates the signature for given json-rpc data and returns signed json-rpc text stream"""

    # Build data object to sign
    sign_time = int(time.time())
    data = {"method": method, "params": params, "result": result, "error": error, "sign_time": sign_time}

    # Serialize data to sign and perform signing
    txt = json.dumps(data)
    signature = sign(private_key, txt)

    # Reconstruct final data object and put signature
    if is_request:
        data = {"id": message_id, "method": method, "params": params, "sign": signature,
                "sign_algo": "ecdsa;SECP256k1", "sign_id": private_key_id, "sign_time": sign_time}
    else:
        data = {'id': message_id, 'result': result, 'error': error, 'sign': signature, 'sign_algo': 'ecdsa;SECP256k1',
                'sign_id': private_key_id, 'sign_time': sign_time}

    # Return original data extended with signature
    return json.dumps(data)


def jsonrpc_loads_verify(public_keys, txt):
    """Public keys is mapping (dict) of sign_id -> ecdsa public key
        This method deserialize provided json-encoded data, load signature ID, perform
        the lookup for public key and check stored signature of the message. If signature
        is OK, returns message data
    """

    data = json.loads(txt)
    signature_algo = data["sign_algo"]
    signature_id = data["sign_id"]
    signature_time = data["sign_time"]

    if signature_algo != "ecdsa;SECP256k1":
        raise UnknownSignatureAlgorithm(f"{signature_algo} is not supported")

    try:
        public_key = public_keys[signature_id]
    except KeyError:
        raise UnknownSignatureId(f"Public key for {signature_id} not found")

    signature = data["sign"]
    message_id = data["id"]
    method = data.get("method", "")
    params = data.get("params", [])
    result = data.get("result", None)
    error = data.get("error", None)

    # Build data object to verify
    data = {"method": method, "params": params, "result": result, "error": error, "sign_time": signature_time}
    txt = json.dumps(data)

    if not verify(public_key, signature, txt):
        raise SignatureVerificationFailed("Signature does not match to given data")

    if method:
        # This is a request
        return {"id": message_id, "method": method, "params": params}
    else:
        # This is a response
        return {"id": message_id, "result": result, "error": error}
