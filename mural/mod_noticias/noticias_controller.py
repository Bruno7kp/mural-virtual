# coding: utf-8
import base64
import datetime
from typing import List

from flask import Blueprint, render_template, request, url_for

from mural.mod_base.auth import logado, Auth
from mural.mod_base.base_model import data_tables_response, json_response, admin_404_response, admin_403_response
from mural.mod_noticias import Noticia, ImagemNoticia

bp_noticias = Blueprint('noticias', __name__, url_prefix='/', template_folder='templates')

# Rotas da área pública
@bp_noticias.route('/noticias')
def noticias():
    return render_template("lista_noticias.html")

# Rotas da área administrativa
@bp_noticias.route('/admin/noticias', methods=['GET'])
@logado
def admin_lista():
    """ Página com listagem de notícias """
    if Auth().is_allowed('cadastra.noticia'):
        return render_template('admin_lista_noticias.html')
    else:
        return admin_403_response()


@bp_noticias.route('/admin/noticias/adicionar', methods=['GET'])
@logado
def admin_cadastro():
    """ Página para cadastro de notícias """
    noticia = Noticia()
    if Auth().is_allowed('cadastra.noticia', noticia):
        return render_template('admin_form_noticia.html', noticia=noticia)
    else:
        return admin_403_response()


@bp_noticias.route('/admin/noticias/adicionar', methods=['POST'])
@logado
def admin_cadastrar():
    """ Cadastro de notícias """
    auth = Auth()
    if auth.is_allowed('cadastra.noticia'):
        noticia = Noticia()
        populate_from_request(noticia)
        noticia.data_cadastro = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        noticia.usuario_id = auth.user.identifier
        if noticia.insert():
            imagens = get_uploaded_images()
            order = 0
            for imagem in imagens:
                imagem.noticia_id = noticia.identifier
                imagem.data_cadastro = noticia.data_cadastro
                imagem.ordem = order
                imagem.insert()
                order = order + 1
            return json_response(message='Notícia cadastrada', data=[noticia], redirect=url_for('noticias.admin_lista'))
        else:
            return json_response(message='Não foi possível cadastrar a notícia', data=[]), 400
    else:
        return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403


@bp_noticias.route('/admin/noticias/<int:identifier>', methods=['GET'])
@logado
def admin_edicao(identifier: int):
    """ Página para edição de notícias """
    noticia = Noticia()
    noticia.select(identifier)
    if noticia.identifier > 0:
        if Auth().is_allowed('edita.noticia', noticia):
            imagem = ImagemNoticia()
            imagens = imagem.select_by_parent(noticia.identifier)
            return render_template('admin_form_noticia.html', noticia=noticia, imagens=imagens)
        else:
            return admin_403_response()
    else:
        return admin_404_response()


@bp_noticias.route('/admin/noticias/<int:identifier>', methods=['POST'])
@logado
def admin_editar(identifier: int):
    """ Edição de notícias """
    noticia = Noticia()
    noticia.select(identifier)
    if noticia.identifier > 0:
        if Auth().is_allowed('edita.noticia', noticia):
            populate_from_request(noticia)
            noticia.data_atualizacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if noticia.update():
                imagens = get_uploaded_images()
                atual = ImagemNoticia()
                atuais = atual.select_by_parent(noticia.identifier)
                count = len(atuais)
                for imagem in imagens:
                    imagem.noticia_id = noticia.identifier
                    imagem.data_cadastro = noticia.data_atualizacao
                    imagem.ordem = count
                    imagem.insert()
                    count = count + 1
                return json_response(message='Notícia atualizado!', data=[noticia],
                                     redirect=url_for('noticias.admin_edicao', identifier=noticia.identifier))
            else:
                return json_response(message='Não foi possível editar a notícia', data=[]), 400
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Notícia não encontrada', data=[]), 404


@bp_noticias.route('/admin/noticias/imagem-ordem/<int:identifier>', methods=['POST'])
@logado
def admin_imagem_ordem(identifier: int):
    noticia = Noticia()
    noticia.select(identifier)
    if noticia.identifier > 0:
        if Auth().is_allowed('edita.noticia', noticia):
            ordem = request.form['ordem']
            lista = ordem.split(',')
            imagem = ImagemNoticia()
            count = 0
            for item in lista:
                imagem.select(item)
                imagem.ordem = count
                imagem.update()
                count = count + 1
            return json_response(message='Ordem atualizada!', data=[])
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Notícia não encontrado', data=[]), 404


@bp_noticias.route('/admin/noticias/imagem/<int:identifier>', methods=['DELETE'])
@logado
def admin_imagem_remover(identifier: int):
    imagem = ImagemNoticia()
    imagem.select(identifier)
    if imagem.identifier > 0:
        if Auth().is_allowed('edita.noticia', imagem.get_parent()):
            if imagem.delete():
                return json_response(message='Imagem removida!', data=[],
                                     redirect=url_for('noticias.admin_edicao', identifier=imagem.noticia_id))
            else:
                return json_response(message='Não foi possível remover a imagem', data=[]), 400
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Imagem não encontrada', data=[]), 404


@bp_noticias.route('/admin/noticias/busca')
@logado
def admin_busca():
    noticia = Noticia()
    busca = request.args.get('search[value]')
    busca = '%' + busca + '%'
    inicio = int(request.args.get('start'))
    fim = int(request.args.get('length'))
    draw = int(request.args.get('draw'))
    resultados = noticia.search(busca, inicio, fim)
    total = noticia.total()
    filtrado = noticia.count(busca)
    return data_tables_response(draw, total, filtrado, resultados)


@bp_noticias.route('/admin/noticias/<int:identifier>', methods=['DELETE'])
@logado
def admin_remover(identifier: int):
    noticia = Noticia()
    noticia.select(identifier)
    if noticia.identifier > 0:
        if Auth().is_allowed('remove.noticia', noticia):
            if noticia.delete():
                return json_response(message='Notícia removida!', data=[])
            else:
                return json_response(message='Não foi possível remover a notícia', data=[]), 400
        else:
            return json_response(message='Você não tem permissão para realizar esta ação', data=[]), 403
    else:
        return json_response(message='Notícia não encontrada', data=[]), 404


def populate_from_request(noticia: Noticia):
    # Atribui valores do post ao model
    noticia.titulo = request.form['titulo']
    noticia.data_entrada = request.form['data_entrada']
    noticia.data_saida = request.form['data_saida']
    noticia.conteudo = request.form['conteudo']
    if 'imagem' in request.files and request.files['imagem'].filename != '':
        noticia.imagem = "data:" + request.files['imagem'].content_type + ";base64," + str(
            base64.b64encode(request.files['imagem'].read()), "utf-8")


def get_uploaded_images():
    images: List[ImagemNoticia] = []
    if 'imagens' in request.files:
        files = request.files.getlist('imagens')
        for file in files:
            if file.filename != '':
                image = "data:" + file.content_type + ";base64," + str(base64.b64encode(file.read()), "utf-8")
                images.append(ImagemNoticia(0, 0, file.filename, image))
    return images
