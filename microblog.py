from appcasorio import appcasorio, db  # o primeiro app é o módulo (subdiretório) e o segundo é a variável que é membro do pacote
from appcasorio.models import User, Image

@appcasorio.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Image': Image}