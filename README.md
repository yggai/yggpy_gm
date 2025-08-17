# yggpy_gm — Python GM/SM2 Utilities (interoperable with yggjs_gm)

## Overview
yggpy_gm is a lightweight Python library focused on China’s GM cryptography, with an emphasis on SM2 public‑key operations. It provides simple building blocks and examples for generating keys and performing encryption/decryption.

This project is designed to interoperate with the JavaScript sibling project yggai/yggjs_gm. Artifacts such as keys, ciphertexts, and message formats are intended to be mutually convertible across Python and JavaScript, enabling real cross‑language workflows (e.g., encrypt in JS, decrypt in Python, and vice versa).

- Language: Python
- Scope: SM2 key utilities and crypto workflows
- Interop: Fully compatible with yggai/yggjs_gm (JS)
- Status: Personal research project

## Relationship to yggai/yggjs_gm
- yggpy_gm (Python) and yggjs_gm (JavaScript) implement compatible SM2 workflows.
- Data produced by one can be consumed by the other when using the same agreed formats (key encoding, IVs/nonces if applicable, and ciphertext encoding).
- Example cross‑language scenario:
  1) Generate an SM2 key pair.
  2) Encrypt in JavaScript using yggjs_gm.
  3) Decrypt in Python using yggpy_gm (see examples below).
- Conversely, you can generate keys and encrypt in Python, then consume the results in JavaScript.

JS sibling repository:
https://github.com/yggai/yggjs_gm

## Features
- SM2 key generation
- SM2 encryption/decryption
- Cross‑language conversion/interop with yggjs_gm
- Ready‑to‑run examples and tests

## Project Structure
- yggpy_gm/ — Library source (e.g., sm2.py)
- examples/ — Minimal scripts demonstrating common tasks:
  - c01_get_sm2_key.py
  - c02_js_encrypt_py_decrypt.py
  - c03_sm2_encrypt_decrypt.py
- tests/ — Basic unit tests (e.g., test_get_key.py, test_sm2.py)
- docs/ — Notes and build/obfuscation docs
- dist/ — Built wheels (if present)
- build.py, setup.py — Packaging/build helpers

## Installation
Option A: From source (editable install)
1) Clone this repository
2) In the project root:
   - pip install -e .

Option B: From a local wheel (if provided under dist/)
- pip install dist/yggpy_gm-0.0.1-py3-none-any.whl

Note: If you encounter dependency issues, please open an issue with your environment details.

## Usage
See the examples directory for end‑to‑end scripts:
- c01_get_sm2_key.py — Generate an SM2 key pair
- c02_js_encrypt_py_decrypt.py — Demonstrates JS→Py interoperability with yggjs_gm
- c03_sm2_encrypt_decrypt.py — Local SM2 encrypt/decrypt in Python

Because function signatures may evolve as this research project iterates, the examples are the most up‑to‑date reference for usage.

## Testing
- Run tests from the project root:
  - pytest

If pytest is not installed:
- pip install pytest

## License
- License: PolyForm Noncommercial License 1.0.0
- Summary: You may use the software for noncommercial purposes only, under the terms of the PolyForm Noncommercial 1.0.0 license.
- Full text: https://polyformproject.org/licenses/noncommercial/1.0.0/

## Author
- Name: 源滚滚
- Email: 1156956636.com

## Contributing
This is a personal research project:
- Pull Requests: Not accepted
- Issues: Welcome — please include clear reproduction steps, versions, and environment details

## Disclaimer
Cryptography is subtle. Use at your own risk. Validate all security assumptions and compliance requirements before using in any product.
