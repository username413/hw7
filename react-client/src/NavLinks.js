import React from "react";

export default function NavLinks({ profile }) {
    if (!profile) {
        return '';
    }
    return (
        <ul>
            <li>
                <button id="blue-highlight">API Docs</button>
            </li>
            <li>
                <button>{profile.username}</button>
                </li>
            <li>
                <button id="blue-highlight">Sign out</button>
            </li>
        </ul>
    );

}
