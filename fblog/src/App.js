import logo from './logo.svg';
import './App.css';

import Header from './components/header';

import { HashRouter as Router, Routes, Route } from 'react-router-dom';


import Home from './pages/home';
import ContactPage from './pages/contact';
import About from './pages/about';
import BlogPost from './pages/blog-post';

function App() {

  return (
    <div className="App">
      <Router>
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<ContactPage />} />

          // wildcard route for blog posts
          <Route path="blog/:blog_name" element={<BlogPost/>} />
          
        </Routes>
      </Router>
    </div>
  );
}

export default App;
