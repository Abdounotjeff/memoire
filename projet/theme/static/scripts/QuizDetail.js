document.addEventListener("DOMContentLoaded", function () {
    console.log("QuizDetail.js loaded!");

    const quizBox = document.getElementById("quiz-box");
    const scoreBox = document.getElementById("score-box");
    const resultBox = document.getElementById("result-box");
    const timerBox = document.getElementById("timer-box");
    const quizForm = document.getElementById("quiz-form");
    const csrf = document.getElementsByName("csrfmiddlewaretoken")[0];

    if (!quizBox) {
        console.error("Element #quiz-box not found!");
        return;
    }

    const baseUrl = window.location.href.endsWith("/") ? window.location.href : window.location.href + "/";

    const activateTimer = (time) => {
        let minutes = time - 1;
        let seconds = 60;
        timerBox.innerHTML = `<b>${String(time).padStart(2, "0")}:00</b>`;

        const timer = setInterval(() => {
            seconds--;
            if (seconds < 0) {
                seconds = 59;
                minutes--;
            }

            let displayMinutes = String(minutes).padStart(2, "0");
            let displaySeconds = String(seconds).padStart(2, "0");

            if (minutes === 0 && seconds === 0) {
                clearInterval(timer);
                timerBox.innerHTML = "<b>00:00</b>";
                setTimeout(() => {
                    alert("Time's up!");
                    sendData();
                }, 500);
            } else {
                timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`;
            }
        }, 1000);
    };

    // Fetch quiz data
    $.ajax({
        type: "GET",
        url: baseUrl + "data",
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

            // Start the timer after loading the quiz
            if (response.time) {
                activateTimer(response.time);
            }
        },
        error: function (error) {
            console.error("Error fetching quiz data:", error);
        }
    });

    const sendData = () => {
        if (!csrf) {
            console.error("CSRF token missing!");
            return;
        }

        const elements = [...document.getElementsByClassName("ans")];
        const data = { csrfmiddlewaretoken: csrf.value };

        elements.forEach(el => {
            if (el.checked) {
                data[el.name] = el.value;
            } else if (!(el.name in data)) {
                data[el.name] = null;  // Ensures unanswered questions are recorded once
            }
        });

        $.ajax({
            type: "POST",
            url: baseUrl + "save/",
            data: data,
            success: function (response) {
                console.log(response);
                quizForm.style.display = "none";

                scoreBox.innerHTML = `${response.passed ? "🎉 Congratulations! " : "😞 Oops... "} You scored: ${response.score.toFixed(2)}%`;

                resultBox.innerHTML = ""; // Clear previous results
                response.results.forEach(res => {
                    const resDiv = document.createElement("div");
                    resDiv.style.padding = "1rem";
                    resDiv.style.color = "white";
                    resDiv.style.fontSize = "1.75rem";
                    resDiv.style.backgroundColor = "#343a40";
                    resDiv.style.borderRadius = "5px";
                    resDiv.style.marginBottom = "1rem";

                    for (const [question, resp] of Object.entries(res)) {
                        resDiv.innerHTML += `<b>${question}</b><br>`;
                        if (resp === "not answered") {
                            resDiv.innerHTML += "❌ Not answered";
                            resDiv.classList.add("bg-danger");
                        } else {
                            const answer = resp["answered"];
                            const correct = resp["correct Answer"];

                            if (answer === correct) {
                                resDiv.classList.add("bg-success");
                                resDiv.innerHTML += `✅ Correct Answer: ${correct} | You answered: ${answer}`;
                            } else {
                                resDiv.classList.add("bg-warning");
                                resDiv.innerHTML += `❌ Correct Answer: ${correct} | You answered: ${answer}`;
                            }
                        }
                    }
                    resultBox.appendChild(resDiv);
                });
            },
            error: function (xhr, status, error) {
                console.error("AJAX Error:", status, error);
            }
        });
    };

    quizForm.addEventListener("submit", (e) => {
        e.preventDefault();
        sendData();
    });
});
