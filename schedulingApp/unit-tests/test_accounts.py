from django.core.exceptions import ValidationError
from schedulingApp.models import Profile
from django.contrib.auth.models import User
from django.test import TestCase


# Fields: EMail Phone Address FirstName LastName PermissionLevel OfficeHours
class CreateUser(TestCase):
    def test_emptyEmail(self):
        with self.assertRaises(ValidationError,
                               msg="Should raise ValidationError for no arguments, requires a email"):
            a = User.objects.create_user(username="user", email="", password="pass")
            a.full_clean()

    def test_emptyPassword(self):
        with self.assertRaises(ValidationError,
                               msg="Should raise ValidationError for no arguments, requires a password"):
            a = User.objects.create_user(username="user", email="test@uwm.edu", password="")
            a.full_clean()


class CreateProfile(TestCase):
    def test_conflictingEmailCreation(self):
        user = User.objects.create_user(username="user", email="test@uwm.edu", password="pass")
        profile1 = Profile(user=user, phoneNumber="0123456789", homeAddress="home", permission=Profile.TA)

        with self.assertRaises(TypeError, msg="New Email should not match any other account's email"):
            profile2 = Profile(user=user, phoneNumber="9876543210", homeAddress="home", permission=Profile.TA)

    def test_validInfo(self):
        user = User.objects.create_user(username="user", email="test@uwm.edu", password="pass")
        self.assertEqual(user.username, "user", msg="User did not successfully create with a valid user name.")
        self.assertEqual(user.email, "test@uwm.edu", msg="User did not successfully create with a valid email.")
        self.assertEqual(user.password, "pass", msg="User did not successfully create with a valid password.")
        profile = Profile(user=user, phoneNumber="0123456789", homeAddress="home", permission=Profile.TA)
        self.assertEqual(profile.phoneNumber, "0123456789", msg="Profile did not successfully create with a valid "
                                                                "phone number")
        self.assertEqual(profile.homeAddress, "home", msg="Profile did not successfully create with a valid home "
                                                          "address")
        self.assertEqual(profile.permission, profile.TA, msg="Profile did not successfully create with a valid "
                                                             "permission")


class EditAccount(TestCase):
    theUser = None

    def setUp(self):
        user = User.objects.create_user(username="Robert Smith", email="srobert@uwm.edu", password="pass")
        profile = Profile(user=user, phoneNumber="2345678901", homeAddress="Someplace Ave 123", permission=Profile.TA)

    # add more test cases

    # Implementation: Method that takes all fields as value with
    # default value as an invalid character signifying no change

    # Either breaks into smaller functions to edit each field or directly edits each field

    def test_blankUsername(self):
        self.assertRaises(TypeError, self.profile.setUsername(),
                          msg="Calling setUserName with a blank argument should throw TypeError")

    def test_blankEmailAddress(self):
        self.assertRaises(TypeError, self.profile.setEmailAddress(),
                          msg="Calling setEmailAddress with a blank argument should throw TypeError")

    def test_blankPassword(self):
        self.assertRaises(TypeError, self.profile.setPassword(),
                          msg="Calling setPassword with a blank argument should throw TypeError")

    def test_blankHomeAddress(self):
        self.assertRaises(TypeError, self.profile.setHomeAddress(),
                          msg="Calling setHomeAddress with a blank argument should throw TypeError")

    def test_blankPhoneNumber(self):
        self.assertRaises(TypeError, self.profile.setPhoneNumber(),
                          msg="Calling setPhoneNumber with a blank argument should throw TypeError")

    def test_blankPermission(self):
        self.assertRaises(TypeError, self.profile.setPermission(),
                          msg="Calling setPermission with a blank argument should throw TypeError")

    def test_invalidUsername(self):
        with self.assertRaises(ValidationError, msg="Calling setUserName with no argument should throw ValueError"):
            self.profile.setUsername("")
            self.profile.full_clean()

    def test_invalidEmailAddress(self):
        with self.assertRaises(ValidationError,
                               msg="Calling setEmailAddress with no argument should throw ValueError"):
            self.profile.setEmailAddress("")
            self.profile.full_clean()

    def test_invalidPassword(self):
        with self.assertRaises(ValidationError,
                               msg="Calling setLastName with no argument should throw ValueError"):
            self.profile.setPassword("")
            self.profile.full_clean()

    def test_invalidHomeAddress(self):
        with self.assertRaises(ValueError, msg="Calling setHomeAddress with no argument should throw ValueError"):
            self.profile.setHomeAddress("")
            self.profile.full_clean()

    def test_invalidPhoneNumber(self):
        with self.assertRaises(ValidationError,
                               msg="Calling setPhoneNumber with no argument should throw ValueError"):
            self.profile.setPhoneNumber("")
            self.profile.full_clean()

    def test_invalidPermission(self):
        with self.assertRaises(ValidationError,
                               msg="Calling setPermission with no argument should throw ValueError"):
            self.profile.setPermission("")
            self.profile.full_clean()

    def test_changeUsername(self):
        self.profile.setUsername("Rob Adams")
        self.assertEqual(self.profile.getUsername(), "Rob Adams",
                         msg="Changing the first name to a new one wasn't successful")

    def test_changeEmailAddress(self):
        self.profile.setEmailAddress("arob@uwm.edu")
        self.assertEqual(self.profile.getEmailAddress(), "arob@uwm.edu",
                         msg="Changing the email to a new one wasn't successful")

    def test_changePassword(self):
        self.profile.setPassword("pass1")
        self.assertEqual(self.profile.getPassword(), "pass1",
                         msg="Changing the password to a new one wasn't successful")

    def test_changeHomeAddress(self):
        self.profile.setHomeAddress("Otherplace Rd 234")
        self.assertEqual(self.profile.getHomeAddress(), "Otherplace Rd 234",
                         msg="Changing the address to a new one wasn't successful")

    def test_changePhoneNumber(self):
        self.profile.setPhoneNumber("4567891234")
        self.assertEqual(self.profile.getPhoneNumber(), "4567891234",
                         msg="Changing the phone number to a new one wasn't successful")

    def test_changePermission(self):
        self.profile.setPermission(Profile.TA)
        self.assertEqual(self.profile.getPermission(), Profile.TA,
                         msg="Changing the permissions to a new value one wasn't successful")

    def test_noChangeUsername(self):
        self.assertEqual(self.profile.getUsername(), "Robert Smith",
                         msg="Changing the first name to a new one wasn't successful")

    def test_noChangeEmailAddress(self):
        self.assertEqual(self.profile.getEmailAddress(), "srobert@uwm.edu",
                         msg="Changing the email to a new one wasn't successful")

    def test_noChangePassword(self):
        self.assertEqual(self.profile.getPassword(), "pass",
                         msg="Changing the password to a new one wasn't successful")

    def test_noChangeHomeAddress(self):
        self.assertEqual(self.profile.getHomeAddress(), "Someplace Ave 123",
                         msg="Changing the address to a new one wasn't successful")

    def test_noChangePhoneNumber(self):
        self.assertEqual(self.profile.getPhoneNumber(), "2345678901",
                         msg="Changing the phone number to a new one wasn't successful")

    def test_noChangePermission(self):
        self.assertEqual(self.profile.getPermission(), Profile.TA,
                         msg="Changing the permissions to a new value one wasn't successful")

    # if changing perm level is valid, add the following 2 methods
    # def test_invalidPermLevel(self):
    #     pass
    # def test_editPermissionLevel(self):
    #     pass

    # To email used in another account
    def test_toConflictingEmail(self):
        user1 = User.objects.create_user(username="Rob Adams", email="arob@uwm.edu", password="pass")
        profile1 = Profile(user=user1, phoneNumber="4567891234", homeAddress="Otherplace Rd 234", permission=Profile.TA)

        profile1.setEmailAddress("srobert@uwm.edu")
        self.assertFalse(profile1.getEmailAddress() == "srobert@uwm.edu",
                         msg="Email should not match any other accounts")

    def test_toConflictingPhoneNumbers(self):
        user1 = User.objects.create_user(username="Rob Adams", email="arob@uwm.edu", password="pass")
        profile1 = Profile(user=user1, phoneNumber="4567891234", homeAddress="Otherplace Rd 234", permission=Profile.TA)

        profile1.setPhoneNumber("2345678901")
        self.assertFalse(profile1.getPhoneNumber() == "2345678901",
                         msg="Phone number should not match any other accounts")


class DeleteAccount(TestCase):
    theUser = None

    def test_accountNotFound(self):
        user = Profile.objects.get(self.theUser)
        self.assertRaises(NameError, user.delete(),
                          msg="Trying to delete nonexistent user should throw NameError")

    def setUp(self):
        user = User.objects.create_user(username="Robert Smith", email="srobert@uwm.edu", password="pass")
        profile = Profile(user=user, phoneNumber="2345678901", homeAddress="Someplace Ave 123", permission=Profile.TA)

    def test_deletingCurrentAccount(self):
        user = Profile.objects.get(self.theUser)
        self.assertRaises(NameError, user.delete(),
                          msg="Account should have been deleted")

    def test_validAndExistingAccount(self):
        Profile.objects.filter(self.profile).delete()

        self.assertFalse(self.profile.getUsername() == "Robert Smith",
                         msg="First name for deleted user should no longer exist.")

        self.assertFalse(self.profile.getEmailAddress() == "srobert@uwm.edu",
                         msg="Email for deleted user should no longer exist.")

        self.assertFalse(self.profile.getPassword() == "pass",
                         msg="Password for deleted user should no longer exist.")

        self.assertFalse(self.profile.getHomeAddress() == "Someplace Ave 123",
                         msg="Home address for deleted user should no longer exist.")

        self.assertFalse(self.profile.getPhoneNumber() == "2345678901",
                         msg="Phone number for deleted user should no longer exist.")

        self.assertFalse(self.profile.getPermission() == Profile.TA,
                         msg="Permission for deleted user should no longer exist.")

