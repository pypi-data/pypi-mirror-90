from awslambdalawm.security.core.__impl.domain import Principal

class PermissionsHelper:
    @staticmethod
    def hasPermissionToAny(principal:Principal, *authorisedRoles):
        # system client has full access to its own tenant
        if principal.subjectType == Principal.SUBJECT_TYPE_SYSTEM: 
            return True
        for role in principal.roles:
            if role in authorisedRoles:
                return True
        return False

    @staticmethod
    def hasPermissionToAll(principal:Principal, *requiredRoles):
        # system client has full access to its own tenant
        if principal.subjectType == Principal.SUBJECT_TYPE_SYSTEM: 
            return True
        return (
            len(requiredRoles) == 0 
        ) or (
            len(requiredRoles) > 0 and set(requiredRoles).issubset(set(principal.roles))
        )
