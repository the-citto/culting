"""Shell."""

import shutil



class Git:
    """Git."""

    def __init__(self) -> None:
        """Init."""
        self.bin = shutil.which("git")



