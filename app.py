from flask import Flask, request
from newspaper import Article
from googletrans import Translator
import asyncio

app = Flask(__name__)

@app.route('/')
def hello():
    return "ok"

@app.route('/news', methods=['POST'])
def news():
    url = request.form["url"]
    lang = request.form["lang"]

    article = Article(url)
    article.download()
    article.parse()

    keywords = article.meta_keywords
    text = ""

    async def translate_article():
        async with Translator() as translator:
            if lang == "en":
                return article.text
            else:
                result = await translator.translate(article.text, dest=lang)
                return result.text

    text = asyncio.run(translate_article())

    return {
        "text": text,
        "keywords": keywords,
        "title": article.title,
        "img_url": article.top_image
    }

if __name__ == '__main__':
    app.run()
