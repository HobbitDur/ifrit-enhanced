import glob
import os
import pathlib
import shutil
import subprocess

DELING_PATH = os.path.join("Resources", "ArchiveManagementCLI")
DELING_LIST_FILES = glob.glob(os.path.join(DELING_PATH, "*"))
DELING_OUTPUT_ROOT_PATH = os.path.join("OutputFiles", "battle")


def unpack(source_path, dest_path):
    os.makedirs(dest_path, exist_ok=True)
    subprocess.run(["Resources/ArchiveManagementCLI/deling-cli.exe", "export", os.path.join(source_path, "battle.fs"), dest_path])


def pack(special_battle_path, dest_path):
    """The deling-cli.exe create the .fl by taking the relative path of where the file is executed,
    which is not good for the "official" .fl file."""
    for file in DELING_LIST_FILES:
        if os.path.isfile(file):
            shutil.copy(file, DELING_OUTPUT_ROOT_PATH)
    wd = os.getcwd()
    os.chdir(DELING_OUTPUT_ROOT_PATH)
    subprocess.run(["deling-cli.exe", "import", "-c", "lzs", special_battle_path, "battle.fs", "-f"])
    os.chdir(wd)
    for file in DELING_LIST_FILES:
        file_name = os.path.basename(file)
        path = os.path.join(dest_path, file_name)
        if os.path.isfile(path):
            pathlib.Path.unlink(pathlib.Path(path))
