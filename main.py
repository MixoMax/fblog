from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
import os
import json

from md_to_json import convert_markdown_to_json

app = FastAPI()
articles_dir = "./articles"
base_url = "http://localhost:8000"

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

def get_article_data(article_name) -> dict:
    article_path = os.path.join(articles_dir, article_name + ".md")
    if not os.path.exists(article_path):
        return None
    
    cached_json_path = os.path.join(articles_dir, article_name + ".json")
    
    if not os.path.exists(cached_json_path):
        data = convert_markdown_to_json(article_path)
        with open(cached_json_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    else:
        metadata = os.stat(article_path)
        cached_metadata = os.stat(cached_json_path)
        if metadata.st_mtime > cached_metadata.st_mtime:
            # Markdown file is newer than the cached JSON
            data = convert_markdown_to_json(article_path)
            with open(cached_json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        else:
            with open(cached_json_path, "r", encoding="utf-8") as file:
                data = json.load(file)
    
    return data

def get_all_article_names() -> list:
    articles = []
    for file in os.listdir(articles_dir):
        if file.endswith(".md"):
            article_name = file[:-3]
            articles.append(article_name)
    return articles


@app.get("/")
def read_root():
    return FileResponse("./index.html")

@app.get("/api/articles_descriptions")
def read_all_articles():
    """
    Get a list of all articles in the articles directory

    returns:
    a list of:
        {
            "title": str,
            "url": str
            "description": str
        }
    """
    articles = get_all_article_names()
    
    articles_data = []
    for article_name in articles:
        data = get_article_data(article_name)
        
        title = None
        description = ""
        for element in data:
            tag = element["tag"]
            if tag == "h1" and title is None:
                title = element["text"]
            
            elif tag in ["p", "h2", "h3", "a"] and len(description) < 100:
                description += element["text"]
                description += " "
        
        if title is None:
            title = article_name
        
        articles_data.append({
            "title": title,
            "url": article_name,
            "description": description
        })

    return JSONResponse(content=articles_data)

@app.get("/api/search")
async def search_articles(q: str):

    article_names = get_all_article_names()
    articles_data = []
    for article_name in article_names:
        data = get_article_data(article_name)
        
        for element in data:
            if "text" in element:
                if q.lower() in element["text"].lower():
                    articles_data.append({
                        "title": element["text"],
                        "url": article_name
                    })
                    break
    
    return JSONResponse(content=articles_data)


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
    