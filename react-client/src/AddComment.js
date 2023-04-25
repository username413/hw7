import React from "react";
import { getHeaders } from "./utils";

export default function AddComment({ token, post, requeryPost }) {
    const postID = post.id;
    async function comment() {
        const userIn = document.querySelector("#comment-in-" + postID);
        await fetch("/api/comments/", {
            method: "POST",
            headers: getHeaders(token),
            body: JSON.stringify({
                "post_id": postID,
                "text": userIn.value
            })
        });
        requeryPost();
        userIn.value = "";
        userIn.focus();
    }

    return (
        <div id="add-comment">
            <form action="emote"><i className="fa-regular fa-face-smile"></i></form>
            <input type="text" id={"comment-in-" + postID} placeholder="Add a comment.." />
            <button type="submit" id="post-comment-button" onClick={comment}>Post</button>
        </div>
    );
}