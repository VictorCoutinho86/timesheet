from app import app, db
from app.models import Usuario, Integracao, Ocorrencia


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Usuario': Usuario, 'Integracao': Integracao, 'Ocorrencia': Ocorrencia}
