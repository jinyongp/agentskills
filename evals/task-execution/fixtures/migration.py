import sqlite3


def batch(db, *, fail_after=None):
    db.execute('BEGIN IMMEDIATE')
    try:
        cursor = db.execute('SELECT last_id FROM progress WHERE id = 1').fetchone()[0]
        rows = db.execute(
            'SELECT id, old_label FROM items WHERE id > ? ORDER BY id LIMIT 3',
            (cursor,),
        ).fetchall()
        for position, (key, label) in enumerate(rows, 1):
            db.execute(
                'UPDATE items SET new_label = ? WHERE id = ? '
                'AND new_label IS NULL AND old_label = ?', (label, key, label),
            )
            if position == fail_after:
                raise RuntimeError('injected interruption')
        if rows:
            db.execute('UPDATE progress SET last_id = ? WHERE id = 1', (rows[-1][0],))
        db.commit()
        return bool(rows)
    except Exception:
        db.rollback()
        raise


def missing(db):
    return db.execute('SELECT COUNT(*) FROM items WHERE new_label IS NULL').fetchone()[0]


def reconcile(db):
    with db:
        db.execute('UPDATE items SET new_label = old_label WHERE new_label IS NULL')


def connect(path):
    return sqlite3.connect(path, isolation_level=None)
