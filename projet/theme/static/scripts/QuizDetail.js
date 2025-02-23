document.addEventListener("DOMContentLoaded", function () {
    console.log("QuizDetail.js loaded!");

    const quizBox = document.getElementById("quiz-box");
    if (!quizBox) {
        console.error("Element #quiz-box not found!");
        return; // Stop execution if the element doesn't exist
    }

    const url = window.location.href;

    $.ajax({
        type: "GET",
        url: `${url}data`,  // Ensure the endpoint is correct
        success: function (response) {
            console.log(response);
            const data = response.data;

            data.forEach(el => {
                for (const [question, answers] of Object.entries(el)) {
                    quizBox.innerHTML += `
                        <hr>
                        <div class="mb-2">
                            <b>${question}</b>
                        </div>
                    `;

                    answers.forEach(answer => {
                        quizBox.innerHTML += `
                            <div>
                                <input type="radio" name="${question}" value="${answer}" class="ans" id="${question}-${answer}">
                                <label for="${question}-${answer}">${answer}</label>
                            </div>
                        `;
                    });
                }
            });
        },
        error: function (error) {
            console.log(error);
        }
    });
});
