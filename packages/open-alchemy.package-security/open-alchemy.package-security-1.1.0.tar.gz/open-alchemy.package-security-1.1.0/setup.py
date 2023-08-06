# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['open_alchemy', 'open_alchemy.package_security']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.47,<2.0.0', 'pytest>=6.2.1,<7.0.0']

entry_points = \
{'pytest11': ['open_alchemy_package_security = '
              'open_alchemy.package_security.pytest_plugin']}

setup_kwargs = {
    'name': 'open-alchemy.package-security',
    'version': '1.1.0',
    'description': 'Security helper for the OpenAlchemy package service',
    'long_description': '# Security\n\nPerforms calculations for creating pubic and secret keys. A credential is made\nup of a public and secret key, a salt and a hash of the secret key that is safe\nto store.\n\n## Service Secret\n\nFor certain operations, such as the creation of secret keys, a service secret\nis retrieved which required access to AWS secrets manager.\n\n## Create\n\nCreate a new credential.\n\nInput:\n\n- `sub`: unique identifier for the user.\n\nOutput:\n\n- `public_key`: a unique public identifier for the key,\n- `secret_key`: a secret key for the public key,\n- `salt`: a random value used to create the credential and\n- `secret_key_hash`: a value derived from the secret key that is safe to store.\n\n## Retrieve Secret\n\nRe-calculates the secret key based on known values.\n\nInput:\n\n- `sub` and\n- `salt`.\n\nOutput:\n\n- `secret_key`.\n\n## Calculate Secret Hash\n\nCalculate the secret key has for a secret.\n\nInput:\n\n- `secret_key` and\n- `salt`.\n\nOutput:\n\n- `secret_key_hash`.\n\n## Compare Secret Hashes\n\nSafely compare two secret key hashes\n\nInput:\n\n- `left`: a `secret_key_hash` and\n- `right`: a `secret_key_hash`.\n\nOutput:\n\n- Whether `left` == `right`.\n\nAlgorithm:\n\n1. use <https://docs.python.org/3/library/hmac.html#hmac.compare_digest> to\n   compare the secret key hashes.\n\n## Salt\n\nA salt is a random string generated using\n<https://docs.python.org/3/library/secrets.html#secrets.token_bytes>.\n\n## Public Key\n\nThe public key is a hash based on the `sub` of the user and a salt. The\nfollowing algorithm is used:\n\n1. create a message by combining the `sub` and a random salt created using\n   <https://docs.python.org/3/library/secrets.html#secrets.token_bytes>,\n1. digest the message using `sha256` using\n   <https://docs.python.org/3/library/hashlib.html#hash-algorithms>\n   and\n1. convert to string using\n   <https://docs.python.org/3/library/base64.html#base64.urlsafe_b64encode>\n   decoding and and pre-pending it with `pk_`.\n\n## Secret Key\n\nThe secret key is a hash based on the `sub`, `salt` and a secret associated\nwith the service. The following algorithm is used:\n\n1. retrieve the service secret,\n1. create a message by combining `sub`, `salt` and the service secret,\n1. digest the message using `sha256` using\n   <https://docs.python.org/3/library/hashlib.html#hash-algorithms>\n   and\n1. convert to string using\n   <https://docs.python.org/3/library/base64.html#base64.urlsafe_b64encode>\n   decoding and and pre-pending it with `sk_`.\n\n## Secret Key Hash\n\nThe secret key itself is not stored but a value that is derived from it but\nhard to reverse is. The following function is used to calculate it:\n<https://docs.python.org/3/library/hashlib.html#hashlib.scrypt>\nwhere:\n\n- `password` is the `secret_key`,\n- `salt` is the credential salt,\n- `n` is `2 ** 14`,\n- `r` is 8 and\n- `p` is 1.\n\n## CI-CD\n\nThe workflow is defined here:\n[../.github/workflows/ci-cd-security.yaml](../.github/workflows/ci-cd-security.yaml).\n\nThere are a few groups of jobs in the CI-CD:\n\n- `test`: runs the tests for the package in supported python versions,\n- `build`: builds the security package,\n- `deploy`: deploys security infrastructure to AWS,\n- `release-required`: determines whether a release to PyPI is required and\n- `release`: a combination of deploying to test and production PyPI and\n  executing tests on the published packages\n\n### `test`\n\nExecutes the tests defined at [tests](tests).\n\n### `build`\n\nBuilds the security package defined at [.](.).\n\n### `release-required`\n\nHas 2 outputs:\n\n- `result`: whether a release to PyPI is required based on the latest released\n  version and the version configured in the project and\n- `project-version`: the version configured in the code base.\n\n### `deploy`\n\nDeploys the CloudFormation stack for the security defined at\n[../infrastructure/lib/security-stack.ts](../infrastructure/lib/security-stack.ts).\n\n### `release`\n\nIf the `result` output from `release-required` is true, the package is deployed\nto both test and production PyPI.\n\nIrrespective of whether the release was executed, the version of the package\ndefined in the code base is installed from both test and production PyPI and\nthe tests defined at [../test/security/tests](../test/security/tests) are\nexecuted against the deployed infrastructure on AWS.\n\n## Periodic Production Tests\n\nThe workflow is defined here:\n[../.github/workflows/production-test-security.yaml](../.github/workflows/production-test-security.yaml).\n\nExecutes the tests defined at [../test/security/tests](../test/security/tests)\nagainst a configured version of the package and against the currently deployed\ninfrastructure on AWS.\n\n## Pytest Plugin\n\nA pytest plugin is made available to make testing easier. It is defined at\n[open_alchemy/package_security/pytest_plugin.py](open_alchemy/package_security/pytest_plugin.py).\n\n### Fixtures\n\nAll fixtures that have an effect but yield `None` are prefixed with `_` so that\ntools like pylint do not complain about unused arguments for test functions.\n\n#### `service_secret`\n\nConfigures the package to use a dummy service secret and yields it.\n\n#### `_service_secret`\n\nThe same as `service_secret` except that it is prefix with a leading `_`.\n',
    'author': 'David Andersson',
    'author_email': 'jdkandersson@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
