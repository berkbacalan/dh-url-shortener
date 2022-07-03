from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.helper import generate_short_url

from . import models
from .schema import URLInfo, URLBase, URLListResponse
from .database import SessionLocal, engine


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return "Default backend with status 200"


@app.post("/url", response_model=URLInfo)
def create_url(url: URLBase, db: Session = Depends(get_db)):

    short_url = generate_short_url()
    db_url = models.URL(
        original_url=url.original_url, short_url=short_url
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url


@app.get("/list", response_model=URLListResponse)
def get_urls(db: Session = Depends(get_db)):
    urls = db.query(models.URL).all()

    return urls


@app.get("/{url_key}")
def redirect_to_url(
        url_key: str,
        db: Session = Depends(get_db)
    ):
    db_url = (
        db.query(models.URL)
        .filter(models.URL.short_url == url_key)
        .first()
    )
    if db_url:
        db_url.clicks = db_url.clicks + 1
        db.commit()
        return RedirectResponse(db_url.original_url)
    else:
        HTTPException(status_code=404, detail="No url with this key.")
