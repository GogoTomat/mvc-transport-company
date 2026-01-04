from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, transport, routes, trips, cargo, users, utils

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Transport Company Management System",
    description="API для управления транспортной компанией",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(transport.router)
app.include_router(routes.router)
app.include_router(trips.router)
app.include_router(cargo.router)
app.include_router(users.router)
app.include_router(utils.router)

@app.get("/")
def root():
    return {
        "message": "Добро пожаловать в систему управления транспортной компанией",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
