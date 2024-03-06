import pathlib
import textwrap
import sys
import google.generativeai as genai

# from IPython.display import display
# from IPython.display import Markdown
#
#
# def to_markdown(text):
#   text = text.replace('•', '  *')
#   return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
genai.configure(api_key=sys.argv[1])
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("".join(["respond very briefly: ", sys.argv[2]]))
# return response.text