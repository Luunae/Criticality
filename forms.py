import npyscreen
from npyscreen import Form


def add_standard_handlers(form: Form):
    def finish():
        form.editing = False

    form.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = finish
