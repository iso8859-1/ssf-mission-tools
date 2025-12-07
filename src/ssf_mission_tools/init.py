from argparse import ArgumentParser
from mimetypes import init
from typing import Any

from ssf_mission_tools.config import Config


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

    def create_directory_structure(self, workdir: str) -> None:
        import os
        #scripts: lua scripts used for the mission
        #mission: sanatized mission files as json
        #configs: configuration for the ssf-mission-tools (e.g. mission name, build configurations)
        #build: temporary build output
        dirs = ["scripts", "mission", "configs", "build"]
        for d in dirs:
            os.makedirs(os.path.join(workdir, d), exist_ok=True)

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
        print(f"Development directory {workdir} initialized successfully.")
        return 0