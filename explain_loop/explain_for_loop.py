import os
import file_system_db as db
import openai_pptx as ai
import asyncio
import logging

# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


db = db.explainer_file_db()

already_processed_files_uid = set(db.get_all_download_uid())


async def explain_presentation(slides, name, uid):
    """
    Asynchronously explain a presentation using the AI model.

    Args:
        slides (list): List of slides in the presentation.
        name (str): The name of the presentation.
        uid (str): The UID associated with the presentation.

    Returns:
        dict: Dictionary containing the UID, explanation, and name.
    """
    explain = await ai.async_get_explanation_to_presentation(slides, name)
    return {'uid': uid, 'explain': explain, 'name': name}


async def explain_new_presentation():
    """
    Asynchronously explain new presentations.

    This function retrieves all new uploaded presentations, processes them using the AI model,
    and saves the explanations to the download directory.
    """
    all_upload_files_uid = db.get_all_upload_uid()

    tasks = []
    for uid in all_upload_files_uid:

        if uid in already_processed_files_uid:
            continue

        presentation = db.get_from_uploads(uid)

        tasks.append(explain_presentation(presentation['slides'], presentation['topic'], uid))

    explanations = await asyncio.gather(*tasks)

    for exp in explanations:
        db.save_to_download(exp['explain'], exp['uid'], exp['name'])
        logger.info('Explained: ' + exp['name'])
        already_processed_files_uid.add(exp['uid'])

if __name__ == '__main__':
    logger.info("Starting the explanation process...")
    asyncio.run(explain_new_presentation())
    logger.info("Explanation process completed.")