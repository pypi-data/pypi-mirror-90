# pytest-gnupg-fixtures

## Overview

Pytest fixtures to dynamically create [GnuPG](https://www.gnupg.org/) instances for testing.

## Getting Started

Update <tt>setup.py</tt> to include:

```python
setup(
	tests_require=["pytest-gnupg-fixtures"]
)
```

All fixtures should be automatically included via the <tt>pytest11</tt> entry point.
```python
import pytest
from pytest_gnupgfixtures import GnuPGKeypair  # Optional, for typing

def test_custom_signer(gnupg_keypair: GnuPGKeypair):
    custom_signer = CustomSigner(
        keyid=gnupg_keypair.fingerprints[1],
        passphrase="testing",
        homedir=gnupg_keypair.gnupg_home,
    )
    assert "PGP SIGNATURE" in custom_signer.sign("my data")
```

* Tested with python 3.8

## Installation
### From [pypi.org](https://pypi.org/project/pytest-gnupg-fixtures/)

```
$ pip install pytest_gnupg_fixtures
```

### From source code

```bash
$ git clone https://github.com/crashvb/pytest-gnupg-fixtures
$ cd pytest-gnupg-fixtures
$ virtualenv env
$ source env/bin/activate
$ python -m pip install --editable .[dev]
```

## Fixtures

### <a name="gnupg_gen_key_conf"></a> gnupg_gen_key_conf

Provides the path to a GnuPG script file that is used to generate a temporary keypair. If a user-defined script (<tt>tests/gnupg_gen_key.conf</tt>) can be located, it is used. Otherwise, an embedded script is copied to temporary location and returned. This fixture is used by the [gnupg_keypair](#gnupg_keypair) fixture.

### <a name="gnupg_keypair"></a> gnupg_keypair

Provides a keypair within a temporary GnuPG trust store.

#### NamedTuple Fields

The following fields are defined in the tuple provided by this fixture:

* **fingerprints** - A list of key fingerprints. Typically pubkey, subkey...
* **gen_key_conf** - from [gnupg_gen_key_conf](#gnupg_gen_key_conf)
* **gnupg_home** - from [gnupg_trust_store](#gnupg_trust_store)
* **keyid** - The public key id of the temporary keypair.

Typing is provided by `pytest_gnupg_fixtures.GnuPGKeypair`.


### <a name="gnupg_trust_store"></a> gnupg_trust_store

Provides a temporary, initialized, GnuPG trust store that is contains no keys. This fixture is used by the [gnupg_keypair](#gnupg_keypair) fixture.

#### NamedTuple Fields

The following fields are defined in the tuple provided by this fixture:

* **gnupg_home** - The path to the temporary trust store.

Typing is provided by `pytest_gnupg_fixtures.GnuPGTrustStore`.


## <a name="limitations"></a>Limitations

1. This has been coded to work with gpg2.
2. The generated keypair is very simple. TBD if this will be expanded to support a more realistic configuration.

## Changelog

### 0.1.1 (2021-01-06)

* Bug Fix: Correct package_data.

### 0.1.1 (2021-01-06)

* Initial release.

## Development

[Source Control](https://github.com/crashvb/pytest-gnupg-fixtures)
