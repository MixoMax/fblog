import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./blog_post.css";

const BlogPost = () => {
    const { postId } = useParams();
    const [post, setPost] = useState(null);
    const [scroll_Y, setScroll_Y] = useState(0);


    useEffect(() => {
        console.log(postId);
        if (!postId) return;

        fetch(`https://jsonplaceholder.typicode.com/posts/${postId}`)
            .then((response) => response.json())
            .then((data) => setPost(
                {
                    title: data.title,
                    body: data.body.repeat(100)
                }
                ));
    }, [postId]);

    useEffect(() => {
        window.addEventListener("scroll", () => {
            setScroll_Y(window.scrollY);
        });
    }
    , []);

    useEffect(() => {
        console.log(scroll_Y);
        var window_height = window.innerHeight;
        var animation_end_pos = window_height * 0.1;
        // for each blog-text-line, check if it is in the viewport
        var blog_text_lines = document.getElementsByClassName("blog-text-line");
        console.log(blog_text_lines.length);

        for (var i = 0; i < blog_text_lines.length; i++) {
            var line = blog_text_lines[i];
            var line_top = line.getBoundingClientRect().top;
            var animation_has_started = line.getAttribute("animation-has-started");
            

            // check if the line is in the viewport
            if (line_top < window_height && !animation_has_started) {
                // animation goes here
                var distance_from_bottom = Math.abs(window_height - line_top);
                var percent_overlap = distance_from_bottom / animation_end_pos;
                var percent_overlap = Math.min(1, percent_overlap);

                var scale_range = [0.2, 1];
                var opacity_range = [0, 1];

                var scale = scale_range[0] + percent_overlap * (scale_range[1] - scale_range[0]);
                var opacity = opacity_range[0] + percent_overlap * (opacity_range[1] - opacity_range[0]);

                line.style.transform = `scale(${scale})`;
                line.style.opacity = opacity;
            }
        }

    }, [scroll_Y]);

    const splitText = (text) => { // Function to split text into lines
        return text.split("\n").map((line, index) => (
            <p 
            className="blog-text-line" 
            key={index}
            >
                {line}
            </p>
        ));
    };

    return post ? (
        <div className="blog-post">
            <h1>{post.title}</h1>
            <div className="blog-text">
                <p>{splitText(post.body)}</p>
            </div>
        </div>
    ) : (
        <p>Loading...</p>
    );
};

export default BlogPost;