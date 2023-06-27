class Config:

    MODEL = "gpt-3.5-turbo"

    MAX_TOKENS = 500

    TEMPLATE_PREFIX_TO_OPENAI_SLIDE_EXPLANATION = "This is a slide from a presentation about {}, " \
                                                  "the text of the slide is: '{}'. please explain me the slide"
    # in debug dont use the openai api
    DEBUG_MODE = False

    # time out to get compilation from open ai
    TIMEOUT = 2