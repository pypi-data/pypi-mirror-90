import os
import copy

from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_this, run_cdo
import warnings


def to_nc(self, out, zip=True, overwrite=False):
    """
    Save a dataset to a named file
    This will only work with single file datasets.

    Parameters
    -------------
    out : str
        Output file name.
    zip : boolean
        True/False depending on whether you want to zip the file. Default is True.
    overwrite : boolean
        If out file exists, do you want to overwrite it? Default is False.
    """

    # If you are trying to overwrite a file in self.current, cdo cannot simultaneously have it opened and written to
    if out in self and (overwrite is True):
        self.run()

    if type(self.current) is list:
        ff = copy.deepcopy(self.current)
    else:
        ff = [copy.deepcopy(self.current)]

    # Figure out if it is possible to write the file, i.e. if a dataset is still an
    # ensemble, you cannot write.
    write = False

    if type(self.current) is str:
        write = True

    if self._merged:
        write = True

    if write is False:
        raise ValueError("You cannot save multiple files!")

    # Check if outfile exists and overwrite is set to False
    # This should maybe be a warning, not an error
    if (os.path.exists(out)) and (overwrite is False):
        raise ValueError("The out file exists and overwrite is set to false")

    if len(self.history) == len(self._hold_history):
        if zip:
            cdo_command = f"cdo -z zip_9 copy {ff[0]} {out}"
            run_cdo(cdo_command, target=out, overwrite=overwrite)

            self.history.append(cdo_command)
            self._hold_history = copy.deepcopy(self.history)
            self.current = out

        else:
            cdo_command = f"cdo copy {ff[0]} {out}"
            run_cdo(cdo_command, target=out, overwrite=overwrite)
            self.history.append(cdo_command)
            self._hold_history = copy.deepcopy(self.history)

            self.current = out

    else:
        if zip:
            cdo_command = "cdo -z zip_9 "
        else:
            cdo_command = "cdo "

        self._execute = True

        run_this(cdo_command, self, out_file=out)
        self._execute = False

    if os.path.exists(out) is False:
        raise ValueError("File zipping was not successful")

    self.current = out

    cleanup()
