import pytest
import subprocess

@pytest.mark.parametrize("class_str, input_file, expected_file", [
    ("C", "analyzer/tests/test1/lib.py", "analyzer/tests/test1/libC.txt"),
    ("D", "analyzer/tests/test1/lib.py", "analyzer/tests/test1/libD.txt"),
    ("pinho", "analyzer/tests/test1/newApp.py", "analyzer/tests/test1/newApppinho.txt"),
    ("A", "analyzer/tests/test1/app.py", "analyzer/tests/test1/appA.txt"),
    ("B", "analyzer/tests/test1/app.py", "analyzer/tests/test1/appB.txt"),
    ("new", "analyzer/tests/test1/app.py", "analyzer/tests/test1/appnew.txt"),
    ("Animal", "analyzer/tests/test2/animal.py", "analyzer/tests/test2/animalAnimal.txt"),
    ("Animal", "analyzer/tests/test2/wild.py", "analyzer/tests/test2/wildAnimal.txt"),
    ("Feline", "analyzer/tests/test2/wild.py", "analyzer/tests/test2/wildFeline.txt"),
    ("Dog", "analyzer/tests/test2/pet.py", "analyzer/tests/test2/petDog.txt"),
    ("Cat", "analyzer/tests/test2/pet.py", "analyzer/tests/test2/petCat.txt"),
    ("A", "analyzer/tests/test3/a.py", "analyzer/tests/test3/aA.txt"),
    ("B", "analyzer/tests/test3/b.py", "analyzer/tests/test3/bB.txt"),
    ("C", "analyzer/tests/test3/c.py", "analyzer/tests/test3/cC.txt"),
    ("D", "analyzer/tests/test3/d.py", "analyzer/tests/test3/dD.txt"),
    ("Animal", "analyzer/tests/test4/hierarchy.py", "analyzer/tests/test4/hierarchyAnimal.txt"),
    ("Mammal", "analyzer/tests/test4/hierarchy.py", "analyzer/tests/test4/hierarchyMammal.txt"),
    ("Human", "analyzer/tests/test4/hierarchy.py", "analyzer/tests/test4/hierarchyHuman.txt"),
    ("FormalLanguage", "analyzer/tests/test5/overriding.py", "analyzer/tests/test5/overridingFormalLanguage.txt"),
    ("Colloquial", "analyzer/tests/test5/overriding2.py", "analyzer/tests/test5/overriding2Colloquial.txt"),
    ("Person", "analyzer/tests/test6/person.py", "analyzer/tests/test6/personPerson.txt"),
    ("Employee", "analyzer/tests/test6/employee.py", "analyzer/tests/test6/employeeEmployee.txt"),
    ("Manager", "analyzer/tests/test6/manager.py", "analyzer/tests/test6/managerManager.txt"),
    ("latin", "analyzer/tests/test7/latin.py", "analyzer/tests/test7/latinlatin.txt"),
    ("french", "analyzer/tests/test7/french.py", "analyzer/tests/test7/frenchfrench.txt"),
    ("italian", "analyzer/tests/test7/italian.py", "analyzer/tests/test7/italianitalian.txt"),
    ("english", "analyzer/tests/test7/english.py", "analyzer/tests/test7/englishenglish.txt"),
    ("UglySoup", "analyzer/tests/bs4-import/app.py", "analyzer/tests/bs4-import/appUglySoup.txt"),
    ("Question", "analyzer/tests/django-import/djangotutorial/polls/models.py", "analyzer/tests/django-import/djangoQuestion.txt"),
    ("Choice", "analyzer/tests/django-import/djangotutorial/polls/models.py", "analyzer/tests/django-import/djangoChoice.txt"),
    ("TestCategorizeByAge", "analyzer/tests/unittest-import/test_age.py", "analyzer/tests/unittest-import/testcategorize.txt"),
]) 


def test_process(class_str, input_file, expected_file):
    result = subprocess.run(
        ["python3", "analyzer/cha.py", "-c", class_str, input_file],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()
