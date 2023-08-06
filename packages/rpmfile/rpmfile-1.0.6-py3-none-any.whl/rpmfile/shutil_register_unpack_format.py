import shutil

from .cli import main

def unpack(archive_path, dest):
    main("-xC", dest, archive_path)

shutil.register_unpack_format("rpm", [".rpm"], unpack, [], "RPM file"])
