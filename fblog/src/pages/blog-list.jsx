import React, { useState, useEffect } from "react";
import { NavLink } from "react-router-dom";

import "./blog-list.css";

const BlogList = () => {
    const [posts, setPosts] = useState(null);

    useEffect(() => {
        fetch("https://jsonplaceholder.typicode.com/posts")
            .then((response) => response.json())
            .then((data) => setPosts(data));
    }, []);

    useEffect(() => {
        // make the <a> link undraggable
        var links = document.getElementsByClassName("blog-list-item-link");
        for (var i = 0; i < links.length; i++) {
            links[i].ondragstart = () => false;
        }
    }
    , [posts]);

    return (
        <div className="blog-list">
            <h1>Blog List</h1>
            <div id = "blog-list-container">
                {posts &&
                    posts.map((post) => (
                        <div key={post.id} className="blog-list-item">
                            <NavLink to={`/blog/${post.id}`} className="blog-list-item-link"></NavLink>
                            <h2>{post.title}</h2>
                            <p>{post.body.length < 100 ? post.body : post.body.slice(0, 100) + "..."}</p>
                        </div>
                    ))}
            </div>
        </div>
    );
}

export default BlogList;