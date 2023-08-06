# -*- coding: utf-8 -*-

import warnings


__version__ = "0.0.0.git"
try:
    from pkg_resources import get_distribution, DistributionNotFound

    __version__ = get_distribution("tuxbuild").version
except ImportError:
    warnings.warn(
        UserWarning(
            "tuxbuild needs pkg_resources to determine it's own version number, but that is not available"
        )
    )
except DistributionNotFound:
    warnings.warn(UserWarning("tuxbuild not installed, can't determine version number"))
    pass
