import React from "react";

export default function Story({ story }) {
    return (
        <div>
            <img src={story.user.thumb_url} alt="user profile thumbnail"></img>
            <p>{story.user.username}</p>
        </div>
    )
}