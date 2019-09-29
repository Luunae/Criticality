import npyscreen
from npyscreen import Form


def add_standard_handlers(form: Form, quit=False):
    def finish():
        form.editing = False
        if quit:
            exit(0)

    form.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = finish


def add_handlers(form, handlers):
    """
    Add handlers with upper and lowercase
    :param form: form
    :param handlers: lowercase handlers
    """
    form.add_handlers(handlers)
    form.add_handlers({x.upper(): y for x, y in handlers.items()})
