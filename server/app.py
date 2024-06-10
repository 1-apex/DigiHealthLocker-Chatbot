import socketio
from aiohttp import web

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

@sio.event
async def connect(sid, environ):
    print('Client connected:', sid)

@sio.event
async def disconnect(sid):
    print('Client disconnected:', sid)

@sio.event
async def py_client_message(sid, data):
    print('Received message:', data)

    response = process_message(data['message'])
    # print('Sending response:', response)
    data['message'] = response

    await sio.emit('py_bot_response', data, to=sid)

def process_message(message):
    message = "ajun tr kaam krty"
    return f"{message}"

if __name__ == '__main__':
    web.run_app(app, port=5000)
