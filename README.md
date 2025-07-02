# ASESeminar-AutogenStudio

### 1. Clone repository into virtual environment

### 2. Install autogen studio

```
pip install -U autogenstudio
```

### 3. Run autogen studio

```
autogenstudio ui --port 8085 --appdir ./ASESeminar-AutogenStudio/AGSdir
```

- `SWE-Bench-Lite API` is expected to run at port `8081`
- `SWE-Bench-Lite Tester` is expected to run at port `8082`

### 4. Visit localhost:8085

- set OpenAI key: Gallery -> Default Component Gallery -> Models -> OpenAI GPT-4o Mini
- try out: Playground -> new Session with AGSTeam2 -> Enter prompt: `Fix problem 1`
