import React, { useEffect } from "react";
import { getHeaders } from "./utils";

export default function Suggestion({ suggestion, token }) {
    let buttonText, aria_label, aria_checked
    if (suggestion.following) {
        buttonText = "unfollow";
        aria_label = "Following this user."
        aria_checked = "true";
    } else {
        buttonText = "follow";
        aria_label = "Not following this user."
        aria_checked = "false";
    }

    async function updateFollowing(userID) {
        const buttonValue = document.querySelector("#button_" + userID);
        if (buttonValue.innerHTML === "follow") {
            const res = await fetch("/api/following/", {
                method: "POST",
                headers: getHeaders(token),
                body: JSON.stringify({ "user_id": userID })
            });
            const data = await res.json();

            buttonValue.innerHTML = "unfollow";
            buttonValue.dataset.userid = data.id;
            document.querySelector("#suggestion-button-" + userID).setAttribute("aria-label", "Following this user.");
            document.querySelector("#suggestion-button-" + userID).setAttribute("aria-checked", "true");
        } else {
            await fetch("/api/following/" + buttonValue.dataset.userid, {
                method: "DELETE",
                headers: getHeaders(token)
            });

            buttonValue.innerHTML = "follow";
            document.querySelector("#suggestion-button-" + userID).setAttribute("aria-label", "Not following this user.");
            document.querySelector("#suggestion-button-" + userID).setAttribute("aria-checked", "false");
        }
    }

    return (
        <section id={"suggestion_" + suggestion.id} key={"suggestion_" + suggestion.id}>
            <img src={suggestion.following ? suggestion.following.image_url : suggestion.image_url} alt="suggested profile"></img>
            <div>
                <p className="username">
                    {suggestion.following ? suggestion.following.username : suggestion.username}
                </p>
                <p id="suggested-for-you">
                    suggested for you
                </p>
            </div>
            <div id={"suggestion-button-" + suggestion.id} aria-label={aria_label} aria-checked={aria_checked}>
                <button data-userid={suggestion.id} id={"button_" + suggestion.id} onClick={() => updateFollowing(suggestion.id)}>
                    {buttonText}
                </button>
            </div>
        </section>
    )
}