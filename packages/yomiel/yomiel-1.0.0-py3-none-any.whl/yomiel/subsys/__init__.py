#
# jomiel-yomiel
#
# Copyright
#  2019 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""


def init():
    """Initiates the application subsystems."""

    from yomiel.subsys import log

    log.init()

    from yomiel.log import lg

    lg().info("all subsystems initiated")


# vim: set ts=4 sw=4 tw=72 expandtab:
