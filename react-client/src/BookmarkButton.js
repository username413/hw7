import React from "react";
import { getHeaders } from "./utils";

export default function BookmarkButton({ currBookmarkID, token, post, requeryPost }) {
    async function bookmark() {
        await fetch("/api/bookmarks/", {
            method: "POST",
            headers: getHeaders(token),
            body: JSON.stringify({ "post_id": post.id })
        });
        requeryPost();
    }

    async function unbookmark() {
        await fetch("/api/bookmarks/" + currBookmarkID, {
            method: "DELETE",
            headers: getHeaders(token)
        });
        requeryPost();
    }

    return (
        currBookmarkID == null
            ? <button type="button" title="Bookmark this post." onClick={bookmark}> <i aria-label="Post is not bookmarked." aria-checked="false" className="fa-regular fa-bookmark"></i> </button>
            : <button type="button" title="Unbookmark this post." onClick={unbookmark}> <i aria-label="Post is bookmarked." aria-checked="true" className="fa-solid fa-bookmark"></i> </button>
    );
}