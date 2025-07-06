from quart import Quart, render_template, websocket


app = Quart(__name__)


spectators = set()


@app.get("/")
async def index():
    video_src = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4"
    return await render_template("index.html", video_src=video_src)


@app.get("/view")
async def spectator_page():
    video_src = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4"
    return await render_template("user.html", video_src=video_src)


@app.websocket('/ws/host')
async def host_ws():
    try:
        while True:
            data = await websocket.receive_json()
            print(data)
            for ws in spectators.copy():
                try:
                    await ws.send_json(data)
                except:
                    spectators.discard(ws)
    except:
        pass


@app.websocket('/ws/spectator')
async def spectator_ws():
    ws = websocket._get_current_object()
    spectators.add(ws)
    try:
        while True:
            await websocket.receive()  # опционально
    except:
        pass
    finally:
        spectators.discard(ws)


app.run("0.0.0.0", 116, debug=True)
