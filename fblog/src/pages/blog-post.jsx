import React from 'react';
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import './blog_post.css'

const BlogPost = () => {
    const { postId } = useParams();
    console.log(postId);
    const [post, setPost] = useState(null);

    useEffect(() => {
        if (!postId) return;
        fetch(`https://jsonplaceholder.typicode.com/posts/${postId}`)
            .then((response) => response.json())
            .then((data) => setPost(data));
        
    }, [postId]);

    function splitText(text) {
        // split a long text into single <p> elements for each word (split by space)
        // for animation purposes
        return text.split(' ').map((word, index) => <span className='blog-word' key={index}>{word}</span>);
    }

    return post ? (
    <div className="blog-post">
        <h2>{post.title}</h2>
        <p className="blog-text">
            {splitText(post.body.repeat(100))}
        </p>
    </div>
    ) : (
    <p>Loading...</p>
    );
};

export default BlogPost;