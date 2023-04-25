import React, { useEffect, useState } from 'react';
import Suggestion from './Suggestion';
import { getHeaders } from './utils';

export default function Suggestions({ token }) {
    const [suggestions, setSuggestions] = useState(null);
    useEffect(() => {
        async function suggestedAccs() {
            const res = await fetch("/api/suggestions/", {
                headers: getHeaders(token)
            });
            const data = await res.json();
            setSuggestions(data);
        }
        suggestedAccs()
    }, [token])

    if (!suggestions) {
        return "";
    }
    return (
        <section className="suggestions">
            <p>Suggestions for you</p>
            {
                suggestions.map(suggestion => {
                    return <Suggestion suggestion={suggestion} token={token} />
                })
            }
        </section>
    );
}