import React, { useEffect, useContext } from 'react'

import {Link, NavLink} from 'react-router-dom';

import "../global.css";
import "./header.css";


function Header() {
    return (
        <header>
        <nav className="hbox" id="nav">
            <NavLink to="/" activeClassName="active">Home</NavLink>
            <NavLink to="/about" activeClassName="active">About</NavLink>
            <NavLink to="/contact" activeClassName="active">Contact</NavLink>
        </nav>
        </header>
    )
}

export default Header