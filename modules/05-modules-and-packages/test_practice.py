"""Tests for Module 05: Modules and Packages."""

import tempfile
from pathlib import Path

from practice import (
    create_init_reexport,
    detect_circular_imports,
    filter_imports,
    import_from_path,
    validate_package_structure,
)


class TestImportFromPath:
    def test_import_function(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("def greet(name):\n    return f'Hello, {name}'\n")
            tmp_path = Path(f.name)

        try:
            func = import_from_path(str(tmp_path), "greet")
            assert func("World") == "Hello, World"
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_import_class(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("class Person:\n    def __init__(self, name):\n        self.name = name\n")
            tmp_path = Path(f.name)

        try:
            Person = import_from_path(str(tmp_path), "Person")  # noqa: N806
            p = Person("Alice")
            assert p.name == "Alice"
        finally:
            tmp_path.unlink(missing_ok=True)


class TestValidatePackageStructure:
    def test_valid_package(self, tmp_path):
        pkg = tmp_path / "mypkg"
        pkg.mkdir()
        (pkg / "__init__.py").touch()
        (pkg / "module.py").touch()
        issues = validate_package_structure(str(pkg))
        assert issues == []

    def test_missing_init(self, tmp_path):
        pkg = tmp_path / "badpkg"
        pkg.mkdir()
        issues = validate_package_structure(str(pkg))
        assert any("__init__.py" in issue for issue in issues)

    def test_not_a_directory(self, tmp_path):
        f = tmp_path / "notadir"
        f.write_text("content")
        issues = validate_package_structure(str(f))
        assert any("directory" in issue.lower() for issue in issues)


class TestDetectCircularImports:
    def test_no_cycle(self):
        deps = {"a": ["b"], "b": ["c"], "c": []}
        assert detect_circular_imports(deps) == []

    def test_simple_cycle(self):
        deps = {"a": ["b"], "b": ["a"]}
        cycles = detect_circular_imports(deps)
        assert len(cycles) > 0

    def test_three_way_cycle(self):
        deps = {"a": ["b"], "b": ["c"], "c": ["a"]}
        cycles = detect_circular_imports(deps)
        assert len(cycles) > 0


class TestCreateInitReexport:
    def test_basic(self):
        exports = ["ClassA", "ClassB", "function_c"]
        result = create_init_reexport(exports)
        for name in exports:
            assert name in result


class TestFilterImports:
    def test_basic(self):
        result = filter_imports(
            ["os", "math", "numpy", "requests"],
            allowed=["os", "math", "sys", "json"],
        )
        assert result == ["os", "math"]

    def test_disallowed_imports(self):
        disallowed = filter_imports(
            ["secret_module", "os"],
            allowed=["os"],
        )
        assert "secret_module" not in disallowed
        assert "os" in disallowed
