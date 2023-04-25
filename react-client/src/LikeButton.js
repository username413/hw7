import React from "react";
import { getHeaders } from "./utils";

export default function LikeButton({ currLikeID, token, post, requeryPost }) {
    async function like() {
        await fetch("/api/posts/likes/", {
            method: "POST",
            headers: getHeaders(token),
            body: JSON.stringify({ "post_id": post.id })
        });
        requeryPost();
    }

    async function unlike() {
        await fetch("/api/posts/likes/" + currLikeID, {
            method: "DELETE",
            headers: getHeaders(token)
        });
        requeryPost();
    }

    return (
        currLikeID == null
            ? <button type="button" title="Like this post." onClick={like}> <i aria-label="Post is not liked." aria-checked="false" className="fa-regular fa-heart"></i> </button>
            : <button type="button" title="Unlike this post." onClick={unlike}> <i aria-label="Post is liked." aria-checked="true" className="fa-solid fa-heart" style={{ color: "red" }}></i> </button>
    );
}