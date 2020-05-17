import nox


@nox.session(python=False)
def tests(session):
    session.run('poetry', 'shell')
    session.run('poetry', 'install')
    session.cd('app')
    session.run('pytest')
