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
    ("A", "tests/test3/a.py", "tests/test3/aA.txt"),
    ("B", "tests/test3/b.py", "tests/test3/bB.txt"),
    ("C", "tests/test3/c.py", "tests/test3/cC.txt"),
    ("D", "tests/test3/d.py", "tests/test3/dD.txt"),
    ("Animal", "tests/test4/hierarchy.py", "tests/test4/hierarchyAnimal.txt"),
    ("Mammal", "tests/test4/hierarchy.py", "tests/test4/hierarchyMammal.txt"),
    ("Human", "tests/test4/hierarchy.py", "tests/test4/hierarchyHuman.txt"),
    ("FormalLanguage", "tests/test5/overriding.py", "tests/test5/overridingFormalLanguage.txt"),
    ("Colloquial", "tests/test5/overriding2.py", "tests/test5/overriding2Colloquial.txt"),
    ("Person", "tests/test6/person.py", "tests/test6/personPerson.txt"),
    ("Employee", "tests/test6/employee.py", "tests/test6/employeeEmployee.txt"),
    ("Manager", "tests/test6/manager.py", "tests/test6/managerManager.txt"),
    ("latin", "tests/test7/latin.py", "tests/test7/latinlatin.txt"),
    ("french", "tests/test7/french.py", "tests/test7/frenchfrench.txt"),
    ("italian", "tests/test7/italian.py", "tests/test7/italianitalian.txt"),
    ("english", "tests/test7/english.py", "tests/test7/englishenglish.txt"),
    ("UglySoup", "tests/bs4-import/app.py", "tests/bs4-import/appUglySoup.txt"),
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
