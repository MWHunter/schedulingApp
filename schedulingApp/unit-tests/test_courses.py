from django.test import TestCase


# Fields: Title
class CreateCourse(TestCase):
    def test_emptyTitle(self):
        pass

    def test_conflictingTitle(self):
        pass

    def test_validInfo(self):
        pass


class EditCourse(TestCase):
    def test_blankTitle(self):
        pass

    def test_invalidTitle(self):
        pass

    def test_conflictingTitle(self):
        pass

    def test_noChange(self):
        pass

    def test_validEdit(self):
        pass


class DeleteCourse(TestCase):
    def test_courseNotFound(self):
        pass

    def test_validAndExistingCourse(self):
        pass
