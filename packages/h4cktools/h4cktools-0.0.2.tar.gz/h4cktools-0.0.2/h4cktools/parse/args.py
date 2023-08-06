__all__ = ["ip_args", "urls_args", "connect_back_args"]


def ip_args(parser, required=True):
    """Add ip arguments to parser
    
    Args:
        parser (argparse.ArgumentParser): user arguments object
    """
    #: Arguments group
    hosts = parser.add_mutually_exclusive_group(required=required)
    hosts.add_argument(
        "-i",
        "--ip", 
        help="Define an ip addresse: [hostname]:[port]",
        metavar="[hostname]:[port]",
        type=str,
    )
    hosts.add_argument(
        "-il",
        "--ip-list",
        help="Path to a list of url: [hostname]:[port] on each line.",
        metavar="file_path",
        type=str,
    )


def urls_args(parser, required=True):
    """Add urls arguments to parser
    
    Args:
        parser (argparse.ArgumentParser): user arguments object
    """
    #: Arguments group
    urls = parser.add_mutually_exclusive_group(required=required)
    urls.add_argument(
        "-u", 
        "--url", 
        help="Define an url: ",
        metavar="[scheme]://[hostname]:[port]",
        type=str,
    )
    urls.add_argument(
        "-ul",
        "--url-list",
        help="Path to an url list: [scheme]://[hostname]:[port] on each line",
        metavar="file_path",
        type=str,
    )


def connect_back_args(parser):
    """Add connect back arguments to parser
    
    Args:
        parser (argparse.ArgumentParser): arguments object
    """
    #: Arguments group
    connect_back = parser.add_argument_group("Connect Back")

    # Set server for connect back
    connect_back.add_argument(
        "-cb", 
        "--connect-back",
        help="Define a server for connect back",
        metavar=["hostname", "port"],
        nargs=2,
    )


def session_args(parser):
    """Add session arguments to parser

    Args:
        parser (argparse.ArgumentParser): user arguments object
    """
    #: Arguments group
    session = parser.add_argument_group("Session")

    # Set custom headers
    session.add_argument(
        "-H", "--headers", metavar="name:value", default=[], nargs="+",
        help="Replace default headers.",
    )

    # Add custom headers
    session.add_argument(
        "-aH", "--add-headers", metavar="name:value", nargs="+",
        help="add header to actual headers "
        "(Useful to set cookies with default headers for exemple).",
    )

    # Set a proxy
    session.add_argument(
        "-x", "--proxy", type=str, help="Use the specified HTTP proxies",
        metavar="[protocol]://[user]:[password]@[proxyhost]:[port]",
    )

    # Threads
    session.add_argument(
        "-T", "--threads", type=int, metavar="nb_threads", default=5,
        help="Define number of concurrent threads.",
    )
    
    # Allow to check ssl certificate check
    session.add_argument(
        "--ssl-check", action="store_true", default=False,
        help="Unauthorize invalid servers certificates.",
    )

    # Set timeout beetween requests
    session.add_argument(
        "-d", "--delay", metavar="seconds", default=0, type=float,
        help="define time delay beetween requests in seconds.",      
    )


def output_args(parser):
    """Add output arguments to parser

    Args:
        parser (argparse.ArgumentParser): user arguments object
    """
    #: Arguments group
    output = parser.add_argument_group("Output")

    output.add_argument(
        "-o", "--output", type=str, metavar="output_path", default="",
        help="output file location",
    )
    output.add_argument(
        "-v", "--verbosity", action="count", default=0, 
        help="Increase verbosity",
    )
    output.add_argument(
        "--no-colors", action="store_true", help="enable colored logging",
    )

   