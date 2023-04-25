import React, { useEffect, useState } from 'react';
import NavLinks from './NavLinks';
import Profile from './Profile';
import Stories from './Stories';
import Suggestions from './Suggestions';
import Posts from './Posts';
import { getHeaders } from './utils';
import Modal from './Modal';

export default function App({ token }) {
    const [profile, setProfile] = useState(null);
    useEffect(() => {
        async function fetchProfile() {
            const response = await fetch('/api/profile', {
                headers: getHeaders(token)
            });
            const data = await response.json();
            setProfile(data)
        }
        fetchProfile();
    }, [token]);

    return (
        <div>
            <nav className="main-nav">
                <h1>Photo App</h1>
                <NavLinks profile={profile} />
            </nav>

            <aside>
                <Profile profile={profile} />
                <Suggestions token={token} />
            </aside>
            <main>
                <Stories token={token} />

                <div id="posts">
                    <Posts token={token} />
                </div>

                <Modal />
            </main>
        </div>
    );

}