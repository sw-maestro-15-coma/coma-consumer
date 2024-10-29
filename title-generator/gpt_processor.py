from openai import OpenAI
from openai.types.chat import ChatCompletion

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
    query = ("Find the funniest point in the subscription."
             "Result Format is HH:MM:SS ~ HH:MM:SS."
             "Don't mention any other sentence. Just show me HH:MM:SS ~ HH:MM:SS."
             "And minimum interval is 30 seconds, and Maximum interval is 1 Minutes."
             "The following shows the whole subscription:"
             f"{subscription}")

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

    print(answer)

    return EditPoint(start=0, end=1)

def test_start():
    subscription = ""
    with open('test_subscription.txt', 'r') as file:
        for line in file.readlines():
            subscription += line

    answer = create_shorts_title_gpt(subscription)
    print(answer)