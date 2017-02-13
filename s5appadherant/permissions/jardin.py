import rules


@rules.predicate
def is_jardin_proprietaire(user, jardin):
    return user == jardin.proprietaire.user


@rules.predicate
def in_jardin_cultivateur_accepted(user, jardin):
    return user in [cultivateur.adherant.user for cultivateur in jardin.cultivateur_set.filter(accepte=True)]


@rules.predicate()
def in_jardin_cultivateur_pending(user, jardin):
    return user in [cultivateur.adherant.user for cultivateur in jardin.cultivateur_set.filter(pending=True)]


rules.add_perm('s5appadherant.change_jardin',
               is_jardin_proprietaire | in_jardin_cultivateur_accepted)

rules.add_perm('s5appadherant.request_cultivateur',
               ~is_jardin_proprietaire & ~in_jardin_cultivateur_pending & ~in_jardin_cultivateur_accepted)

rules.add_perm('s5appadherant.manage_cultivateurs', is_jardin_proprietaire)
