from apps.models import BaseModel, db
from datetime import datetime
import pytz


class Blog(BaseModel):
    __tablename__ = 'blog'

    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    date = db.Column(db.Date(), nullable=False, default=datetime.now(tz=pytz.timezone('Asia/Shanghai')))
    author = db.Column(db.String(255), nullable=False)
    intro = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return self.title


class Featured(BaseModel):
    featured = db.Column('featured', db.Integer(), db.ForeignKey('blog.id'))
    blog = db.relationship('Blog', backref=db.backref('featured', lazy='dynamic'))

    def __str__(self):
        return 'featured ID: ' + str(self.featured)
