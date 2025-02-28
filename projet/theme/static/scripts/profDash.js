document.addEventListener("DOMContentLoaded", function () {
    console.log("Dashboard script loaded!");

    const modalBtns = document.querySelectorAll(".modal-button");
    const projectBtns = document.querySelectorAll(".project-link");
    const modalBody = document.getElementById("modal-body-confirm");
    const modalTitle = document.getElementById("detailsModalLabel");
    const detailsModal = new bootstrap.Modal(document.getElementById("detailsModal"));

    console.log("Found quiz buttons:", modalBtns.length);
    console.log("Found project buttons:", projectBtns.length);

    // Function to open modal with dynamic content
    function openModal(title, content) {
        modalTitle.innerText = title;
        modalBody.innerHTML = content;
        detailsModal.show();
    }

    // Event listener for quiz buttons
    modalBtns.forEach(modalBtn => {
        modalBtn.addEventListener("click", function () {
            console.log("Quiz clicked:", modalBtn);
            const name = modalBtn.getAttribute("data-quiz");
            const numbQuestions = modalBtn.getAttribute("data-questions");
            const difficulty = modalBtn.getAttribute("data-difficulty");
            const scoreToPass = modalBtn.getAttribute("data-pass");
            const time = modalBtn.getAttribute("data-time");

            console.log("Quiz Data:", { name, numbQuestions, difficulty, scoreToPass, time });

            const content = `
                <div class="h5 mb-3">Détails du Quiz: <strong>${name}</strong></div>
                <ul>
                    <li><strong>Nombre de questions :</strong> ${numbQuestions}</li>
                    <li><strong>Difficulté :</strong> ${difficulty}</li>
                    <li><strong>Score à atteindre :</strong> ${scoreToPass}%</li>
                    <li><strong>Durée :</strong> ${time} minutes</li>
                </ul>
            `;

            openModal("Détails du Quiz", content);
        });
    });

    // Event listener for project links
    projectBtns.forEach(project => {
        project.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default link behavior

            console.log("Project clicked:", project);
            const projectTitle = project.getAttribute("data-title");
            const projectDescription = project.getAttribute("data-description");

            console.log("Project Data:", { projectTitle, projectDescription });

            const content = `
                <p><strong>Nom du Projet:</strong> ${projectTitle}</p>
                <p><strong>Description:</strong> ${projectDescription}</p>
            `;

            openModal("Détails du Projet", content);
        });
    });
});

