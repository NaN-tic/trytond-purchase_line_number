import unittest
from decimal import Decimal

from proteus import Model
from trytond.modules.company.tests.tools import create_company
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class TestPurchase(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):
        activate_modules('purchase_line_number')
        create_company()
        Party = Model.get('party.party')
        Purchase = Model.get('purchase.purchase')
        supplier = Party(name='Supplier')
        supplier.save()

        purchase = Purchase(party=supplier)
        purchase.lines.new(
            sequence=20, description='Second', quantity=1,
            unit_price=Decimal('10'))
        purchase.lines.new(
            sequence=10, description='First', quantity=1,
            unit_price=Decimal('20'))
        purchase.save()
        self.assertTrue(all(l.line_number is None for l in purchase.lines))
        purchase.click('quote')
        self.assertEqual(purchase.state, 'quotation')
        self.assertEqual(
            [(l.description, l.line_number) for l in purchase.lines],
            [('First', 1), ('Second', 2)])

        purchase.click('draft')
        purchase.lines.new(sequence=15, type='comment', description='Inserted')
        purchase.lines.new(
            sequence=30, description='Last', quantity=1,
            unit_price=Decimal('30'))
        purchase.click('quote')
        self.assertEqual(purchase.state, 'quotation')
        self.assertEqual(
            [(l.description, l.line_number) for l in purchase.lines],
            [('First', 1), ('Inserted', 3), ('Second', 2), ('Last', 4)])

        purchase.click('draft')
        purchase.click('quote')
        self.assertEqual([l.line_number for l in purchase.lines], [1, 3, 2, 4])

        copied, = Purchase.duplicate([purchase])
        self.assertTrue(all(l.line_number is None for l in copied.lines))
        copied.click('quote')
        self.assertEqual(copied.state, 'quotation')
        self.assertEqual([l.line_number for l in copied.lines], [1, 2, 3, 4])
