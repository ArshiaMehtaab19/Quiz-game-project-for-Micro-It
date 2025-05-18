def predict_difficulty(score, total_questions_asked):
    """
    Predicts next question difficulty based on current score.

    Args:
        score (int): Number of correct answers so far.
        total_questions_asked (int): Number of questions answered so far.

    Returns:
        str: Difficulty level - 'easy', 'medium', or 'hard'
    """
    if total_questions_asked == 0:
        return 'easy'

    accuracy = score / total_questions_asked

    if accuracy > 0.8:
        return 'hard'
    elif accuracy > 0.5:
        return 'medium'
    else:
        return 'easy'
