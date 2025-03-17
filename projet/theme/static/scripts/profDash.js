document.addEventListener("DOMContentLoaded", function () {
    console.log("Dashboard script loaded!");

    const modalBtns = document.querySelectorAll(".modal-button");
    const projectBtns = document.querySelectorAll(".project-link");
    const meetingBtns = document.querySelectorAll(".meeting-link"); 
    const modalBody = document.getElementById("modal-body-confirm");
    const modalTitle = document.getElementById("detailsModalLabel");
    const detailsModal = new bootstrap.Modal(document.getElementById("detailsModal"));

    console.log("Found quiz buttons:", modalBtns.length);
    console.log("Found project buttons:", projectBtns.length);
    console.log("Found meeting buttons:", meetingBtns.length);

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
            const id = modalBtn.getAttribute("data-pk");
            const name = modalBtn.getAttribute("data-quiz");
            const numbQuestions = modalBtn.getAttribute("data-questions");
            const difficulty = modalBtn.getAttribute("data-difficulty");
            const scoreToPass = modalBtn.getAttribute("data-pass");
            const time = modalBtn.getAttribute("data-time");

            console.log("Quiz Data:", { id, name, numbQuestions, difficulty, scoreToPass, time });
            // ✅ Update the "Modifier Quiz" button inside the modal
            
            
            const content = `
                <div class="h5 mb-3">Détails du Quiz: <strong>${name}</strong></div>
                <ul>
                    <li><strong>ID :</strong> ${id}</li>
                    <li><strong>Nombre de questions :</strong> ${numbQuestions}</li>
                    <li><strong>Difficulté :</strong> ${difficulty}</li>
                    <li><strong>Score à atteindre :</strong> ${scoreToPass}%</li>
                    <li><strong>Durée :</strong> ${time} minutes</li>
                </ul>
            `;
            let editBtn = document.getElementById("editQuizBtn");
            if (editBtn) {
                editBtn.href = `/edit-quiz/${id}/`; // Update link dynamically
            }
        
        
            openModal("Détails du Quiz", content);
        });
    });

    // Event listener for project links
    projectBtns.forEach(project => {
        project.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default link behavior

            console.log("Project clicked:", project);
            const projectId = project.getAttribute("data-pk");
            const projectTitle = project.getAttribute("data-title");
            const projectDescription = project.getAttribute("data-description");

            console.log("Project Data:", { projectTitle, projectDescription });

            let editBtn = document.getElementById("editQuizBtn");
            if (editBtn) {
                editBtn.href = `/edit-project/${projectId}/`; // Update link dynamically
            }
            const content = `
                <p><strong>ID du Projet:</strong> ${projectId}</p>
                <p><strong>Nom du Projet:</strong> ${projectTitle}</p>
                <p><strong>Description:</strong> ${projectDescription}</p>
            `;

            openModal("Détails du Projet", content);
        });
    });

    // Event listener for meeting links
    // Event listener for meeting links
meetingBtns.forEach(meet => {
    meet.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent default link behavior

        console.log("Meeting clicked:", meet);
        const meetId = meet.getAttribute("data-pk");
        const meetTitle = meet.getAttribute("data-title");
        const meetLink = meet.getAttribute("data-link");  // Fixing variable name
        const meetDescription = meet.getAttribute("data-description");

        console.log("Meeting Data:", { meetTitle, meetDescription, meetLink });

        let editBtn = document.getElementById("editQuizBtn");
        if (editBtn) {
            editBtn.href = `/edit-meeting/${meetId}/`; // Update link dynamically
        }

        const content = `
            <p><strong>ID du meeting:</strong> ${meetId}</p>
            <p><strong>Nom du meeting:</strong> ${meetTitle}</p>
            <p><strong>Meeting link:</strong> <a href="${meetLink}" target="_blank" class="text-blue-500 underline">${meetLink}</a></p>
            <p><strong>Description:</strong> ${meetDescription}</p>
        `;

        openModal("Détails du meeting", content);
    });
});


    //button of grades
    document.querySelectorAll(".save-btn").forEach(button => {
        button.addEventListener("click", function () {
            let studentId = this.getAttribute("data-student-id");
            let grades = [];

            document.querySelectorAll(`.grade-input[data-student-id="${studentId}"]`).forEach(input => {
                grades.push({
                    project_id: input.getAttribute("data-project-id"),
                    score: input.value
                });
            });

            fetch("/update_project_scores/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": "{{ csrf_token }}"
                },
                body: JSON.stringify({
                    student_id: studentId,
                    grades: grades
                })
            }).then(response => response.json())
              .then(data => {
                  if (data.success) {
                      alert("Notes mises à jour avec succès !");
                  } else {
                      alert("Erreur lors de la mise à jour des notes.");
                  }
              });
        });
    });
});


