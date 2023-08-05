Backup Utils
============


[![Build Status](https://drone.oprax.fr/api/badges/Oprax/backup-utils/status.svg)](https://drone.oprax.fr/Oprax/backup-utils)
[![codecov](https://codecov.io/gl/Oprax/backup-utils/branch/master/graph/badge.svg?token=V9T1OFP3JO)](https://codecov.io/gl/Oprax/backup-utils)
[![Documentation Status](https://readthedocs.org/projects/backup-utils/badge/?version=latest)](https://backup-utils.readthedocs.io/en/latest/?badge=latest)
[![PyPI - License](https://img.shields.io/pypi/l/backup-utils.svg)](https://gitlab.com/Oprax/backup-utils/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/backup-utils.svg)](https://pypi.org/project/backup-utils/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/backup-utils.svg)](https://pypi.org/project/backup-utils/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


The goal of this project is to create a front to a backup program like Borg.
Indeed, Borg is a really great tool for backup,
but I always write a bash script to specify directories I want to save.
I also use Rclone to synchronize my backup to a remote.
And finally, I need to backup my database.

There are three steps to backup :
1. Database export
2. Archiving
3. Synchronize

For each step, you can use multiple drivers for multiple tools.
Also if something goes wrong, all Exceptions are catches to send a notification.

By default, database export use **mysql**, archiving **borg**, and synchronize **rclone**.

Visit [documentation](https://backup-utils.readthedocs.io/) for more details.
