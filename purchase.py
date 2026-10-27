from trytond.model import fields
from trytond.pool import Pool, PoolMeta


class Purchase(metaclass=PoolMeta):
    __name__ = 'purchase.purchase'

    @classmethod
    def quote(cls, purchases):
        super().quote(purchases)
        Line = Pool().get('purchase.line')
        to_save = []
        for purchase in purchases:
            number = max(
                (line.line_number or 0 for line in purchase.lines), default=0)
            for line in purchase.lines:
                if line.line_number is None:
                    number += 1
                    line.line_number = number
                    to_save.append(line)
        Line.save(to_save)


class Line(metaclass=PoolMeta):
    __name__ = 'purchase.line'

    line_number = fields.Integer("Line Number", readonly=True)

    @classmethod
    def copy(cls, lines, default=None):
        default = default.copy() if default is not None else {}
        default.setdefault('line_number', None)
        return super().copy(lines, default=default)
