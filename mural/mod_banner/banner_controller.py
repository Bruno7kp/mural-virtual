# coding: utf-8
import base64
import datetime

from flask import Blueprint, render_template, request, url_for

from mural.mod_banner import Banner
from mural.mod_base.auth import logado, Auth
from mural.mod_base.base_model import admin_403_response, json_response, admin_404_response
from mural.mod_logs import Logs

bp_banner = Blueprint('banner', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública


# Rotas da área administrativa
@bp_banner.route('/admin/destaque', methods=['GET'])
@logado
def admin_lista():
    """ Página com listagem de banners """
    if Auth().is_allowed('edita.universidade'):
        banner = Banner()
        banners = banner.all()
        return render_template('admin_lista_banners.html', banners=banners)
    else:
        return admin_403_response()


@bp_banner.route('/admin/destaque/adicionar', methods=['GET'])
@logado
def admin_cadastro():
    """ Página para cadastro de banners """
    banner = Banner()
    banners = banner.all()
    if Auth().is_allowed('edita.universidade') and len(banners) < 10:
        return render_template('admin_form_banner.html', banner=banner)
    else:
        return admin_403_response()


@bp_banner.route('/admin/destaque/adicionar', methods=['POST'])
@logado
def admin_cadastrar():
    """ Cadastro de banner """
    auth = Auth()
    banner = Banner()
    banners = banner.all()
    if auth.is_allowed('edita.universidade') and len(banners) < 10:
        populate_from_request(banner)
        banner.data_cadastro = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        banner.usuario_id = auth.user.identifier
        banner.ordem = len(banners)
        if banner.insert():
            Logs(0, auth.user.identifier,
                 auth.user.nome + '(' + auth.user.cpf + ')' + ' cadastrou um banner [Cód. ' + banner.identifier.__str__() + ']',
                 'banner', banner.identifier, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).insert()
            return json_response(message='Banner cadastrado!', data=[banner], redirect=url_for('banner.admin_lista'))
        else:
            return json_response(message='Não foi possível cadastrar o banner', data=[]), 400
    else:
        return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403


@bp_banner.route('/admin/destaque/<int:identifier>', methods=['GET'])
@logado
def admin_edicao(identifier: int):
    """ Página para edição de banner """
    banner = Banner()
    banner.select(identifier)
    if banner.identifier > 0:
        if Auth().is_allowed('edita.universidade', banner):
            return render_template('admin_form_banner.html', banner=banner)
        else:
            return admin_403_response()
    else:
        return admin_404_response()


@bp_banner.route('/admin/destaque/<int:identifier>', methods=['POST'])
@logado
def admin_editar(identifier: int):
    """ Edição de banner """
    banner = Banner()
    banner.select(identifier)
    auth = Auth()
    if banner.identifier > 0:
        if auth.is_allowed('edita.universidade', banner):
            populate_from_request(banner)
            banner.data_atualizacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if banner.update():
                Logs(0, auth.user.identifier,
                     auth.user.nome + '(' + auth.user.cpf + ')' + ' editou um banner [Cód. ' + banner.identifier.__str__() + ']',
                     'banner', banner.identifier, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).insert()
                return json_response(message='Banner atualizado!', data=[banner], redirect=url_for('banner.admin_lista'))
            else:
                return json_response(message='Não foi possível editar o banner', data=[]), 400
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Banner não encontrado', data=[]), 404


@bp_banner.route('/admin/destaque/imagem-ordem', methods=['POST'])
@logado
def admin_imagem_ordem():
    auth = Auth()
    if auth.is_allowed('edita.universidade'):
        ordem = request.form['ordem']
        lista = ordem.split(',')
        imagem = Banner()
        count = 0
        for item in lista:
            imagem.select(item)
            imagem.ordem = count
            imagem.update()
            count = count + 1
        Logs(0, auth.user.identifier,
             auth.user.nome + '(' + auth.user.cpf + ')' + ' alterou a ordem dos banners',
             'banner', 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).insert()
        return json_response(message='Ordem atualizada!', data=[])
    else:
        return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403


@bp_banner.route('/admin/destaque/<int:identifier>', methods=['DELETE'])
@logado
def admin_remover(identifier: int):
    banner = Banner()
    banner.select(identifier)
    auth = Auth()
    if banner.identifier > 0:
        if auth.is_allowed('edita.universidade', banner):
            if banner.delete():
                Logs(0, auth.user.identifier,
                     auth.user.nome + '(' + auth.user.cpf + ')' + ' removeu o banner [Cód. ' + banner.identifier.__str__() + ']',
                     'banner', banner.identifier, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).insert()
                return json_response(message='Banner removido!', data=[])
            else:
                return json_response(message='Não foi possível remover o banner', data=[]), 400
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Banner não encontrado', data=[]), 404


def populate_from_request(banner: Banner):
    # Atribui valores do post ao model
    banner.redireciona_url = request.form['redireciona_url']
    if 'imagem' in request.files and request.files['imagem'].filename != '':
        banner.imagem = "data:" + request.files['imagem'].content_type + ";base64," + str(
            base64.b64encode(request.files['imagem'].read()), "utf-8")
