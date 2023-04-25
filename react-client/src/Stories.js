import React, { useEffect, useState } from 'react';
import Story from './Story';
import { getHeaders } from './utils';

export default function Stories({ token }) {
    const [stories, setStory] = useState(null);
    useEffect(() => {
        async function getStories() {
            const res = await fetch("/api/stories", {
                headers: getHeaders(token)
            });
            const data = await res.json();
            setStory(data);
        }
        getStories();
    }, [token])

    if (!stories) {
        return "";
    }
    return (
        <header className="stories">
            {
                stories.map(story => {
                    return <Story story={story}></Story>
                })
            }
        </header>
    );
}