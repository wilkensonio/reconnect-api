import os
import logging
import pandas as pd
from api.crud import crud_user
from .. import database
from ..schemas import response_schema, user_schema
from api.utils import jwt_utils
from api.utils.mail_utils import EmailVerification
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from dotenv import load_dotenv


load_dotenv()

EXPRIRES_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


router = APIRouter()

verifier = EmailVerification()
user_crud = crud_user.UserCrud()


@router.post("/verify-email/", response_model=dict)
def send_email_verification(email: user_schema.EmailVerification) -> dict:
    """Verify email address using verification code (sent to the user) 6 characters long

    Args:

        Email (str): email address

    Returns:

        dict: {"verification_code" : str}
    """

    email = email.email

    if not email.endswith("@southernct.edu"):
        raise HTTPException(
            status_code=400,
            detail="Invalid southern email address"
        )

    code = verifier.verification(email)

    if code['verification_code']:
        return code

    logging.error("Error sending verification code", exc_info=True)

    raise HTTPException(
        status_code=400,
        detail="An error occurred while attempting to send email verification code"
    )


@router.post("/verify-email-code/")
def verify_email_code(verify: user_schema.EmailVerificationCode):
    """Verify email address using verification code sent to the user

    Args:

        user_code (str): code entered by the user

        secret_code (str): Verification code

    Returns:

        dict: {"detail" : bool}
    """

    user_code, secret_code = verify.user_code, verify.secret_code
    return verifier.verify_email_code(user_code, secret_code)


@router.post("/signup/", response_model=response_schema.UserResponse)
async def create_user(user: user_schema.UserCreate, db: Session = Depends(database.get_db)):
    """Create a new user

    args:

        user : user_schema.UserCreate
            User detail


    Raises:

        HTTPException
            code : 400
            Email already registered
            An error occurred while attempting to signup

        HTTPException
            code : 400
            Invalid southern email address


    Returns:

        user_schema.UserResponse
            User detail

    """
    if not user.email.endswith("@southernct.edu"):
        raise HTTPException(
            status_code=400,
            detail="Invalid southern email address"
        )

    new_user = user_crud.create_user(db=db, user=user)

    return response_schema.UserResponse(
        id=new_user.id,
        user_id=new_user.user_id,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        phone_number=new_user.phone_number,
        created_at=new_user.created_at
    )


@router.post("/signin/", response_model=response_schema.SigninResponse)
async def login_user(
    login_request: user_schema.LoginRequest,
    db: Session = Depends(database.get_db),
):
    """Login a user by email and password

    Attributes
    ----------
        login_request : user_schema.LoginRequest
            User login detail
        db : Session
            Database session

    Raises
    ------
        HTTPException
            code : 400
            User not found
            Invalid email or password

    Returns
    -------
        user_schema.TokenResponse
            User detail with access token 
    """

    if not login_request.email.endswith("@southernct.edu"):
        raise HTTPException(
            status_code=400,
            detail="Invalid southern email address"
        )

    user = user_crud.get_user_by_email(db, email=login_request.email)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    if not user.check_password(login_request.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )

    response = response_schema.SigninResponse(
        id=user.id,
        user_id=user.user_id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
    )

    return response


@router.post("/signup-student/", response_model=response_schema.CreateStudentResponse)
async def create_student_user(
    student: user_schema.StudentCreate,
    db: Session = Depends(database.get_db),
    token: str = Depends(jwt_utils.oauth2_scheme),
):
    """Create a new student user

    Args:

        user : user_schema.StudentCreate
            Student detail

    Raises:

        HTTPException
            Email already registered
            An error occurred while attempting to signup

    Returns:

        user_schema.UserResponse
            Student detail"""

    jwt_utils.verify_token(token)

    if not student.email.endswith("@southernct.edu"):
        raise HTTPException(
            status_code=400,
            detail="Invalid southern email address"
        )

    student = user_crud.create_student(db=db, student=student)

    return response_schema.CreateStudentResponse(
        id=student.id,
        student_id=student.student_id,
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        phone_number=student.phone_number,
    )


@router.post("/students/upload")
async def upload_students_csv(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    token: str = Depends(jwt_utils.oauth2_scheme),
):
    """Upload a CSV file containing student details

        Must contain the following columns in the CSV file:
            Email, ID, Pref. First, Last Name 

    Args:

        file : UploadFile
            CSV file containing student details

    raises:

            HTTPException
                code : 400
                Invalid file type. Please upload a CSV file.

    returns:

        dict: {"status" : str, "added_students" : added_students }"""

    jwt_utils.verify_token(token)

    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload a CSV file.")

    try:
        df = pd.read_csv(file.file)

        # Map CSV headers to match DB fields
        df = df.rename(columns={
            'Email': 'email',
            'ID': 'student_id',
            'Pref. First': 'first_name',
            'Last Name': 'last_name',
        })
        df['phone_number'] = '0000000000'

        # Filter out unnecessary columns
        required_columns = ['email', 'student_id',
                            'first_name', 'last_name', 'phone_number']
        df = df[required_columns]

        # Convert the DataFrame to a list of dictionaries for validation
        students_data = df.to_dict(orient="records")

        # Validate and create student objects
        students = [user_schema.StudentCreate(
            **student) for student in students_data]
        added_students = user_crud.add_student_csv(db=db, students=students)

        return {"status": "success", "added_students": added_students}

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing the file: {e}")


@router.post("/blacklist/{user_id}", response_model=dict)
def blacklist_user_by_id(
    user_id: str,
    db: Session = Depends(database.get_db),
    token: str = Depends(jwt_utils.oauth2_scheme),
):
    """Blacklist a user by id

    Args:

        user_id : str
            Student id (hootloot) or email

        token : str
            User token

    Returns:

        dict: {"detail" : str}
    """
    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="User ID cannot be empty"
        )

    jwt_utils.verify_token(token)

    if user_crud.blacklist_user(db, student_id=user_id):
        return {"detail": f"User {user_id} blacklisted"}

    return {"detail": f"User {user_id} not found or already blacklisted"}


@router.get("/blacklist/", response_model=List[response_schema.BlacklistResponse])
def blacklist_user(
        db: Session = Depends(database.get_db),
        token: str = Depends(jwt_utils.oauth2_scheme)):
    """Blacklist a user

    Args:

        token : str
            User token

    Returns:

        dict: {"detail" : str}
    """

    jwt_utils.verify_token(token)
    blacklisted = []
    try:
        blacklisted = user_crud.get_blacklisted_students(db)
        if not blacklisted:
            return []
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=400,
            detail="An error occurred while attempting to blacklist user"
        )

    return [response_schema.BlacklistResponse(student_id=student.user_id) for student in blacklisted]


@router.post("/kiosk-signin/", response_model=response_schema.KioskSigninResponse)
async def kiosk_login(
    login_request: user_schema.KioskLoginRequest,
    db: Session = Depends(database.get_db),
):
    """Login a user via kiosk (using last 4 digits of ID or full barcode)
    args:

        user_id (str) : student full ID or last 4 digits of ID (hootloot)

    Raises:

            HTTPException
                code : 400
                No User exists with the provided ID


    Returns: 

        user_schema.TokenResponse
    """

    user = user_crud.get_student_by_id(db, login_request.user_id)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="No User exists with the provided ID"
        )

    create_token = jwt_utils.create_access_token(
        data={"sub": login_request.user_id},
        expires_delta=jwt_utils.timedelta(minutes=int(EXPRIRES_MINUTES))
    )

    return response_schema.KioskSigninResponse(
        id=user.id,
        student_id=user.student_id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        access_token=create_token
    )


@router.get("/users/", response_model=List[response_schema.UserResponse])
async def get_users(token: str = Depends(jwt_utils.oauth2_scheme),
                    db: Session = Depends(database.get_db)):
    """Retrieve all users. 

    Raises
    ------
        HTTPException
            code : 400
            An error occurred while attempting to retrieve users

    Returns
    -------
        List[user_schema.UserResponse]
            List of all users"""

    jwt_utils.verify_token(token)

    try:
        users = user_crud.get_users(db)
        return users
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=400,
            detail="An error occurred while attempting to retrieve users"
        )


@router.get("/user/email/{email}", response_model=response_schema.UserResponse)
async def get_user_by_email(email: str, db: Session = Depends(database.get_db),
                            token: str = Depends(jwt_utils.oauth2_scheme)):
    """Retrieve a user by email.

    Attributes
    ---------- 
        email : str
            User email


    Raises
    ------
        HTTPException
            code : 400
            User not found

    Returns
    -------
        user_schema.UserResponse
            User detail"""

    jwt_utils.verify_token(token)

    try:
        user = user_crud.get_user_by_email(db, email)
        return user
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )


@router.get("/user/id/{user_id}", response_model=response_schema.UserResponse)
def get_user_by_id(user_id: str, db: Session = Depends(database.get_db), token: str = Depends(jwt_utils.oauth2_scheme)):
    """Retrieve a user by id.

    Attributes
    ---------- 
        user_id : str
            User id


    Raises
    ------
        HTTPException
            code : 404
            User not found

    Returns
    -------
        user_schema.UserResponse
            User detail"""

    jwt_utils.verify_token(token)
    user = user_crud.get_user_by_id(db, user_id)
    return user


@router.get("/students/", response_model=List[response_schema.Get_StudentResponse])
def get_students(db: Session = Depends(database.get_db),
                 token: str = Depends(jwt_utils.oauth2_scheme)):
    """Get all students 


    Returns:

        List[Student]: List of all students
    """
    jwt_utils.verify_token(token)

    student = user_crud.get_students(db)
    if not student:
        raise HTTPException(
            status_code=404,
            detail="No student found"
        )
    return student


@router.put("/reset-password/", response_model=dict)
def reset_password(data: user_schema.ResetPassword, db:  Session = Depends(database.get_db)):
    """Reset user password

    Args:

        email : str
            User email

    Returns:

        dict: {"detail" : str"""

    email, password = data.email, data.password

    if not email.lower().endswith("@southernct.edu"):
        raise HTTPException(
            status_code=400,
            detail="Invalid southern email address"
        )
    if not password:
        raise HTTPException(
            status_code=400,
            detail="Password cannot be empty"
        )
    res = user_crud.reset_password(db, email, password)
    return {
        "detail": res
    }


@router.delete("/user/delete/{email_or_id}", response_model=dict)
def delete_by_email_or_id(email_or_id: str, db: Session = Depends(database.get_db),
                          token: str = Depends(jwt_utils.oauth2_scheme)):
    """Delete a user by id or by email

    Attributes
    ----------
        email_or_id : str
            User email or user_id 

    Raises
    ------
        HTTPException
            code : 400
            User not found
            An error occurred while attempting to delete user

    Returns
    -------
        dict: {"detail" : str}

        """

    jwt_utils.verify_token(token)

    try:
        if user_crud.delete_user(db, email=email_or_id):
            return {"detail": "User deleted successfully"}
        elif user_crud.delete_user(db, user_id=email_or_id):
            return {"detail": "User deleted successfully"}
        else:
            raise HTTPException(
                status_code=400,
                detail="User not found"
            )
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=400,
            detail="An error occurred while attempting to delete user"
        )
