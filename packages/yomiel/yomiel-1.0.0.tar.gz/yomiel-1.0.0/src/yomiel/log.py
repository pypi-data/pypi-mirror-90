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


def lg():
    """Returns the logger instance used to print to the logging
    subsystem to record new events.

    The subsystem is configured via a separate logger YAML configuration
    file. The configuration supports different logger identities.

    To use this function (lg):

        from jomiel import lg
        lg().debug('foo=%s' % foo)

    Returns
        The logger instance

    """
    from yomiel.cache import opts
    import logging as lg

    return lg.getLogger(opts.logger_ident)


# vim: set ts=4 sw=4 tw=72 expandtab:
