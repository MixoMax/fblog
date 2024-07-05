from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
import os
import json

from md_to_json import convert_markdown_to_json

app = FastAPI()
articles_dir = "./articles"

json_404 = [
    {
        "tag": "h1",
        "text": "404 - Not Found",
        "style": "color: red;"
    },
    {
        "tag": "p",
        "text": "The requested page could not be found."
    }
]


@app.get("/")
def read_root():
    return FileResponse("./index.html")

@app.get("/{article_name}")
def read_index(article_name: str):
    return FileResponse("./index.html")

@app.get("/{article_name}/json")
def read_article_json(article_name: str):
    article_path = os.path.join(articles_dir, article_name + ".md")
    
    if not os.path.exists(article_path):
        return JSONResponse(content=json_404)
    
    cached_json_path = os.path.join(articles_dir, article_name + ".json")
    if os.path.exists(cached_json_path):
        metadata = os.stat(article_path)
        cached_metadata = os.stat(cached_json_path)
        if metadata.st_mtime < cached_metadata.st_mtime:
            # Cached JSON is newer than the markdown file
            with open(cached_json_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return JSONResponse(content=data)
    
    json_data = convert_markdown_to_json(article_path)
    with open(cached_json_path, "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)
    
    return JSONResponse(content=json_data)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    