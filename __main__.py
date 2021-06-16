"""
Файл который использует пайчарм чтобы запускать сервак
"""
import uvicorn


uvicorn.run(
    'fast_api_tutorial.20UpdatesPUT:app',
    # host=settings.server_host,
    # port=settings.server_port,
    reload=True,
)
