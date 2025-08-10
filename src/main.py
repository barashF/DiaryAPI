import uvicorn
from application.app import create_app


app = create_app()

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        reload=True
    )