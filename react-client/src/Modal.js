import React from "react";

export default function Modal() {
    const modalElement = document.querySelector('.modal-bg');

    function closeModal() {
        modalElement.classList.add("hidden");
        modalElement.setAttribute("aria-hidden", "true");
        // document.querySelector('.open').focus();
    }

    return (
        <div className="modal-bg hidden" aria-hidden="true" role="dialog">
            <button className="close" aria-label="Close the modal window" onClick={closeModal}>
                <i className="fa-sharp fa-solid fa-xmark"></i>
            </button>
            <section className="modal">
                <div className="modal-body">
                    <div className="image"></div>
                    <section className="the-comments">

                    </section>
                </div>
            </section>
        </div>
    );
}