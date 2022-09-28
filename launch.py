import json

import uvicorn

if __name__ == "__main__":
    with open("config.json", "r") as f:
        config = json.load(f)
    uvicorn.run(
        "app:app",
        host=config.get("host", "127.0.0.1"),
        port=config.get("port", 8080),
        reload=config.get("reload", False),
    )
