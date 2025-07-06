from quart import Quart, render_template


app = Quart(__name__)


@app.get("/")
async def index():
    video_src = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4"
    return await render_template("index.html", video_src=video_src)


app.run("0.0.0.0", 116)
