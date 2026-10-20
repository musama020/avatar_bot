# Avatar Chatbot MVP Plan

## Goal
- A user talks by voice to an AI avatar that answers with natural speech, synced lips, head movement and facial expressions.
- Low latency, and the user can interrupt the avatar at any time.

## Language
- Build in English first, then switch to Polish
- Polish STT: test self-hosted first; fall back to ElevenLabs STT

## Stack
- **Framework:** LiveKit Agents + LiveKit Cloud
- **VAD:** Silero
- **STT:** NVIDIA Nemotron Speech Streaming 0.6B, self-hosted on our GPU
- **End of turn:** LiveKit turn detector (open weights, CPU)
- **LLM:** Llama via Groq (free tier); switch to OpenAI GPT if we hit the limits
- **TTS:** ElevenLabs Flash
- **Avatar:** SoulX-FlashHead Lite on our own GPU; fallback is Anam or Simli
- **Frontend:** web page using the LiveKit browser SDK

## How it works
- User speaks → VAD + Nemotron transcribe it, and the turn detector decides when they've finished → Llama replies (streaming) → ElevenLabs speaks → FlashHead animates the face → audio and video go back to the user together.
- If the user interrupts: stop the LLM, the TTS and the avatar immediately.

## Steps

### 1. Setup
- LiveKit Cloud project and keys
- Groq and ElevenLabs keys
- Rent a GPU (RTX 4090 / L40S); the whole repo runs on it
- Repo skeleton, config, Python environment

### 2. Voice agent (no avatar)
- Self-host Nemotron STT on the GPU and build its LiveKit connector
- Connect VAD → STT → turn detector → LLM → TTS
- Tune end-of-turn detection and interruptions
- Target: voice reply in under 0.8 s

### 3. FlashHead test (in parallel with step 2)
- Measure the time from the first audio to the first video frame (pass: ≤ 300 ms)
- Check lip quality with short audio chunks
- Check the idle face, instant stop and weights licence
- Decide: our own FlashHead service, or the hosted fallback

### 4. Avatar
- **If FlashHead passes:** build the GPU avatar service, send audio and video together, handle stop and idle, and write the LiveKit connector
- **If it fails:** plug in the Anam or Simli LiveKit plugin

### 5. Polish
- Connect RAG to the LLM step (lookup under 100 ms)
- Build the web page
- Test interruptions, background noise and long sessions
- Final check against the targets

## MVP targets
- Reply starts within ~1.2 s
- Avatar stops within ~300 ms when the user interrupts
- No visible lip drift

## Timeline (estimate)
- About 4–5 weeks with FlashHead
- About 3 weeks with the hosted fallback

## Risks and fallbacks
- **FlashHead too slow, or licence not usable:** hosted avatar
- **Self-hosted STT too slow or inaccurate:** Deepgram Flux ($200 free signup credit)
- **STT and FlashHead competing for the GPU:** measure in step 3; add a second GPU if needed
- **Groq free-tier limits:** OpenAI key
- **ElevenLabs too slow:** Cartesia

## Tracking
- Progress tracker: https://claude.ai/artifact/5BKRkfAsSb9eProdsJAYcC
