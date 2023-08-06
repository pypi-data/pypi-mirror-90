from nctoolkit.runthis import run_this


def resample_grid(self, factor = None):
    """
    Resample the horizontal grid of a dataset

    Parameters
    -------------
    factor : int
        The resampling factor. Must be a positive integer. No interpolation occurs.
        Example: factor of 2 will sample every other grid cell
    """
    if factor is None:
        raise ValueError("Please provide a resampling factor")

    if type(factor) is not int:
        raise TypeError(f"{factor} is not an integer")

    if factor < 1:
        raise ValueError(f"{factor} is not a postive integer greater than 1")

    cdo_command = f"cdo -samplegrid,{factor}"
    run_this(cdo_command, self, output="ensemble")
