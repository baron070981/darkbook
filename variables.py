
from dataclasses import dataclass
import datetime
from datetime import datetime as dtm


@dataclass
class Datas:
    idd:int = -1
    mdate:object = datetime.date(dtm.now().year,
                                 dtm.now().month,
                                 dtm.now().day,
                            )
    many:float = 0.0










