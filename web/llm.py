import requests
import json
import logging as log
log.basicConfig(level=log.INFO, 
                format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                datefmt='%Y-%m-%dT%H:%M:%S')

def stream_llm_response(completions_url: str, model: str, prompt: str):
    try:
        with requests.post(
            completions_url,
            json={
                "model": model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": True
            },
            stream=True,
        ) as response:

            if response.status_code != 200:
                yield f"[ERROR] {response.status_code}: {response.text}"
                return

            for line in response.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data: "):
                    continue

                data_str = line[len("data: "):]
                if data_str.strip() == "[DONE]":
                    break

                try:
                    chunk = json.loads(data_str)
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    if delta:
                        yield delta
                except Exception as e:
                    log.warning(f"Failed to parse chunk: {e}")
                    continue

    except Exception as e:
        yield f"[EXCEPTION] {e}"