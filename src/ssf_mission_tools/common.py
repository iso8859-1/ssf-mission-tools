import os
from pathlib import Path

def expand_path(path_str: str) -> str:
    expanded = os.path.expandvars(path_str)
    return Path(expanded).expanduser().as_posix()

def copy_kneeboard(workdir: str) -> None:
    import shutil
    import os
    kneeboard_src = os.path.join(workdir, "build", "kneeboard")
    kneeboard_dst = os.path.join(workdir, "mission", "kneeboard")
    if not os.path.isdir(kneeboard_src):
        return
    shutil.copytree(kneeboard_src, kneeboard_dst, dirs_exist_ok=True)

def copy_resources(workdir: str) -> None:
    import shutil
    import os
    resources_src = os.path.join(workdir, "build", "I10n")
    resources_dst = os.path.join(workdir, "mission", "I10n")
    # only proceed if the source directory exists
    if not os.path.isdir(resources_src):
        return

    # ensure destination parent exists
    os.makedirs(resources_dst, exist_ok=True)

    # copy everything except these resource names
    # the files in skip_names need to be sanitized and copied separately to allow proper handling in git
    skip_names = {"dictionary", "mapResource"}
    for name in os.listdir(resources_src):
        if name in skip_names:
            continue
        src_path = os.path.join(resources_src, name)
        dst_path = os.path.join(resources_dst, name)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
        else:
            shutil.copy2(src_path, dst_path)