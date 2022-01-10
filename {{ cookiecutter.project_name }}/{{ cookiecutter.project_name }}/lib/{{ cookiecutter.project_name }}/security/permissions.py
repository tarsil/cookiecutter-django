from guardian.shortcuts import assign_perm, remove_perm


def assign_user_perm(perm, user_or_group, obj, revoke=False):
    """Assigns permissions for a given object to a given django user or group
    Args:
      perm: permission to be assigned
      user_or_group: django user or group
      obj: object to assign to
      revoke: is is to remove a current permission or not
    Example:
    `assign_user_perm('is_super_user', hub_user.user, employee)` (Default value = False)
    Returns:
    """
    if not revoke:
        assign_perm(perm, user_or_group, obj)
    else:
        remove_perm(perm, user_or_group, obj)
