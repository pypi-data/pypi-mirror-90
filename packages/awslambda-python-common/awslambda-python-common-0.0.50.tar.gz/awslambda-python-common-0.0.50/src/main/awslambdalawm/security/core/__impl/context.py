from awslambdalawm.security.core.__impl.domain import Principal

class __Context:
    def __init__(self):
        self.principal = None
    
    def setPrincipal(self, principal:Principal):
        self.principal = principal

    def getPrincipal(self):
        return self.principal

__context = __Context()

def setPrincipal(principal:Principal) -> None:
    __context.setPrincipal(principal)

def getPrincipal() -> Principal:
    return __context.getPrincipal()