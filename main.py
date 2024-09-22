from datetime import datetime, timedelta
from decimal import Decimal

date_format = '%Y-%m-%d'


def add(items, title, amount, expiration_date=None):
    if title not in items:
        items[title] = []
    if expiration_date:
        expiration_date = datetime.strptime(expiration_date,
                                            date_format).date()  # if expiration_date else expiration_date

    items[title].append({'amount': amount, 'expiration_date': expiration_date})

    return items


def add_by_note(items, note):
    # parts = note.split()

    # if len(parts[-1].split('-')) == 3:

    # expiration_date = None
    # amount = parts[-1]
    # title = ' '.join(parts[:-1])
    # else:
    # expiration_date = None
    # amount = Decimal(parts[-1])
    # title = ' '.join(parts[0:-1])

    # add(items, title, Decimal(amout), expiration_date)

    parts = note.split()

    if len(parts[-1].split('-')) == 3 and parts[-1].replace('-', '').isdigit:
        expiration_date = parts[-1]
        amount = parts[-2]
        title = ' '.join(parts[:-2])
    else:
        expiration_date = None
        amount = parts[-1]
        title = ' '.join(parts[:-1])

    add(items, title, Decimal(amount), expiration_date)


def find(items, needle):
    results = []
    needle = needle.lower()
    for title in items:
        title_lower = title.lower()
        if needle in title_lower:
            results.append(title)
    return results


def amount(items, needle):
    found_items = find(items, needle)
    total_amount = Decimal(0)

    for title in found_items:
        if title in items:
            for batch in items[title]:
                total_amount += batch['amount']
    return total_amount


def expire(items, in_advance_days=0):
    current_date = datetime.today().date()
    target_date = current_date + timedelta(days=in_advance_days)
    expiring_items = {}

    for title, batches in items.items():
        for batch in batches:
            expiration_date = batch.get('expiration_date')

            if expiration_date and expiration_date <= target_date:
                if title in expiring_items:
                    expiring_items[title] += batch['amount']
                else:
                    expiring_items[title] = batch['amount']

    return [(title, amount) for title, amount in expiring_items.items()]


goods = {
    'Water': [

        {'amount': Decimal('0.5'), 'expiration_date': datetime(2023, 7, 15).date()},

        {'amount': Decimal('2'), 'expiration_date': datetime(2023, 8, 1).date()},
    ],
    'Bread': [
        {'amount': Decimal('1.5'), 'expiration_date': None}
    ],
}
goods = {}
add_by_note(goods, 'Яйца Фабрики 1 4 2024-10-01')
print(goods)
