from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define the Role model
class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    character_name = Column(String)

    # One to many relationship: One role can have many auditions
    auditions = relationship("Audition", back_populates="role")

    # Property: return list of actors
    @property
    def actors(self):
        return [audition.actor for audition in self.auditions]

    # Property: return list of locations
    @property
    def locations(self):
        return [audition.location for audition in self.auditions]

    # Property: get the lead actor (the first hired audition)
    def lead(self):
        for audition in self.auditions:
            if audition.hired:
                return audition.actor
        return "no actor has been hired for this role"

    # Property: get the understudy actor (second hired audition)
    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if len(hired_auditions) > 1:
            return hired_auditions[1].actor
        return "no actor has been hired for understudy for this role"

# Define the Audition model
class Audition(Base):
    __tablename__ = 'auditions'
    id = Column(Integer, primary_key=True)
    actor = Column(String)
    location = Column(String)
    phone = Column(Integer)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    # Relationship: Many auditions belong to one role
    role = relationship("Role", back_populates="auditions")

    # Method: Hire the actor (set hired to True)
    def call_back(self):
        self.hired = True
