import rules


@rules.predicate
def is_jardin_proprietaire(user, jardin):
    return user == jardin.proprietaire.user


@rules.predicate
def is_jardin_cultivateur_accepted(user, jardin):
    return user in [cultivateur.adherant.user for cultivateur in jardin.cultivateur_set.filter(accepte=True)]


@rules.predicate()
def is_jardin_cultivateur_all(user, jardin):
    return user in [cultivateur.adherant.user for cultivateur in jardin.cultivateur_set.all()]


rules.add_perm('s5appadherant.change_jardin',
               is_jardin_proprietaire | is_jardin_cultivateur_accepted)

rules.add_perm('s5appadherant.add_cultivateur',
               ~is_jardin_proprietaire & ~is_jardin_cultivateur_all)

