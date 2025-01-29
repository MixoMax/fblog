import datetime
import json
import os
import sqlite3

from dataclasses import dataclass
from enum import Enum

import openai
import requests

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


# TODO:
# Add post categories
# Add post tags support

BASE_URL = "http://localhost:8000"
# BASE_URL = "https://blog.linush.org"


with open("./openrouter.token", "r") as f:
    token = f.read().strip()

client = openai.Client(
    base_url="https://openrouter.ai/api/v1",
    api_key=token
)

with open("./data/prompt.txt", "r") as f:
    prompt = f.read().strip()


class QdrantStatus(Enum):
    WAITING_FOR_SUMMARY = 0
    READY = 1
    DONE = 2

qdrant = QdrantClient(url="http://188.245.231.101:6333/")

try:
    qdrant.create_collection(
        collection_name="blog",
        vectors_config=VectorParams(
            size=1024,
            distance=Distance.COSINE
        )
    )
except:
    pass



def get_completion(model_id: str, q: str) -> str:
    global client, extra_headers
    completion = client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": "user",
                "content": q
            }
        ]
    )
    return completion.choices[0].message.content

default_model_id = "google/gemini-flash-1.5-8b"



embed_base_url = "https://embedding-api.linush.org"
embed_url = "{embed_base_url}/api/v1/embedding?text={text}"
embed_session = requests.Session()



def get_vector(query: str) -> list[float]:
    url = embed_url.format(embed_base_url=embed_base_url, text=query)
    response = embed_session.get(url)
    embedding = response.json()["embedding"]
    return embedding


@dataclass
class BlogPost:
    id: int
    title: str
    title_cleaned: str
    content: str
    summary: str
    created_at: datetime.datetime
    author: str
    tags: list[str]
    qdrant_status: QdrantStatus

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "title_cleaned": self.title_cleaned,
            "content": self.content,
            "summary": self.summary,
            "created_at": self.created_at.isoformat(),
            "author": self.author,
            "tags": self.tags,
            "qdrant_status": self.qdrant_status.value
        }
    
    @staticmethod
    def from_json(data: dict) -> "BlogPost":
        return BlogPost(
            id=data["id"],
            title=data["title"],
            title_cleaned=data["title_cleaned"],
            content=data["content"],
            summary=data["summary"],
            created_at=datetime.datetime.fromisoformat(data["created_at"]),
            author=data["author"],
            tags=data["tags"],
            qdrant_status=QdrantStatus(data["qdrant_status"])
        )
    
    @staticmethod
    def from_db_row(row: tuple) -> "BlogPost":
        return BlogPost(
            id=row[0],
            title=row[1],
            title_cleaned=row[2],
            content=row[3],
            summary=row[4],
            created_at=datetime.datetime.fromisoformat(row[5]),
            author=row[6],
            tags=json.loads(row[7]),
            qdrant_status=QdrantStatus(row[8])
        )
    
    def to_db_row(self) -> tuple:
        return (
            self.id,
            self.title,
            self.title_cleaned,
            self.content,
            self.summary,
            self.created_at.isoformat(),
            self.author,
            json.dumps(self.tags),
            self.qdrant_status.value
        )
    
    def process(self):
        global prompt

        if self.qdrant_status == QdrantStatus.WAITING_FOR_SUMMARY:
            q = prompt.replace("[TITLE]", self.title).replace("[CONTENT]", self.content)
            completion = get_completion(default_model_id, q)
            self.summary = completion
            self.qdrant_status = QdrantStatus.READY
        if self.qdrant_status == QdrantStatus.READY:
            vector = get_vector(self.summary)

            point = PointStruct(
                id=self.id,
                vector=vector,
                payload=self.to_json()
            )
            qdrant.upsert(
                collection_name="blog",
                points=[point],
                wait=True
            )
            self.qdrant_status = QdrantStatus.DONE
        
        return self

    def __hash__(self):
        return hash(self.content + self.title + self.author + self.created_at.isoformat() + str(self.summary) + str(self.tags))


class DB:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                title TEXT,
                title_cleaned TEXT,
                content TEXT,
                summary TEXT,
                created_at TEXT,
                author TEXT,
                tags TEXT,
                qdrant_status INTEGER
            )
        """)
        self.conn.commit()
    
    def add_post(self, post: BlogPost):
        self.cursor.execute("INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", post.to_db_row())
        self.conn.commit()
    
    def get_post(self, post_id: int) -> BlogPost:
        self.cursor.execute("SELECT * FROM posts WHERE id=?", (post_id,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        return BlogPost.from_db_row(row)
    
    
    def get_post_by_cleaned_title(self, title: str) -> BlogPost:
        self.cursor.execute("SELECT * FROM posts WHERE title_cleaned=?", (title,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        return BlogPost.from_db_row(row)
    
    
    def get_all_posts(self) -> list[BlogPost]:
        self.cursor.execute("SELECT * FROM posts")
        rows = self.cursor.fetchall()
        return [BlogPost.from_db_row(row) for row in rows]
    
    def update_post(self, post: BlogPost):
        cmd = "UPDATE posts SET title=?, title_cleaned=?, content=?, summary=?, created_at=?, author=?, tags=?, qdrant_status=? WHERE id=?"
        params = [*post.to_db_row()[1:], post.id]
        self.cursor.execute(cmd, params)
        self.conn.commit()
        
    
    def delete_post(self, post_id: int):
        self.cursor.execute("DELETE FROM posts WHERE id=?", (post_id,))
        self.conn.commit()
    
    def search_posts(self, query: str, limit: int = 10) -> list[BlogPost]:
        vector = get_vector(query)
        points = qdrant.search(
            collection_name="blog",
            query_vector=vector,
            limit=limit,
            with_payload=True
        )
        return [BlogPost.from_json(point.payload) for point in points]
    
    def newest_posts(self, limit: int = 10) -> list[BlogPost]:
        self.cursor.execute("SELECT * FROM posts ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = self.cursor.fetchall()
        return [BlogPost.from_db_row(row) for row in rows]
    

    def background_process(self):
        # Background process:
        # 1. poll ./posts directory for new .md files and add them to the database
        # 2. process all posts in the database
        # 3. update the database with the processed posts

        if os.path.exists("./data/lock.txt"):
            #return
            pass
        
        with open("./data/lock.txt", "w") as f:
            f.write("lock")

        new_post_ids = []

        for file in os.listdir("./posts"):
            print(file)
            if file.endswith(".md"):
                with open(f"./posts/{file}", "r", encoding="utf-8") as f:
                    content_lines = f.readlines()
                
                title = content_lines[0].lstrip("#").strip()
                title_cleaned = title.replace(" ", "-").lower()
                content = "".join(content_lines[1:]).strip()
                
                post = BlogPost(
                    id=None,
                    title=title,
                    title_cleaned=title_cleaned,
                    content=content,
                    summary="",
                    created_at=datetime.datetime.now(),
                    author="Linus Horn",
                    tags=[],
                    qdrant_status=QdrantStatus.WAITING_FOR_SUMMARY
                )

                if self.get_post_by_cleaned_title(title_cleaned) is None:
                    self.add_post(post)
                    new_post_ids.append(self.get_post_by_cleaned_title(title_cleaned).id)
                else:
                    existing_post = self.get_post_by_cleaned_title(title_cleaned)
                    # compare timestamps
                    if existing_post.created_at < post.created_at:
                        post.id = existing_post.id
                        self.update_post(post)
                        new_post_ids.append(existing_post.id)
        

        print("New post ids:", new_post_ids)


        for post_id in new_post_ids:
            post = self.get_post(int(post_id))

            with open("./a.json", "w") as f:
                f.write(json.dumps(post.to_json(), indent=4))
            
            post.process()

            with open("./b.json", "w") as f:
                f.write(json.dumps(post.to_json(), indent=4))
            
            self.update_post(post)

        

        try:
            os.remove("./data/lock.txt")
        except:
            pass
    
    def close(self):
        self.conn.close()

