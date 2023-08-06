from dateutil.parser import parse
from datetime import timedelta

from beancount.ingest import importer
from beancount.core import data
from beancount.core import amount
from beancount.core.number import D
from beancount.ingest.importers.mixins import identifier

import camelot
import re


class Importer(identifier.IdentifyMixin, importer.ImporterProtocol):
    """An importer for Bank Cler ZAK PDF files files."""

    def __init__(self, regexps, account):
        identifier.IdentifyMixin.__init__(self, matchers=[
            ('filename', regexps)
        ])
        self.account = account

    def file_account(self, file):
        return self.account

    def createEntry(self, file, date, amt, text):
        bookingNrRgexp = re.compile(r'BC Buchungsnr. (?P<bookingRef>\d+)$')
        m = bookingNrRgexp.search(text)
        bookingRef = m.group('bookingRef')
        text = re.sub(bookingNrRgexp, '', text)

        meta = data.new_metadata(file.name, 0, {'zakref': bookingRef})
        return data.Transaction(
            meta,
            parse(date.strip(), dayfirst=True).date(),
            '*',
            '',
            text.strip(),
            data.EMPTY_SET,
            data.EMPTY_SET,
            [
                data.Posting(self.account, amount.Amount(D(amt), 'CHF'), None, None, None, None),
            ]
        )

    def createBalanceEntry(self, file, date, amt):
        meta = data.new_metadata(file.name, 0)
        return data.Balance(
            meta,
            parse(date.strip(), dayfirst=True).date() + timedelta(days=1),
            self.account,
            amount.Amount(D(amt), 'CHF'),
            None,
            None,
        )

    def cleanNumber(self, number):
        if isinstance(number, str):
            return D(number.replace('\'', ''))
        else:
            return number

    def extract(self, file, existing_entries):
        entries = []

        tables = camelot.read_pdf(file.name, flavor='stream', pages='all', table_regions=['60,450,600,200'])
        df = tables[0].df
        new_header = df.iloc[0]
        df = df[1:]
        df.columns = new_header

        date = None
        text = ''
        amount = None
        saldo = None

        for row in df.itertuples():
            if row.Saldo:
                if date and amount:
                    entries.append(self.createEntry(file, date, amount, text))

                date = None
                amount = None
                text = ''

            if row.Valuta:
                date = row.Valuta

            if row.Text:
                text += ' ' + row.Text

            if row.Belastung:
                amount = -self.cleanNumber(row.Belastung)

            if row.Gutschrift:
                amount = self.cleanNumber(row.Gutschrift)

            if row.Saldo:
                saldo = self.cleanNumber(row.Saldo)

        if date and amount:
            entries.append(self.createEntry(file, date, amount, text))

        dateRegexp = re.compile(r'\d\d.\d\d.\d\d\d\d')
        m = dateRegexp.search(text)
        date = m.group()
        entries.append(self.createBalanceEntry(file, date, saldo))

        return entries
