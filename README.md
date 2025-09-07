# ConanTemplates
bootstrap conan cmake templates with vscode configurations

# Usage

make sure you have python conan package installed (latest version is recommended).

## bootstrap tempaltes

```bash
python scripts/bootstrap_templates.py
```

## use templates

```bash
mkdir test_vscode_cmake_exe
cd test_vscode_cmake_exe
conan new vscode_cmake_exe -d name=test
```

this will generate conan cmake project with VS Code support (clangd and CMake Tools).