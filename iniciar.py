import uvicorn
import webbrowser
from threading import Timer

def abrir_navegador():
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    Timer(1, abrir_navegador).start()

    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )