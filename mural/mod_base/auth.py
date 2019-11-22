import time
from enum import Enum
from functools import wraps
from typing import Union, List

from flask import session, redirect, url_for


class Roles(Enum):
    admin = 1
    mod_noticia = 2
    mod_aviso = 3
    usuario = 4
    visitante = 5


class Resource(object):
    def __init__(self, resource: str, roles: List[Roles], author: Union[List[Roles], None] = None):
        """

        :param resource: O nome do recurso ou ação.
        :param roles: Os níveis com autorização de acessar o recurso.
        :param author: Níveis em que pode-se acessar apenas se o usuário for o criador/responsável do recurso acessado.
        """
        if author is None:
            author = []

        self.resource = resource
        self.roles = roles
        self.author = author


permissions = [
    Resource("cadastra.noticia", roles=[Roles.admin, Roles.mod_noticia]),
    Resource("edita.noticia", roles=[Roles.admin, Roles.mod_noticia]),
    Resource("remove.noticia", roles=[Roles.admin], author=[Roles.mod_noticia]),
    Resource("cadastra.aviso", roles=[Roles.admin, Roles.mod_aviso]),
    Resource("edita.aviso", roles=[Roles.admin, Roles.mod_aviso]),
    Resource("remove.aviso", roles=[Roles.admin], author=[Roles.mod_aviso]),
    Resource("edita.universidade", roles=[Roles.admin]),
    Resource("cadastra.usuario", roles=[Roles.admin, Roles.visitante]),
    Resource("edita.usuario", roles=[Roles.admin], author=[Roles.mod_noticia, Roles.mod_aviso, Roles.usuario]),
    Resource("remove.usuario", roles=[Roles.admin]),
    Resource("cadastra.anuncio", roles=[Roles.admin, Roles.mod_noticia, Roles.mod_aviso], author=[Roles.usuario]),
    Resource("edita.anuncio", roles=[Roles.admin, Roles.mod_noticia, Roles.mod_aviso], author=[Roles.usuario]),
    Resource("remove.anuncio", roles=[Roles.admin], author=[Roles.mod_noticia, Roles.mod_aviso]),
    Resource("aprova.anuncio", roles=[Roles.admin, Roles.mod_noticia, Roles.mod_aviso])
]


class Auth:
    user = None

    def __init__(self):
        from mural.mod_usuarios import Usuario
        Auth.user = Usuario()
        if 'user' in session:
            userid = session['user']['identifier']
            Auth.user.select(userid)

    @staticmethod
    def in_role(role: Roles) -> bool:
        """
        :param role: Nível de permissão
        :return: Indica se o usuário está no nível de permissão passado por parâmetro
        """
        from mural.mod_usuarios import Usuario
        if Auth.user is Usuario:
            return Roles(Auth.user.get_role()) == role
        else:
            return False

    @staticmethod
    def is_guest() -> bool:
        """
        :return: Indica se o usuário é visitante
        """
        return Auth.in_role(Roles.visitante)

    @staticmethod
    def is_logged() -> bool:
        """
        :return: Indica se o usuário está logado no sistema
        """
        return not Auth.is_guest()

    @staticmethod
    def get_resource(resource: str) -> Union[Resource, None]:
        """
        :param resource: Nome do recurso a ser buscado
        :return: Retorna o recurso buscado ou None caso não seja encontrado
        """
        for p in permissions:
            if p.resource == resource:
                return p
        else:
            return None

    @staticmethod
    def is_allowed(resource: str, relation=None) -> bool:
        """
        :param resource: Nome do recurso que está sendo verificada a permissão
        :param relation: Entidade relacionada ao recurso
        :return: Indica se o usuário tem permissão para acessar o recurso
        """
        permission = Auth.get_resource(resource)
        from mural.mod_usuarios import Usuario
        from mural.mod_base import BaseModel
        # Se o recurso não for encontrado, ou se não tiver um usuário, retornará falso
        if permission is not None and isinstance(Auth.user, Usuario):
            if Roles(Auth.user.get_role()) in permission.roles:
                # Se o nível do usuário está entre os permitidos
                return True
            elif Roles(Auth.user.get_role()) in permission.author and relation is BaseModel:
                # Se é permitido acessar um recurso relacionado ao usuário (Ex: Anúncio cadastrado pelo próprio usuário)
                return Auth.user.get_owner_id() == relation.get_owner_id()
        return False


SESSION_LIMIT = 30


def logado(f):
    """Verifica se usuario esta logado, impede que acesse o site caso tenha atingido o limite de tempo na sessao"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('usuarios.entrar'))
        if 'time' in session:
            now = time.time()
            diff_seconds = now - session['time']
            diff_minutes = diff_seconds / 60
            if diff_minutes >= SESSION_LIMIT:
                return redirect(url_for('usuarios.entrar', erro=2))
        return f(*args, **kwargs)
    return decorated_function
