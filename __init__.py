from trytond.pool import Pool

from . import purchase


def register():
    Pool.register(
        purchase.Purchase,
        purchase.Line,
        module='purchase_line_number', type_='model')
