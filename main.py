from fastapi import FastAPI, WebSocket
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect

templates = Jinja2Templates(directory='templates')


async def message_list(request):
    return templates.TemplateResponse('index.html', {'request': request})

routes = [
    Route('/', endpoint=message_list),
    Mount('/static', app=StaticFiles(directory='static'), name='static')
]

app = FastAPI(debug=True, routes=routes)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    message_id = 1
    await websocket.accept()

    while True:
        try:
            data = await websocket.receive_json()
            message = data.get('send_message')
            response = {
                "send_message": message,
                "message_id": message_id,
            }
            message_id += 1
            await websocket.send_json(response)

        except WebSocketDisconnect:
            pass

        except RuntimeError:
            break

