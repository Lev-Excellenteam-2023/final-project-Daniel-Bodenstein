import asyncio
import zipfile
from flaskApi import parser
import openai_pptx
from pathlib import Path
import util
import os


async def get_explanation_to_pptx_into_json(pptx_path, pptx_topic=None, path_to_json=None):
    """
    Generate explanations for a PowerPoint (.pptx) file and save the results in JSON format.

    Args:
        pptx_path (str): The path to the PowerPoint file.
        pptx_topic (str, optional): The topic of the PowerPoint file. If not provided, the file name without extension will be used as the topic.
        path_to_json (str, optional): The path to save the resulting JSON file. If not provided, a JSON file will be created in the same directory as the PowerPoint file with a name derived from the PowerPoint file name.

    Returns:
        None

    Raises:
        zipfile.BadZipfile: If the provided file is not a valid PowerPoint file.

    """
    try:
        presentation_as_list_of_slides = parser.get_presentation_as_list_of_slides(pptx_path)
    except zipfile.BadZipfile as e:
        print('this not a power point file')
        return

    if not pptx_topic:
        pptx_topic = util.get_file_name_without_extension(pptx_path)

    presentation_explanation_slides_list = await openai_pptx.async_get_explanation_to_presentation(
                                                                  presentation_as_list_of_slides, topic=pptx_topic)

    if not path_to_json:
        path_to_json = os.path.join(util.get_directory_path(pptx_path),
                                    util.get_file_name_without_extension(pptx_path) + '_explanation.json')

    util.write_list_to_json(presentation_explanation_slides_list, path_to_json)
    print(f'finish write in  {path_to_json}')


async def main():
    while True:
        pptx_path = await util.async_input("enter path to pttx file or E to exit:    ")

        if pptx_path == 'E':
            return

        # convert path to python format
        pptx_path = Path(pptx_path)

        if not util.check_file_exists(pptx_path):
            print('file dont exist')
            continue

        pptx_topic = await util.async_input("enter the topic of the presentation or enter D to take the name of the "
                                            "file as topic:  ")

        if pptx_topic == 'D':
            pptx_topic = None

        asyncio.create_task(get_explanation_to_pptx_into_json(pptx_path=pptx_path, pptx_topic=pptx_topic))


if __name__ == '__main__':
    asyncio.run(main())
