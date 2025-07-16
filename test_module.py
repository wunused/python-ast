import pytest
import subprocess

@pytest.mark.parametrize("class_str, input_file, expected_file", [
    ("C", "tests/test1/lib.py", "tests/test1/libC.txt"),
    ("D", "tests/test1/lib.py", "tests/test1/libD.txt"),
    ("pinho", "tests/test1/newApp.py", "tests/test1/newApppinho.txt"),
    ("A", "tests/test1/app.py", "tests/test1/appA.txt"),
    ("B", "tests/test1/app.py", "tests/test1/appB.txt"),
    ("new", "tests/test1/app.py", "tests/test1/appnew.txt"),
    ("Animal", "tests/test2/animal.py", "tests/test2/animalAnimal.txt"),
    ("Animal", "tests/test2/wild.py", "tests/test2/wildAnimal.txt"),
    ("Feline", "tests/test2/wild.py", "tests/test2/wildFeline.txt"),
    ("Dog", "tests/test2/pet.py", "tests/test2/petDog.txt"),
    ("Cat", "tests/test2/pet.py", "tests/test2/petCat.txt"),
]) 


def test_process(class_str, input_file, expected_file):
    result = subprocess.run(
        ["python3", "analyzer/analyzer.py", "-c", class_str, input_file],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()
