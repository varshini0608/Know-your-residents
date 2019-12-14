
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import (
    ForeignKey,
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    Boolean,
    String,
    Sequence
)

from .meta import Base


class pwdgen(Base):
    __tablename__ = 'user_auth'
    flat_id = Column(Text, primary_key=True)
    pwd=Column(Text)
    email_id=Column(Text)
    #con1 = relationship("complaint", back_populates="user")

class Houseowner(Base):
    __tablename__= 'houseowners'
    houseownerid=Column(Integer,Sequence('housown_id_seq'),primary_key=True)
    houseownername=Column(String(55),nullable=False)
    fathername=Column(String(55))
    permanentaddress=Column(String(155))
    contactmobileno=Column(String(255))
    landline_no=Column(String(20))
    emailid=Column(String(50))
    username=Column(String(30))
    password=Column(String(15), nullable=False)
    emergencycontactname=Column(String(55))
    emergencymobileno=Column(String(255))
    emergencyaddress=Column(String(100))
    corpus=Column(String(55))
    corpuscheck=Column(Boolean)
    verified=Column(Boolean)
    #vehicleid=(Integer,Foriegnkey('vehicle.vehicleid'))
    #tenant = relationship("Tenant", order_by="Tenant.tenantid", backref="houseowner")


class complaint(Base):
    __tablename__ = 'complaint_status'
    issue_id = Column(Integer, primary_key=True)
    time_created = Column(DateTime, server_default=func.now())
    allocate_by = Column(Text)
    title = Column(Text)
    issue = Column(Text)
    flat_id = Column(Integer, ForeignKey('houseowners.houseownerid'))
    dept_id=Column(Integer,ForeignKey('dept_master.dept_id'))
    complaint_status=Column(Text)
    time_viewed= Column(DateTime)
    time_alloc= Column(DateTime)
    #time_completed = Column(DateTime(timezone=True), onupdate=func.now())
    time_completed = Column(DateTime)
    reply=Column(Text)
    #user = relationship("pwdgen", back_populates="con1")

class authgen(Base):
    __tablename__ = 'auth_master'
    auth_id = Column(Text, primary_key=True)
    pwd=Column(Text)
    user_role=Column(Integer)

class deptgen(Base):
    __tablename__ = 'dept_master'
    dept_id = Column(Integer, primary_key=True)
    dept_name=Column(Text)
    visible = Column(Boolean)
