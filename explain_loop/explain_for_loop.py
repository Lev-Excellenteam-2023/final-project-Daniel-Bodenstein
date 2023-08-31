import os
import datetime
import file_system_db as file_db
from sql.sql_db import sqldb
import sql.queries
import sql.sql_tables
import openai_pptx as ai
import asyncio
import logging

# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_db = file_db()
sql_db = sqldb()

already_processed_files_uid = set(file_db.get_all_download_uid())


async def explain_presentation(slides, topic):
    """
    Asynchronously explain a presentation using the AI model.

    Args:
        slides (list): List of slides in the presentation.
        topic: the topic of the presentation.

    Returns:
        dict: Dictionary containing the UID, explanation, and name.
    """

    logger.info("Explaining presentation...")
    explain = await ai.async_get_explanation_to_presentation(slides, topic)
    logger.info("Presentation explained.")
    return explain


async def explain_new_presentation():
    """
    Asynchronously explain new presentations.

    This function retrieves all new uploaded presentations, processes them using the AI model,
    and saves the explanations.
    """
    logger.info("Checking for new presentations...")
    pending_uploads = sql_db.get_uploads_by_status(status=sql.Status.PENDING)
    logger.info(f"Found {len(pending_uploads)} pending presentation(s).")

    if not pending_uploads:
        return
    logger.info(f"{pending_uploads}")

    explain_tasks = [explain_presentation(file_db.get(upload.upload_path), upload.filename) for upload in
                     pending_uploads]
    explanations = await asyncio.gather(*explain_tasks, return_exceptions=True)

    uploads_id_change_status = []
    for upload, explain in zip(pending_uploads, explanations):
        if isinstance(explain, Exception):
            logger.error(f"Error occurred while explaining presentation: {explain}")
            continue

        logger.info("Saving explanation...")
        file_db.save(explain, upload.downloads_path)
        logger.info("Explanation saved.")
        uploads_id_change_status.append(upload.id)

    logger.info("Updating status of completed presentations...")
    sql_db.update_uploadds_by_id_list(uploads_id_change_status,
                                      {'status': sql.Status.complete, 'finish_time': datetime.datetime.now()})
    logger.info("Status updated for completed presentations.")

if __name__ == '__main__':
    logger.info("Starting the explanation process...")
    asyncio.run(explain_new_presentation())
    logger.info("Explanation process completed.")