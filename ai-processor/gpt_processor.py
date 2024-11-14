from openai import OpenAI
from openai.types.chat import ChatCompletion

from utils import hhmmss_to_seconds


__OPENAI_API_KEY = "sk-svcacct-2O4EB8Ztb9YKx764tSr8T3BlbkFJ5dr1henfflQ83g5R5YfJ"


def create_shorts_title_gpt(subscription: str) -> str:
    client = OpenAI(
        api_key=__OPENAI_API_KEY
    )

    model = "gpt-4o-mini"
    query = ("Convert the following subscription into a Youtube Shorts title. "
             "The Shorts title should be in the same language as the original title and should be under 20 characters long. "
             f"Do not include special symbols or emojis. Subscription : {subscription}")

    messages = [{
        "role": "system",
        "content": ("You are an expert in generating catchy and engaging titles specifically for YouTube Shorts. "
                   "Your goal is to create titles that are eye-catching and entertaining.")
    }, {
        "role": "user",
        "content": query
    }]

    try:
        response: ChatCompletion = client.chat.completions.create(model=model,
                                                      messages=messages,
                                                      timeout=10.0)
    except Exception as e:
        raise RuntimeError(e, "chat gpt api에서 오류가 발생했습니다")

    answer = response.choices[0].message.content

    if not answer:
        raise RuntimeError("chat gpt로부터 답을 받지 못했습니다")

    return answer


class EditPoint:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end


def create_shorts_edit_point(subscription: str) -> EditPoint:
    client = OpenAI(
        api_key=__OPENAI_API_KEY
    )

    model = "gpt-4o-mini"
    query = (
        "Analyze the following transcript and identify the funniest continuous interval "
        "that is between 30 seconds and 1 minute long. Evaluate multiple intervals "
        "and choose the one with the highest humor impact. "
        "Provide the result in HH:MM:SS~HH:MM:SS format. "
        f"Transcript: {subscription}"
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert at analyzing transcripts to identify the funniest moments. "
                "Your goal is to select a continuous interval of humor that will be most engaging for viewers."
            ),
        },
        {
            "role": "user",
            "content": query,
        },
    ]

    try:
        response: ChatCompletion = client.chat.completions.create(model=model,
                                                      messages=messages,
                                                      timeout=10.0)
    except Exception as e:
        raise RuntimeError(e, "chat gpt api에서 오류가 발생했습니다")

    answer = response.choices[0].message.content

    answers = answer.split('~')
    start: int = hhmmss_to_seconds(answers[0])
    end: int = hhmmss_to_seconds(answers[1])

    return EditPoint(start=start, end=end)