import nox

@nox.session
def tests(session):
    session.install('-r', 'requirements_dev.txt')
    session.run('pytest')

@nox.session
def lint(session):
    session.install('flake8')
    session.run('flake8')

