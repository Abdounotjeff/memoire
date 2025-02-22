document.addEventListener("DOMContentLoaded", function () {

    const modalBtns = document.querySelectorAll(".modal-button");
    const modalBody = document.getElementById("modal-body-confirm");

    console.log("Found buttons:", modalBtns.length);  // Debugging

    modalBtns.forEach(modalBtn => {
        modalBtn.addEventListener("click", function () {

            const name = modalBtn.getAttribute("data-quiz");
            const numbQuestions = modalBtn.getAttribute("data-questions");
            const scoreToPass = modalBtn.getAttribute("data-pass");
            const time = modalBtn.getAttribute("data-time");

            modalBody.innerHTML = `
                <div class="h5 mb-3">Vous êtes sûr de commencer le quiz <strong>${name}</strong> ?</div>
                <ul>
                    <li><strong>Nombre de questions :</strong> ${numbQuestions}</li>
                    <li><strong>Score à atteindre :</strong> ${scoreToPass}%</li>
                    <li><strong>Durée :</strong> ${time} minutes</li>
                </ul>
            `;
        });
    });
});
