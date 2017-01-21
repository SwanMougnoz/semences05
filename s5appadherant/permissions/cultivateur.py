import rules


@rules.predicate()
def is_cultivateur_proprietaire(user, cultivateur):
    return user == cultivateur.jardin.proprietaire.user


@rules.predicate()
def is_cultivateur_adherant(user, cultivateur):
    return user == cultivateur.adherant.user


@rules.predicate()
def cultivateur_pending(user, cultivateur):
    return not cultivateur.accepte


rules.add_perm('s5appadherant.accept_cultivateur',
               is_cultivateur_proprietaire & cultivateur_pending & ~is_cultivateur_adherant)
