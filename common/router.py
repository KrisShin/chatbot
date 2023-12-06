from apps.apis import router


def register_router(app):
    """
    register router to app
    """

    app.include_router(
        router,
        tags=['chat'],
        responses={404: {'description': 'Not Found'}},
        prefix="/api",
    )
