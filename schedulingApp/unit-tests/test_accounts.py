from django.test import TestCase, Client


class CreateAccount:
    def test_emptyUsernameAndPassword(self):
        pass

    def test_emptyUsername(self):
        pass

    def test_emptyPassword(self):
        pass

    def test_validInfo(self):
        pass


class EditAccount:
    # add more test cases
    # EMail Phone Address FirstName LastName PermissionLevel OfficeHours

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

    def test_editPermissionLevel(self): # if changing perm level is valid, add test_invalidPermLevel
        pass

    def test_toSameValue(self):
        pass

    def test_noChange(self):
        pass

    def test_validEditAllFields(self):
        pass


class DeleteAccount:
    def test_accountNotFound(self):
        pass

    def test_deletingCurrentAccount(self):
        pass

    def test_validAndExistingAccount(self):
        pass
