# Module 11 — Memory Systems

## Project: Persistent Memory Chatbot

A small hands-on project to understand how memory works in LLM-based applications.

## Objective

Build a chatbot that demonstrates:

- Short-term conversation memory
- Buffer-window memory
- Long-term user memory
- Memory retrieval
- Memory injection into an LLM prompt
- Memory management

## Architecture

```text
User
  |
  v
Application
  |
  v
Memory Manager
  |
  +----------------------+
  |                      |
  v                      v
Short-Term Memory    Long-Term Memory
  |                      |
  |                      v
  |                  Memory Store
  |                      |
  +----------+-----------+
             |
             v
      Relevant Memories
             |
             v
        Prompt Builder
             |
             v
            LLM
             |
             v
          Response