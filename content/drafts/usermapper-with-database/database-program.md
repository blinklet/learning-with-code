In this post, I will describe a Python program that creates a single, simple table in a database and how I added, retrieved, and deleted data from that table. The program must, neccessarily, include functions that interact with the database and with the user.

But, before I create a project structure and write all the Python modules that contain those functions,

(use unicodetext for user data so you can store xml doc)

```python
from sqlalchemy import String, UnicodeText, DateTime
from sqlalchemy.orm import mapped_column

python
class Userdata(Base):
    __tablename__ = "userdata"
    user_id = mapped_column(String(32), primary_key=True, nullable=False)
    user_data = mapped_column(UnicodeText)
    time_stamp = mapped_column(DateTime(timezone=True))
```