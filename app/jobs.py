from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response, File, UploadFile, Form
from .database import get_db
from tempfile import NamedTemporaryFile
import os
import sys
import shutil
from pathlib import Path
import uuid
import re
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


router = APIRouter()

limit_upload_type = ["image/jpeg", "image/png"]


@router.get('/')
def get_jobs(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    notes = db.query(models.Jobs).filter().limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(notes), 'notes': notes}


@router.post("/upload/", summary="上传图片")
def upload_image(
    image: UploadFile = File(...),
    image_prompt: str = Form(),
    db: Session = Depends(get_db)
):
    global limit_upload_type
    print(image.filename)
    print(image_prompt)

    if not image or image.content_type not in limit_upload_type:
        return {"code": 9000, "message": "未上传合法图片。仅限jpeg、png格式，10MB以内"}

    tmp_prompt_format = re.match(
        r'^[a-zA-Z0-9 ]{0,50}$', image_prompt, re.M | re.I)
    print(tmp_prompt_format)
    if not image_prompt or len(image_prompt) > 50 or not tmp_prompt_format:
        return {"code": 9001, "message": "image prompt不合法。仅限英文、数字、空格，50个字符以内"}

    save_dir = f"/Users/caritasem/Downloads/tmp"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    try:
        suffix = Path(image.filename).suffix
        # print(Path(file.filename))
        iname_ary = image.filename.split(".")
        uid1 = uuid.uuid1()
        new_img_name = str(uid1)
        destination = Path(
            save_dir + "/" + new_img_name + "." + iname_ary[1])
        with destination.open("wb") as buffer:
            # print(destination)
            # with NamedTemporaryFile(delete=False, suffix=suffix, dir=save_dir) as tmp:
            shutil.copyfileobj(image.file, buffer)
            tmp_file_name = Path(buffer.name).name
    finally:
        image.file.close()

    new_job = models.Jobs()
    new_job.id = str(uid1)
    new_job.img_name = new_img_name
    new_job.img_path = str(destination)
    new_job.img_prompt = image_prompt
    new_job.step = 0
    new_job.createdAt = datetime.now()
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {"code": 200, "status": "success", "tmp_file_name": tmp_file_name}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_note(payload: schemas.NoteBaseSchema, db: Session = Depends(get_db)):
    new_note = models.Note(**payload.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {"status": "success", "note": new_note}


@router.patch('/{noteId}')
def update_note(noteId: str, payload: schemas.NoteBaseSchema, db: Session = Depends(get_db)):
    note_query = db.query(models.Note).filter(models.Note.id == noteId)
    db_note = note_query.first()

    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {noteId} found')
    update_data = payload.dict(exclude_unset=True)
    note_query.filter(models.Note.id == noteId).update(update_data,
                                                       synchronize_session=False)
    db.commit()
    db.refresh(db_note)
    return {"status": "success", "note": db_note}


@router.get('/{noteId}')
def get_post(noteId: str, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == noteId).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No note with this id: {id} found")
    return {"status": "success", "note": note}


@router.delete('/{noteId}')
def delete_post(noteId: str, db: Session = Depends(get_db)):
    note_query = db.query(models.Note).filter(models.Note.id == noteId)
    note = note_query.first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {id} found')
    note_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
