from django.core.exceptions import ValidationError
from schedulingApp.models import Profile
from django.contrib.auth.models import User
from django.test import TestCase


class CreateProfile(TestCase):
    def test_conflictingEmailCreation(self):
        self.user = User.objects.create_user(username="test@uwm.edu", first_name="admin", last_name="user",
                                             email="test@uwm.edu", password="pass")
        self.profile1 = Profile(user=self.user, phoneNumber="0123456789", homeAddress="home", permission=Profile.TA,
                                skills="java")

        with self.assertRaises(TypeError, msg="New Email should not match any other account's email"):
            self.profile2 = Profile(user=self.user, phoneNumber="9876543210", homeAddress="home", permission=Profile.TA,
                                    skills="java")

    def test_validInfo(self):
        self.user = User.objects.create_user(username="test@uwm.edu", first_name="admin", last_name="user",
                                             email="test@uwm.edu", password="pass")
        self.assertEqual(self.user.username, "test@uwm.edu",
                         msg="User did not successfully create with a valid user name.")
        self.assertEqual(self.user.first_name, "admin", msg="User did not successfully create with a valid first name.")
        self.assertEqual(self.user.last_name, "user", msg="User did not successfully create with a valid last name.")
        self.assertEqual(self.user.email, "test@uwm.edu", msg="User did not successfully create with a valid email.")
        self.assertEqual(self.user.password, "pass", msg="User did not successfully create with a valid password.")

        self.profile = Profile(user=self.user, phoneNumber="0123456789", homeAddress="home", permission=Profile.TA,
                               skills="java")
        self.assertEqual(self.profile.phoneNumber, "0123456789", msg="Profile did not successfully create with a valid "
                                                                     "phone number")
        self.assertEqual(self.profile.homeAddress, "home", msg="Profile did not successfully create with a valid home "
                                                               "address")
        self.assertEqual(self.profile.permission, Profile.TA, msg="Profile did not successfully create with a valid "
                                                                  "permission")
        self.assertEqual(self.profile.skills, "java", msg="Profile did not successfully create with a valid "
                                                          "skills")


class EditAccount(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="srobert@uwm.edu", first_name="Robert", last_name="Smith",
                                             email="srobert@uwm.edu", password="pass")
        self.profile = Profile(user=self.user, phoneNumber="2345678901", homeAddress="Someplace Ave 123",
                               permission=Profile.TA, skills="java")

    # add more test cases

    # Implementation: Method that takes all fields as value with
    # default value as an invalid character signifying no change

    # Either breaks into smaller functions to edit each field or directly edits each field

    def test_blankUsername(self):
        self.assertRaises(TypeError, self.profile.setUsername(),
                          msg="Calling setUserName with a blank argument should throw TypeError")

    def test_blankFirstName(self):
        self.assertRaises(TypeError, self.profile.setFirstName(),
                          msg="Calling setFirstName with a blank argument should throw TypeError")

    def test_blankLastName(self):
        self.assertRaises(TypeError, self.profile.setLastName(),
                          msg="Calling setLastName with a blank argument should throw TypeError")

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

    def test_blankSkills(self):
        self.assertRaises(TypeError, self.profile.setSkills(),
                          msg="Calling setSkills with a blank argument should throw TypeError")

    def test_invalidUsername(self):
        with self.assertRaises(ValidationError, msg="Calling setUserName with no argument should throw ValueError"):
            self.profile.setUsername("")
            self.profile.full_clean()

    def test_invalidFirstName(self):
        with self.assertRaises(ValidationError, msg="Calling setFirstName with no argument should throw ValueError"):
            self.profile.setFirstName("")
            self.profile.full_clean()

    def test_invalidLastName(self):
        with self.assertRaises(ValidationError, msg="Calling setLastName with no argument should throw ValueError"):
            self.profile.setLastName("")
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

    def test_invalidSkills(self):
        with self.assertRaises(ValidationError, msg="Calling setSkills with no argument should throw ValueError"):
            self.profile.setSkills("")
            self.profile.full_clean()

    def test_changeUsername(self):
        self.profile.setUsername("arob@uwm.edu")
        self.assertEqual(self.profile.getUsername(), "arob@uwm.edu",
                         msg="Changing the first name to a new one wasn't successful")

    def test_changeFirstName(self):
        self.profile.setFirstName("Rob")
        self.assertEqual(self.profile.getFirstName(), "Rob",
                         msg="Changing the first name to a new one wasn't successful")

    def test_changeLastName(self):
        self.profile.setLastName("Adams")
        self.assertEqual(self.profile.getLastName(), "Adams",
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

    def test_changeSkills(self):
        self.profile.setSkills("python")
        self.assertEqual(self.profile.getSkills(), "python",
                         msg="Changing the permissions to a new value one wasn't successful")

    def test_noChangeUsername(self):
        self.assertEqual(self.profile.getUsername(), "srobert@uwm.edu",
                         msg="Not changing the username wasn't successful")

    def test_noChangeFirstName(self):
        self.assertEqual(self.profile.getFirstName(), "srobert@uwm.edu",
                         msg="Not changing the first name wasn't successful")

    def test_noChangeLastName(self):
        self.assertEqual(self.profile.getLastName(), "Robert",
                         msg="Not changing the last name wasn't successful")

    def test_noChangeEmailAddress(self):
        self.assertEqual(self.profile.getEmailAddress(), "Smith",
                         msg="Not changing the email wasn't successful")

    def test_noChangePassword(self):
        self.assertEqual(self.profile.getPassword(), "pass",
                         msg="Not changing the password wasn't successful")

    def test_noChangeHomeAddress(self):
        self.assertEqual(self.profile.getHomeAddress(), "Someplace Ave 123",
                         msg="Not changing the address wasn't successful")

    def test_noChangePhoneNumber(self):
        self.assertEqual(self.profile.getPhoneNumber(), "2345678901",
                         msg="Not changing the phone number wasn't successful")

    def test_noChangePermission(self):
        self.assertEqual(self.profile.getPermission(), Profile.TA,
                         msg="Not changing the permissions wasn't successful")

    def test_noChangeSkills(self):
        self.assertEqual(self.profile.getSkills(), "java",
                         msg="Not changing the skills wasn't successful")

    # To email used in another account
    def test_toConflictingEmail(self):
        self.user1 = User.objects.create_user(username="arob@uwm.edu", first_name="Rob", last_name="Adams",
                                              email="arob@uwm.edu", password="pass")
        self.profile1 = Profile(user=self.user1, phoneNumber="4567891234", homeAddress="Otherplace Rd 234",
                                permission=Profile.TA, skills="python")

        self.profile1.setEmailAddress("srobert@uwm.edu")
        self.assertFalse(self.profile1.getEmailAddress() == "srobert@uwm.edu",
                         msg="Email should not match any other accounts")

    def test_toConflictingPhoneNumbers(self):
        self.user1 = User.objects.create_user(username="arob@uwm.edu", first_name="Rob", last_name="Adams",
                                              email="arob@uwm.edu", password="pass")
        self.profile1 = Profile(user=self.user1, phoneNumber="4567891234", homeAddress="Otherplace Rd 234",
                                permission=Profile.TA, skills="python")

        self.profile1.setPhoneNumber("2345678901")
        self.assertFalse(self.profile1.getPhoneNumber() == "2345678901",
                         msg="Phone number should not match any other accounts")


class DeleteAccount(TestCase):
    def test_accountNotFound(self):
        self.profile = Profile.objects.get(Profile)
        self.assertRaises(NameError, self.profile.delete(),
                          msg="Trying to delete nonexistent user should throw NameError")

    def setUp(self):
        self.user = User.objects.create_user(username="srobert@uwm.edu", first_name="Robert", last_name="Smith",
                                             email="srobert@uwm.edu", password="pass")
        self.profile = Profile(user=self.user, phoneNumber="2345678901", homeAddress="Someplace Ave 123",
                               permission=Profile.TA, skills="java")

    def test_deletingCurrentAccount(self):
        self.assertRaises(NameError, Profile.objects.filter(self.profile).delete(),
                          msg="Account should have been deleted")

    def test_validAndExistingAccount(self):
        self.assertFalse(self.profile.getUsername() == "srobert@uwm.edu",
                         msg="Username for deleted user should no longer exist.")

        self.assertFalse(self.profile.getFirstName() == "Robert",
                         msg="First name for deleted user should no longer exist.")

        self.assertFalse(self.profile.getLastName() == "Smith",
                         msg="Last name for deleted user should no longer exist.")

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

        self.assertFalse(self.profile.getSkills() == "java",
                         msg="Permission for deleted user should no longer exist.")
