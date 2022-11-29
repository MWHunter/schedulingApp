from django.test import TestCase


# Fields: EMail Phone Address FirstName LastName PermissionLevel OfficeHours
class CreateAccount(TestCase):
    def test_emptyUsernameAndPassword(self):
        pass

    def test_emptyUsername(self):
        pass

    def test_emptyPassword(self):
        pass

    def test_conflictingUsername(self):
        pass

    def test_validInfo(self):
        pass


class EditAccount(TestCase):
    # add more test cases

    # Implementation: Method that takes all fields as value with
    # default value as an invalid character signifying no change

    # Either breaks into smaller functions to edit each field or directly edits each field

    def test_blankField(self):
        pass

    def test_invalidEmail(self):
        pass

    def test_invalidPhone(self):
        pass

    def test_invalidAddress(self):
        pass

    def test_invalidFirstName(self):
        pass

    def test_invalidLastName(self):
        pass

    def test_invalidOfficeHours(self):
        pass

    # if changing perm level is valid, add the following 2 methods
    # def test_invalidPermLevel(self):
    #     pass
    # def test_editPermissionLevel(self):
    #     pass

    # To email used in another account
    def test_toConflictingEmail(self):
        pass

    def test_noChange(self):
        pass

    def test_validEditAllFields(self):
        pass


class DeleteAccount(TestCase):
    def test_accountNotFound(self):
        pass

    def test_deletingCurrentAccount(self):
        pass

    def test_validAndExistingAccount(self):
        pass
