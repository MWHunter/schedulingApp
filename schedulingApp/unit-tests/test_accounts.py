from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User


# Fields: EMail Phone Address FirstName LastName PermissionLevel OfficeHours
class CreateAccount(TestCase):
    def test_emptyUsername(self):
        with self.assertRaises(ValidationError,
                               msg="Should raise ValidationError for no arguments, requires a first and last name"):
            a = User("", "")
            a.full_clean()

    def test_emptyFirstName(self):
        with self.assertRaises(ValidationError,
                               msg="Should raise ValidationError for no arguments, requires a first name"):
            a = User("", "Smith")
            a.full_clean()

    def test_emptyLastName(self):
        with self.assertRaises(ValidationError,
                               msg="Should raise ValidationError for no arguments, requires a last name"):
            a = User("Robert", "")
            a.full_clean()

    def test_conflictingEmailCreation(self):
        a = User("Rob", "Adams", "arob@uwm.edu", "Otherplace Rd 234", "4567891234", "ta")

        with self.assertRaises(TypeError, msg="New Email should not match any other account's email"):
            b = User("Bob", "Adams", "arob@uwm.edu", "Otherplace Rd 234", "4567891234", "ta")

    def test_validInfo(self):
        a = User("Robert", "Smith")
        self.assertEqual(a.firstName, "Robert", msg="User did not successfully create with a valid first name.")
        self.assertEqual(a.lastName, "Robert", msg="User did not successfully create with a valid last name.")


class EditAccount(TestCase):
    theUser = None

    def setUp(self):
        theUser = User("Robert", "Smith", "srobert@uwm.edu", "Someplace Ave 123", "2345678901", "admin")
        theUser.firstName = "Robert"
        theUser.lastName = "Smith"
        theUser.emailAddress = "srobert@uwm.edu"
        theUser.homeAddress = "Someplace Ave 123"
        theUser.phoneNumber = "2345678901"
        theUser.permission = "admin"

    # add more test cases

    # Implementation: Method that takes all fields as value with
    # default value as an invalid character signifying no change

    # Either breaks into smaller functions to edit each field or directly edits each field

    def test_blankFirstName(self):
        self.assertRaises(TypeError, self.theUser.setUserName(),
                          msg="Calling setUserName with no argument should throw TypeError")

    def test_blankLastName(self):
        self.assertRaises(TypeError, self.theUser.setLastName(),
                          msg="Calling setLastName with no argument should throw TypeError")

    def test_blankEmailAddress(self):
        self.assertRaises(TypeError, self.theUser.setEmailAddress(),
                          msg="Calling setEmailAddress with no argument should throw TypeError")

    def test_blankHomeAddress(self):
        self.assertRaises(TypeError, self.theUser.setHomeAddress(),
                          msg="Calling setHomeAddress with no argument should throw TypeError")

    def test_blankPhoneNumber(self):
        self.assertRaises(TypeError, self.theUser.setPhoneNumber(),
                          msg="Calling setPhoneNumber with no argument should throw TypeError")

    def test_blankPermission(self):
        self.assertRaises(TypeError, self.theUser.setPermission(),
                          msg="Calling setPermission with no argument should throw TypeError")

    def test_invalidFirstName(self):
        with self.assertRaises(ValidationError,  msg="Calling setUserName with no argument should throw ValueError"):
            self.theUser.setUserName("")
            self.theUser.full_clean()

    def test_invalidLastName(self):
        with self.assertRaises(ValidationError, msg="Calling setLastName with no argument should throw ValueError"):
            self.theUser.setLastName("")
            self.theUser.full_clean()

    def test_invalidEmailAddress(self):
        with self.assertRaises(ValidationError,
                               msg="Calling setEmailAddress with no argument should throw ValueError"):
            self.theUser.setEmailAddress("")
            self.theUser.full_clean()

    def test_invalidHomeAddress(self):
        with self.assertRaises(ValueError, msg="Calling setHomeAddress with no argument should throw ValueError"):
            self.theUser.setHomeAddress("")
            self.theUser.full_clean()

    def test_invalidPhoneNumber(self):
        with self.assertRaises(ValidationError,
                               msg="Calling setPhoneNumber with no argument should throw ValueError"):
            self.theUser.setPhoneNumber("")
            self.theUser.full_clean()

    def test_invalidPermission(self):
        with self.assertRaises(ValidationError,
                               msg="Calling setPermission with no argument should throw ValueError"):
            self.theUser.setPermission("")
            self.theUser.full_clean()

    def test_changeFirstName(self):
        self.theUser.setFirstName("Rob")
        self.assertEqual(self.theUser.getFirstName(), "Rob",
                         msg="Changing the first name to a new one wasn't successful")

    def test_changeLastName(self):
        self.theUser.setLastName("Adams")
        self.assertEqual(self.theUser.getLastName(), "Adams",
                         msg="Changing the last name to a new one wasn't successful")

    def test_changeEmailAddress(self):
        self.theUser.setEmailAddress("arob@uwm.edu")
        self.assertEqual(self.theUser.getEmailAddress(), "arob@uwm.edu",
                         msg="Changing the email to a new one wasn't successful")

    def test_changeHomeAddress(self):
        self.theUser.setHomeAddress("Otherplace Rd 234")
        self.assertEqual(self.theUser.getHomeAddress(), "Otherplace Rd 234",
                         msg="Changing the address to a new one wasn't successful")

    def test_changePhoneNumber(self):
        self.theUser.setPhoneNumber("4567891234")
        self.assertEqual(self.theUser.getPhoneNumber(), "4567891234",
                         msg="Changing the phone number to a new one wasn't successful")

    def test_changePermission(self):
        self.theUser.setPermission("ta")
        self.assertEqual(self.theUser.getPermission(), "ta",
                         msg="Changing the permissions to a new value one wasn't successful")

    def test_noChangeFirstName(self):
        self.assertEqual(self.theUser.getFirstName(), "Robert",
                         msg="Changing the first name to a new one wasn't successful")

    def test_noChangeLastName(self):
        self.assertEqual(self.theUser.getLastName(), "Smith",
                         msg="Changing the last name to a new one wasn't successful")

    def test_noChangeEmailAddress(self):
        self.assertEqual(self.theUser.getEmailAddress(), "srobert@uwm.edu",
                         msg="Changing the email to a new one wasn't successful")

    def test_noChangeHomeAddress(self):
        self.assertEqual(self.theUser.getHomeAddress(), "Someplace Ave 123",
                         msg="Changing the address to a new one wasn't successful")

    def test_noChangePhoneNumber(self):
        self.assertEqual(self.theUser.getPhoneNumber(), "2345678901",
                         msg="Changing the phone number to a new one wasn't successful")

    def test_noChangePermission(self):
        self.assertEqual(self.theUser.getPermission(), "admin",
                         msg="Changing the permissions to a new value one wasn't successful")

    # if changing perm level is valid, add the following 2 methods
    # def test_invalidPermLevel(self):
    #     pass
    # def test_editPermissionLevel(self):
    #     pass

    # To email used in another account
    def test_toConflictingEmail(self):
        a = User("Rob", "Adams", "arob@uwm.edu", "Otherplace Rd 234", "4567891234", "ta")

        a.setEmailAddress("srobert@uwm.edu")
        self.assertFalse(a.emailAddress == "srobert@uwm.edu",
                         msg="Email should not match any other accounts")

    def test_toConflictingPhoneNumbers(self):
        a = User("Rob", "Adams", "arob@uwm.edu", "Otherplace Rd 234", "4567891234", "ta")

        a.setPhoneNumber("2345678901")
        self.assertFalse(a.phoneNumber == "2345678901",
                         msg="Phone number should not match any other accounts")


class DeleteAccount(TestCase):
    theUser = None

    def test_accountNotFound(self):
        user = User.objects.get(self.theUser)
        self.assertRaises(NameError, user.delete(),
                          msg="Trying to delete nonexistent user should throw NameError")

    def setUp(self):
        theUser = User("Robert", "Smith", "dogs123", "srobert@uwm.edu", "Someplace Ave 123", "2345678901", "admin")
        theUser.firstName = "Robert"
        theUser.lastName = "Smith"
        theUser.emailAddress = "srobert@uwm.edu"
        theUser.homeAddress = "Someplace Ave 123"
        theUser.phoneNumber = "2345678901"
        theUser.permission = "admin"

    def test_deletingCurrentAccount(self):
        user = User.objects.get(self.theUser)
        self.assertRaises(NameError, user.delete(),
                          msg="Account should have been deleted")

    def test_validAndExistingAccount(self):
        User.objects.filter(self.theUser).delete()

        self.assertFalse(self.theUser.getFirstName() == "Robert",
                         msg="First name for deleted user should no longer exist.")

        self.assertFalse(self.theUser.getLastName() == "Smith",
                         msg="Last name for deleted user should no longer exist.")

        self.assertFalse(self.theUser.getPassword() == "dogs123",
                         msg="Password for deleted user should no longer exist.")

        self.assertFalse(self.theUser.getEmailAddress() == "srobert@uwm.edu",
                         msg="Email for deleted user should no longer exist.")

        self.assertFalse(self.theUser.getHomeAddress() == "Someplace Ave 123",
                         msg="Home address for deleted user should no longer exist.")

        self.assertFalse(self.theUser.getPhoneNumber() == "2345678901",
                         msg="Phone number for deleted user should no longer exist.")

        self.assertFalse(self.theUser.getPermission() == "admin",
                         msg="Permission for deleted user should no longer exist.")
