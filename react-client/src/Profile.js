import React from "react";

export default function Profile({ profile }) {
    if (!profile) {
        return "";
    }
    return (
        <header>
            <img src={profile.thumb_url} alt="profile" />
            <button>{profile.username}</button>
        </header>
    );
}