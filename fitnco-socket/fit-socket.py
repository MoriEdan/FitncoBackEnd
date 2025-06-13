import eventlet
import socketio

sio = socketio.Server(cors_allowed_origins="*", always_connect=True, async_handlers=False, logger=True,
                      engineio_logger=True)
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})


@sio.event
def connect(sid, environ):
    print('-----------')
    print('user is connected', sid)
    print('-----------')


@sio.event
def disconnect(sid):
    print('-----------')
    print('user is disconnected', sid)
    print('-----------')


@sio.on('send')
def send(sid, data):
    print('message ', data)
    print('sid ', sid)
    return_data = {
        "to_user": data['to_user'],
        "method": data['method']
    }
    sio.emit('receive', return_data)


@sio.on('receive')
def receive(sid, data):
    print('message ', data)
    print('sid ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5005)), app)
