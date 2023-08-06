"""Extract paragraphs and chapters from LTTextBox by pdfminer.six.

Coordinate system of pdfminer LTTextBox is defined below::

    *-page------------------------*
    |                             |
    |                             |
    |                             |
    |        +-LTTextBox-+        |
    |<--x0-->|           |   ^    |
    |        |           |   |    |
    |<-------|---x1----->|   |    |
    |        +-----------+   |    |
    |            ^           |    |
    |           y0          y1    |
    |            v           v    |
    *-----------------------------*

So the LTTextBox coordinates are::

    (x0,y1)---------(x1,y1)
    |                     |
    |                     |
    |                     |
    (x0,y0)---------(x1,y0)

pdfminer sees y0 and y1 from the bottom of the page, so y0 is smaller than y1.
All coordinates are given in points where 72 points are 1 inch.
"""
import logging
import re
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Union

from libpdf import parameters
from libpdf.catalog import catalog
from libpdf.log import logging_needed
from libpdf.models.chapter import Chapter
from libpdf.models.figure import Figure
from libpdf.models.link import Link
from libpdf.models.page import Page
from libpdf.models.paragraph import Paragraph
from libpdf.models.position import Position
from libpdf.models.table import Table
from libpdf.parameters import (
    ANNO_X_TOLERANCE,
    CHAPTER_RECTANGLE_EXTEND,
    MIN_OUTLINE_TITLE_TEXTBOX_SIMILARITY,
    TABLE_MARGIN,
)
from libpdf.progress import bar_format_lvl2, tqdm
from libpdf.utils import page_crop

from pdfminer.layout import (
    LTAnno,
    LTChar,
    LTText,
    LTTextBox,
    LTTextLineHorizontal,
)


LOG = logging.getLogger(__name__)


def extract_paragraphs_chapters(
    pdf,
    figure_list: List[Figure],
    table_list: List[Table],
    page_list: List[Page],
    no_chapters,
    no_paragraphs,
) -> Tuple[List[Paragraph], List[Chapter]]:
    """Extract paragraphs and chapter's headline from given pdf."""
    extracted_textboxes = extract_textboxes(pdf, figure_list, table_list, page_list)
    chapter_list = []
    if no_chapters:
        LOG.info('Excluding chapters extraction')
    else:
        if catalog['outline']:
            chapter_list = render_chapters(extracted_textboxes, page_list)

    paragraph_list = []
    if no_paragraphs:
        LOG.info('Excluding paragraphs extraction')
    else:
        LOG.info('Extracting paragraphs ...')
        paragraph_list = render_paragraphs(extracted_textboxes, page_list)
    return paragraph_list, chapter_list


def extract_textboxes(pdf, figure_list, table_list, page_list):
    """
    Extract and filter textboxes using pdfminer.

    First, a list of LTTextBoxes is extracted and they are sorted by pages from pdfminer as textboxes
    Second, textboxes inside the elements (figures or tables) are removed from the list.

    :param pdf:
    :param figure_list:
    :param table_list:
    :param page_list:
    :return:
    """
    page_textboxes = pdfminer_get_textboxes(pdf)  # noqa: F841  # flake8 not used warning

    for idx_page, _ in page_textboxes.copy().items():
        # pages that shall be extracted
        if idx_page + 1 not in [page.number for page in page_list]:
            del page_textboxes[idx_page]

    if table_list is not None or figure_list is not None:
        page_textboxes_filtered = remove_textboxes_in_tables_figures(page_textboxes, figure_list, table_list)
    else:
        page_textboxes_filtered = page_textboxes

    # remove textbox that only contains LTAnno like \n or whitespaces
    page_textboxes_filtered_noise = {}
    for page_idx, textboxes in page_textboxes_filtered.items():
        textboxes_without_noise = []
        for textbox in textboxes:
            # remove empty texbox only contains whitespaces or newlines
            if not re.match(r'^\s*$', textbox.get_text()):
                # remove all the \n at the end of textbox
                if textbox._objs[-1]._objs[-1].get_text() == '\n':  # pylint: disable=protected-access
                    del textbox._objs[-1]._objs[-1]  # pylint: disable=protected-access
                    textboxes_without_noise.append(textbox)
        page_textboxes_filtered_noise[page_idx] = textboxes_without_noise

    return page_textboxes_filtered_noise


def render_chapters(  # pylint: disable=too-many-branches
    page_textboxes_filtered: Dict[int, List[LTTextBox]],
    page_list: List[Page],
) -> List[Chapter]:
    """
    Render libpdf chapters from LTTextboxes according to outline catalog.

    The algorithm follows the steps below

    1. Sort the flatten outline chapters into a dict by pages
    2. Iterate the sorted outline chapters by pages
    3. chapter_examiner checks if a certain chapter matches the textboxes on the same page
    4. Instantiate the chapter if the matched textboxes is found. Otherwise, a virtual chapter is instantiated.
    5. The matched textboxes are removed from the list "page_textboxes_filtered"

    :param page_textboxes_filtered: all of the textboxes sorted by pages
    :param page_list: a list of libpdf pages
    :return: a list of libpdf chapters
    """
    chapter_list = []
    flatten_outline = []
    _flatten_outline(nested_outline=catalog['outline']['content'], flatten_outline=flatten_outline)

    # sort the flatten outline chapters into a dict by pages
    chapters_sorted_by_page = {}
    extracted_page_nums = [page.number for page in page_list]
    for chapter in flatten_outline:
        if chapter['position']['page'] in extracted_page_nums:
            if chapter['position']['page'] not in chapters_sorted_by_page:
                chapters_sorted_by_page[chapter['position']['page']] = []
            chapters_sorted_by_page[chapter['position']['page']].append(chapter)

    for page_number, chapters in chapters_sorted_by_page.items():
        if page_number - 1 in page_textboxes_filtered:
            textboxes = page_textboxes_filtered[page_number - 1]
            for page in page_list:
                if page.number == page_number:
                    chapter_page = page
            for chapter in chapters:
                chapter_textboxes = chapter_examiner(chapter, textboxes, chapter_page)
                if chapter_textboxes:
                    # render chapter based on the textbox
                    x0 = min(chapter_textboxes, key=lambda x: x.x0).x0
                    y0 = min(chapter_textboxes, key=lambda x: x.y0).y0
                    x1 = max(chapter_textboxes, key=lambda x: x.x1).x1
                    y1 = max(chapter_textboxes, key=lambda x: x.y1).y1
                    position = Position(x0, y0, x1, y1, chapter_page)

                    if len(chapter_textboxes) == 2 and ('virt.' in chapter['number']):
                        # the case where chapter's number and title are grouped into two different textboxes,
                        # and outline catalog doesn't have chapter number.
                        chapter['number'] = min(chapter_textboxes, key=lambda x: x.x0).get_text().strip()

                    # remove textboxes recognised as the chapters from page_textboxes_filtered. By doing so,
                    # these textboxes will not be instantiated as paragraphs.
                    for textbox in chapter_textboxes:
                        textboxes.remove(textbox)
                else:
                    # if no matched textboxes are found, the position of a virtual chapter is rendered
                    position = virtual_chapter_position_generator(chapter, chapter_page)
                    LOG.info(
                        'The chapter "%s" on page %s can not be detected. The virtual chapter number "%s" is applied. '
                        'This number may not be consistent with the numerical order in the content',
                        chapter['title'],
                        chapter['position']['page'],
                        chapter['number'],
                    )

                chapter_obj = Chapter(chapter['title'], chapter['number'], position, content=[], chapter=None)
                chapter_list.append(chapter_obj)
        else:
            pass

    return chapter_list


def virtual_chapter_position_generator(chapter: Dict, page: Page) -> Position:
    """
    Generate the position of a virtual chapter.

    :param chapter: an outline chapter from the catalog
    :param page: a libpdf page
    :return: an instance of libpdf position
    """
    if chapter['position']['y1'] - CHAPTER_RECTANGLE_EXTEND > 0:
        y0 = chapter['position']['y1'] - CHAPTER_RECTANGLE_EXTEND
    else:
        # expand to bottom
        y0 = 0

        # calculate chapter textbox x1
    if chapter['position']['x0'] + CHAPTER_RECTANGLE_EXTEND < page.width:
        x1 = chapter['position']['x0'] + CHAPTER_RECTANGLE_EXTEND
    else:
        # expand to right side
        x1 = page.width

    position = Position(chapter['position']['x0'], y0, x1, chapter['position']['y1'], page)

    return position


def chapter_examiner(chapter: Dict, textboxes: List[LTTextBox], page: Page) -> Union[None, List[LTTextBox]]:
    """
    Check if certain textboxes are or a certain textbox is the chapter.

    Three kinds of the similarities, number, title, content are evaluated with a certain chapter.

    Let's say a chapter's text in its content is "3.4.5 Chapter Example"
    The number of a chapter is "3.4.5".
    The title of a chapter is "Chapter Example"
    The content of a chapter is "3.4.5 Chapter Example"

    The chapter format in PDFs varies. There are a few possibilities below

    1. All chapters in PDF and outline have numbers and titles
    2. All chapters in PDF and outline have only titles
    3. Some chapters are only with titles and others have numbers and titles in the PDF and outline
    4. Chapters have numbers and titles in outline, but not in PDF content
    5. Chapters have numbers and titles in PDF content, but not in outline

    In any case, chapters with numbers and titles are expected. In case 2 and 3, a virtual number of the chapter will
    be introduced directly from the outline catalog extracted for those without numbers in outline and PDF content.

    In case 5, the number of chapters will be extracted in the algorithm and filled the number back to outline catalog.

    :param chapter: a chapter in the outline catalog
    :param textboxes: textboxes on a certain page
    :param page: a libpdf page
    :return: None means no textboxes are matched to the outline chapter. If the match is found, a list of textboxes
             is returned
    """
    # The width of the rectangle is the width of the page.
    # The height of the rectangle is a half of the page's height.
    # The vertical center of the rectangle is the y coordinate of the outline chapter. Then a fourth of the page's
    # height is extended upwards and downwards from the vertical center. It covers a half page based on the vertical
    # center of the outline chapter.
    # The coordinates of the rectangle are rect = (x0, y0, x1, y1).
    # This assumption may not work in PDFs with multiple columns.
    y0 = chapter['position']['y1'] - (page.height / 4)
    y1 = chapter['position']['y1'] + (page.height / 4)
    if y0 < 0:
        y0 = 0
    if y1 > page.height:
        y1 = page.height

    rect = (0, y0, page.width, y1)

    # get the textboxes completely in the detection rectangle
    textboxes_in_rect = page_crop(rect, textboxes, LTText, contain_completely=True)

    if not textboxes_in_rect:
        return None

    similarity_textboxes = []
    # evaluate the similarities of number, title and content of textboxes with a chapter
    for textbox in textboxes_in_rect:
        # check if textbox text and headline text has a certain similarity
        similarity_title = SequenceMatcher(None, textbox.get_text().strip(), chapter['title']).ratio()
        if 'virt.' in chapter['number']:
            similarity_number = None
            similarity_content = None
        else:
            similarity_number = SequenceMatcher(None, textbox.get_text().strip(), chapter['number']).ratio()
            similarity_content = SequenceMatcher(
                None,
                textbox.get_text().strip(),
                f"{chapter['number']} {chapter['title']}",
            ).ratio()

        similarity_textboxes.append(
            {'title': similarity_title, 'number': similarity_number, 'content': similarity_content},
        )

    winners = similarity_referee(similarity_textboxes, textboxes_in_rect, chapter)

    return winners


def similarity_referee(  # pylint: disable=too-many-branches  # for readability
    similarity_textboxes: List[Dict],
    textboxes_in_rect: List[LTTextBox],
    chapter: Dict,
) -> List:
    """
    Select the textboxes with the highest similarity among titles, numbers or contents.

    It is possible to have a few textboxes having the same similarity. In this case, the textbox which
    is the vertically closest to the outline chapter will be picked up as the winner.

    :param similarity_textboxes: the similarity of the textboxes in the rectangle. The index of each similarity is
                                mapped to the textboxes_in_rect
    :param textboxes_in_rect: The textboxes in the given rectangle
    :param chapter: a chapter of outline catalog
    :return: A list of the textboxes with highest similarity among titles, numbers or contents
    """
    # decide who is the winner according to their similarities
    winners = []

    # find the winner of the title similarity
    title_winners_idx = [
        i for i, x in enumerate(similarity_textboxes) if x == max(similarity_textboxes, key=lambda x: x['title'])
    ]
    if len(title_winners_idx) > 1:
        # find the winner who has the shortest vertical distance to the jumping point of the outline chapter.
        # Presumably, the jumping point is on the top-left of the outline chapter

        title_winner_idx = min(
            title_winners_idx,
            key=lambda x: abs(textboxes_in_rect[x].y1 - chapter['position']['y1']),
        )
    else:
        title_winner_idx = title_winners_idx[0]

    if 'virt.' in chapter['number']:
        # if the chapter is virtual, only the title needs to be taken into account.

        if similarity_textboxes[title_winner_idx]['title'] > MIN_OUTLINE_TITLE_TEXTBOX_SIMILARITY:
            winners.append(textboxes_in_rect[title_winner_idx])
            # search for the textbox which may be the number of the chapter
            # The assumption is that the number is always located on the left of the chapter
            potential_chapter_number = [
                x
                for x in textboxes_in_rect
                if x.x0 < textboxes_in_rect[title_winner_idx].x0
                and abs(x.y0 - textboxes_in_rect[title_winner_idx].y0) < CHAPTER_RECTANGLE_EXTEND
                and abs(x.y1 - textboxes_in_rect[title_winner_idx].y1) < CHAPTER_RECTANGLE_EXTEND
            ]
            if len(potential_chapter_number) == 1:
                winners.append(potential_chapter_number[0])

    else:
        # the content of the chapter contains number and title
        # find the winner of the content similarity
        content_winners_idx = [
            i for i, x in enumerate(similarity_textboxes) if x == max(similarity_textboxes, key=lambda x: x['content'])
        ]
        if len(content_winners_idx) > 1:
            content_winner_idx = min(
                content_winners_idx,
                key=lambda x: abs(textboxes_in_rect[x].y1 - chapter['position']['y1']),
            )
        else:
            content_winner_idx = content_winners_idx[0]

        # find the winner of the number similarity
        number_winners_idx = [
            i for i, x in enumerate(similarity_textboxes) if x == max(similarity_textboxes, key=lambda x: x['number'])
        ]
        if len(number_winners_idx) > 1:
            number_winner_idx = min(
                number_winners_idx,
                key=lambda x: abs(textboxes_in_rect[x].y1 - chapter['position']['y1']),
            )
        else:
            number_winner_idx = number_winners_idx[0]

        # content_winner_idx, content_winner_value = max(enumerate(similarity_textboxes), key=lambda x: x[1]['content'])
        # title_winner_idx, title_winner_value = max(enumerate(similarity_textboxes), key=lambda x: x[1]['title'])
        # number_winner_idx, number_winner_value = max(enumerate(similarity_textboxes), key=lambda x: x[1]['number'])

        # If the textbox is 100% similar to the chapter in terms of its content (chapter number amd title),
        # it is considered the outline chapter jump target.
        if similarity_textboxes[content_winner_idx]['content'] == 1:
            # The case where the content of the textbox is 100% identical to the chapter's number plus title.
            winners.append(textboxes_in_rect[content_winner_idx])
        elif (
            similarity_textboxes[content_winner_idx]['content'] < similarity_textboxes[title_winner_idx]['title']
            and number_winner_idx != title_winner_idx
            and similarity_textboxes[number_winner_idx]['number'] > MIN_OUTLINE_TITLE_TEXTBOX_SIMILARITY
            and similarity_textboxes[title_winner_idx]['title'] > MIN_OUTLINE_TITLE_TEXTBOX_SIMILARITY
        ):
            # The case where chapter number and chapter title are broken into two different textboxes by pdfminer.
            # For the textbox which wins on the basis of the content, if the similarity of its title is bigger
            # than its content, it means the textbox contains title text only because if the textbox has the number
            # and title, its content similarity shall be the highest.
            winners.append(textboxes_in_rect[number_winner_idx])
            winners.append(textboxes_in_rect[title_winner_idx])
        elif (
            title_winner_idx == content_winner_idx
            and similarity_textboxes[content_winner_idx]['content'] >= similarity_textboxes[title_winner_idx]['title']
            and similarity_textboxes[content_winner_idx]['content'] > MIN_OUTLINE_TITLE_TEXTBOX_SIMILARITY
        ):
            # The case where chapter number and its title are in the same textbox
            # For the textbox which has high potential to be a chapter, it shall win the similarity
            # of both the title and the content. Its similarity of the content shall be bigger than that of title
            # in the case of the existence of chapter number. If the chapter number is not available,
            # the similarty of them shall be the same.
            winners.append(textboxes_in_rect[content_winner_idx])
        else:
            # If none of the terms is met, there is no winner in this case. It means none of the textboxes are outline
            # chapters.
            pass

    return winners


def render_paragraphs(  # pylint: disable=too-many-branches
    page_textboxes_filtered: Dict[int, List[LTTextBox]],
    page_list: List[Page],
) -> List[Paragraph]:
    """
    Render paragraphs from LTTextBox.

    :param page_textboxes_filtered: a dict where several lists of LTTextBox instances are sorted by pages excluding
                                    LTTextBox instances inside figures and tables
    :param page_list: list of libpdf Page objects
    :return: list of rendered paragraphs
    """
    paragraph_list = []
    paragraph_id = 1

    for page_index, textboxes in page_textboxes_filtered.items():
        # add textbox to a list of paragraphs
        for textbox in textboxes:
            # get position of textbox
            for page in page_list:
                if page.number == page_index + 1:
                    paragraph_page = page
            position = Position(textbox.x0, textbox.y0, textbox.x1, textbox.y1, paragraph_page)

            page_number = page_index + 1
            paragraph = render_single_paragraph(textbox, page_number, paragraph_id, position)
            paragraph_list.append(paragraph)
            paragraph_id += 1

    return paragraph_list


def render_single_paragraph(textbox: LTTextBox, page_number: int, paragraph_id: int, position: Position) -> Paragraph:
    """
    Render a paragraph with linked characters from the textbox.

    :param textbox:
    :param page_number:
    :param paragraph_id:
    :param position:
    :return: instance of a paragraph
    """
    text_textbox = textbox.get_text()
    links = []
    if catalog['annos']:
        links = extract_linked_chars(textbox, page_number)

    paragraph = Paragraph(paragraph_id, text_textbox, position, links)
    return paragraph


def extract_linked_chars(textbox: LTTextBox, page_number: int) -> List[Link]:
    """
    Extract plain texts and linked characters in textboxes.

    If a textbox has intersections with anno-rectangles on the page,
    the code will extract its indices of start and end characters in the anno as well as
    its position of the jump target.
    Conversely, the plan text of the textbox will be extracted for a paragraph

    A textbox may contain an anno or a few annos.

    :param textbox: an instance of LTtextBox, which consists of LTlinehroizontal
    :param page_number: page number starts from 1
    :return: a list of Links in the textbox
    """
    # rect[0] is x0 (left)
    # rect[1] is y0 (bottom)
    # rect[2] is x1 (right)
    # rect[3] is y1 (top)
    links = []
    if page_number in catalog['annos']:
        # collect the annos which are intersected with or in the textbox
        anno_textboxes = [
            x
            for x in catalog['annos'][page_number]['annotation']
            if x['rect'][0] < textbox.x1
            and x['rect'][1] < textbox.y1
            and x['rect'][2] > textbox.x0
            and x['rect'][3] > textbox.y0
        ]

        if anno_textboxes:
            # char_counter is used to count the number of the total chars which has been processed in the scope of
            # textbox,
            char_counter = 0
            for line_horizontal in textbox._objs:  # pylint: disable=protected-access #  easier to access
                # filter again to collect the annos which are in or at least a half vertically intersected with
                # the textline.

                annos_line = [
                    x
                    for x in anno_textboxes
                    if x['rect'][0] < line_horizontal.x1
                    and x['rect'][2] > line_horizontal.x0
                    and line_horizontal.y1 > (x['rect'][1] + abs(x['rect'][1] - x['rect'][3]) / 2) > line_horizontal.y0
                ]

                if annos_line:
                    annos_line.sort(key=lambda x: x['rect'][0])
                    links.extend(annos_scanner(line_horizontal, annos_line, char_counter))
                else:
                    pass
                char_counter = char_counter + len(
                    line_horizontal._objs,  # pylint: disable=protected-access #  easier to access
                )
        else:
            pass
    else:
        pass

    return links


def annos_scanner(
    lt_textline: LTTextLineHorizontal,
    annos_line: List,
    char_counter: int,
) -> List[Link]:  # pylint: disable=too-many-nested-blocks
    """
    Scan the characters annotated as the source link in the scope of a textline.

    The char is checked from left to right in a horizontal direction. As a textline may be intersected or contain a few
    anno-rectangles, the most left anno-rectangle will be used for char checking first.
    Once the chars in the anno-rectangle are all machted according to the positions, the next annon-rectangle will be
    used for the further char matching.

    Please note that LTAnno does not contain any coordinate information. There are a few cases to determine if LTAnno
    should be considered in an anno-rectangle.

    pos_target in the Link Class will be used to explore the libpdf target id when all the elements are extracted
    with success.

    :param lt_textline: LTTextlineHorizontal contains LTChar and LTAnno. LTChar contains the metadata of a char.
    :param annos_line: a list of annotations intersected or in the line, which has been sorted from
                        the left to the right.
    :param char_counter:  In the end of the process, all chars in the scope of a textbox is a char array, this variable
                        is used to index the start and end chars in the textbox
    :return: a list of Links in the textline
    """
    idx_anno = 0
    links = []
    # anno_start_idx is used to index which character is the start of the anno
    # anno_end_idx is used to index in which character has reached the last char in the anno-rectangle
    anno_flags = {'anno_start_idx': None, 'anno_stop_idx': None}

    for idx_char, char in enumerate(lt_textline._objs):  # pylint: disable=protected-access
        # if all the anno-rectangles in a line have all been checked, then just get plain text of chars
        if idx_anno < len(annos_line):
            anno_complete = first_last_char_in_anno_marker(
                idx_char,
                char,
                lt_textline._objs,  # pylint: disable=protected-access # access needed
                annos_line[idx_anno],
                anno_flags,
            )
            if anno_flags['anno_start_idx'] is not None and anno_flags['anno_stop_idx'] is not None:
                # chars are in the anno-rectangle
                # using "not None" is because the index can be 0
                if anno_complete:
                    # the complete anno-rectangle is found and anno_flags are set to None again when linked chars are
                    # rendered with success
                    link = render_link(anno_flags, annos_line[idx_anno], char_counter)
                    links.append(link)
                    idx_anno += 1
                else:
                    # still look for the real last char in the anno-rectangle
                    pass
            else:
                # the char is not in any anno-rectangles
                pass
        else:
            # the char is not in any anno-rectangles
            pass

    return links


def first_last_char_in_anno_marker(  # pylint: disable=too-many-branches # better readability
    idx_char: int,
    char: Union[LTChar, LTAnno],
    ltobjs_in_lttextline: List[Union[LTChar, LTAnno]],
    anno: Dict,
    anno_flags: Dict,
) -> bool:
    """
    Find the indices of the first and the last char in an anno-rectangle from a textline.

    :param idx_char: the index of a char in a textline
    :param char: metadata of a char
    :param ltobjs_in_lttextline: a list of LT objects in a LTTextline
    :param anno: metadata of a anno-rectangle
    :param anno_flags: the indices of start and the last char in an anno-rectangle from in the context of a textline
    :return: True means the a complete anno-rectangle is found, vice versa.
    """
    anno_complete = None
    # only check horizontal boundary.
    # As it is already a horizontal line, the vertical margin of each char in the textline is
    # presumably more and less the same.
    if isinstance(char, LTChar):
        if char.x0 > anno['rect'][0] - ANNO_X_TOLERANCE and char.x1 < anno['rect'][2] + ANNO_X_TOLERANCE:
            # a char is in an anno-rectangle
            if anno_flags['anno_start_idx'] is None:
                # the first character of an anno.
                anno_flags['anno_start_idx'] = idx_char

            # the original index of a end char plus 1 is more intuitive for the string slicing in python
            anno_flags['anno_stop_idx'] = idx_char + 1

            if idx_char == len(ltobjs_in_lttextline) - 1:
                # the last char of the textline
                anno_complete = True
            elif isinstance(ltobjs_in_lttextline[idx_char + 1], LTChar):
                if ltobjs_in_lttextline[idx_char + 1].x0 > anno['rect'][2]:
                    # the next char is outside of the current anno-rectangle
                    anno_complete = True
            else:
                # if the next char is LTAnno then do nothing
                pass
        else:
            # the incoming char is outside the anno-rectangle
            pass

    else:
        # the char is LTAnno
        if idx_char == len(ltobjs_in_lttextline) - 1:
            # the last char of the textline
            anno_complete = True
        elif isinstance(ltobjs_in_lttextline[idx_char + 1], LTChar):
            if ltobjs_in_lttextline[idx_char + 1].x0 > anno['rect'][2]:
                # the next char is outside of the current anno-rectangle
                anno_complete = True
        else:
            raise ValueError('two LTAnno occurs in a row')

    return anno_complete


def render_link(anno_flags: Dict, anno: Dict, char_counter: int) -> Link:
    """
    Render a single Link.

    :param anno_flags: a dict in which the start and end chars are indexed
    :param anno: a single annotation in PDF catalog, which belongs to the link source founded
    :param char_counter: In the end of the process, all chars in the scope of a textbox is a char array, this variable
                        is used to index the start and end chars in the textbox
    :return: a single Link instantiated
    """
    start_idx = anno_flags['anno_start_idx'] + char_counter

    if anno_flags['anno_start_idx'] == anno_flags['anno_stop_idx']:
        #  the annotation contains only one character
        stop_idx = start_idx
    else:
        stop_idx = anno_flags['anno_stop_idx'] + char_counter

    # get the position of the jump target
    if 'des_name' in anno:
        # implicit target which means name destination catalog does not exist in this PDF
        if catalog['dests'] and anno['des_name'] in catalog['dests']:
            pos_target = {
                'page': catalog['dests'][anno['des_name']]['Num'],
                'x': catalog['dests'][anno['des_name']]['X'],
                'y': catalog['dests'][anno['des_name']]['Y'],
            }
        else:
            pos_target = {'page': anno['dest']['page'], 'x': anno['dest']['rect_X'], 'y': anno['dest']['rect_Y']}
    else:
        pos_target = {'page': anno['dest']['page'], 'x': anno['dest']['rect_X'], 'y': anno['dest']['rect_Y']}

    link = Link(start_idx, stop_idx, pos_target)

    # reset the start and end indices of the annotation
    anno_flags['anno_start_idx'] = None
    anno_flags['anno_stop_idx'] = None

    return link


def _flatten_outline(nested_outline, flatten_outline: List):
    """
    Flat a nested outline for the further process in chapters detection.

    A flatten outline provides a easier way to search through itself than a nested one.

    :param nested_outline: a list of nested chapters from outline catalog
    :param flatten_outline: a list of flatten chapters from outline catalog, which is the result of this function
    :return:
    """
    for chapter in nested_outline:
        flatten_outline.append(chapter)
        if chapter['content']:
            _flatten_outline(chapter['content'], flatten_outline)


def remove_textboxes_in_tables_figures(
    page_textboxes: Dict[int, List[LTTextBox]],
    figure_list: List[Figure],
    table_list: List[Table],
):
    """
    Remove textboxes in the coverage of tables or figures from page_textboxes.

    The table and figure lists will be merged first by pages. Afterwards, it filters the textboxes inside tables or
    figures.

    :param page_textboxes:
    :param figure_list:
    :param table_list:
    :return:
    """
    page_textboxes_filter = {}
    for page_index, textboxes in page_textboxes.items():
        figures_tables_list = tables_figures_merge(figure_list, table_list, page_index)
        if figures_tables_list is not None:  # figures or tables exists in the current page
            for element in figures_tables_list:
                # The textbox inside the elements will be filtered out. It return only the boxes outside the elements.
                # Elements here can be tables or figures
                textboxes = list(
                    filter(
                        lambda x, ele=element: x.x0 < (ele.position.x0 - TABLE_MARGIN)  # left
                        or x.x1 > (ele.position.x1 + TABLE_MARGIN)  # right
                        or x.y0 < (ele.position.y0 - TABLE_MARGIN)  # bottom
                        or x.y1 > (ele.position.y1 + TABLE_MARGIN),  # top
                        textboxes,
                    ),
                )

        page_textboxes_filter[page_index] = textboxes

    return page_textboxes_filter


def tables_figures_merge(
    figure_list: List[Figure],
    table_list: List[Table],
    page_index: int,
) -> List[Union[Figure, Table]]:
    """
    Merge tables and figures in the same page.

    Here the return list can be consider a element list which includes tables
    and figures

    :param figure_list: A list of all figures extracted from the pages in this pdf
    :param table_list: A list of all tables extracted from the pages in this pdf
    :param page_index: index of current page number
    :return:
    """
    filter_list_table = list(filter(lambda x: x.position.page.number == page_index + 1, table_list))
    filter_list_figure = list(filter(lambda x: x.position.page.number == page_index + 1, figure_list))
    merge_list: List[Union[Figure, Table]] = filter_list_table + filter_list_figure
    if merge_list:
        merge_list.sort(key=lambda x: x.position.y0, reverse=True)

    return merge_list


def pdfminer_get_textboxes(pdf) -> Dict[int, List[LTTextBox]]:
    """
    Layout analysis done by pdfminer.

    The PDF does not need to be parsed again because pdf.doc contains objects of pdfminer.pdfdocument.PDFdocument.
    Just pdfminer page instance have to be created to run the layout processing because pdfplumber.page.Page class
    deviates from pdfminer.pdfpage.PDFPage class.

    :param pdf: instance of pdfplumber.pdf.PDF class
    :return: dictionary mapping page numbers (0-based) to a list of LTTextBox objects
    """
    LOG.info('Extracting layout ...')
    page_textboxes = {}

    for idx_page, page in enumerate(
        tqdm(
            pdf.pages,
            total=len(pdf.pages),
            desc='###### Extracting layout',
            unit='pages',
            bar_format=bar_format_lvl2(),
            leave=False,
        ),
    ):
        if logging_needed(idx_page, len(pdf.pages)):
            LOG.debug('Extracting layout page %s of %s', idx_page + 1, len(pdf.pages))

        pdf.interpreter.process_page(page.page_obj)
        result = pdf.device.get_result()
        textboxes = [obj for obj in result if isinstance(obj, LTTextBox)]
        # remove detected header and footer textboxes based on given page crop margin parameter
        filter_textboxes = list(
            filter(
                lambda textbox: textbox.y1 < (float(pdf.pages[0].height) - parameters.PAGE_CROP_MARGINS['top'])
                and textbox.y0 > parameters.PAGE_CROP_MARGINS['bottom']
                and textbox.x0 > parameters.PAGE_CROP_MARGINS['left']
                and textbox.x1 < (float(pdf.pages[0].width) - parameters.PAGE_CROP_MARGINS['right']),
                textboxes,
            ),
        )
        page_textboxes[page.page_number - 1] = filter_textboxes

    return page_textboxes
