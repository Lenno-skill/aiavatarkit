OPENAI_API_KEY = "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"

import asyncio
from aiavatar import AIAvatar

aiavatar_app = AIAvatar(
    openai_api_key=OPENAI_API_KEY,
    debug=True
)
asyncio.run(aiavatar_app.start_listening())
