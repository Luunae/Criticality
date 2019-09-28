import npyscreen
from npyscreen import Form


def add_standard_handlers(form: Form, quit=False):
    def finish():
        form.editing = False
        if quit:
            exit(0)

    form.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = finish