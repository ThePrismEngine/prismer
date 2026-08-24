import shutil
from pathlib import Path
from contextlib import contextmanager

import copier


@contextmanager
def use_custom_config(template_path: Path, custom_config_path: Path):
    template_path = Path(template_path)
    custom_config_path = Path(custom_config_path)

    if not custom_config_path.exists():
        raise FileNotFoundError(f"Custom config not found: {custom_config_path}")

    copier_yml = template_path / "copier.yml"
    backup_yml = template_path / "copier.yml.orig"

    if copier_yml.exists():
        copier_yml.rename(backup_yml)
        need_restore = True
    else:
        need_restore = False

    shutil.copy2(custom_config_path, copier_yml)

    try:
        yield
    finally:
        if copier_yml.exists():
            copier_yml.unlink()
        if need_restore and backup_yml.exists():
            backup_yml.rename(copier_yml)


template = Path(rf"C:\Users\Admin\CLionProjects\ProjectTemplate")
custom_config = template / ".prism" / "copier.yml"
dest = Path(rf"C:\Users\Admin\CLionProjects\TestCopier")

with use_custom_config(template, custom_config):
    copier.run_copy(str(template), str(dest), data={"project_name": "SUPER_GIVER_ULTRA_DEMO"})