import os
from pathlib import Path
from functools import cache
from conan.tools.files import save, load, rmdir
from conan.api.conan_api import ConanAPI
from conan.api.output import ConanOutput, ConanException

output = ConanOutput()
project_root = Path(__file__).parents[1]
output_folder = project_root / "output"
rmdir(None, output_folder)

generated_template_folder = output_folder / "generated_template"
test_output_folder = output_folder / "test_new"
target_folder = Path("templates/command/new")
target_templates = ["cmake_exe", "cmake_lib"]


@cache
def get_vscode_template():
    vscode_template_dir = project_root / "vscode-template"
    output = ConanOutput()

    def load_file(file_name: str) -> str:
        file_content = load(conanfile=None, path=vscode_template_dir / file_name)
        output.success(f"File loaded: {vscode_template_dir.name}/{file_name}")
        return file_content

    return {
        ".vscode/launch.json": load_file("launch.json"),
        ".vscode/tasks.json": load_file("tasks.json"),
        ".vscode/settings.json": load_file("settings.json"),
    }


def save_template_files_with_vscode(template: str, output_folder: Path):
    vscode_template_files = get_vscode_template()
    new_api = ConanAPI().new
    files = new_api.get_template(template)  # First priority: user folder
    if not files:  # then, try the templates in the Conan home
        files = new_api.get_home_template(template)
    if files:
        template_files, non_template_files = files
    else:
        template_files = new_api.get_builtin_template(template)
        non_template_files = {}

    if not template_files and not non_template_files:
        raise ConanException(f"Template doesn't exist or not a folder: {template}")

    template_files.update(vscode_template_files)
    for f, v in sorted(template_files.items()):
        path = os.path.join(output_folder, f)
        save(conanfile=None, path=path, content=v)
        output.success("File saved: %s" % f)


for template in target_templates:
    cache_folder = Path(ConanAPI().cache_folder)
    new_template_name = f"vscode_{template}"
    output.highlight(f"Bootstrap template: {new_template_name}")
    curr_template_dir = generated_template_folder / new_template_name
    save_template_files_with_vscode(
        template,
        curr_template_dir,
    )
    output.highlight(f"Install template: {new_template_name}")
    curr_target_dir = cache_folder / target_folder / new_template_name
    if (curr_target_dir).exists():
        output.warning(f"remove previously installed template {new_template_name}")
        rmdir(None, str(curr_target_dir))
    ConanAPI().config.install(
        str(curr_template_dir),
        verify_ssl=False,
        target_folder=str(target_folder / new_template_name),
    )
    output.highlight(f"Test template: {new_template_name}")
    curr_test_dir = test_output_folder / new_template_name
    ConanAPI().new.save_template(
        new_template_name,
        output_folder=curr_test_dir,
        force=True,
    )
