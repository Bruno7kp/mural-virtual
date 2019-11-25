# coding: utf-8
import base64
import datetime
from typing import List

from flask import Blueprint, render_template, request, url_for

from mural.mod_anuncios import Anuncio, ImagemAnuncio
from mural.mod_base.auth import logado, Auth
from mural.mod_base.base_model import data_tables_response, admin_403_response, json_response, admin_404_response
from mural.mod_logs import Logs
from flask_paginate import Pagination, get_page_args

bp_anuncios = Blueprint('anuncios', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública
@bp_anuncios.route('/anuncios')
def anuncios():
    busca = Anuncio()
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = busca.count('%%', 1, 0, True)
    pagination_anuncios = busca.search('%%', offset, per_page, 1, 0, True)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template("lista_anuncios.html", anuncios=pagination_anuncios,
                           page=page,
                           per_page=per_page,
                           pagination=pagination, )


@bp_anuncios.route('/anuncio/<int:identifier>')
def anuncio(identifier: int):
    busca = Anuncio()
    busca.select(identifier)
    return render_template("anuncio.html", anuncio=busca)

# Rotas da área administrativa
@bp_anuncios.route('/admin/anuncios', methods=['GET'])
@logado
def admin_lista():
    """ Página com listagem de anúncios """
    if Auth().is_allowed('cadastra.anuncio'):
        return render_template('admin_lista_anuncios.html')
    else:
        return admin_403_response()


@bp_anuncios.route('/admin/anuncios/aprovacao', methods=['GET'])
@logado
def admin_aprovacao():
    """ Página com listagem de anúncios em aprovação """
    if Auth().is_allowed('edita.anuncio'):
        return render_template('admin_lista_anuncios_aprovacao.html')
    else:
        return admin_403_response()


@bp_anuncios.route('/admin/anuncios/adicionar', methods=['GET'])
@logado
def admin_cadastro():
    """ Página para cadastro de anúncios """
    anuncio = Anuncio()
    if Auth().is_allowed('cadastra.anuncio', anuncio):
        return render_template('admin_form_anuncio.html', anuncio=anuncio)
    else:
        return admin_403_response()


@bp_anuncios.route('/admin/anuncios/adicionar', methods=['POST'])
@logado
def admin_cadastrar():
    """ Cadastro de anúncios """
    auth = Auth()
    if auth.is_allowed('cadastra.anuncio'):
        anuncio = Anuncio()
        populate_from_request(anuncio)
        anuncio.data_cadastro = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        anuncio.usuario_id = auth.user.identifier
        # Apenas usuários que podem editar os anúncios já ficam aprovados
        anuncio.aprovado = auth.is_allowed('edita.anuncio')
        if anuncio.insert():
            imagens = get_uploaded_images()
            order = 0
            for imagem in imagens:
                imagem.anuncio_id = anuncio.identifier
                imagem.data_cadastro = anuncio.data_cadastro
                imagem.ordem = order
                imagem.insert()
                order = order + 1
            Logs(0, auth.user.identifier,
                 auth.user.nome + '(' + auth.user.cpf + ')' + ' cadastrou o anúncio ' + anuncio.titulo + ' [Cód. ' + anuncio.identifier.__str__() + ']',
                 'anuncio', anuncio.identifier, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).insert()
            return json_response(message='Anúncio cadastrado', data=[anuncio],
                                 redirect=url_for('anuncios.admin_edicao', identifier=anuncio.identifier))
        else:
            return json_response(message='Não foi possível cadastrar o anúncio', data=[]), 400
    else:
        return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403


@bp_anuncios.route('/admin/anuncios/<int:identifier>', methods=['GET'])
@logado
def admin_edicao(identifier: int):
    """ Página para edição de anúncios """
    anuncio = Anuncio()
    anuncio.select(identifier)
    if anuncio.identifier > 0:
        if Auth().is_allowed('edita.anuncio', anuncio):
            imagem = ImagemAnuncio()
            imagens = imagem.select_by_parent(anuncio.identifier)
            return render_template('admin_form_anuncio.html', anuncio=anuncio, imagens=imagens)
        else:
            return admin_403_response()
    else:
        return admin_404_response()


@bp_anuncios.route('/admin/anuncios/<int:identifier>', methods=['POST'])
@logado
def admin_editar(identifier: int):
    """ Edição de anúncios """
    anuncio = Anuncio()
    anuncio.select(identifier)
    auth = Auth()
    if anuncio.identifier > 0:
        if auth.is_allowed('edita.anuncio', anuncio):
            populate_from_request(anuncio)
            anuncio.data_atualizacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if anuncio.update():
                imagens = get_uploaded_images()
                atual = ImagemAnuncio()
                atuais = atual.select_by_parent(anuncio.identifier)
                count = len(atuais)
                for imagem in imagens:
                    imagem.anuncio_id = anuncio.identifier
                    imagem.data_cadastro = anuncio.data_atualizacao
                    imagem.ordem = count
                    imagem.insert()
                    count = count + 1
                Logs(0, auth.user.identifier,
                     auth.user.nome + '(' + auth.user.cpf + ')' + ' editou o anúncio ' + anuncio.titulo + ' [Cód. ' + anuncio.identifier.__str__() + ']',
                     'anuncio', anuncio.identifier, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).insert()
                return json_response(message='Anúncio atualizado!', data=[anuncio],
                                     redirect=url_for('anuncios.admin_edicao', identifier=anuncio.identifier))
            else:
                return json_response(message='Não foi possível editar o anúncio', data=[]), 400
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Anúncio não encontrado', data=[]), 404


@bp_anuncios.route('/admin/anuncios/imagem-ordem/<int:identifier>', methods=['POST'])
@logado
def admin_imagem_ordem(identifier: int):
    anuncio = Anuncio()
    anuncio.select(identifier)
    auth = Auth()
    if anuncio.identifier > 0:
        if auth.is_allowed('edita.anuncio', anuncio):
            ordem = request.form['ordem']
            lista = ordem.split(',')
            imagem = ImagemAnuncio()
            count = 0
            for item in lista:
                imagem.select(item)
                imagem.ordem = count
                imagem.update()
                count = count + 1
            Logs(0, auth.user.identifier,
                 auth.user.nome + '(' + auth.user.cpf + ')' + ' alterou a ordem das imagens do anúncio ' + anuncio.titulo + ' [Cód. ' + anuncio.identifier.__str__() + ']',
                 'anuncio', anuncio.identifier, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).insert()
            return json_response(message='Ordem atualizada!', data=[])
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Anúncio não encontrado', data=[]), 404


@bp_anuncios.route('/admin/anuncios/imagem/<int:identifier>', methods=['DELETE'])
@logado
def admin_imagem_remover(identifier: int):
    imagem = ImagemAnuncio()
    imagem.select(identifier)
    auth = Auth()
    if imagem.identifier > 0:
        if auth.is_allowed('edita.anuncio', imagem.get_parent()):
            if imagem.delete():
                anuncio = imagem.get_parent()
                Logs(0, auth.user.identifier,
                     auth.user.nome + '(' + auth.user.cpf + ')' + ' removeu a imagem do anúncio ' + anuncio.titulo + ' [Cód. ' + anuncio.identifier.__str__() + ']',
                     'anuncio', anuncio.identifier, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).insert()
                return json_response(message='Imagem removida!', data=[],
                                     redirect=url_for('anuncios.admin_edicao', identifier=imagem.anuncio_id))
            else:
                return json_response(message='Não foi possível remover a imagem', data=[]), 400
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Imagem não encontrada', data=[]), 404


@bp_anuncios.route('/admin/anuncios/busca', methods=['GET'])
@logado
def admin_busca():
    """ Busca de anúncios """
    anuncio = Anuncio()
    busca = request.args.get('search[value]')
    busca = '%' + busca + '%'
    inicio = int(request.args.get('start'))
    fim = int(request.args.get('length'))
    draw = int(request.args.get('draw'))
    # Filtra listagem de anúncios para que usuário não possam ver anúncios de outros usuários sem permissão
    auth = Auth()
    if auth.is_allowed('edita.anuncio'):
        resultados = anuncio.search(busca, inicio, fim, 1)
        total = anuncio.total(1)
        filtrado = anuncio.count(busca, 1)
    else:
        resultados = anuncio.search(busca, inicio, fim, -1, auth.user.identifier)
        total = anuncio.total(-1, auth.user.identifier)
        filtrado = anuncio.count(busca, -1, auth.user.identifier)

    return data_tables_response(draw, total, filtrado, resultados)


@bp_anuncios.route('/admin/anuncios/busca-aprovacao', methods=['GET'])
@logado
def admin_busca_aprovacao():
    """ Busca de anúncios sem aprovação """
    anuncio = Anuncio()
    busca = request.args.get('search[value]')
    busca = '%' + busca + '%'
    inicio = int(request.args.get('start'))
    fim = int(request.args.get('length'))
    draw = int(request.args.get('draw'))
    auth = Auth()
    if auth.is_allowed('edita.anuncio'):
        resultados = anuncio.search(busca, inicio, fim, 0)
        total = anuncio.total(0)
        filtrado = anuncio.count(busca, 0)
    else:
        resultados = []
        total = 0
        filtrado = 0

    return data_tables_response(draw, total, filtrado, resultados)


@bp_anuncios.route('/admin/anuncios/<int:identifier>', methods=['DELETE'])
@logado
def admin_remover(identifier: int):
    anuncio = Anuncio()
    anuncio.select(identifier)
    auth = Auth()
    if anuncio.identifier > 0:
        if auth.is_allowed('remove.anuncio', anuncio):
            if anuncio.delete():
                Logs(0, auth.user.identifier,
                     auth.user.nome + '(' + auth.user.cpf + ')' + ' removeu o anúncio ' + anuncio.titulo + ' [Cód. ' + anuncio.identifier.__str__() + ']',
                     'anuncio', anuncio.identifier, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).insert()
                return json_response(message='Anúncio removido!', data=[])
            else:
                return json_response(message='Não foi possível remover o anúncio', data=[]), 400
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Anúncio não encontrado', data=[]), 404


def populate_from_request(anuncio: Anuncio):
    # Atribui valores do post ao model
    anuncio.titulo = request.form['titulo']
    anuncio.data_entrada = request.form['data_entrada']
    anuncio.data_saida = request.form['data_saida']
    anuncio.conteudo = request.form['conteudo']
    if 'aprovado' in request.form and Auth().is_allowed('edita.anuncio'):
        anuncio.aprovado = int(request.form['aprovado'])


def get_uploaded_images():
    images: List[ImagemAnuncio] = []
    if 'imagens' in request.files:
        files = request.files.getlist('imagens')
        for file in files:
            if file.filename != '':
                image = "data:" + file.content_type + ";base64," + str(base64.b64encode(file.read()), "utf-8")
                images.append(ImagemAnuncio(0, 0, file.filename, image))
    return images
