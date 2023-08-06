# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['open_alchemy', 'open_alchemy.package_security']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.47,<2.0.0']

setup_kwargs = {
    'name': 'open-alchemy.package-security',
    'version': '1.0.4',
    'description': 'Security helper for the OpenAlchemy package service',
    'long_description': '# Security\n\nPerforms calculations for creating pubic and secret keys. A credential is made\nup of a public and secret key, a salt and a hash of the secret key that is safe\nto store.\n\n## Service Secret\n\nFor certain operations, such as the creation of secret keys, a service secret\nis retrieved which required access to AWS secrets manager.\n\n## Create\n\nCreate a new credential.\n\nInput:\n\n- `sub`: unique identifier for the user.\n\nOutput:\n\n- `public_key`: a unique public identifier for the key,\n- `secret_key`: a secret key for the public key,\n- `salt`: a random value used to create the credential and\n- `secret_key_hash`: a value derived from the secret key that is safe to store.\n\n## Retrieve Secret\n\nRe-calculates the secret key based on known values.\n\nInput:\n\n- `sub` and\n- `salt`.\n\nOutput:\n\n- `secret_key`.\n\n## Calculate Secret Hash\n\nCalculate the secret key has for a secret.\n\nInput:\n\n- `secret_key` and\n- `salt`.\n\nOutput:\n\n- `secret_key_hash`.\n\n## Compare Secret Hashes\n\nSafely compare two secret key hashes\n\nInput:\n\n- `left`: a `secret_key_hash` and\n- `right`: a `secret_key_hash`.\n\nOutput:\n\n- Whether `left` == `right`.\n\nAlgorithm:\n\n1. use <https://docs.python.org/3/library/hmac.html#hmac.compare_digest> to\n   compare the secret key hashes.\n\n## Salt\n\nA salt is a random string generated using\n<https://docs.python.org/3/library/secrets.html#secrets.token_bytes>\n.\n\n## Public Key\n\nThe public key is a hash based on the `sub` of the user and a salt. The\nfollowing algorithm is used:\n\n1. create a message by combining the `sub` and a random salt created using\n   <https://docs.python.org/3/library/secrets.html#secrets.token_bytes>,\n1. digest the message using `sha256` using\n   <https://docs.python.org/3/library/hashlib.html#hash-algorithms>\n   and\n1. convert to string using\n   <https://docs.python.org/3/library/base64.html#base64.urlsafe_b64encode>\n   decoding and and pre-pending it with `pk_`.\n\n## Secret Key\n\nThe secret key is a hash based on the `sub`, `salt` and a secret associated\nwith the service. The following algorithm is used:\n\n1. retrieve the service secret,\n1. create a message by combining `sub`, `salt` and the service secret,\n1. digest the message using `sha256` using\n   <https://docs.python.org/3/library/hashlib.html#hash-algorithms>\n   and\n1. convert to string using\n   <https://docs.python.org/3/library/base64.html#base64.urlsafe_b64encode>\n   decoding and and pre-pending it with `sk_`.\n\n## Secret Key Hash\n\nThe secret key itself is not stored but a value that is derived from it but\nhard to reverse is. The following function is used to calculate it:\n<https://docs.python.org/3/library/hashlib.html#hashlib.scrypt>\nwhere:\n\n- `password` is the `secret_key`,\n- `salt` is the credential salt,\n- `n` is `2 ** 14`,\n- `r` is 8 and\n- `p` is 1.\n',
    'author': 'David Andersson',
    'author_email': 'jdkandersson@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
