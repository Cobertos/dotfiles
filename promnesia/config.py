from promnesia import Source
from promnesia.sources import auto, reddit

'''
List of sources to use.

You can specify your own, add more sources, etc.
See https://github.com/karlicoss/promnesia#setup for more information
'''
SOURCES = [
    Source(
        auto.index,
        '/home/cobertos/Seafile/notes',
        name="notes"
    ),
    # Source(
    #     auto.index,
    #     '/home/cobertos/Seafile/projects',
    #     name="projects"
    # )
    reddit
]
