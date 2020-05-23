from recipe_parser.helper import text_to_number
import json


def parse_instructions(recipe):

    # base dictionary

    if len(blocks.pages[0].blocks) < 2:

        # parse string to check if there is a detectable structure in the string -
        # 1. followed by 2. followed by 3. etc. to indicate steps.

        # apply text2num library

        # recipe = text_to_number(recipe)

        # transform to iterable format

        # recipe = recipe.splitlines()

        instructions_dict = {"instructions": [texts[0].description]}
        return json.dumps(instructions_dict)

    else:

        all_blocks = ""

        for a in range(len(blocks.pages[0].blocks)):

            all_blocks = all_blocks + "new block"

            for b in range(len(blocks.pages[0].blocks[a].paragraphs)):

                for c in range(len(blocks.pages[0].blocks[a].paragraphs[b].words)):

                    all_blocks = all_blocks + " "
                    for d in range(len(blocks.pages[0].blocks[a].paragraphs[b].words[c].symbols)):

                        all_blocks = all_blocks + \
                            blocks.pages[0].blocks[a].paragraphs[b].words[c].symbols[d].text

        blocks_splitted = all_blocks.split("new block")[1:]

        instructions_dict = {"instructions": blocks_splitted}
        return json.dumps(instructions_dict)
