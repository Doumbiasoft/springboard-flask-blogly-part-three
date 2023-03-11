"""Seed file to make sample data for db."""

from models import db, User, Post,Tag,PostTag
from app import app

# Create all tables
db.drop_all()
db.create_all()

User.query.delete()

# Add sample users
user2 = User(first_name='Denzel', last_name='Washington', image_url='https://m.media-amazon.com/images/I/61eAcaU-gGL._AC_SL1000_.jpg')
user3 = User(first_name='Kylian', last_name='Mbappé', image_url='https://www.sportsunfold.com/wp-content/uploads/2022/08/284095.jpg')
user1 = User(first_name='Mouhamed', last_name='Doumbia', image_url='')


db.session.add_all([user1, user2, user3])
db.session.commit()

post1=Post(title=f"""How to Install SQL Server Management Studio on a Mac""",content=f"""SQL Server Management Studio (SSMS) is a free integrated tool that allows you to access, configure, manage and administer all components of the SQL server, Azure SQL Database, Azure SQL Managed Instance and Azure Synapse Analytics. While it only runs on Windows, it can be installed on a Mac either using a virtual machine or via Docker. The first way is to install a virtual machine (VM) using programs like VirtualBox, Parallels Desktop, etc. Then you’ll install Windows onto that VM, which requires a payment for the license, and finally, you’ll use the VM to install SSMS. The second option is to install the SQL server using Docker. Microsoft provides Azure Data Studio as a graphical user interface to run the SQL server on Mac. This article covers the second option. Docker is a tool designed to make the creation, deployment, and running of applications by using containers much easier. Below are the following steps to run SSMS on Mac.""",user_id=user2.id)
post2=Post(title=f"""Bootstrap 5""",content=f"""As with previous versions of Bootstrap, DataTables can also be integrated seamlessly with Bootstrap 5. This integration is done simply by including the DataTables Bootstrap 5 files (CSS and JS) which sets the defaults required for DataTables to be initialised as normal, as shown in this example.""",user_id=user3.id)

db.session.add_all([post1, post2])
db.session.commit()

# Add tags

tag1=Tag(name="Fun")
tag2=Tag(name="Even More")
tag3=Tag(name="Bloop")
tag4=Tag(name="Zope")

db.session.add_all([tag1, tag2, tag3,tag4])
db.session.commit()


# Add Post tags

postTag1=PostTag(post_id=post1.id,tag_id=tag1.id)
postTag2=PostTag(post_id=post1.id,tag_id=tag2.id)
postTag3=PostTag(post_id=post2.id,tag_id=tag1.id)
postTag4=PostTag(post_id=post2.id,tag_id=tag2.id)
postTag5=PostTag(post_id=post2.id,tag_id=tag3.id)
postTag6=PostTag(post_id=post2.id,tag_id=tag4.id)

db.session.add_all([postTag1, postTag2, postTag3,postTag4,postTag5,postTag6])
db.session.commit()


