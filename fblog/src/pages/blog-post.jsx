import React from 'react';
import { useState, useEffect } from 'react';

const BlogPost = () => {
    //window.location.href

    const [blog_name, setBlogName] = useState('');
    useEffect(() => {
      setBlogName(window.location.href.split('/').pop());
    }, []);

    function get_blog_html() {
      return `<h1>${blog_name}</h1>
      <p>This is a blog post.</p>`;
    }

    return (
      <div>
        <div dangerouslySetInnerHTML={{ __html: get_blog_html(blog_name) }} />
      </div>
    );
  };

export default BlogPost;