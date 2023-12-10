import sys
import requests
import re
from collections import defaultdict

def url_content(url):
    try:
        response = requests.get(url)
        return response.text
    except requests.RequestException as err:
        print(f"Error fetching {url}: {err}")
        return None

def get_text_from_url_content(url_content):
    text = re.sub(r'<.*?>', '', url_content)  # tags removal
    return re.sub(r'[^\w\s]', '', text)  # removal of punctuation marks and special characters

def count_words(text):
    counts = defaultdict(int)
    words = text.lower().split()
    for word in words:
        counts[word] += 1
    return counts

def get_top_10(word_counts):
    ordered = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    return ordered

def write_results_to_file(words):
    with open('results.txt', 'w') as file:
        for word, count in words:
            file.write(f"{word}: {count}\n")

def extract_top_words(url):
    content = url_content(url)
    if content:
        text = get_text_from_url_content(content)
        word_counts = count_words(text)
        top_words = get_top_10(word_counts)
        write_results_to_file(top_words)
        return top_words
    return None

# # Unit tests
def test_extract_text_from_html():
    html_content = "<html><body><div>one word after another word</div></body></html>"
    expected_text = "one word after another word"
    assert get_text_from_url_content(html_content) == expected_text

def test_count_words():
    text = "words and yet another words to be counted"
    expected_word_counts = {'words': 2, 'and': 1, 'yet': 1, 'another': 1, 'to': 1, 'be': 1, 'counted': 1}
    assert count_words(text) == expected_word_counts

test_extract_text_from_html()
test_count_words()

if __name__ == '__main__':
    n = len(sys.argv)
    if n == 2:
        source = sys.argv[1]
        top_words = extract_top_words(source)
        if top_words:
            print("Top 10 words and number of occurrences:")
            for word, count in top_words:
                print(f"{word}: {count}")
    else:
        print("Please provide exactly one argument as the source to extract the text from. Example: https://onet.pl")