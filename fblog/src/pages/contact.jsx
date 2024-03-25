import React from 'react';

const ContactPage = () => {
    return (
        <div>
            <h1>Contact Us</h1>
            <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod
                justo nec tortor tincidunt, id aliquet nunc ultrices. Nulla facilisi.
                Nullam nec elit id nunc tincidunt tincidunt. Sed sed nunc id nunc
                tincidunt tincidunt. Sed sed nunc id nunc tincidunt tincidunt. Sed sed
                nunc id nunc tincidunt tincidunt.
            </p>
            <form>
                <label htmlFor="name">Name:</label>
                <input type="text" id="name" name="name" />

                <label htmlFor="email">Email:</label>
                <input type="email" id="email" name="email" />

                <label htmlFor="message">Message:</label>
                <textarea id="message" name="message" rows="4" />

                <button type="submit">Submit</button>
            </form>
        </div>
    );
};

export default ContactPage;