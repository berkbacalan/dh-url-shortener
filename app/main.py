from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse, JSONResponse

from datetime import datetime
from sqlalchemy.orm import Session

from app.helper import generate_short_url

from . import models
from .schema import URLBase, URLListResponse, CreateURLResponse, CustomUrl
from .database import SessionLocal, engine
from .config import BASE_URL, PROTOCOL


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


@app.post("/url", response_model=CreateURLResponse)
def create_url(url: URLBase, db: Session = Depends(get_db)):

    url_exists = db.query(models.URL).filter(models.URL.original_url == url.original_url).first()

    if bool(url_exists):
        res = CreateURLResponse(url=BASE_URL+url_exists.short_url)
    else:
        while True:
            short_url = generate_short_url()
            short_url_exist = bool(db.query(models.URL)
            .filter(models.URL.short_url == short_url)
            .first())
            if not short_url_exist:
                break
        db_url = models.URL(
            original_url=url.original_url, short_url=short_url
        )
        db.add(db_url)
        db.commit()
        db.refresh(db_url)

        res = CreateURLResponse(url=BASE_URL+db_url.short_url)

    return res


@app.post("/custom-url", response_model=CreateURLResponse)
def create_url(url: CustomUrl, db: Session = Depends(get_db)):
    short_url_exists = db.query(models.URL).filter(models.URL.short_url == url.short_url).first()
    if bool(short_url_exists):
        return JSONResponse(status_code=400, content="Short url you desired already in use.")

    db_url = models.URL(
        original_url=url.original_url, short_url=url.short_url
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    res = CreateURLResponse(url=BASE_URL+db_url.short_url)

    return res


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
        .filter(models.URL.short_url == url_key and models.URL.expiry_date <= datetime.utcnow())
        .first()
    )
    if bool(db_url):
        db_url.clicks = db_url.clicks + 1
        db.commit()
        return RedirectResponse(url=PROTOCOL+db_url.original_url)
    else:
        return JSONResponse(status_code=404, content="No url with this key.")
