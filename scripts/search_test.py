import os

from perplexity import Perplexity
from dotenv import load_dotenv

load_dotenv()

perplexity = Perplexity(api_key=os.getenv("PERPLEXITY_API_KEY"))

search = perplexity.chat.completions.create(
    messages=[
        {
            "role": "user", 
            "content": "Show me image and a url for 'The pleasure of finding things out'. Response format is {'image': image, 'url': url}"
        }
    ],
    return_images=True,
    model="sonar",
)

print(search.choices[0].message.content)
