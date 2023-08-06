from typing import Final

import pkg_resources

__VERSION__: Final[str] = pkg_resources.get_distribution('exclock').version
