import sys
import uvicorn

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py [dev|start]")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == "dev":
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    elif mode == "start":
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
    else:
        print("Unknown mode. Use 'dev' or 'start'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
