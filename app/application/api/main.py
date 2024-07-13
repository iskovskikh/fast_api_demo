from fastapi import FastAPI

from application.api.chat.handlers import router as chat_router


def create_app() -> FastAPI:
    app = FastAPI(
        title='MQ demo',
        docs_url='/api/docs',
        debug=True
    )

    app.include_router(chat_router, prefix='/chat')

    return app
