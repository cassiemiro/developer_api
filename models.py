from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

engine = create_engine("sqlite:///activities.db")
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    name = Column(String(40), index=True)
    age = Column(Integer)

    def __repr__(self) -> str:
        return f"<People {self.name}>"

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def as_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "age": self.age}


class Activities(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    person_id = Column(Integer, ForeignKey("person.id"))
    person = relationship("Person")

    def __repr__(self) -> str:
        return f"<Activities {self.name}>"

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def as_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "person": self.person.name}


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
