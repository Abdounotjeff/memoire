@login_required
def edit_quiz(request, quiz_id):    
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Ensure only the professor who created the quiz can edit it
    if not request.user.is_professor() or quiz.created_by != request.user.professor:
        messages.error(request, "You are not authorized to edit this quiz.")
        return redirect('index')  # Redirect unauthorized users

    if request.method == "POST":
        form = QuizForm(request.POST, instance=quiz, professor=request.user.professor)
        if form.is_valid():
            form.save()

            # Handle questions and answers
            questions_texts = request.POST.getlist("questions[]")  # Get all questions
            correct_answers = request.POST.getlist("correct_answers[]")  # Get correct answers

            # Clear existing questions (optional, but be cautious)
            quiz.question_set.all().delete()

            for i, question_text in enumerate(questions_texts):
                if question_text.strip():
                    # Create a new question
                    question = Question.objects.create(
                        quiz=quiz,
                        text=question_text,
                        created=datetime.now()
                    )

                    # Get answers for this question
                    answers_texts = request.POST.getlist(f"answers[{i}][]")
                    
                    # Ensure there's a correct answer for this question
                    if i < len(correct_answers) and correct_answers[i]:
                        correct_answer_index = int(correct_answers[i])
                    else:
                        correct_answer_index = 0  # Default to the first answer if no correct answer is selected

                    for j, answer_text in enumerate(answers_texts):
                        if answer_text.strip():
                            # Create an answer
                            Answer.objects.create(
                                question=question,
                                text=answer_text,
                                correct=(j == correct_answer_index),
                                created=datetime.now()
                            )

            messages.success(request, "Quiz updated successfully!")
            return redirect('professor')  # Redirect to quiz list
    else:
        form = QuizForm(instance=quiz, professor=request.user.professor)

    return render(request, 'quizes/edit_quiz.html', {'form': form, 'quiz': quiz})
