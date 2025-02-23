console.log("Quiz.js loaded!");

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded.");

    const modalBtns = document.querySelectorAll(".modal-button");
    const modalBody = document.getElementById("modal-body-confirm");

    console.log("Found buttons:", modalBtns.length);  // Debugging

    modalBtns.forEach(modalBtn => {
        modalBtn.addEventListener("click", function () {
            console.log("Button clicked:", modalBtn);
            const quizId = modalBtn.getAttribute("data-pk");
            const name = modalBtn.getAttribute("data-quiz");
            const numbQuestions = modalBtn.getAttribute("data-questions");
            const difficulty = modalBtn.getAttribute("data-difficulty");
            const scoreToPass = modalBtn.getAttribute("data-pass");
            const time = modalBtn.getAttribute("data-time");

            console.log("Data Attributes:", { name, numbQuestions, difficulty, scoreToPass, time });

            modalBody.innerHTML = `
                <div class="h5 mb-3">Vous êtes sûr de commencer le quiz <strong>${name}</strong> ?</div>
                <ul>
                    <li><strong>Nombre de questions :</strong> ${numbQuestions}</li>
                    <li><strong>Difficulté :</strong> ${difficulty}</li>
                    <li><strong>Score à atteindre :</strong> ${scoreToPass}%</li>
                    <li><strong>Durée :</strong> ${time} minutes</li>
                </ul>
            `;
            // Set the "Commencer" button's link dynamically
            startButton.onclick = function () {
                window.location.href = `/quizes/${quizId}/`;  // Adjust the URL structure as needed
            };
        });
    });
});
