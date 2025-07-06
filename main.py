from quart import Quart, render_template, jsonify, request
import random
import uuid


app = Quart(__name__)


users = {}


@app.get("/")
async def index():
    video_src = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4"
    return await render_template("index.html", video_src=video_src)


# @app.get("/init")
# async def init():
#     uid = uuid.uuid4()
#     users.setdefault(uid, {
#         "session": 1
#     })


@app.post("/updateTime")
async def update_time():
    data = await request.get_json()
    print(data)
    return "OK"


@app.post("/test")
async def update():
    data = await request.get_json()
    print(data["currentTime"])
    data = {
        "test": random.randint(1, 47)
    }
    return jsonify(data)


app.run("0.0.0.0", 116, debug=True)
