# coding=utf-8
from flask_pro import create, db
from module import Author, Book, Admin
from flask_migrate import MigrateCommand
from flask_script import Manager, Shell
import click
from flask import render_template
from datetime import datetime

app = create()
manage = Manager(app)
manage.add_command('db', MigrateCommand)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', current_time=datetime.utcnow())


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=True, help='The password used to login.')
def initadmin(username, password):
    """Building Bluelog, just for you."""

    click.echo('Initializing the database...')
    db.create_all()

    admin = Admin.query.first()
    if admin is not None:
        click.echo('The administrator already exists, updating...')
        admin.username = username
        admin.set_password(password)
    else:
        click.echo('Creating the temporary administrator account...')
        admin = Admin(
            username=username
        )
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        click.echo('Done.')


@app.cli.command()
@click.option('--count', default=20, help='Quantity of dbrecode, default is 20.')
def forge(count):
    """Generate fake messages."""
    from faker import Faker

    fake = Faker(locale='zh_CN')
    click.echo('Working...')

    for i in range(count):
        author = Author(
            author_name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number()
        )
        db.session.add(author)
    db.session.commit()

    for i in range(count):
        book = Book(
            book_name=fake.file_name(),
            create_time=fake.date_time_this_year(),
            author_id=fake.random_digit_not_null()
        )
        db.session.add(book)

    db.session.commit()
    click.echo('Created %d fake messages.' % count)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Author=Author, Book=Book)
# manage.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manage.run()
