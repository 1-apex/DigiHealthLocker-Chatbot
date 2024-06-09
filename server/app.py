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
async def message(sid, data):
    print('Received message:', data)
    response = process_message(data)
    print('Sending response:', response)
    await sio.emit('response', response, to=sid)

def process_message(message):
    message = "ajun tr kaam krty"
    return f"Processed: {message}"

if __name__ == '__main__':
    web.run_app(app, port=5000)
