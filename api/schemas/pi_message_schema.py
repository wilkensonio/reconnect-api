
from pydantic import Field, BaseModel


class PiMessage(BaseModel):
    """Base model for creating a availability (faculty)"""

    user_id: str = Field(...,
                         description="The faculty id", unique=True)

    duration: int = Field(...,
                          description="Length the message should be displayed (e.g. 30)")

    duration_unit: str = Field(...,
                               description=" Seconds, Minutes, etc. (e.g. seconds)")

    message: str = Field(...,
                         description="The message to be display")
