import pytest
import subprocess

@pytest.mark.parametrize("format_type, input_file, expected_file", [
    ("google", "docstring_parser/tests/google_cases/add.py", "docstring_parser/tests/google_cases/add.txt"),
    ("google", "docstring_parser/tests/google_cases/foo.py", "docstring_parser/tests/google_cases/foo.txt"),
    ("google", "docstring_parser/tests/google_cases/google.py", "docstring_parser/tests/google_cases/google.txt"),
    ("google", "docstring_parser/tests/google_cases/multiline.py", "docstring_parser/tests/google_cases/multiline.txt"),
    ("google", "docstring_parser/tests/google_cases/gg_vehicles.py", "docstring_parser/tests/google_cases/gg_vehicles.txt"),
    ("google", "docstring_parser/tests/google_cases/classann.py", "docstring_parser/tests/google_cases/classann.txt"),
]) 

def test_google(format_type, input_file, expected_file):
    result = subprocess.run(
        ["python3", "docstring_parser/dsp.py", input_file, format_type],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()



@pytest.mark.parametrize("format_type, input_file, expected_file", [
    ("sphinx", "docstring_parser/tests/sphinx_cases/sphinx.py", "docstring_parser/tests/sphinx_cases/sphinx.txt"),
])

def test_sphinx(format_type, input_file, expected_file):
    result = subprocess.run(
        ["python3", "docstring_parser/dsp.py", input_file, format_type],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()



@pytest.mark.parametrize("format_type, input_file, expected_file", [
    ("numpy", "docstring_parser/tests/numpy_cases/numpy.py", "docstring_parser/tests/numpy_cases/numpy.txt"),
    ("numpy", "docstring_parser/tests/numpy_cases/np_vehicles.py", "docstring_parser/tests/numpy_cases/np_vehicles.txt"),
])

def test_numpy(format_type, input_file, expected_file):
    result = subprocess.run(
        ["python3", "docstring_parser/dsp.py", input_file, format_type],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()



@pytest.mark.parametrize("format_type, input_file, expected_file", [
    ("epytext", "docstring_parser/tests/epytext_cases/epytext.py", "docstring_parser/tests/epytext_cases/epytext.txt"),
])

def test_epytext(format_type, input_file, expected_file):
    result = subprocess.run(
        ["python3", "docstring_parser/dsp.py", input_file, format_type],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()



@pytest.mark.parametrize("format_type, input_file, expected_file", [
    ("google", "docstring_parser/tests/other_cases/noannotations.py", "docstring_parser/tests/other_cases/noannotations.txt"),
    ("google", "docstring_parser/tests/other_cases/oneline.py", "docstring_parser/tests/other_cases/oneline.txt"),
])

def test_other(format_type, input_file, expected_file):
    result = subprocess.run(
        ["python3", "docstring_parser/dsp.py", input_file, format_type],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()
