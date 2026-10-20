# Avatar Chatbot

Real-time voice chatbot with a talking AI avatar (lip-sync, head movement, facial expression). MVP stage.

## Progress tracker

https://claude.ai/artifact/5BKRkfAsSb9eProdsJAYcC

Full plan: [plan.md](plan.md)

## Stack

| Stage | Choice |
|---|---|
| Framework | LiveKit Agents + LiveKit Cloud |
| VAD | Silero |
| STT | NVIDIA Nemotron Speech Streaming 0.6B (self-hosted, GPU) |
| End of turn | LiveKit turn detector (open weights, CPU) |
| LLM | Llama via Groq API, free tier (fallback: OpenAI GPT if limits are hit) |
| TTS | ElevenLabs Flash |
| Avatar | SoulX-FlashHead Lite (fallback: Anam or Simli) |

## Project layout

```
main.py                   one entry point, picks which process to run
worker/config.py          every setting; secrets come from .env
worker/handler.py         wires the stages into one agent session
worker/livekit/           shared LiveKit helpers (tokens, token server)
worker/stages/listening/  Silero VAD, Nemotron STT (server + connector), turn detector
worker/stages/reasoning/  Groq/OpenAI LLM, system prompt, RAG hook
worker/stages/speaking/   ElevenLabs TTS
worker/stages/avatar/     FlashHead (server + connector)
evaluation/               latency and lip-sync tests
web/                      browser page
assets/                   avatar face photo (not committed)
```

Each stage is self-contained. Other code calls a stage only through its `handler.py`.

## Running

Copy `.env.example` to `.env` and fill in the keys, then start each process in its own terminal:

```
python main.py speech
python main.py avatar
python main.py token
python main.py agent
```

## MVP targets

- Reply starts within ~1.2 s
- Avatar stops within ~300 ms when the user interrupts
- No visible lip drift
