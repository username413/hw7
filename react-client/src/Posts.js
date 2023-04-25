import React, { useEffect, useState } from "react";
import Post from "./Post";
import { getHeaders } from "./utils";

export default function Posts({ token }) {
    const [posts, setPost] = useState(null);
    useEffect(() => {
        async function getPosts() {
            const res = await fetch("/api/posts", {
                headers: getHeaders(token)
            });
            const data = await res.json();
            setPost(data);
        }
        getPosts();
    }, [token])

    if (!posts) {
        return "";
    }
    return (
        posts.map(post => {
            return <Post token={token} post={post} />
        })
    );
}