from fastapi import Header, Query

from insnail_ai_tools.web import create_fast_api_app
from insnail_ai_tools.web.sso_decorator import register_middleware

app = create_fast_api_app()


register_middleware(app)


@app.get("/")
# @fast_api_sso
def index(authorization: str = Header(None), a: str = Query(...)):
    print(index.__annotations__)
    return {"a": a}


# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=8008)
