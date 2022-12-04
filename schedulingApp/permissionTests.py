from schedulingApp.models import Profile


def user_has_ta_permission(user):
    if not user.is_authenticated:
        return False
    permission = Profile.objects.get(user=user).permission
    return permission == Profile.TA or permission == Profile.PROFESSOR or permission == Profile.ADMIN


def user_has_professor_permission(user):
    if not user.is_authenticated:
        return False
    permission = Profile.objects.get(user=user).permission
    return permission == Profile.PROFESSOR or permission == Profile.ADMIN


def user_has_admin_permission(user):
    if not user.is_authenticated:
        return False
    permission = Profile.objects.get(user=user).permission
    return permission == Profile.ADMIN
