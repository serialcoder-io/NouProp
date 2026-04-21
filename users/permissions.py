def is_collector(user):
    return user.is_authenticated and user.role and user.role.name == "collector"