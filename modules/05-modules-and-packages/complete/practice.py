"""Module 05: Modules and Packages — Reference Implementation."""

import importlib.util
import sys
from pathlib import Path


def import_from_path(module_path, symbol_name):
    path = Path(module_path).resolve()
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    return getattr(module, symbol_name)


def validate_package_structure(package_dir):
    issues = []
    path = Path(package_dir)
    if not path.is_dir():
        issues.append(f"'{package_dir}' is not a directory")
        return issues
    if not (path / "__init__.py").exists():
        issues.append(f"Missing __init__.py in '{package_dir}'")
    return issues


def detect_circular_imports(dependencies):
    cycles = []
    visited = set()
    path = []

    def dfs(node):
        if node in path:
            cycle_start = path.index(node)
            cycles.append(path[cycle_start:] + [node])
            return
        if node in visited:
            return
        visited.add(node)
        path.append(node)
        for neighbor in dependencies.get(node, []):
            dfs(neighbor)
        path.pop()

    for node in dependencies:
        dfs(node)
    return cycles


def create_init_reexport(exports):
    lines = [f"from .module import {', '.join(exports)}", ""]
    lines.append(f"__all__ = {exports!r}")
    return "\n".join(lines) + "\n"


def filter_imports(imports, allowed):
    return [m for m in imports if m in set(allowed)]
