from argparse import ArgumentParser
from mimetypes import init
from typing import Any

from ssf_mission_tools.config import Config
from ssf_mission_tools.utils import unzip


class Init:
    
    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg

    def check_workdir_does_not_exist(self, workdir: str) -> bool:
        import os
        return not os.path.exists(workdir)

    def check_workdir_empty(self, workdir: str) -> bool:
        import os
        return len(os.listdir(workdir)) == 0
    
    def check_mission_exists(self, mission_name: str) -> bool:
        import os
        mission_path = os.path.join(self.cfg.mission_dir, mission_name)
        return os.path.exists(mission_path)
    
    def init_git_repo(self, workdir: str) -> None:
        import subprocess
        subprocess.run(["git", "init"], cwd=workdir, check=True)
        
    def unpack_mission_files(self, mission_name: str, workdir: str) -> None:
        import shutil
        import os
        mission_src = os.path.join(self.cfg.mission_dir, mission_name)
        mission_dst = os.path.join(workdir, "build")
        # clean up build directory if it exists
        if os.path.exists(mission_dst):
            shutil.rmtree(mission_dst)
        # unzip mission files into build directory
        unzip(mission_src, mission_dst)

    def create_directory_structure(self, workdir: str) -> None:
        import os
        #scripts: lua scripts used for the mission
        #mission: sanatized mission files as json
        #configs: configuration for the ssf-mission-tools (e.g. mission name, build configurations)
        #build: temporary build output
        dirs = ["scripts", "mission", "configs", "build"]
        for d in dirs:
            os.makedirs(os.path.join(workdir, d), exist_ok=True)

        # create a sensible .gitignore for the repository
        gitignore_path = os.path.join(workdir, ".gitignore")
        gitignore_lines = [
            "# Ignore build output\n",
            "build/\n",
        ]
        if not os.path.exists(gitignore_path):
            with open(gitignore_path, "w", encoding="utf-8") as gh:
                gh.writelines(gitignore_lines)
        else:
            # ensure build/ is present in existing .gitignore
            try:
                with open(gitignore_path, "r", encoding="utf-8") as gh:
                    existing = gh.read()
            except Exception:
                existing = ""
            if "build/" not in existing:
                with open(gitignore_path, "a", encoding="utf-8") as gh:
                    gh.write("\n# Ignore build output\nbuild/\n")

    @classmethod
    def add_subparser(cls, parser: ArgumentParser) -> None:
        parser.add_argument("-d", "--directory", type=str, default=".", help="Target directory for initialization")
        parser.add_argument("-m", "--mission", type=str, required=True, help="Mission used for initialization")

    @classmethod
    def handle_arguments(cls, args: Any, cfg: Config) -> None:
        workdir = args.directory
        mission_name =args.mission
        print(f"Initializing development directory at {workdir} for mission {mission_name}")
        init = Init(cfg)
        if not init.check_mission_exists(mission_name):
            print(f"Mission {mission_name} does not exist in {cfg.mission_dir}")
            return -1
        if init.check_workdir_does_not_exist(workdir):
            import os
            os.makedirs(workdir)
            print(f"Created directory {workdir}")
        if not init.check_workdir_empty:
            print(f"Directory {workdir} is not empty")
            return -1
        # Preconditions satisfied, proceed with initialization
        # create mission-config, copy mission files
        init.init_git_repo(workdir)
        init.create_directory_structure(workdir)
        print("Unpacking mission files...")
        init.unpack_mission_files(mission_name, workdir)
        print(f"Development directory {workdir} initialized successfully.")
        return 0