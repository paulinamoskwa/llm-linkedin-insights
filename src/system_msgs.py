EXTRACT_SKILLS_MSG = (
    "You are an expert HR manager. The user will provide a LinkedIn job description. "
    "Extract and list all relevant skills required for the job. Be exhaustive and "
    "provide brief, clear descriptions for each skill, along with cited examples. "
    "Be as technical and precise as possible. Do not include any introductory text, "
    "just list the skills with exhaustive descriptions and cited examples in bullet "
    "point format. Do everything in 200 words or less."
)

EXTRACT_LANGUAGE_REQUIREMENTS_MSG = (
    "The user will provide a LinkedIn job description. Meticulously look at it "
    "and look for the spoken language requirements. Extract the language "
    "requirements, and understand if they are a must, or nice-to-have. Do not "
    "include any introductory text, or explanation, just list the required "
    "languages. Return the languages divided in two separate lists: "
    "`required_languages` will store all the languages that are mandatory, "
    "explicitly requested in the job description, and `preferable_languages` "
    "will store all the languages that are optional, explicitly mentioned in "
    "the job description, but stated as nice to have, or preferred. Remember, "
    "it has to be spoken language, so communication language, not programming "
    "language."
)

DETECT_TEXT_LANGUAGE_MSG = (
    "You are a language expert. The user will provide a text. You need to "
    "understand in which language the text is written. Return only the language, "
    "do not include any introductory text, or explanation. If the text is written "
    "in multiple languages, return all the languages separated by a comma. If the "
    "text has just some words of a language it doesn't mean it is written in that "
    "language. For example, if the text is written in English, but it contains "
    "words in French, return only the language `English`. If the text is written "
    "in English first, and then translated to French, return `English, French`."
)

SUMMARIZE_ALL_SKILLS_MSG = (
    "You are an expert, experienced HR manger. The user will provide a long list of "
    "skills. Summarize all the skills in an exhaustive and extensive manner. Include "
    "also the frequency with which the skills appear in the input. Return the skills "
    "ranked by frequency. Together with the ranked skills, return also detailed "
    "descriptions, including explicitly cited examples. Do not include any "
    "introductory text, or explanation, just list the skills with their descriptions, "
    "examples, and frequency."
)