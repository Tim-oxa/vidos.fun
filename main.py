from quart import Quart, render_template, websocket, redirect
import asyncio
import uuid


app = Quart(__name__)


rooms = {}


async def broadcast(ws, room: str, data: dict):
    try:
        await ws.send_json(data)
    except:
        rooms[room]["spectators"].discard(ws)


@app.get("/")
async def index():
    room = str(uuid.uuid4())
    rooms.setdefault(room, {
        "video": "https://vkvd551.okcdn.ru/?srcIp=77.37.182.155&pr=40&expires=1752348773320&srcAg=CHROME_MAC&fromCache=1&ms=185.226.55.189&type=5&subId=5282777991697&sig=p5x7YSVIsl4&ct=0&urls=45.136.20.178&clientType=13&appId=512000384397&id=8151257057809",
        "spectators": set()
    })
    return redirect("/host/"+room)


@app.get("/host/<room>")
async def host_page(room: str):
    if room in rooms:
        return await render_template("index.html", room=room, video_src=rooms[room]["video"])
    else:
        return 404


@app.get("/<room>")
async def spectator_page(room: str):
    if room in rooms:
        return await render_template("user.html", room=room, video_src=rooms[room]["video"])
    else:
        return 404


@app.websocket("/ws/host/<room>")
async def host_ws(room: str):
    if room in rooms:
        try:
            while True:
                data = await websocket.receive_json()
                print(data)
                tasks = []
                for ws in rooms[room]["spectators"].copy():
                    tasks.append(broadcast(ws, room, data))
                await asyncio.gather(*tasks, return_exceptions=True)
        except:
            pass
    else:
        await websocket.close(1000, "Комната не найдена")


@app.websocket("/ws/spectator/<room>")
async def spectator_ws(room: str):
    ws = websocket._get_current_object()
    if room in rooms:
        rooms[room]["spectators"].add(ws)
        try:
            while True:
                await websocket.receive()  # опционально
        except:
            pass
        finally:
            rooms[room]["spectators"].discard(ws)
    else:
        await websocket.close(1000, "Комната не найдена")


app.run("0.0.0.0", 116, debug=True)
