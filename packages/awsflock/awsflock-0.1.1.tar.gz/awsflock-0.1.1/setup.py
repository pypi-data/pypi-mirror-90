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
    'version': '0.1.1',
    'description': 'Simple locking in AWS',
    'long_description': 'AWS flock\n=========\n\n`flock`-like functionality for applications in AWS, using dynamodb as a\nbackend for synchronization.\n\nA simple CLI, on-par with the classic `flock` tool for synchronizing\napplications.\n\nUse Cases\n---------\n\n- Synchronizing multiple automated jobs across workers in AWS\n- Writing scripts that only one human operator can be running at a time (e.g.\n  production deployment tools with terraform, CFN, etc)\n- Synchronizing jobs in non-AWS systems (e.g. GitHub Actions) using AWS\n  credentials\n\nBehavior / Model\n----------------\n\nLocks are held for a limited period of time.\nAfter that time, if not renewed, the lock expires and another worker may reclaim\nthe lock.\nWhile the lock is held, the worker holding it has a "lease" on the lock, proven\nby a given `LEASE_ID`.\nA `LEASE_ID` can be used to "renew" or "release" a given lock.\n\n`awsflock` requires a table in DynamoDB to store active locks.\nBy default, the table name is `awsflock`, but custom names can be used.\nYou must create the table before locks can be used (it will never be created\nautomatically).\nLocks are identified by name, and those names are unique keys into the\n`awsflock` table.\n\nLocks have a limited lifetime (default: 2 hours) if not explicitly released,\nafter which they may be "reclaimed" by anyone trying to acquire that lock.\n\n.. note::\n\n    Local clock time is compared against lock expirations to determine whether\n    or not reclamation may be tried. The default reclamation window (5 seconds)\n    is more than sufficient for most use-cases, but assumes that your clocks\n    are synchronized by NTP or a similar protocol. Usage where clocks cannot be\n    trusted may result in incorrect lock reclamations.\n\nWhen you acquire a lock, you get back a `LEASE_ID`. The `LEASE_ID` can then be\nused to renew the lock or release it. In this way, locks are held by a single\nowner for a limited period of time, and the `LEASE_ID` constitutes proof of\nownership.\n\nUsage\n-----\n\nFull usage info can be found with `awsflock --help`.\n\nAcquire a lock, with a 15 minute expiration, and get the lock `LEASE_ID`:\n\n.. code-block:: bash\n\n    LEASE_ID="$(awsflock acquire LockFoo --expiration 900)"\n\nRenew the lock, getting back the new `LEASE_ID` and reducing the expiration\nwindow to 5 minutes:\n\n.. code-block:: bash\n\n    LEASE_ID="$(awsflock renew LockFoo "$LEASE_ID" --expiration 300)"\n\nRelease the lock, so that others may use it:\n\n.. code-block:: bash\n\n    awsflock release LockFoo "$LEASE_ID"\n\nAttempt to acquire another lock, but don\'t block and wait for it to be\nacquired:\n\n.. code-block:: bash\n\n    LEASE_ID="$(awsflock acquire LockBar --no-wait)"\n    if [ $? -eq 0 ]; then\n      # lock acquired ...\n    else\n      # lock not acquired ...\n    fi\n',
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
