from dotenv import load_dotenv
import os
import asyncio
from config import Config
import openai
import platform


if platform.system() == 'Windows':
    # Set the event loop policy to ensure compatibility with Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_TOKEN")
openai.api_key = OPENAI_KEY


def genarate_prompt_to_slide(slide_text, topic):
    """
      Generate a prompt to openai to ask gpt to explain the slide text

      Args:
          slide_text(str):  the text to explain

      Returns:
           str:the prompt to gpt
      """
    return Config.TEMPLATE_PREFIX_TO_OPENAI_SLIDE_EXPLANATION.format(topic, slide_text)


async def async_get_explanation_to_presentation(list_of_slides, topic):
    """
      Asynchronously generates explanations for each slide in a presentation.

      Args:
          list_of_slides (list): A list of slide texts.
          topic (str): The topic of the presentation.

      Returns:
          list: A list of explanations for each slide.

      """
    tasks_slide_explains = [get_explanation_to_slide(slide_text, topic) for slide_text in list_of_slides]
    explanations_list = await asyncio.gather(*tasks_slide_explains)
    return explanations_list


async def async_ask_openai(prompt):
    """
       Asynchronously sends a prompt to the OpenAI Chat API and returns the generated completion.

       Args:
           prompt (str): The prompt to send to the OpenAI Chat API.

       Returns:
           str: The generated completion from the OpenAI Chat API.

       """

    if Config.DEBUG_MODE:
        return 'debug mode'

    try:
        completion = await openai.ChatCompletion.acreate(max_tokens=Config.MAX_TOKENS, model=Config.MODEL,
                                                         messages=[{"role": "user", "content": prompt}], timeout=Config.TIMEOUT)
    except openai.error.RateLimitError as e:
        return f'api key get to the limit msg:{e}'

    except openai.error.Timeout as e:
        return f'openai time out :{e}'

    except openai.error.AuthenticationError as e:
        return f'invalid openAI token: {e}'

    return completion.choices[0].message.content


async def get_explanation_to_slide(slide_text, topic):
    """
     Asynchronously generates an explanation for a slide using the provided slide text and topic.

     Args:
         slide_text (str): The text content of the slide.
         topic (str): The topic of the presentation.

     Returns:
         str: The generated explanation for the slide.

     """
    if not slide_text:
        return ""

    prompt = genarate_prompt_to_slide(slide_text, topic)
    slide_explanation = await async_ask_openai(prompt)

    return slide_explanation
