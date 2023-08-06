import atexit
import glob
import copy
import multiprocessing as mp
import os
import pandas as pd
import random
import re
import string
import subprocess
import warnings
import urllib.request
import platform

from netCDF4 import Dataset

from nctoolkit.cleanup import cleanup, clean_all, temp_check
from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_cdo
from nctoolkit.session import nc_protected, session_info, nc_safe
from nctoolkit.show import (
    nc_variables,
    nc_years,
    nc_months,
    nc_levels,
    nc_times,
    nc_format,
)
from nctoolkit.temp_file import temp_file


# context manager code so that thredds checks will be stopped if slow
import signal
import time
from contextlib import contextmanager


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException(
            "Timed out. Connecting to the thredds server is very slow!"
        )

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


# A custom format for warnings.
def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + "\n"


warnings.formatwarning = custom_formatwarning

# set up the session info
letters = string.ascii_lowercase
session_info["stamp"] = (
    "nctoolkit" + "".join(random.choice(letters) for i in range(8)) + "nctoolkit"
)
session_info["temp_dir"] = "/tmp/"
session_info["user_dir"] = False
session_info["thread_safe"] = False
session_info["lazy"] = False
session_info["precision"] = None

if platform.system() == "Linux":
    result = os.statvfs("/tmp/")
    session_info["size"] = result.f_frsize * result.f_bavail
else:
    session_info["size"] = 0


session_info["latest_size"] = 0
session_info["cores"] = 1

# register clean_all to clean temp files on exit
atexit.register(clean_all)

# run temp_check to see if any files are held over from previous sessions
temp_check()


def is_url(x):
    regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    return re.match(regex, x) is not None


def options(**kwargs):
    """
    Define session options.
    Set the options in the session. Available options are thread_safe and lazy.
    Set thread_safe = True if hdf5 was built to be thread safe.
    Set lazy = True if you want methods to evaluate lazy by default.

    Parameters
    ---------------
    **kwargs
        Define options using key, value pairs.

    """

    valid_keys = [
        "thread_safe",
        "lazy",
        "cores",
        "precision",
        "user",
        "password",
        "temp_dir",
    ]

    for key in kwargs:
        if key not in valid_keys:
            raise AttributeError(key + " is not a valid option")
        if type(kwargs[key]) is not bool:
            if key == "temp_dir":
                if type(kwargs[key]) is str:
                    if os.path.exists(kwargs[key]) == False:
                        raise ValueError("The temp_dir specified does not exist!")
                    session_info[key] = os.path.abspath(kwargs[key])
                    session_info["user_dir"] = True
                return None

            if key == "cores":
                if type(kwargs[key]) is int:
                    if kwargs[key] > mp.cpu_count():
                        raise ValueError(
                            str(kwargs[key])
                            + " is greater than the number of system cores ("
                            + str(mp.cpu_count())
                            + ")"
                        )
                    session_info[key] = kwargs[key]
                else:
                    raise TypeError("cores must be an int")
            else:
                if key == "precision":
                    if kwargs[key] not in ["I8", "I16", "I32", "F32", "F64"]:
                        raise ValueError("precision supplied is not valid!")
                    session_info[key] = kwargs[key]
                else:
                    raise AttributeError(key + " is not valid session info!")
        else:
            session_info[key] = kwargs[key]


def convert_bytes(num):
    """
    A function to make file size human readable
    """
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if num < 1000.0:
            return str(num) + " " + x
        num /= 1000.0


def file_size(file_path):
    """
    A function to return file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return file_info.st_size


def open_data(x=None, suppress_messages=False, checks=False, **kwargs):
    """
    Read netcdf data as a DataSet object

    Parameters
    ---------------
    x : str or list
        A string or list of netcdf files or a single url. The function will check the
        files exist. If x is not a list, but an iterable it will be converted to a list.
        If a url is given the file will be downloaded before processing.
        If a *.nc style wildcard is supplied, open_data will use all files available.
    thredds : boolean
        Are you accessing a thredds server? Must end with .nc.
    checks: boolean
        Do you want basic checks to ensure cdo can read files?
    """
    #from nctoolkit.temp_file import temp_file

    if type(x) is str:
        if x.endswith("*.nc"):
            x = glob.glob(x)

    thredds = False

    ftp_details = None
    wait = None
    file_stop = None
    for key in kwargs:
        if key == "thredds":
            thredds = kwargs[key]
        if key == "ftp_details":
            ftp_details = kwargs[key]
        if key == "wait":
            wait = kwargs[key]
        if key == "file_stop":
            file_stop = kwargs[key]

    # make sure data has been supplied
    if x is None:
        raise ValueError("No data was supplied!")

    # coerce an iterable to a list
    if type(x) is not str:
        x = [y for y in x]
        for ff in x:
            if type(ff) is not str:
                raise TypeError("You have not supplied an iterable made of file paths!")

    if type(x) is list:
        if len(x) == 1:
            x = x[0]

    # check the files provided exist
    stop_time = 10000000000000000000000000000000000
    if wait is not None:
        stop_time = min(wait, stop_time)
    if file_stop is not None:
        stop_time = min(file_stop, stop_time)

    if type(x) is str:
        if os.path.exists(x) is False:

            if is_url(x):

                if thredds is False:
                    new_x = temp_file(".nc")
                    print(f"Downloading {x}")
                    print("\033[A                             \033[A")

                    if ftp_details is not None and x.startswith("ftp"):
                        user = ftp_details["user"]
                        password = ftp_details["password"]
                        x = x.replace("ftp://", f"ftp://{user}:{password}@")

                    start = time.time()

                    i = 0

                    search = True
                    while search:
                        if os.path.exists(new_x) == False:
                            try:
                                # work out if there is a time limit for individual files
                                if stop_time != 10000000000000000000000000000000000:
                                    with time_limit(stop_time):
                                        urllib.request.urlretrieve(x, new_x)
                                else:
                                    urllib.request.urlretrieve(x, new_x)
                            except:
                                nothing = "x"
                        search +=1
                        if os.path.exists(new_x):
                            break

                        if wait is None:
                            if search == 3:
                                break
                        else:
                            end = time.time()
                            if (end - start) > wait:
                                break
                    if os.path.exists(new_x) == False:
                        raise ValueError(f"Could not download {x}")

                    x = new_x
                else:

                    if checks:
                        if wait is not None:
                            with time_limit(stop_time):
                                out = subprocess.run(
                                    "cdo sinfo " + x,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                )
                                if "Open failed" in str(out.stderr):
                                    raise ValueError(f"{x} is not compatible with CDO!")
                        else:
                            out = subprocess.run(
                                "cdo sinfo " + x,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                            )
                            if "Open failed" in str(out.stderr):
                                raise ValueError(f"{x} is not compatible with CDO!")




            else:
                raise ValueError("Data set " + x + " does not exist!")

        if checks:
            out = subprocess.run(
                "cdo sinfo " + x,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if "Open failed" in out.stderr.decode("utf-8"):
                mes = (
                    out.stderr.decode("utf-8")
                    .replace("cdo    sinfo: ", "")
                    .replace("<\n", "")
                    .replace("\n", "")
                )
                mes = re.sub(" +", " ", mes)
                raise ValueError(mes)

        else:
            nc_safe.append(x)
            nc_protected.append(x)

    # it's possible there are duplicates in the data
    # Get rid of them..
    # Note: This will also ensure the original list is deep copied

    if type(x) is list:
        orig_size = len(x)
        x = list(dict.fromkeys(x))
        if len(x) < orig_size:
            warnings.warn(message="Duplicates in data set have been removed!")

    # if type(x) is list:
    #    if len(x) == 1:
    #        x = x[0]

    if type(x) is list:
        if thredds is False:
            if checks:
                if suppress_messages is False:
                    warnings.warn("Performing basic checks on ensemble files")
            if len(x) == 0:
                raise ValueError("You have not provided any files!")

            for ff in x:

                if os.path.exists(ff) is False:
                    raise ValueError("Data set " + ff + " does not exist!")
                else:
                    if checks:
                        out = subprocess.run(
                            "cdo sinfo " + ff,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                        )
                        if "Open failed" in out.stderr.decode("utf-8"):
                            mes = (
                                out.stderr.decode("utf-8")
                                .replace("cdo    sinfo: ", "")
                                .replace("<\n", "")
                                .replace("\n", "")
                            )
                            mes = re.sub(" +", " ", mes)
                            raise ValueError(mes)
                    nc_safe.append(ff)
                    nc_protected.append(x)
        else:
            out = subprocess.run(
                "cdo sinfo " + x[0],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if "Open failed" in str(out.stderr):
                raise ValueError(
                    "First file in the ensemble is not compatible with CDO!"
                )

    # if there is only one file in the list, change it to a single file
    if type(x) is list:
        if len(x) == 1:
            x = x[0]

    d = DataSet(x)
    d._thredds = thredds
    return d


def open_thredds(x=None, wait=None, checks = False):
    """
    Read thredds data as a DataSet object

    Parameters
    ---------------
    x : str or list
        A string or list of thredds urls, which must end with .nc.
    checks : boolean
        Do you want to check if data is available over thredds?
    wait : int
        Time to wait for thredds server to be checked. Limitless if not supplied.

    """

    if type(checks) is not bool:
        raise TypeError("Please provide boolean for checks")

    if wait is not None:
        if type(wait) is not int and float:
            raise TypeError("Please provide an integer for wait!")
        if wait <= 0:
            raise ValueError("Please provide a positive value for wait!")


    if session_info["cores"] > 1:
        warnings.warn(
            message="Using multiple cores on thredds data is volatile. It has therefore been reset to 1."
        )
        session_info["cores"] = 1

    return open_data(x=x, thredds=True, wait=wait, checks = checks)


def open_url(x=None, ftp_details=None, wait=None, file_stop = None):
    """
    Read netcdf data from a url as a DataSet object

    Parameters
    ---------------
    x : str
        A string with a url. Prior to processing data will be downloaded to
        a temp folder.
    ftp_details : dict
        A dictionary giving the user name and password combination for ftp downloads: {"user":user, "password":pass}
    wait : int
        Time to wait, in seconds, for data to download. A minimum of 3 attempts will be made to download the data.
    file_stop : int
        Time limit, in minutes, for individual attempts at downloading data. This is useful to get around download freezes.

    """

    if wait is not None:
        if type(wait) is not int:
            raise TypeError("Please provide a valid wait!")

        if wait <= 0:
            raise TypeError("Please provide a valid wait!")

    if file_stop is not None:
        if type(file_stop) is not int:
            raise TypeError("Please provide a valid file_stop!")

        if file_stop <= 0:
            raise TypeError("Please provide a valid file_stop!")


    if ftp_details is not None:
        if len(ftp_details) != 2:
            raise ValueError("ftp_details is not a 2 element dictionary")

        user = ftp_details[list(ftp_details.keys())[0]]
        password = ftp_details[list(ftp_details.keys())[1]]
        new_dict = {"user": user, "password": password}
    else:
        new_dict = None

    return open_data(x=x, ftp_details=new_dict, wait = wait, file_stop = file_stop)


def merge(*datasets, match=["day", "year", "month"]):
    """
    Merge datasets

    Parameters
    -------------
    datasets: kwargs
        Datasets to merge.
    match: list
        Temporal matching criteria. This is a list which must be made up of a subset of
        day, year, month. This checks that the datasets have compatible times.
        For example, if you want to ensure the datasets have the same years, then use
        match = ["year"].
    """
    all_files = []
    for dataset in datasets:
        if ("DataSet" in str(type(dataset))) is False:
            raise TypeError("Please check everything is a DataSet object!")
        # make sure everything has been evaluated
        dataset.run()
        if type(dataset.current) is str:
            all_files += [dataset.current]
        else:
            all_files += dataset.current
    result = open_data(all_files)
    result.merge(match=match)
    return result


def cor_time(x=None, y=None):
    """
    Calculate the temporal correlation coefficient between two datasets
    This will calculate the temporal correlation coefficient, for each time step,
    between two datasets. The datasets must either have the same variables or only
    have one variable.

    Parameters
    -------------
    x: dataset
        First dataset to use
    y: dataset
        Second dataset to use
    """

    if ("DataSet" in str(type(x))) is False:
        raise TypeError("Please check x is a dataset")

    if ("DataSet" in str(type(y))) is False:
        raise TypeError("Please check y is a dataset")
        # make sure everything has been evaluated

    x.run()
    y.run()

    a = x.copy()
    b = y.copy()

    if x.variables != y.variables:
        if len(x.variables) > 1 or len(y.variables) > 1:
            raise ValueError(
                "This method currently only works with single variable datasets or "
                "datasets with identical variables!"
            )

    target = temp_file("nc")

    if len(x.variables) == 1:
        command = (
            "cdo -setname,cor -timcor " + a.current + " " + b.current + " " + target
        )
    else:
        command = "cdo -timcor " + a.current + " " + b.current + " " + target

    target = run_cdo(command, target=target)

    data = open_data(target)

    return data


def cor_space(x=None, y=None):
    """
    Calculate the spatial correlation coefficient between two datasets
    This will calculate the spatial correlation coefficient, for each time step,
    between two datasets. The datasets must either have the same variables or only
    have one variable.

    Parameters
    -------------
    x: dataset
        First dataset to use
    y: dataset
        Second dataset to use
    """

    if ("DataSet" in str(type(x))) is False:
        raise TypeError("Please check x is a dataset")

    if ("DataSet" in str(type(y))) is False:
        raise TypeError("Please check y is a dataset")
        # make sure everything has been evaluated

    x.run()
    y.run()

    a = x.copy()
    b = y.copy()

    if x.variables != y.variables:
        if len(x.variables) > 1 or len(y.variables) > 1:
            raise ValueError(
                "This method currently only works with single variable datasets "
                "or datasets with identical variables!"
            )

    target = temp_file("nc")

    if len(x.variables) == 1:
        command = (
            "cdo -setname,cor -fldcor " + a.current + " " + b.current + " " + target
        )
    else:
        command = "cdo -fldcor " + a.current + " " + b.current + " " + target

    target = run_cdo(command, target=target)

    data = open_data(target)

    return data


class DataSet(object):
    """
    A modifiable ensemble of netcdf files
    """

    def __init__(self, start=""):
        """Initialize the starting file name etc"""
        # Attribuates of interest to users
        self.history = []
        self.start = start
        self._current = start

        # attributes to the module, but not users (probably)
        if session_info["lazy"]:
            self._execute = False
        else:
            self._execute = True
        self._hold_history = []
        self._merged = False
        self._safe = []
        # some trackers to make end of the chain processing easier
        self._thredds = False
        self._zip = False
        self._format = None
        # track number of held over commands
        self._ncommands = 0

    def __getitem__(self, index):
        if type(self.current) is str:
            return self.current

        return self.current[index]

    def __len__(self):
        if type(self.current) is str:
            return 1

        return len(self.current)

    def __iter__(self):
        if type(self.current) is str:
            yield self.current
            return
        if type(self.current) is list:
            for ff in self.current:
                yield ff
            return

    # def __repr__(self):
    #    # tidy up the output first
    #    if isinstance(self.start, list):
    #        start = str(len(self.start)) + " member ensemble"
    #    if type(self.start) == str:
    #        start = self.start

    #    if isinstance(self.current, list):
    #        current = str(len(self.current)) + " member ensemble"
    #    if type(self.current) == str:
    #        current = self.current

    #    return (
    #        "<nctoolkit.DataSet>:\nstart: "
    #        + start
    #        + "\ncurrent: "
    #        + current
    #        + "\noperations: "
    #        + str(len(self.history))
    #    )

    def __repr__(self):
        if isinstance(self.current, list):
            current = str(len(self.current)) + " member ensemble"
        if type(self.current) == str:
            current = self.current

        variables = []
        for ff in self:
            for vv in nc_variables(ff):
                if vv not in variables:
                    variables.append(vv)

        return (
            "<nctoolkit.DataSet>:\nFiles: "
            + current
            + "\n"
            + "Variables: "
            + str_flatten(variables)
        )

    @property
    def size(self):
        """The size of an object
        This will print the number of files, total size, and smallest and largest files
        in an DataSet object.
        """
        if type(self.current) is str:
            result = "Number of files: 1\n"
            result = result + "File size: " + convert_bytes(file_size(self.current))
            return result
        else:
            all_sizes = []

            smallest_file = ""
            largest_file = ""
            min_size = 1e15
            max_size = -1

            for ff in self:

                all_sizes.append(file_size(ff))

                if file_size(ff) > max_size:
                    max_size = file_size(ff)
                    largest_file = ff

                if file_size(ff) < min_size:
                    min_size = file_size(ff)
                    smallest_file = ff

            min_size = convert_bytes(min_size)
            max_size = convert_bytes(max_size)

            sum_size = convert_bytes(sum(all_sizes))
            result = "Number of files in ensemble: " + str(len(self.current)) + "\n"
            result = result + "Ensemble size: " + sum_size + "\n"
            result = (
                result
                + "Smallest file: "
                + smallest_file
                + " has size "
                + min_size
                + "\n"
            )
            result = result + "Largest file: " + largest_file + " has size " + max_size
            return result

    @property
    def variables(self):
        """
        List variables contained in a dataset
        """

        all_variables = []
        for ff in self:
            all_variables += nc_variables(ff)

        all_variables = list(set(all_variables))

        all_variables.sort()

        return all_variables

    @property
    def months(self):
        """
        List months contained in a dataset
        """

        all_months = []
        for ff in self:
            all_months += nc_months(ff)

        all_months = list(set(all_months))

        all_months.sort()

        return all_months

    @property
    def levels(self):
        """
        List levels contained in a dataset
        """

        all_levels = []
        for ff in self:
            all_levels += nc_levels(ff)

        all_levels = list(set(all_levels))

        all_levels.sort()

        return all_levels

    @property
    def times(self):
        """
        List times contained in a dataset
        """

        all_times = []
        for ff in self:
            all_times += nc_times(ff)

        all_times = list(set(all_times))

        all_times.sort()

        return all_times

    @property
    def ncformat(self):
        """
        List formats of files contained in a dataset
        """

        all_formats = []
        for ff in self:
            all_formats += nc_format(ff)

        all_formats = list(set(all_formats))

        all_formats.sort()

        return all_formats

    @property
    def years(self):
        """
        List years contained in a dataset
        """

        all_years = []
        for ff in self:
            all_years += nc_years(ff)

        all_years = list(set(all_years))

        all_years.sort()

        return all_years

    @property
    def variables_detailed(self):
        """
        Detailed list of variables contained in a dataset.
        This will only display the variables in the first file of an ensemble.
        """

        if type(self.current) is list:
            return (
                "This DataSet object is a list. Please inspect individual"
                "files using nc_variables"
            )

        cdo_result = subprocess.run(
            "cdo showname " + self.current,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        cdo_result = (
            str(cdo_result.stdout)
            .replace("b'", "")
            .replace("\\n", "")
            .replace("'", "")
            .strip()
        )
        cdo_result = cdo_result.split()
        dataset = Dataset(self.current)

        longs = None
        units = None
        if "long_name" in str(dataset.variables[cdo_result[0]]):
            longs = [dataset.variables[x].long_name for x in cdo_result]
        if "units" in str(dataset.variables[cdo_result[0]]):
            units = [dataset.variables[x].units for x in cdo_result]

        if longs is None and units is None:
            return cdo_result

        out = subprocess.run(
            "cdo sinfon " + self.current,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out = out.stdout.decode("utf-8")
        out = out.split("\n")
        out_inc = ["Grid coordinates :" in ff for ff in out]
        var_det = []
        i = 1
        while True:
            if out_inc[i]:
                break
            i += 1
            var_det.append(out[i - 1])

        var_det = [ff.replace(":", "") for ff in var_det]
        var_det = [" ".join(ff.split()) for ff in var_det]
        var_det = [
            ff.replace("Parameter name", "variable").split(" ") for ff in var_det
        ]
        sales = var_det[1:]
        labels = var_det[0]
        df = pd.DataFrame.from_records(sales, columns=labels)
        df = df.loc[:, ["Levels", "Points", "variable"]]
        df = df.rename(columns={"Levels": "levels", "Points": "points"})

        df = pd.DataFrame({"variable": cdo_result}).merge(df)

        if longs is not None:
            df["long_name"] = longs
        if units is not None:
            df["units"] = units

        df = df.assign(levels=lambda x: x.levels.astype("int")).assign(
            points=lambda x: x.points.astype("int")
        )

        return df

    @property
    def start(self):
        """
        The starting file or files of the DataSet object
        """
        return self._start

    @start.setter
    def start(self, value):
        if type(value) is str:
            self._start = value
        if isinstance(value, list):
            self._start = value

    @property
    def current(self):
        """
        The current file or files in the DataSet object
        """
        return self._current

    @current.setter
    def current(self, value):
        for ff in self:
            if ff in nc_safe:
                nc_safe.remove(ff)

        if type(value) is str:
            nc_safe.append(value)
            self._current = value
        if isinstance(value, list):
            if len(value) > 1:
                self._current = value
            else:
                self._current = value[0]
            for ff in value:
                nc_safe.append(ff)

    @property
    def history(self):
        """
        The history of operations on the DataSet
        """
        return self._history

    @history.setter
    def history(self, value):
        self._history = value

    def copy(self):
        """
        Make a deep copy of an DataSet object
        """
        self.run()

        new = copy.deepcopy(self)
        if type(new.current) is str:
            nc_safe.append(new.current)
        else:
            for ff in new:
                nc_safe.append(ff)
        return new

    def __del__(self):
        for ff in self:
            if ff in nc_safe:
                nc_safe.remove(ff)
        for ff in self._safe:
            if ff in nc_safe:
                nc_safe.remove(ff)

        cleanup()

    @start.deleter
    def start(self):
        raise AttributeError("You cannot delete the start point")

    # import the methods

    from nctoolkit.add_etc import add
    from nctoolkit.add_etc import subtract
    from nctoolkit.add_etc import multiply
    from nctoolkit.add_etc import divide

    from nctoolkit.anomaly import annual_anomaly
    from nctoolkit.anomaly import monthly_anomaly

    from nctoolkit.append import append

    from nctoolkit.cdo_command import cdo_command
    from nctoolkit.cellareas import cell_areas

    from nctoolkit.centres import centre

    from nctoolkit.cleanup import disk_clean

    from nctoolkit.compare import compare_all

    from nctoolkit.corr import cor_space
    from nctoolkit.corr import cor_time

    from nctoolkit.crop import crop



    from nctoolkit.delete import remove_variables

    from nctoolkit.ensembles import ensemble_mean
    from nctoolkit.ensembles import ensemble_max
    from nctoolkit.ensembles import ensemble_min
    from nctoolkit.ensembles import ensemble_range
    from nctoolkit.ensembles import ensemble_sum

    from nctoolkit.ensembles import ensemble_percentile
    from nctoolkit.expr import mutate
    from nctoolkit.expr import transmute
    from nctoolkit.expr import sum_all

    from nctoolkit.fldstat import spatial_mean
    from nctoolkit.fldstat import spatial_min
    from nctoolkit.fldstat import spatial_max
    from nctoolkit.fldstat import spatial_range
    from nctoolkit.fldstat import spatial_sum
    from nctoolkit.fldstat import spatial_percentile

    from nctoolkit.format import format

    from nctoolkit.inttime import time_interp
    from nctoolkit.inttime import timestep_interp

    from nctoolkit.masking import mask_box

    from nctoolkit.mergers import merge_time
    from nctoolkit.mergers import merge

    from nctoolkit.meridonials import meridonial_mean
    from nctoolkit.meridonials import meridonial_min
    from nctoolkit.meridonials import meridonial_max
    from nctoolkit.meridonials import meridonial_range



    from nctoolkit.nco_command import nco_command

    from nctoolkit.phenology import phenology
    #from nctoolkit.phenology import initiation

    from nctoolkit.plot import plot

    from nctoolkit.reduce import reduce_dims

    from nctoolkit.reduce_grid import reduce_grid

    from nctoolkit.regrid import regrid

    from nctoolkit.release import run

    from nctoolkit.rename import rename

    from nctoolkit.resample import resample_grid

    from nctoolkit.rollstat import rolling_mean
    from nctoolkit.rollstat import rolling_min
    from nctoolkit.rollstat import rolling_max
    from nctoolkit.rollstat import rolling_range
    from nctoolkit.rollstat import rolling_sum



    from nctoolkit.select import select_variables
    from nctoolkit.select import select_timesteps
    from nctoolkit.select import select_seasons
    from nctoolkit.select import select_months
    from nctoolkit.select import select_years
    from nctoolkit.select import select

    from nctoolkit.setters import set_date
    from nctoolkit.setters import set_missing
    from nctoolkit.setters import set_units
    from nctoolkit.setters import set_longnames

    from nctoolkit.shift import shift_hours
    from nctoolkit.shift import shift_days
    from nctoolkit.shift import shift_months
    from nctoolkit.shift import shift_years
    from nctoolkit.shift import shift

    from nctoolkit.split import split

    from nctoolkit.strip_vars import strip_variables

    from nctoolkit.time_stat import mean
    from nctoolkit.time_stat import percentile
    from nctoolkit.time_stat import max
    from nctoolkit.time_stat import median
    from nctoolkit.time_stat import min
    from nctoolkit.time_stat import range
    from nctoolkit.time_stat import variance
    from nctoolkit.time_stat import stdev
    from nctoolkit.time_stat import sum
    from nctoolkit.time_stat import cum_sum

    from nctoolkit.temporal_stat import tmean
    from nctoolkit.temporal_stat import tpercentile
    from nctoolkit.temporal_stat import tmax
    from nctoolkit.temporal_stat import tmedian
    from nctoolkit.temporal_stat import tmin
    from nctoolkit.temporal_stat import trange
    from nctoolkit.temporal_stat import tvariance
    from nctoolkit.temporal_stat import tstdev
    from nctoolkit.temporal_stat import tsum
    from nctoolkit.temporal_stat import tcumsum

    from nctoolkit.to_lonlat import to_latlon

    from nctoolkit.to_nc import to_nc

    from nctoolkit.toxarray import to_xarray
    from nctoolkit.toxarray import to_dataframe

    from nctoolkit.verticals import vertical_mean
    from nctoolkit.verticals import vertical_min
    from nctoolkit.verticals import vertical_max
    from nctoolkit.verticals import vertical_range
    from nctoolkit.verticals import vertical_sum
    from nctoolkit.verticals import vertical_cumsum
    from nctoolkit.verticals import surface
    from nctoolkit.verticals import vertical_interp
    from nctoolkit.verticals import bottom
    from nctoolkit.verticals import bottom_mask
    from nctoolkit.verticals import invert_levels



    from nctoolkit.zip import zip

    from nctoolkit.zonals import zonal_mean
    from nctoolkit.zonals import zonal_min
    from nctoolkit.zonals import zonal_max
    from nctoolkit.zonals import zonal_range

    # deprecated stuff

    from nctoolkit.deprecated import clip

    from nctoolkit.deprecated import release
    from nctoolkit.deprecated import select_timestep
    from nctoolkit.deprecated import select_season
    from nctoolkit.deprecated import write_nc
    from nctoolkit.deprecated import var
    from nctoolkit.deprecated import cum_sum
    from nctoolkit.deprecated import vertical_cum_sum
    from nctoolkit.deprecated import view

    from nctoolkit.deprecated import daily_mean
    from nctoolkit.deprecated import daily_min
    from nctoolkit.deprecated import daily_max
    from nctoolkit.deprecated import daily_range
    from nctoolkit.deprecated import daily_sum

    from nctoolkit.deprecated import daily_mean_climatology
    from nctoolkit.deprecated import daily_min_climatology
    from nctoolkit.deprecated import daily_max_climatology
    from nctoolkit.deprecated import daily_range_climatology

    from nctoolkit.deprecated import monthly_mean
    from nctoolkit.deprecated import monthly_min
    from nctoolkit.deprecated import monthly_max
    from nctoolkit.deprecated import monthly_sum
    from nctoolkit.deprecated import monthly_range
    from nctoolkit.deprecated import monthly_mean_climatology
    from nctoolkit.deprecated import monthly_min_climatology
    from nctoolkit.deprecated import monthly_max_climatology
    from nctoolkit.deprecated import monthly_range_climatology
    from nctoolkit.deprecated import annual_mean
    from nctoolkit.deprecated import annual_min
    from nctoolkit.deprecated import annual_max
    from nctoolkit.deprecated import annual_range
    from nctoolkit.deprecated import annual_sum
    from nctoolkit.deprecated import seasonal_mean
    from nctoolkit.deprecated import seasonal_min
    from nctoolkit.deprecated import seasonal_max
    from nctoolkit.deprecated import seasonal_range

    from nctoolkit.deprecated import seasonal_mean_climatology
    from nctoolkit.deprecated import seasonal_min_climatology
    from nctoolkit.deprecated import seasonal_max_climatology
    from nctoolkit.deprecated import seasonal_range_climatology
