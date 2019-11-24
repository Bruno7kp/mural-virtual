# coding: utf-8
import base64
import datetime

from flask import Blueprint, render_template, request, url_for

from mural.mod_base import Auth
from mural.mod_base.base_model import json_response, admin_403_response
from mural.mod_universidade import Universidade

bp_universidade = Blueprint('universidade', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública


# Rotas da área administrativa
@bp_universidade.route('/admin/universidade', methods=['GET'])
def admin_universidade():
    if Auth().is_allowed('edita.universidade'):
        universidade = Universidade()
        universidade.select(1)
        return render_template('admin_universidade.html', universidade=universidade)
    else:
        return admin_403_response()


@bp_universidade.route('/admin/universidade', methods=['POST'])
def admin_editar():
    """ Edição de universidade """
    universidade = Universidade()
    universidade.select(1)
    if Auth().is_allowed('edita.universidade'):
        populate_from_request(universidade)
        universidade.data_atualizacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if universidade.update():
            return json_response(message='Dados da universidade atualizados!', data=[universidade],
                                 redirect=url_for('universidade.admin_universidade'))
        else:
            return json_response(message='Não foi possível editar a universidade', data=[]), 400
    else:
        return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403


def populate_from_request(universidade: Universidade):
    # Atribui valores do post ao model
    universidade.nome = request.form['nome']
    universidade.telefone = request.form['telefone']
    universidade.email = request.form['email']
    if 'logo' in request.files and request.files['logo'].filename != '':
        universidade.logo = "data:" + request.files['logo'].content_type + ";base64," + str(
            base64.b64encode(request.files['logo'].read()), "utf-8")
