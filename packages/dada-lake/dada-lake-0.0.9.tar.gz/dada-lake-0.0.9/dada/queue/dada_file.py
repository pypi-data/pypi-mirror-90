import logging

from dada_utils import path
import dada_file
import dada_serde

from dada.models.core import db_execute
from dada.queue.core import celery

CELERY_DADA_LOGGER = logging.getLogger()


@celery.task
def save(filepath, **kwargs):
    """
    Upload a file to s3 as a background task
    """
    CELERY_DADA_LOGGER.info(f"[Q.dada_file.save] saving {filepath}")
    df = dada_file.load(filepath, **kwargs)
    df.save_locally()
    df.share_globally()
    # HACK: insert extracted bundle field here
    # because we cant cross import
    # from this file to dada.models.file
    if df.db.file_type == "bundle":
        query = """
            UPDATE file
            SET fields = '{fields}'
            WHERE id = {id}
        """.format(
            id=df.db.get("id"), fields=dada_serde.obj_to_json(df.db.fields)
        )
        db_execute(query)
    path.remove(filepath)
