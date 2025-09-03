import ctypes
import math
import os
import shutil
import platform
from utils.constants import BYTE_TO_MB


def clear_folder(folder_path):
    for entry in os.listdir(folder_path):
        # get the path to the file/subfolder
        entry_path = os.path.join(folder_path, entry)
        try:
            if os.path.isdir(entry_path):
                # if this entry is a subdirectory, remove it and its content
                shutil.rmtree(entry_path)
            elif os.path.isfile(entry_path) or os.path.islink(entry_path):
                # if this entry is a file or a symbolic link, just remove it
                os.unlink(entry_path)
        except Exception as e:
            print(f"Failed to delete {entry_path}. Reason: {e}") 

import os

def get_file_size_on_disk_posix(path: str) -> int:
    """Gets the disk space occupied by a certain file (on a drive on LINUX or MAC)

    Args:
        path (str): the path to the file

    Raises:
        ValueError: if the path does not correspond to a file 
        
    Returns:
        int: the disk space in MB
    """
    if not os.path.isfile(path):
        raise ValueError(f"Not a file: {path}")
    
    stat_result = os.stat(path)
    return stat_result.st_blocks * 512 * BYTE_TO_MB

def get_file_size_on_disk_windows(path: str) -> int :
    """Gets the disk space ocupied by a certain file (on a drive on a windows system)

    Args:
        path (str): the path to the file

    Raises:
        ValueError: if the path does not correspond to a file

    Returns:
        int: the disk space in MB
    """
    if not os.path.isfile(path):
        raise ValueError(f"Not a file: {path}")
    
    # find the allocation_unit_size which is the minimal size that a file can take on the disk (depends on filesystem formatting)
    allocation_unit_size = _get_allocation_unit_size_windows(path)
    # find the logical size of the file depending on the data inside
    file_size = os.path.getsize(path)

    # calculate the size on disk. It's a multiple of the allocation_unit_size (it needs to be whole and bigger than the logical file size)
    file_size_in_alloc_units = file_size / allocation_unit_size
    size_on_disk = math.ceil(file_size_in_alloc_units) * allocation_unit_size

    return size_on_disk * BYTE_TO_MB

def _get_allocation_unit_size_windows(path: str):
    """
    Returns the allocation unit size of the drive containing 'path'
    """
    # get the window's kernel library
    kernel32: ctypes.WinDLL = ctypes.windll.kernel32

    # Extract drive root (e.g., "C:\\")
    drive = os.path.splitdrive(os.path.abspath(path))[0] + '\\'

    # prepare output variables for GetDiskFreeSpaceW() API call to write values to
    sectors_per_alloc_unit = ctypes.c_ulong()
    bytes_per_sector = ctypes.c_ulong()
    free_alloc_units = ctypes.c_ulong()
    total_alloc_units = ctypes.c_ulong()

    # Call the windows API to get the values we want
    result = kernel32.GetDiskFreeSpaceW(
        ctypes.c_wchar_p(drive),
        ctypes.byref(sectors_per_alloc_unit),
        ctypes.byref(bytes_per_sector),
        ctypes.byref(free_alloc_units),
        ctypes.byref(total_alloc_units)
    )

    # raise an error if the API call failed
    if result == 0:
        raise ctypes.WinError()

    # return the size of an allocation unit
    return sectors_per_alloc_unit.value * bytes_per_sector.value

def get_file_size_on_disk(path: str) -> int:
    """Cross-platform: returns size on disk for a file, accounting for actual disk usage.

    Args:
        path (str): the path to the file

    Raises:
        NotImplementedError: if the OS is not supported

    Returns:
        int: the size of the file in MB
    """
    system = platform.system()
    if system == 'Windows':
        return get_file_size_on_disk_windows(path)
    elif system in ('Linux', 'Darwin'):  # Darwin = macOS
        return get_file_size_on_disk_posix(path)
    else:
        raise NotImplementedError(f"Unsupported OS: {system}")