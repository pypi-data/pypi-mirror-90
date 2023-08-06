#
# jomiel-yomiel
#
# Copyright
#  2019-2020 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""
from jomiel_kore.app import App as KoreApp
from jomiel_kore.app import exit_normal
from jomiel_kore.opts import check_if_positive_integer
from yomiel.log import lg


class App(KoreApp):
    """Implements the application."""

    __slots__ = []

    def version_long_packages(self):
        """Return the required package (list) for --version-long."""
        return [
            "jomiel_messages",
            "configargparse",
            "jomiel_comm",
            "jomiel_kore",
            "ruamel.yaml",
            "protobuf",
            "pyzmq",
            "ujson",
        ]

    def run(self):
        """Application entry point; executes the app."""
        from configargparse import get_parser

        parser = get_parser()

        parser.add(
            "uri",
            metavar="<uri>",
            nargs="*",
            help="the URIs to parse",
        )

        parser.add(
            "-o",
            "--output-format",
            help="Print messages in the specified data serialization format",
            choices=["raw", "json", "yaml", "terse"],
            metavar="[raw|json|yaml|terse]",
            default="raw",
        )

        def jomiel_group():
            """Add the jomiel options group."""
            grp = parser.add_argument_group("jomiel")

            grp.add(
                "-r",
                "--router-endpoint",
                help="jomiel router endpoint address to connect to",
                default="tcp://localhost:5514",
                metavar="ADDR",
            )

            grp.add(
                "-t",
                "--connect-timeout",
                help="""Maximum time in seconds that the program should
                        allow the connection to the service to take""",
                type=check_if_positive_integer,
                default=60,
                metavar="TIME",
            )

        jomiel_group()

        def debug_group():
            """Add the debug options group."""
            grp = parser.add_argument_group("debug")

            grp.add(
                "-m",
                "--debug-minify-json",
                help="Minify JSON messages in the logger",
                action="store_true",
            )

        debug_group()

        def auth_group():
            """Add the auth option group."""
            grp = parser.add_argument_group("auth")

            grp.add(
                "--auth-mode",
                help="Select authentication mode",
                choices=["none", "curve", "ssh"],
                metavar="[none|curve|ssh]",
                default="none",
            )

        auth_group()

        def curve_group():
            """Add the auth-curve option group."""
            grp = parser.add_argument_group("auth: curve")

            grp.add(
                "--curve-server-public-key-file",
                help="""Public CURVE certificate key file to use for
                        connecting to jomiel""",
                default=".curve/server.key",
                metavar="FILE",
            )

            grp.add(
                "--curve-client-key-file",
                help="""Secret client CURVE key file to use for connecting
                        to jomiel""",
                default=".curve/client.key_secret",
                metavar="FILE",
            )

        curve_group()

        def ssh_group():
            """Add the auth-ssh option group."""
            grp = parser.add_argument_group("auth: ssh")

            grp.add(
                "--ssh-server",
                help="SSH server to connect to",
                metavar="user@server:port",
            )

            grp.add(
                "--ssh-key-file",
                help="Path to the key file to use",
                metavar="FILE",
            )

            grp.add(
                "--ssh-password",
                help="Password to the SSH server",
                metavar="PASSWD",
            )

            grp.add(
                "--ssh-timeout",
                help="""Time (in seconds) after which no activity will
                        result in the tunnel closing""",
                default=60,
                type=check_if_positive_integer,
                metavar="TIME",
            )

            grp.add(
                "--ssh-paramiko",
                help="Use paramiko instead of pexpect",
                action="store_true",
            )

        ssh_group()

        def dump_terse_response(stdout, media_response):
            """Dump a terse response

            Args:
                stdout (obj): the std output stream to dump the object to
                media_response (obj): the media response object to dump

            """
            stdout.write("---\ntitle: " + media_response.title + "\n")
            stdout.write("quality:\n")

            def get_terse_quality_string():
                """Return terse string for a stream quality."""
                return "  profile: {}\n    width: {}\n    height: {}\n".format(
                    stream_quality.profile,
                    stream_quality.width,
                    stream_quality.height,
                )

            for stream in media_response.stream:
                stream_quality = stream.quality
                quality_string = get_terse_quality_string()
                stdout.write(quality_string)

        def dump_metadata(response):
            """Print the metadata to standard output."""

            def has_stream():
                """Has stream data."""
                return response.media.stream

            def has_image():
                """Has image data."""
                return response.media.image

            if has_stream():
                lg().info("has video")
            elif has_image():
                lg().info("has image")
            else:
                handle_error("unexpected response (empty media lists)")

            from sys import stdout

            if "raw" in opts.output_format:
                stdout.write(str(response.media))
            else:
                if "json" in opts.output_format:
                    from jomiel_comm.formatter import to_json

                    to_json(
                        response.media,
                        minified=opts.debug_minify_json,
                        stream=stdout,
                    )
                elif "yaml" in opts.output_format:
                    from jomiel_comm.formatter import to_yaml

                    to_yaml(response.media, stream=stdout)
                elif "terse" in opts.output_format:
                    dump_terse_response(stdout, response.media)
                else:
                    handle_error(
                        "unexpected --output-format value (%s)"
                        % opts.output_format,
                    )

        def determine_auth_opts():
            """Determine whether auth should be used."""
            from jomiel_comm.auth import auth_opts_new

            rval = None

            if "curve" in opts.auth_mode:
                from jomiel_comm.auth import curve_opts_new

                curve_opts = curve_opts_new(
                    opts.curve_server_public_key_file,
                    opts.curve_client_key_file,
                )

                rval = auth_opts_new(curve=curve_opts)

            elif "ssh" in opts.auth_mode:

                if not opts.ssh_server:
                    handle_error(
                        "argument --ssh-server: conflicting option "
                        "string (None) when used with --auth-mode=ssh",
                    )

                from jomiel_comm.auth import ssh_opts_new

                ssh_opts = ssh_opts_new(
                    opts.ssh_server,
                    opts.ssh_key_file,
                    opts.ssh_password,
                    opts.ssh_timeout,
                    opts.ssh_paramiko,
                )

                rval = auth_opts_new(ssh=ssh_opts)

            return rval

        def main_loop():
            """This is the main loop for the application."""
            input_uri = read_input(opts.uri)
            auth_opts = determine_auth_opts()

            from jomiel_comm.inquiry import (
                connect,
                inquire,
                InquireError,
            )

            try:
                lg().info(
                    "connect to %s (timeout=%d)",
                    opts.router_endpoint,
                    opts.connect_timeout,
                )

                sck = connect(
                    opts.router_endpoint,
                    auth=auth_opts,
                    logger=lg(),
                )

                for uri in input_uri:
                    lg().info("inquire <%s>", uri)

                    resp = inquire(
                        sck,
                        uri,
                        timeout=opts.connect_timeout,
                    )

                    dump_metadata(resp)

            except KeyboardInterrupt:
                sigint()

            except OSError as msg:
                handle_error(msg)

            except InquireError as msg:
                handle_error(msg)

            exit_normal()

        opts = super().parse_opts(parser)
        lg().disabled = "terse" in opts.output_format

        from yomiel.subsys import init

        init()
        main_loop()


def handle_error(msg):
    """Handle an error."""
    lg().disabled = False
    lg().error(msg)
    from jomiel_kore.app import exit_error

    exit_error()


def read_input(nargs):
    """Read input (URIs) from the user.

    Returns:
        list: containing the parsed input URIs

    """
    from jomiel_kore.input import read_input as parse

    try:
        input_uri = parse(validate_uri=True, nargs=nargs)
        if not input_uri:
            handle_error("an input URI was not given")
    except KeyboardInterrupt:
        sigint()
    except ValueError as msg:
        handle_error(msg)
    return input_uri


def sigint():
    """Handle SIGINT."""
    lg().error("signal interrupt")
    exit_normal()


# vim: set ts=4 sw=4 tw=72 expandtab:
