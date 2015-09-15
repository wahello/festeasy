from IPython.terminal.interactiveshell import TerminalInteractiveShell
from flask import current_app
from flask.ext.script import Manager, Command
from flask.ext.script import Shell, Server

from backend import create_app, db
from backend import models
from backend.models import User, Product, Event, Cart, Session


manager = Manager(create_app, with_default_commands=False)
manager.add_option(
    '-c', '--config',
    dest='config', default='file', required=False,
)


class RunServer(Server):
    def handle(self, *args, **kwargs):
        Server.handle(self, *args, **kwargs)
manager.add_command(
    'run-api',
    RunServer(use_debugger=True, use_reloader=True, host='0.0.0.0'),
)


class CreateAll(Command):
    def run(self):
        db.create_all()
manager.add_command('create-all', CreateAll())


class DropAll(Command):
    def run(self):
        db.drop_all()
manager.add_command('drop-all', DropAll())


class InitDB(Command):
    def run(self):
        db.drop_all()
        db.create_all()
        test_user = User(
            email_address='test@festeasy.co.za',
            password='123',
            is_admin=True,
            first_name='TestName',
            cart=Cart()
            )
        import datetime
        now = datetime.datetime.now()
        never = now + datetime.timedelta(days=1000)
        session = Session(user=test_user, expires_on=never)
        session.generate_token()
        test_user.sessions.append(
            session,
        )
        users = [
            test_user,
        ]
        products = [
            Product(name='Castle Lite Beer',
                    cost_rands=10, is_enabled=True, price_rands=20),
            Product(name='Lays Small Pack',
                    cost_rands=10, is_enabled=True, price_rands=9),
            Product(name='Coke Can',
                    cost_rands=10, is_enabled=True, price_rands=9),
            Product(name='Windhoek Beer',
                    cost_rands=10, is_enabled=True, price_rands=21),
            Product(name='Text Chocolate',
                    cost_rands=10, is_enabled=True, price_rands=9),
            Product(name='KitKat Chocolate',
                    cost_rands=10, is_enabled=True, price_rands=8),
            Product(name='Jelly Beans',
                    cost_rands=10, is_enabled=True, price_rands=7),
        ]
        events = [
            Event(name='Rocking The Daisies', is_enabled=True),
            Event(name='Sunflower Fest', is_enabled=True),
            Event(name='Oppie Koppie', is_enabled=True),
        ]
        things = users + products + events
        for thing in things:
            db.session.add(thing)
        db.session.commit()
manager.add_command('init-db', InitDB())


def _make_context():
    context = dict(
        db=db,
        current_app=current_app,
    )
    context.update(vars(models))
    return context
manager.add_command('shell', Shell(make_context=_make_context))

if __name__ == '__main__':
    TerminalInteractiveShell.confirm_exit.default_value = False
    manager.run()
