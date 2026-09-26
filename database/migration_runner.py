from database.database import SessionLocal
from database.models import SchemaMigration


def migration_applied(session, version):
    return session.query(
        SchemaMigration
    ).filter(
        SchemaMigration.version == version
    ).first()


def record_migration(
    session,
    name,
    version,
    checksum=None,
):
    session.add(
        SchemaMigration(
            migration_name=name,
            version=version,
            checksum=checksum,
        )
    )
