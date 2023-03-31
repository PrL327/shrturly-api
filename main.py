import validators
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from src.objects.url import URL
from src.database.db import __connect_to_db 


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome"}

@app.get("/health")
def read_health():
    return {"message": "I am healthy"}

@app.post("/shorten_url")
def create_shortened_url(url: URL):
    print(validators.url(url.path))
    if validators.url(url.path) is not True:
        raise HTTPException(status_code=422, detail="Malformed URL provided");
    elif validators.url(url.path) is True:
        print(validators.url(url.path))
        query = 'INSERT INTO urls (code,url,uuid,createdAt) VALUES(?,?,?,?)'
        conn = __connect_to_db()
        cur = conn.cursor()
        val = (url.code, url.path, url.uuid, url.createdAt)
        cur.execute(query, val);
        conn.commit()
        cur.close()
        return url

@app.get("/{code}")
def shortened_url(code):
    conn = __connect_to_db()
    query = "SELECT u.url FROM urls u WHERE u.code=?;"
    cur = conn.cursor()
    cur.execute(query,[code])
    records = cur.fetchall()
    for row in records:
        return RedirectResponse(url=row[0], status_code=303)
    cur.close()

@app.get("/records/{uuid}")
def get_record(uuid):
    conn = __connect_to_db()
    query = "SELECT * FROM urls u WHERE u.uuid=?;"
    cur = conn.cursor()
    cur.execute(query,[uuid])
    records = cur.fetchall()
    if len(records) == 0:
        raise HTTPException(status_code=404, detail="Record not found");
    else:
        for row in records:
            return row
    cur.close()

@app.delete("/records/{uuid}")
def delete_record(uuid):
    conn = __connect_to_db()
    query = "SELECT * FROM urls u WHERE u.uuid=?;"
    cur = conn.cursor()
    cur.execute(query,[uuid])
    records = cur.fetchall()
    if len(records) == 0:
        raise HTTPException(status_code=404, detail="Record not found");
    else:
        for row in records:
            query = "DELETE FROM urls WHERE uuid=?;"
            cur = conn.cursor()
            cur.execute(query,[uuid])
            conn.commit()
            cur.close()
            return 'success'