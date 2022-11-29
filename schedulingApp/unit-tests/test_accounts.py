from django.test import TestCase
from models import User


# Fields: EMail Phone Address FirstName LastName PermissionLevel OfficeHours
class CreateAccount(TestCase):
    def test_emptyUsernameAndPassword(self):
        a = User()
        self.assertRaises(TypeError, msg="Should raise TypeError for no arguments, requires a username and password")

    def test_emptyUsername(self):
        a = User("", "", "dogs123")
        self.assertRaises(TypeError, msg="Should raise TypeError for no arguments, "
                                         "requires a username with the password")

    def test_emptyPassword(self):
        a = User("Robert", "Smith", "")
        self.assertRaises(TypeError, msg="Should raise TypeError for no arguments, "
                                         "requires a password for the username")

    def test_conflictingUsername(self):
        a = User("Robert", "Smith", "dogs123")
        self.assertRaises(ValueError, User("Robert", "Smith", "dogs123"),
                          msg="Duplicate names aren't allowed; that user already exists")

    def test_validInfo(self):
        a = User("Robert", "Smith", "dogs123")
        self.assertEqual(a.firstName, "Robert", msg="User did not successfully create with a valid title.")
        self.assertEqual(a.lastName, "Robert", msg="User did not successfully create with a valid title.")
        self.assertEqual(a.password, "dogs123", msg="User did not successfully create with a valid semester")


class EditAccount(TestCase):
    theUser = None

    def setUp(self):
        theUser = User("Robert", "Smith", "dogs123", "srobert@uwm.edu", "Someplace Ave 123",
                       "(234) 567-8901", "admin", "CS361", "Fall 2022")
        theUser.firstName = "Robert"
        theUser.lastName = "Smith"
        theUser.password = "dogs123"
        theUser.emailAddress = "srobert@uwm.edu"
        theUser.homeAddress = "Someplace Ave 123"
        theUser.phoneNumber = "(234) 567-8901"
        theUser.permission = "admin"

    # add more test cases

    # Implementation: Method that takes all fields as value with
    # default value as an invalid character signifying no change

    # Either breaks into smaller functions to edit each field or directly edits each field

    def test_blankField(self):
        self.setUp()
        self.assertRaises(TypeError, self.theUser.setUserName(),
                          msg="Calling setUserName with no argument should throw TypeError")

        self.assertRaises(TypeError, self.theUser.setLastName(),
                          msg="Calling setLastName with no argument should throw TypeError")

        self.assertRaises(TypeError, self.theUser.setPassword(),
                          msg="Calling setPassword with no argument should throw TypeError")

        self.assertRaises(TypeError, self.theUser.setEmailAddress(),
                          msg="Calling setEmailAddress with no argument should throw TypeError")

        self.assertRaises(TypeError, self.theUser.setHomeAddress(),
                          msg="Calling setHomeAddress with no argument should throw TypeError")

        self.assertRaises(TypeError, self.theUser.setPhoneNumber(),
                          msg="Calling setPhoneNumber with no argument should throw TypeError")

        self.assertRaises(TypeError, self.theUser.setPermission(),
                          msg="Calling setPermission with no argument should throw TypeError")

    def test_invalid(self):
        self.setUp()

        self.assertRaises(ValueError, self.theUser.setUserName(""),
                          msg="Calling setUserName with no argument should throw ValueError")

        self.assertRaises(ValueError, self.theUser.setLastName(""),
                          msg="Calling setLastName with no argument should throw ValueError")

        self.assertRaises(ValueError, self.theUser.setPassword(""),
                          msg="Calling setPassword with no argument should throw ValueError")

        self.assertRaises(ValueError, self.theUser.setEmailAddress(""),
                          msg="Calling setEmailAddress with no argument should throw ValueError")

        self.assertRaises(ValueError, self.theUser.setHomeAddress(""),
                          msg="Calling setHomeAddress with no argument should throw ValueError")

        self.assertRaises(ValueError, self.theUser.setPhoneNumber(""),
                          msg="Calling setPhoneNumber with no argument should throw ValueError")

        self.assertRaises(ValueError, self.theUser.setPermission(""),
                          msg="Calling setPermission with no argument should throw ValueError")

    def test_change(self):
        self.setUp()

        self.theUser.setFirstName("Rob")
        self.assertEqual(self.theUser.getFirstName(), "Rob",
                         msg="Changing the first name to a new one wasn't successful")

        self.theUser.setLastName("Adams")
        self.assertEqual(self.theUser.getLastName(), "Adams",
                         msg="Changing the last name to a new one wasn't successful")

        self.theUser.setPassword("cats123")
        self.assertEqual(self.theUser.getPassword(), "cats123",
                         msg="Changing the password to a new one wasn't successful")

        self.theUser.setEmailAddress("arob@uwm.edu")
        self.assertEqual(self.theUser.getEmailAddress(), "arob@uwm.edu",
                         msg="Changing the email to a new one wasn't successful")

        self.theUser.setHomeAddress("Otherplace Rd 234")
        self.assertEqual(self.theUser.getHomeAddress(), "Otherplace Rd 234",
                         msg="Changing the address to a new one wasn't successful")

        self.theUser.setPhoneNumber("(456) 789-1234")
        self.assertEqual(self.theUser.getPhoneNumber(), "(456) 789-1234",
                         msg="Changing the phone number to a new one wasn't successful")

        self.theUser.setPermission("ta")
        self.assertEqual(self.theUser.getPermission(), "ta",
                         msg="Changing the permissions to a new value one wasn't successful")

    def test_noChange(self):
        self.setUp()

        self.assertEqual(self.theUser.getFirstName(), "Robert",
                         msg="Changing the first name to a new one wasn't successful")

        self.assertEqual(self.theUser.getLastName(), "Smith",
                         msg="Changing the last name to a new one wasn't successful")

        self.assertEqual(self.theUser.getPassword(), "dogs123",
                         msg="Changing the password to a new one wasn't successful")

        self.assertEqual(self.theUser.getEmailAddress(), "srobert@uwm.edu",
                         msg="Changing the email to a new one wasn't successful")

        self.assertEqual(self.theUser.getHomeAddress(), "Someplace Ave 123",
                         msg="Changing the address to a new one wasn't successful")

        self.assertEqual(self.theUser.getPhoneNumber(), "(234) 567-8901",
                         msg="Changing the phone number to a new one wasn't successful")

        self.assertEqual(self.theUser.getPermission(), "admin",
                         msg="Changing the permissions to a new value one wasn't successful")

    # if changing perm level is valid, add the following 2 methods
    # def test_invalidPermLevel(self):
    #     pass
    # def test_editPermissionLevel(self):
    #     pass

    # To email used in another account
    def test_toConflictingEmail(self):
        self.setUp()
        a = User("Rob", "Adams", "cats123", "arob@uwm.edu", "Otherplace Rd 234",
                 "(456) 789-1234", "ta")

        a.emailAddress = "srobert@uwm.edu"
        self.assertFalse(a.emailAddress == "srobert@uwm.edu",
                         msg="Email should not match any other accounts")


class DeleteAccount(TestCase):
    theUser = None

    def setUp(self):
        theUser = User("Robert", "Smith", "dogs123", "srobert@uwm.edu", "Someplace Ave 123",
                       "(234) 567-8901", "admin", "CS361", "Fall 2022")
        theUser.firstName = "Robert"
        theUser.lastName = "Smith"
        theUser.password = "dogs123"
        theUser.emailAddress = "srobert@uwm.edu"
        theUser.homeAddress = "Someplace Ave 123"
        theUser.phoneNumber = "(234) 567-8901"
        theUser.permission = "admin"

    def test_accountNotFound(self):
        self.assertRaises(NameError, self.myUser.__del__(),
                          msg="Trying to delete nonexistent user should throw NameError")

    def test_deletingCurrentAccount(self):
        self.setUp()
        self.assertRaises(NameError, self.myUser.__del__(),
                          msg="Account should have been deleted")

    def test_validAndExistingAccount(self):
        self.setUp()
        self.theUser.__del__()
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

        self.assertFalse(self.theUser.getPhoneNumber() == "(234) 567-8901",
                         msg="Phone number for deleted user should no longer exist.")

        self.assertFalse(self.theUser.getPermission() == "admin",
                         msg="Permission for deleted user should no longer exist.")
