if not file:
    return {"message": "No upload file sent"}

if not file.filename.endswith('.json'):
    raise HTTPException(status_code=400, detail="Invalid file type. Only JSON files are allowed.")

contents = await file.read()
try:
    json.loads(contents.decode('utf-8'))
except (json.JSONDecodeError, UnicodeDecodeError):
    raise HTTPException(status_code=400, detail="Invalid file encoding. Only UTF-8 encoded JSON files are allowed.")