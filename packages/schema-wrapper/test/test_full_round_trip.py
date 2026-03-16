import json
import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SPEC_DIR = ROOT / "specs"
JSON_DIR = SPEC_DIR / "json"
YAML_DIR = SPEC_DIR / "yaml"
GENERATOR = ROOT / "tests" / "tools" / "generate_python_code.mjs"
RUNNER = ROOT / "tests" / "tools" / "run_spec_file.py"


def load_json_fixture(name: str) -> dict:
    return json.loads((JSON_DIR / f"{name}.json").read_text(encoding="utf-8"))


def run_subprocess(command: list[str], **kwargs) -> str:
    completed = subprocess.run(command, check=True, capture_output=True, text=True, **kwargs)
    return completed.stdout


def generate_python(spec_path: Path) -> str:
    return run_subprocess(["node", str(GENERATOR), str(spec_path)], cwd=ROOT)


def run_generated_python(code: str, tmp_path: Path) -> dict:
    py_file = tmp_path / "spec_gen.py"
    py_file.write_text(code, encoding="utf-8")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")

    stdout = run_subprocess(["python", str(RUNNER), str(py_file)], cwd=ROOT, env=env)
    return json.loads(stdout)


JSON_EXAMPLES = sorted(path.stem for path in JSON_DIR.glob("*.json"))
YAML_EXAMPLES = sorted(
    path.stem for path in YAML_DIR.glob("*.yaml") if (JSON_DIR / f"{path.stem}.json").exists()
)


@pytest.mark.parametrize("example_name", JSON_EXAMPLES)
def test_json_round_trip(example_name: str, tmp_path: Path):
    original = load_json_fixture(example_name)
    generated = run_generated_python(
        generate_python(JSON_DIR / f"{example_name}.json"),
        tmp_path,
    )

    assert generated == original, (
        f"Round-trip JSON mismatch for '{example_name}'.\n"
        f"> original:  {original}\n"
        f"> generated: {generated}"
    )


@pytest.mark.parametrize("example_name", YAML_EXAMPLES)
def test_yaml_round_trip(example_name: str, tmp_path: Path):
    fixture = load_json_fixture(example_name)
    generated = run_generated_python(
        generate_python(YAML_DIR / f"{example_name}.yaml"),
        tmp_path,
    )

    assert generated == fixture, (
        f"Round-trip YAML mismatch for '{example_name}'.\n"
        f"> fixture:   {fixture}\n"
        f"> generated: {generated}"
    )
