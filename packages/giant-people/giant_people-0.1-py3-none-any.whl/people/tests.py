import pytest
from people.models import Department, Location, Person, Role


class TestPerson:
    @pytest.fixture
    def person_instance(self):
        return Person(name="test person", linkedin_url="https://www.linkedin.com/in/testperson")

    def test_str(self, person_instance):
        assert f"{person_instance}" == "test person"


class TestRole:
    @pytest.fixture
    def role_instance(self):
        return Role(role="test role", role_id="123")

    def test_str(self, role_instance):
        assert f"{role_instance}" == "test role"


class TestLocation:
    @pytest.fixture
    def location_instance(self, mocker):
        return Location(
            location="test location", department=Department(department="test_department")
        )

    def test_str(self, location_instance):
        assert f"{location_instance}" == "test_department, test location"


class TestDepartment:
    @pytest.fixture
    def department_instance(self):
        return Department(department="test_department")

    def test_str(self, department_instance):
        assert str(department_instance) == "test_department"
