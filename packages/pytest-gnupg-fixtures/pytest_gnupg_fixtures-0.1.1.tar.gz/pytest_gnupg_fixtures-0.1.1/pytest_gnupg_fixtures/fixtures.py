#!/usr/bin/env python

# pylint: disable=redefined-outer-name

"""The actual fixtures, you found them ;)."""

import logging
import re
import shutil
import subprocess

from pathlib import Path
from typing import Generator, List, NamedTuple

import pytest

from _pytest.tmpdir import TempPathFactory

from .utils import get_embedded_file, get_user_defined_file

LOGGER = logging.getLogger(__name__)


class GnuPGKeypair(NamedTuple):
    # pylint: disable=missing-class-docstring
    fingerprints: List[str]
    gen_key_conf: Path
    gnupg_home: Path
    keyid: str


class GnuPGTrustStore(NamedTuple):
    # pylint: disable=missing-class-docstring
    gnupg_home: Path


@pytest.fixture()
def gnupg_gen_key_conf(
    pytestconfig: "_pytest.config.Config", tmp_path_factory: TempPathFactory
) -> Generator[Path, None, None]:
    """Provides the location of the GnuPG script to generate a temporary keypair."""
    name = "gnupg-gen-key.conf"
    yield from get_user_defined_file(pytestconfig, name)
    yield from get_embedded_file(tmp_path_factory, name=name)


@pytest.fixture
def gnupg_keypair(
    gnupg_gen_key_conf: Path, gnupg_trust_store: GnuPGTrustStore
) -> GnuPGKeypair:
    """Provides a keypair within a temporary GnuPG trust store."""

    LOGGER.debug("Initializing GPG keypar ...")
    environment = {"HOME": "/dev/null"}
    result = subprocess.run(
        [
            "gpg",
            "--batch",
            "--homedir",
            str(gnupg_trust_store.gnupg_home),
            "--gen-key",
            "--keyid-format",
            "long",
            str(gnupg_gen_key_conf),
        ],
        capture_output=True,
        check=True,
        env=environment,
    )
    keyid = re.findall(
        r"gpg: key (\w+) marked as ultimately trusted", result.stderr.decode("utf-8")
    )[0]
    # LOGGER.debug("  keyid        : %s", keyid)

    result = subprocess.run(
        [
            "gpg",
            "--fingerprint",
            "--fingerprint",  # Double --fingerprint needed for subkeys
            "--homedir",
            str(gnupg_trust_store.gnupg_home),
            "--with-colons",
            str(keyid),
        ],
        capture_output=True,
        check=True,
        env=environment,
    )
    # Fingerprint order: pubkey [, subkey ]...
    fingerprints = re.findall(r"fpr:{9}(\w+):", result.stdout.decode("utf-8"))
    LOGGER.debug("  Fingerprints:")
    for fingerprint in fingerprints:
        LOGGER.debug("    %s", fingerprint)

    yield GnuPGKeypair(
        fingerprints=fingerprints,
        gen_key_conf=gnupg_gen_key_conf,
        gnupg_home=gnupg_trust_store.gnupg_home,
        keyid=keyid,
    )


@pytest.fixture
def gnupg_trust_store(request, tmp_path_factory: TempPathFactory) -> GnuPGTrustStore:
    """Provides a temporary, initialized, GnuPG trust store."""

    # https://github.com/isislovecruft/python-gnupg/issues/137#issuecomment-459043779
    tmp_path = tmp_path_factory.mktemp("gnupg_trust_store")
    LOGGER.debug("Initializing GPG home: %s ...", tmp_path)
    tmp_path.chmod(0o0700)

    path = tmp_path.joinpath("gpg-agent.conf")
    with path.open("w") as file:
        file.write("allow-loopback-pinentry\n")
        file.write("max-cache-ttl 60\n")
    path.chmod(0o600)

    def _stop_gpg_agent():
        LOGGER.debug("Stopping gpg-agent ...")
        subprocess.run(
            [
                "/usr/bin/gpg-connect-agent",
                "--homedir",
                str(tmp_path),
                "--no-autostart",
                "killagent",
                "/bye",
            ],
            check=False,
        )

    request.addfinalizer(_stop_gpg_agent)

    yield GnuPGTrustStore(gnupg_home=tmp_path)
    shutil.rmtree(tmp_path, ignore_errors=True)
