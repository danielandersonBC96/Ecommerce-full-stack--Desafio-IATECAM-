from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from Routers import  user, analytics, tag, output, storage, sse 
from Config.database import create_tables, get_db

app = FastAPI()

# Middleware CORS para permitir requisições do localhost:4200
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
def on_startup():
    create_tables()
# Rota para verificar a raiz da aplicação
@app.get("/", response_class=HTMLResponse)
def read_root():
    return "<h1>Welcome to FastAPI Application</h1>"

# Rota para favicon
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return ""

# Incluir os roteadores para as funcionalidades específicas
app.include_router(user.router)
app.include_router(analytics.router)
app.include_router(tag.router)
app.include_router(output.router)
app.include_router(storage.router)
app.include_router(sse.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
