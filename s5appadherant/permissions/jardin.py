import rules


@rules.predicate
def is_jardin_proprietaire(user, jardin):
    return jardin.proprietaire.user == user


@rules.predicate
def is_jardin_cultivateur(user, jardin):
    return user in [cultivateur.adherant.user for cultivateur in jardin.cultivateur_set.filter(accepte=True)]

rules.add_perm('s5appadherant.change_jardin', is_jardin_proprietaire | is_jardin_cultivateur)
