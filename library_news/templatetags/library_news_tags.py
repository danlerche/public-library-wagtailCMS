from django import template
from bs4 import BeautifulSoup

register = template.Library()

@register.filter(name="first_sentence")
def first_sentence(html_string):
	# Parse the HTML
	soup = BeautifulSoup(html_string, 'html.parser')
    
    # Get text from the HTML
	html_text = soup.get_text()
    
    # Split the text into sentences
	sentences = html_text.split('.')
   
	# Return the first sentence
	if len(sentences) > 0:
		return sentences[0].strip()
	else:
		return ""