# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awsflock']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.47,<2.0.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['awsflock = awsflock:cli']}

setup_kwargs = {
    'name': 'awsflock',
    'version': '0.2.0',
    'description': 'Simple locking in AWS',
    'long_description': '# AWS flock\n\n`flock`-like functionality for applications in AWS, using dynamodb as a\nbackend for synchronization.\n\nA CLI tool as simple as the classic `flock` command.\n\n## Use Cases\n\n- Synchronizing multiple automated jobs across workers in AWS\n- Writing scripts that only one human operator can be running at a time (e.g.\n  production deployment tools with terraform, CFN, etc)\n- Synchronizing jobs in non-AWS systems (e.g. GitHub Actions) using AWS\n  credentials\n\n## Usage\n\nFull usage info can be found with\n\n```bash\nawsflock --help\n```\n\nCreate the table in DynamoDB in order to start using `awsflock`:\n\n```bash\nawsflock table-create\n```\n\nAcquire a lock, with a 15 minute expiration, and get the lock `LEASE_ID`:\n\n```bash\nLEASE_ID="$(awsflock acquire LockFoo --lease-duration \'15 minutes\')"\n```\n\nRenew the lock, getting back the new `LEASE_ID` and reducing the expiration\nwindow to 5 minutes, specified in seconds:\n\n```bash\nLEASE_ID="$(awsflock renew LockFoo "$LEASE_ID" --lease-duration \'300s\')"\n```\n\nRelease the lock, so that others may use it:\n\n```bash\nawsflock release LockFoo "$LEASE_ID"\n```\n\nAttempt to acquire another lock, but don\'t block and wait for it to be\nacquired:\n\n```bash\nLEASE_ID="$(awsflock acquire LockBar --no-wait)"\nif [ $? -eq 0 ]; then\n  # lock acquired ...\nelse\n  # lock not acquired ...\nfi\n```\n\n## Behavior / Model\n\nLocks are held for a limited period of time.\nAfter that time, if not renewed, the lock expires and another worker may reclaim\nthe lock.\nWhile the lock is held, the worker holding it has a "lease" on the lock, proven\nby a given `LEASE_ID`.\nA `LEASE_ID` can be used to "renew" or "release" a given lock.\n\n`awsflock` requires a table in DynamoDB to store active locks.\nBy default, the table name is `awsflock`, but custom names can be used.\nYou must create the table before locks can be used (it will never be created\nautomatically).\nLocks are identified by name, and those names are unique keys into the\n`awsflock` table.\n\nLocks have a limited lifetime (default: 2 hours) if not explicitly released,\nafter which they may be "reclaimed" by anyone trying to acquire that lock.\n\n> **NOTE:**\n> Local clock time is compared against lock expirations to determine whether\n> or not reclamation may be tried. The default reclamation window (5 seconds)\n> is more than sufficient for most use-cases, but assumes that your clocks\n> are synchronized by NTP or a similar protocol. Usage where clocks cannot be\n> trusted may result in incorrect lock reclamations.\n\nWhen you acquire a lock, you get back a `LEASE_ID`. The `LEASE_ID` can then be\nused to renew the lock or release it. In this way, locks are held by a single\nowner for a limited period of time, and the `LEASE_ID` constitutes proof of\nownership.\n\n## CHANGELOG\n\n### 0.2.0\n\n* More advanced parsing of durations\n\n### 0.1.1\n\n* Minor fixup\n\n### 0.1.0\n\n* Initial release\n',
    'author': 'Stephen Rosen',
    'author_email': 'sirosen@globus.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
