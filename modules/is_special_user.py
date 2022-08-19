def isSpecialUser(user):
    '''
    check wheter user is in 'special_user' groups
    '''
    return user.groups.filter(name='special_user').exists()