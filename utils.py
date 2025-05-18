import pandas as pd

def load_questions(filepath="data/questions.csv"):
    """
    Load quiz questions from a CSV file.

    Returns:
        A list of dictionaries, each containing question data.
    """
    try:
        df = pd.read_csv(filepath)
        questions = df.to_dict(orient='records')  # Convert DataFrame to list of dicts
        return questions
    except FileNotFoundError:
        print("Question file not found.")
        return []
    except Exception as e:
        print(f"Error loading questions: {e}")
        return []
