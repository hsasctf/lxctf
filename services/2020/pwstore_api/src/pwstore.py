from aiohttp import web

from dbinit import DBconn
from utils import *


app: web.Application = web.Application()
conn: DBconn = DBconn(DB_PATH, INITFILE_PATH)
routes = web.RouteTableDef()


@routes.post('/register')
@JsonContentType
async def on_register(request: web.Request):
    try:
        uname, masterpw = await get_args(request, ('username', 'masterpw'))
    except MissingargumentError as e:
        return res_bad_request(str(e))

    try:
        register_user(conn, uname=uname, masterpw=masterpw)
    except ValueError as e:
        return res_conflict(str(e))
        
    return res_ok_created({
        'username': uname
    })

@routes.put('/addentry')
@JsonContentType
async def on_addentry(request: web.Request):
    try:
        uname, masterpw, pw_entry, description, pw_hash = await get_args(
            request, ('username', 'masterpw', 'pw_entry', 'description'), ('pw_hash',)
        )
    except MissingArgumentError as e:
        return res_bad_request(str(e))
    
    if not check_provided_pw(conn, uname, masterpw):
        return res_unauthorized('invalid credentials')

    try:
        pw_id = add_entry(conn, uname, pw_entry, description)
    except ValueError as e:
        return res_conflict(f'unable to add entry for user \'{uname}\': {str(e)}')

    return res_ok_created({
        'pw_entry': {
            'pw_id': pw_id,
            'description': description,
            'user': uname
    }})

@routes.get('/getentry')
@JsonContentType
#TODO
async def on_getentry(request: web.Request):
    try:
        uname, masterpw, pw_id, pw_hash = await get_args(
            request, ('username', 'masterpw', 'pw_id'), ('pw_hash',)
        )
    except MissingArgumentError as e:
        return res_bad_request(str(e))

    if not check_provided_pw(conn, uname, masterpw) or (pw_hash and not check_hash(conn, uname, pw_hash)):
        return res_unauthorized('invalid credentials')

    try:
        return res_ok({
            'pw_entry': get_entry(conn, pw_id)
        })
    except ValueError as e:
        return res_not_found(str(e))
    
    assert False, 'code line should be unreachable'

@routes.get('/isregistered')
async def on_isregistered(request: web.Request):
    if 'name' in request.query:
        user = is_user_registered(conn, request.query['name'])
        if user:
            return res_ok({'user': user})
        return res_not_found(request.query['name'])
    return res_bad_request('no "name" query parameter provided')
        

@routes.get('/getids')
@JsonContentType
async def on_getids(request: web.Request):
    try:
        uname, masterpw, pw_hash = await get_args(request, ('username', 'masterpw'), ('pw_hash',))
    except MissingArgumentError as e:
        return res_bad_request(str(e))

    if not check_provided_pw(conn, uname, masterpw) or (pw_hash and not check_hash(conn, uname, pw_hash)):
        return res_unauthorized('invalid credentials')

    try:
        return res_ok(get_ids(conn, uname))
    except ValueError as e:
        return res_not_found(str(e))

    assert False, 'code line should be unreachable'

if __name__ == '__main__':
    app.add_routes(routes)
    web.run_app(app, port=5102)
