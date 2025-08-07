import pytest
import subprocess

@pytest.mark.parametrize("class_str, input_file, expected_file", [
    ("C", "class_hierarchy_analyzer/tests/test1/lib.py", "class_hierarchy_analyzer/tests/test1/libC.txt"),
    ("D", "class_hierarchy_analyzer/tests/test1/lib.py", "class_hierarchy_analyzer/tests/test1/libD.txt"),
    ("pinho", "class_hierarchy_analyzer/tests/test1/newApp.py", "class_hierarchy_analyzer/tests/test1/newApppinho.txt"),
    ("A", "class_hierarchy_analyzer/tests/test1/app.py", "class_hierarchy_analyzer/tests/test1/appA.txt"),
    ("B", "class_hierarchy_analyzer/tests/test1/app.py", "class_hierarchy_analyzer/tests/test1/appB.txt"),
    ("new", "class_hierarchy_analyzer/tests/test1/app.py", "class_hierarchy_analyzer/tests/test1/appnew.txt"),
]) 


def test_test1(class_str, input_file, expected_file):
    result = subprocess.run(
        ["python3", "class_hierarchy_analyzer/cha.py", "-c", class_str, input_file],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()



@pytest.mark.parametrize("class_str, input_file, expected_file", [
    ("Animal", "class_hierarchy_analyzer/tests/test2/animal.py", "class_hierarchy_analyzer/tests/test2/animalAnimal.txt"),
    ("Animal", "class_hierarchy_analyzer/tests/test2/wild.py", "class_hierarchy_analyzer/tests/test2/wildAnimal.txt"),
    ("Feline", "class_hierarchy_analyzer/tests/test2/wild.py", "class_hierarchy_analyzer/tests/test2/wildFeline.txt"),
    ("Dog", "class_hierarchy_analyzer/tests/test2/pet.py", "class_hierarchy_analyzer/tests/test2/petDog.txt"),
    ("Cat", "class_hierarchy_analyzer/tests/test2/pet.py", "class_hierarchy_analyzer/tests/test2/petCat.txt"),
])

def test_test2(class_str, input_file, expected_file): 
    result = subprocess.run(
        ["python3", "class_hierarchy_analyzer/cha.py", "-c", class_str, input_file],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()



@pytest.mark.parametrize("class_str, input_file, expected_file", [
    ("A", "class_hierarchy_analyzer/tests/test3/a.py", "class_hierarchy_analyzer/tests/test3/aA.txt"),
    ("B", "class_hierarchy_analyzer/tests/test3/b.py", "class_hierarchy_analyzer/tests/test3/bB.txt"),
    ("C", "class_hierarchy_analyzer/tests/test3/c.py", "class_hierarchy_analyzer/tests/test3/cC.txt"),
    ("D", "class_hierarchy_analyzer/tests/test3/d.py", "class_hierarchy_analyzer/tests/test3/dD.txt"),
])

def test_test3(class_str, input_file, expected_file): 
    result = subprocess.run(
        ["python3", "class_hierarchy_analyzer/cha.py", "-c", class_str, input_file],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()



@pytest.mark.parametrize("class_str, input_file, expected_file", [
    ("Animal", "class_hierarchy_analyzer/tests/test4/hierarchy.py", "class_hierarchy_analyzer/tests/test4/hierarchyAnimal.txt"),
    ("Mammal", "class_hierarchy_analyzer/tests/test4/hierarchy.py", "class_hierarchy_analyzer/tests/test4/hierarchyMammal.txt"),
    ("Human", "class_hierarchy_analyzer/tests/test4/hierarchy.py", "class_hierarchy_analyzer/tests/test4/hierarchyHuman.txt"),
])

def test_test4(class_str, input_file, expected_file): 
    result = subprocess.run(
        ["python3", "class_hierarchy_analyzer/cha.py", "-c", class_str, input_file],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()



@pytest.mark.parametrize("class_str, input_file, expected_file", [
    ("FormalLanguage", "class_hierarchy_analyzer/tests/test5/overriding.py", "class_hierarchy_analyzer/tests/test5/overridingFormalLanguage.txt"),
    ("Colloquial", "class_hierarchy_analyzer/tests/test5/overriding2.py", "class_hierarchy_analyzer/tests/test5/overriding2Colloquial.txt"),
])

def test_test5(class_str, input_file, expected_file): 
    result = subprocess.run(
        ["python3", "class_hierarchy_analyzer/cha.py", "-c", class_str, input_file],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()



@pytest.mark.parametrize("class_str, input_file, expected_file", [
    ("Person", "class_hierarchy_analyzer/tests/test6/person.py", "class_hierarchy_analyzer/tests/test6/personPerson.txt"),
    ("Employee", "class_hierarchy_analyzer/tests/test6/employee.py", "class_hierarchy_analyzer/tests/test6/employeeEmployee.txt"),
    ("Manager", "class_hierarchy_analyzer/tests/test6/manager.py", "class_hierarchy_analyzer/tests/test6/managerManager.txt"),
])

def test_test6(class_str, input_file, expected_file): 
    result = subprocess.run(
        ["python3", "class_hierarchy_analyzer/cha.py", "-c", class_str, input_file],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()



@pytest.mark.parametrize("class_str, input_file, expected_file", [
    ("latin", "class_hierarchy_analyzer/tests/test7/latin.py", "class_hierarchy_analyzer/tests/test7/latinlatin.txt"),
    ("french", "class_hierarchy_analyzer/tests/test7/french.py", "class_hierarchy_analyzer/tests/test7/frenchfrench.txt"),
    ("italian", "class_hierarchy_analyzer/tests/test7/italian.py", "class_hierarchy_analyzer/tests/test7/italianitalian.txt"),
    ("english", "class_hierarchy_analyzer/tests/test7/english.py", "class_hierarchy_analyzer/tests/test7/englishenglish.txt"),
])

def test_test7(class_str, input_file, expected_file): 
    result = subprocess.run(
        ["python3", "class_hierarchy_analyzer/cha.py", "-c", class_str, input_file],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()



@pytest.mark.parametrize("class_str, input_file, expected_file", [
    ("UglySoup", "class_hierarchy_analyzer/tests/bs4-import/app.py", "class_hierarchy_analyzer/tests/bs4-import/appUglySoup.txt"),
])

def test_testbs4(class_str, input_file, expected_file): 
    result = subprocess.run(
        ["python3", "class_hierarchy_analyzer/cha.py", "-c", class_str, input_file],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()



@pytest.mark.parametrize("class_str, input_file, expected_file", [
    ("Question", "class_hierarchy_analyzer/tests/django-import/djangotutorial/polls/models.py", "class_hierarchy_analyzer/tests/django-import/djangoQuestion.txt"),
    ("Choice", "class_hierarchy_analyzer/tests/django-import/djangotutorial/polls/models.py", "class_hierarchy_analyzer/tests/django-import/djangoChoice.txt"),
])

@pytest.mark.skip(reason="This test is temporarily disabled due to test errors.")
def test_testdjango(class_str, input_file, expected_file): 
    result = subprocess.run(
        ["python3", "class_hierarchy_analyzer/cha.py", "-c", class_str, input_file],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()



@pytest.mark.parametrize("class_str, input_file, expected_file", [
    ("TestCategorizeByAge", "class_hierarchy_analyzer/tests/unittest-import/test_age.py", "class_hierarchy_analyzer/tests/unittest-import/testcategorize.txt"),
])

def test_testunittest(class_str, input_file, expected_file): 
    result = subprocess.run(
        ["python3", "class_hierarchy_analyzer/cha.py", "-c", class_str, input_file],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()



@pytest.mark.parametrize("class_str, input_file, expected_file", [
    ("someClass", "class_hierarchy_analyzer/tests/testForDot/app.py", "class_hierarchy_analyzer/tests/testForDot/app.txt"),
    ("someClass2", "class_hierarchy_analyzer/tests/testForDot/app2.py", "class_hierarchy_analyzer/tests/testForDot/app2.txt"),
])

def test_testDot(class_str, input_file, expected_file): 
    result = subprocess.run(
        ["python3", "class_hierarchy_analyzer/cha.py", "-c", class_str, input_file],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"


    with open(expected_file) as f:
        expected = f.read()

    assert result.stdout.strip() == expected.strip()
