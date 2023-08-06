## Travitia Talk

Async ChatBot API wrapper for https://public-api.travitia.xyz/talk

### Installation

Travitia Talk is available on PyPi
```shell
pip install travitia_talk
```

### Getting API key

- Join Travitia API Discord at https://discord.gg/C98nsXt
- TODO

### Usage

#### Interactive session

```shell
python -m travitia_talk
```

#### Basic usage

```python
import travitia_talk as tt

API_KEY = "SECRET_KEY"

chatbot = tt.ChatBot(API_KEY)
response = await chatbot.ask("How are you?")
print(response)
# I'm doing okay, you?

await chatbot.close()
```

#### Emotions

Travitia Talk supports multiple emotions

```python
import random

emotion = random.choice(list(tt.Emotion))
response = await chatbot.ask("How are you?", emotion=emotion)
```

#### Contexts

It is possible to add context to query for more accurate answers (up to 2 answers currently).
By default library uses in-memory context, but it is possible to define your own by using `travitia_talk.Context`.

Context looks up previous queries using an identifier. In case of discord bot this could be user id.
Example:

```python
@bot.command
async def cb(self, ctx, *, text: str):
    response = await ctx.bot.chatbot.ask(text, id=ctx.author.id)

    await ctx.send(response.text)
```

#### Custom session

It is possible to use custom aiohttp session with configured timeouts and other settings.

```python
from aiohttp import ClientSession, ClientTimeout
import travitia_talk as tt

API_KEY = "SECRET_KEY"

chatbot = tt.ChatBot(API_KEY, session=ClientSession(timeout=ClientTimeout))
```

#### Custom API URL

In case URL gets changed for some reason or library adds support for other backends it is possible to overwrite API URL:

```python
import travitia_talk as tt

API_KEY = "SECRET_KEY"

chatbot = tt.ChatBot(API_KEY, api_url="https://paid-api.travitia.xyz/talk")
```
