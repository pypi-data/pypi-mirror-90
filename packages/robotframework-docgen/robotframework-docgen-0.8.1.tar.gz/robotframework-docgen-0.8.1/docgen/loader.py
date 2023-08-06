from robot.libdocpkg import LibraryDocumentation
from docgen import utils


def load(value):
    """Parse library into container, with caching."""
    try:
        with utils.silent():
            return LibraryDocumentation(str(value))
    except (Exception, SystemExit):
        utils.debug_traceback()
        raise ImportError(f"Failed to load library: {value}")
