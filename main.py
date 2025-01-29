from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse, HTMLResponse
import uvicorn

import markdown

import requests
import os
import sys

from datetime import datetime

from core import DB, get_vector, BlogPost

app = FastAPI()

db = DB("./data/blog.db")


def md_to_html(md_str: str) -> str:
    return markdown.markdown(md_str)



@app.get("/api/v1/search")
async def search(q: str):
    """
    GET /api/v1/search?q={q}

    Returns a list of posts that match the search query {q} in this JSON format:

        [
        {
            "id": int
            "title": str,
            "title_cleaned": str,
            "summary": str,
            "created_at": str,
            "author": str,
            "tags": list[str],
            "url": str
        },
        ...
    ]
    """

    global db
    posts: list[BlogPost] = db.search_posts(q)
    data = [post.to_json() for post in posts]
    return JSONResponse(content=data)

@app.get("/api/v1/newest_posts")
async def newest_posts(limit: int = 10):
    """
    GET /api/v1/newest_posts

    Returns the {limit:int=10} newest posts in this JSON format:

    [
        {
            "id": int
            "title": str,
            "title_cleaned": str,
            "summary": str,
            "created_at": str,
            "author": str,
            "tags": list[str],
            "url": str
        },
        ...
    ]
    """
    global db
    posts: list[BlogPost] = db.newest_posts(limit)
    data = [post.to_json() for post in posts]
    for post, d in zip(posts, data):
        d["url"] = f"/{post.title_cleaned}"
    return JSONResponse(content=data)

@app.get("/api/v1/_reindex")
async def reindex():
    global db
    db.background_process()
    return JSONResponse(content={"status": "success"})

@app.get("/api/v1/get_post")
async def get_post(post_id: int):
    global db
    post = db.get_post(post_id)
    if post is None:
        return JSONResponse(content={"status": "error", "message": "Post not found"})
    return JSONResponse(content=post.to_json())


@app.get("/")
@app.get("/index.html")
async def index():
    return FileResponse("./static/index.html")

@app.get("/styles.css")
async def style():
    return FileResponse("./static/styles.css")


@app.get("/error/{code}")
async def error(code: int):
    fp = f"./static/error/{code}.html"
    if os.path.exists(fp):
        return FileResponse(fp)
    else:
        return FileResponse("./static/error/404.html")


@app.get("/{post_title_cleaned}")
async def post(post_title_cleaned: str):
    global db
    post = db.get_post_by_cleaned_title(post_title_cleaned)

    if post is None:
        return RedirectResponse(url="/error/404")
    
    with open("./static/post_template.html", "r", encoding="utf-8") as f:
        template = f.read()
    
    replacements = {
        "[TITLE]": post.title,
        "[CONTENT]": md_to_html(post.content),
        "[CREATED_AT]": str(post.created_at.strftime("%d %B %Y")),
        "[AUTHOR]": post.author,
        "[TAGS]": ", ".join(post.tags)
    }

    for key, value in replacements.items():
        template = template.replace(key, value)
    
    return HTMLResponse(content=template)



if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    uvicorn.run(app, host="0.0.0.0", port=port)