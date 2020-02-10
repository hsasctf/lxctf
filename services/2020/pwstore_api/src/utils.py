from os import path
from sys import stderr
from hashlib import blake2b
from time import mktime
from datetime import datetime
from collections import namedtuple
from typing import Tuple, Type, Optional
from sqlite3 import IntegrityError

from aiohttp import web

from dbinit import DBconn, QueryExecutionError


BASE_DIR = path.dirname(path.abspath(__file__))
DB_PATH = path.join(BASE_DIR, 'db.sqlite')
INITFILE_PATH = path.join(BASE_DIR, 'init.sql')
ADMIN_PW = blake2b(bytes('adm1n', 'utf8'), digest_size=16).hexdigest()

def JsonContentType(aiohttp_request_handler):
    """@JsonContentType
    Decorator for aiohttp request handlers to check for Json mime type.
    Does not validate the body for being actual Json but ensures having a readable body.
    """

    error_msg = 'request has to be of mimetype \'application/json; charset=utf-8\' and has to provide json in body'

    def _wrapper(request: web.Request):
        if not request.content_type == str.casefold('application/json') or not request.can_read_body:
            return res_unsupported_media_type(error_msg)
        return aiohttp_request_handler(request)
    return _wrapper

def res_unsupported_media_type(msg: str) -> web.Response:
    return web.json_response({'reason': msg} ,status=415)

def res_bad_request(msg: str) -> web.Response:
    return web.json_response({'reason': msg}, status=400)

def res_ok(entity: Optional[dict]) -> web.Response:
    if entity:
        return web.json_response(entity, status=200)
    return web.json_response(status=200)

def res_ok_created(entity: dict) -> web.Response:
    return web.json_response(entity, status=201)

def res_conflict(msg: str) -> web.Response:
    return web.json_response({'reason': msg}, status=409)

def res_not_found(msg: str) -> web.Response:
    return web.json_response({'entity': msg}, status=404)

def res_unauthorized(msg: str) -> web.Response:
    return web.json_response({'reason': msg}, status=401)

class MissingArgumentError(Exception):
    """ One or more required Arguments are missing """
    def __init__(self, *args):
        super().__init__(self, *args)

async def get_args(request: web.Request, required: Tuple[str], optional: Optional[Tuple[str]] = tuple()) -> dict:
    """"
    Checks request body for Json containing required and optional args as Json-object.
    Returns namedtuple of required and optional args. 
    Optional args are set to None if missing.
    If required args are missing, MissingArgumentError is raised.
    """
    defaults = (None for _ in range(len(optional)))
    provided_args = await request.json()
    ExtractedArgs: Type = namedtuple('ExtractedArgs', required+optional, defaults=defaults)
    try:
        return ExtractedArgs(**{
            argname: None or provided_args[argname] for argname in provided_args 
            if argname in required or argname in optional
            and not provided_args[argname].isspace() or provided_args[argname]==''
        })
    except TypeError as e:
        args_str = ','.join(('\''+arg+'\'' for arg in required))
        raise MissingArgumentError(f'request has to provide: {args_str}')
    except Exception as e:
        raise ValueError('error parsing required arguments')

    assert False, 'code line should be unreachable'   

def register_user(conn: DBconn, uname: str, masterpw: str) -> None:
    pwhash = hash_pw(masterpw)
    try:
        conn.execute_query(
            f'insert into user values(NULL, {_query_name(uname)}, "{pwhash}", {is_admin_user(pwhash)})'
        )
    except QueryExecutionError as e:
        if isinstance(e.base_execption, IntegrityError):
            raise ValueError(f'user "{uname}" already exists')
        raise ValueError('could create user')

def hash_pw(pw: str):
    return blake2b(bytes(pw, 'utf8'), digest_size=16).hexdigest()

def is_admin_user(pwhash: str) -> int:
    return 1 if pwhash == ADMIN_PW else 0

def is_user_registered(conn: DBconn, name: str) -> bool:
    return conn.execute_query(f'select * from user where name="{name}"').fetchone()

def generate_id(*args: Tuple['str']) -> int:
    """takes an an arbitrary ammount of strings, concatenates them and returns a 32bit hash out of that"""
    h = int.from_bytes(blake2b(bytes(''.join(args), 'utf8'), digest_size=4).digest(), 'big')
    assert isinstance(h, int) and h <= (2**63)-1, 'digest > max int value for sqlite'
    return h

def check_provided_pw(conn: DBconn, uname: str, provided_pw: str) -> bool:
    data = conn.execute_query(f'select pwhash, isadmin from user where name={_query_name(uname)}').fetchone()
    if data and len(data) == 2:
        pwhash, isadmin = data
        if pwhash == hash_pw(provided_pw) or isadmin:
            return True
    return False

def get_entry(conn: DBconn, pw_id: int) -> dict:
    try:
        query = conn.execute_query(
            f'''select u.name, p.pw_id, p.description, p.creation_timestamp, p.pw
            from pwentry as p 
            inner join user as u on p.user_id=u.user_id
            where pw_id={pw_id}'''
        )
    except QueryExecutionError as e:
        raise ValueError(f'no entry for pw_id: {pw_id}')
        
    entry = query.fetchone()
    if not entry or not len(entry) == 5:
        raise ValueError(f'no entry for pw_id: {pw_id}')

    uname, _, description, creation_timestamp, pw = entry

    return {
        'username': uname,
        'pw_id': int(pw_id),
        'description': description,
        'creation_timestamp': creation_timestamp,
        'pw': pw,
    }

_query_name = lambda uname: '"*"' if is_admin_user(uname) else f'"{uname}"'
_query_name.__doc__ = 'get name surrounded by "" to fit sql syntax'

#TODO
def add_entry(conn: DBconn, uname: str, pw_entry: str, description: str) -> int:

    try:
        user_id_query = conn.execute_query(f'select user_id from user where name={_query_name(uname)}')
    except QueryExecutionError:
        raise ValueError(f'no user for username: {uname}')

    user_id = int(user_id_query.fetchone()[0])
    
    # todo: encrypt pw
    pw_id = generate_id(uname, pw_entry, description)
    timestamp = datetime.now().isoformat()

    try:
        conn.execute_query(
            f'insert into pwentry values({pw_id}, {user_id}, "{pw_entry}", "{timestamp}", "{description}")'
        )
    except QueryExecutionError as e:
        if isinstance(e.base_execption, IntegrityError):
            raise ValueError('entry already present. did not create duplicate')
        raise ValueError('could creade pw_entry')

    return pw_id

def check_hash(conn: DBconn, uname: str, pwhash: str):
    data = conn.execute_query(f'select pwhash from user where name={_query_name(uname)}').fetchone()
    if data and len(data) == 1 and  pwhash == data[0]:
        return True
    return False

def get_ids(conn: DBconn, uname: str) -> dict:
    try:
        user_pw_ids_query = conn.execute_query(
            f'''select pwentry.pw_id, pwentry.description
            from pwentry inner join user on pwentry.user_id=user.user_id
            where user.name={_query_name(uname)}'''
        )
    except QueryExecutionError as e:
        raise ValueError(f'error retrieving ids for user: {uname}')

    user_pw_ids = user_pw_ids_query.fetchall()

    return {
        "username": uname,
        "id_list": [{pw_id: description} for pw_id, description in user_pw_ids]
    }
