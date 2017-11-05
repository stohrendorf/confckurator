from sqlalchemy_continuum import transaction_class, Operation, parent_class
from sqlalchemy_continuum.transaction import TransactionBase

from db import make_session


def _marshal_changed_entities(transaction: TransactionBase, with_details):
    return [{
        'entity': parent_class(versioned_class).__name__,
        'changesets': [_marshal_changeset(changeset, with_details) for changeset in changesets]
    } for versioned_class, changesets in transaction.changed_entities.items()]


def _marshal_changeset(changeset, with_details):
    if changeset.operation_type == Operation.INSERT:
        return {
            'type': 'create',
            'revision': changeset.index,
            'fields': [
                {'field': field, 'value': change[1]}
                for field, change in changeset.changeset.items()
            ] if with_details else None
        }
    elif changeset.operation_type == Operation.DELETE:
        return {
            'type': 'delete',
            'revision': changeset.index,
            'fields': [
                {'field': field, 'old': change[0]}
                for field, change in changeset.changeset.items()
            ] if with_details else None
        }
    elif changeset.operation_type == Operation.UPDATE:
        return {
            'type': 'update',
            'revision': changeset.index,
            'fields': [
                {'field': field, 'old': change[0], 'value': change[1]}
                for field, change in changeset.changeset.items()
            ] if with_details else None
        }
    else:
        raise RuntimeError('Unhandled changeset operation type {}'.format(changeset.operation_type))


def get_history_for_entity(cls, limit=10, with_details=False):
    transaction = transaction_class(cls)
    transaction_changes = cls.__versioned__['transaction_changes']
    with make_session() as session:
        transactions = (session
                        .query(transaction)
                        .join(transaction.changes)
                        .filter(transaction_changes.entity_name.in_([cls.__name__]))
                        .order_by(transaction.issued_at.desc())
                        .limit(limit)
                        .all())

        return [{
            'transaction_id': transaction.id,
            'issued_at': transaction.issued_at.isoformat(),
            'remote_address': transaction.remote_addr,
            'changed_entities': _marshal_changed_entities(transaction, with_details)
        } for transaction in transactions]
