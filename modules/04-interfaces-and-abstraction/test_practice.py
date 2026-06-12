# ruff: noqa: E402 — sys.path must be set before imports; conftest.py fixes this in P1
"""Tests for Module 04: Interfaces and Abstraction."""

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
target = HERE / os.environ.get("PRACTICE_TARGET", "complete")
sys.path.insert(0, str(target))

import json

import pytest
from practice import (
    DataStore,
    DictStore,
    LRUStore,
    save_to_file,
)


class TestDictStore:
    def test_get_set_delete(self):
        store = DictStore()
        store.set("a", 1)
        assert store.get("a") == 1
        store.delete("a")
        with pytest.raises(KeyError):
            store.get("a")

    def test_is_datastore(self):
        assert isinstance(DictStore(), DataStore)

    def test_cannot_instantiate_abc(self):
        with pytest.raises(TypeError):
            DataStore()


class TestLRUStore:
    def test_basic_operations(self):
        store = LRUStore(capacity=2)
        store.set("a", 1)
        store.set("b", 2)
        assert store.get("a") == 1
        assert store.get("b") == 2

    def test_eviction(self):
        store = LRUStore(capacity=2)
        store.set("a", 1)
        store.set("b", 2)
        store.set("c", 3)
        with pytest.raises(KeyError):
            store.get("a")
        assert store.get("b") == 2
        assert store.get("c") == 3

    def test_access_updates_lru_order(self):
        store = LRUStore(capacity=2)
        store.set("a", 1)
        store.set("b", 2)
        store.get("a")
        store.set("c", 3)
        assert store.get("a") == 1
        with pytest.raises(KeyError):
            store.get("b")
        assert store.get("c") == 3

    def test_is_datastore(self):
        assert isinstance(LRUStore(2), DataStore)


class TestSaveToFile:
    def test_serializable(self, tmp_path):
        class User:
            def to_json(self):
                return json.dumps({"name": "Alice", "age": 30})

        filepath = tmp_path / "test.json"
        save_to_file(User(), filepath)
        saved = filepath.read_text()
        assert "Alice" in saved
        assert "30" in saved

    def test_non_serializable(self, tmp_path):
        class NoMethod:
            pass

        with pytest.raises(TypeError, match="to_json"):
            save_to_file(NoMethod(), tmp_path / "bad.json")
