from django.test import TestCase


# Fields: course, title, assignedTA
class CreateSection:
    def test_emptyFields(self):
        pass

    def test_blankCourse(self):
        pass

    def test_nonExistantCourse(self):
        pass

    def test_blankTitle(self):
        pass

    def test_blankTA(self):
        pass

    def test_nonExistantTA(self):
        pass

    def test_validInfo(self):
        pass


class EditSection:
    def test_blankFields(self):
        pass

    def test_invalidCourse(self):
        pass

    def test_invalidTitle(self):
        pass

    def test_invalidTA(self):
        pass

    def test_toConflictingName(self):
        pass

    def test_toTAWithConflictingTime(self):
        pass

    def test_noChange(self):
        pass

    def test_validEditAllFields(self):
        pass


class DeleteSection:
    def test_sectionNotFound(self):
        pass

    def test_validAndExistingSection(self):
        pass
