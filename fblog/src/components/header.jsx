import React, { useEffect, useContext } from 'react'

import {Link, NavLink} from 'react-router-dom';

import "../global.css";
import "./header.css";


function Header() {
    return (
        <header>
            <nav className="hbox" id="nav">
                <NavLink to="/" activeClassName="active" className="logo nav-item">FBlog</NavLink>
                <NavLink to="/blog/list" activeClassName="active" className="nav-item">Blog</NavLink>
                <NavLink to="/about" activeClassName="active" className="nav-item">About</NavLink>
                <NavLink to="/contact" activeClassName="active" className="nav-item">Contact</NavLink>
            </nav>
        </header>
    )
}

export default Header