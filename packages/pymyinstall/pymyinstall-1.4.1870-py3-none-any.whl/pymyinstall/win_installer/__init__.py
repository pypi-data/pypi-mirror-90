"""
@file
@breif shortcuts to win_installer
"""

from .pywin32_helper import import_pywin32, fix_pywin32_installation
from .win_exception import WinInstallException
from .win_extract import extract_msi, extract_exe
from .win_setup_r import r_run_script
from .win_setup_main import win_python_setup
from .win_innosetup_helper import inno_install_kernels
from .win_packages import win_install_package_other_python, is_package_installed
from .win_patch import win_patch_paths
from .win_setup_main_checkings import distribution_checkings, import_every_module
