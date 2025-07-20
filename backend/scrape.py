import requests
from bs4 import BeautifulSoup

def scrape_stripe_docs(url="https://stripe.com/docs/api"):
    """
    scrape the Stripe API documentation for endpoints & their descriptions
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # grabbing the paragraph content
    chunks = []
    for tag in soup.find_all(["p", "li", "code"]):
        text = tag.get_text(strip=True)
        if len(text) > 50:
            chunks.append(text)

    return chunks

if __name__ == "__main__":
    data = scrape_stripe_docs()
    print(data[:5])
