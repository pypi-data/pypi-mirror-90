import itertools
from operator import itemgetter
from collections import Counter
from pdf2txt.core.token import Token
import numpy as np
import pandas as pd
from . import utils
from pdf2txt.settings import DEFAULT_X_TOLERANCE, DEFAULT_Y_TOLERANCE
from itertools import chain, zip_longest
from .exceptions import (
    TableExtractionError,
    NoTokenFoundError,
    MultipleTokensFoundError,
    InvalidTableError,
    InvalidTableHeaderError,
)
from copy import deepcopy

DEFAULT_SNAP_TOLERANCE = 3
DEFAULT_JOIN_TOLERANCE = 3
DEFAULT_MIN_WORDS_VERTICAL = 3
DEFAULT_MIN_WORDS_HORIZONTAL = 3

from copy import copy





class Table(object):
    def __init__(self, page, textlines=None, rect=None, settings={}):

        if textlines==None and rect==None:
            raise Exception("Incomplete infromation for the table. You should give either a list of tokens or a bounding box coordinates")
        self.page = page
        self.settings = dict(DEFAULT_TABLE_SETTINGS)
        self.settings.update(settings)
        if textlines:
            self.textlines=textlines
            self.settings["edge_min_length"]=max(l[-1].right-l[0].left for l in self.textlines)
        # else:
        #     self.textlines=utils.get_widthin_BoundingBox(page.tokens, rect)
        self._data = []
        self.df=None

        self._nb_headers=1
        self.get_edges()

    @property
    def bbox(self):
        return utils.BoundingBox(
        left=min(map(itemgetter(0), self._data)),
        top=min(map(itemgetter(1), self._data)),
        right=max(map(itemgetter(2), self._data)),
        bittom=max(map(itemgetter(3), self._data))
    )
    def vertically_in_line_with(self, token, linelist, tolerance: float = 0.0):


            tolerance = min(token.width / 2, tolerance)
            bounding_box = utils.BoundingBox(
                left=token.left - tolerance,
                right=token.right + tolerance,
                top=self.page.top,
                bottom=self.page.bottom,
            )
            results = set()

            for line in linelist:
                for tok in line:
                    if tok.partially_within(bounding_box):
                        results.add(tok)
            return frozenset(results)


    def get_edges(self):

        v = utils.filter_edges(self.page.edges, "v")

        h = utils.filter_edges(self.page.edges, "h")

        left_right = utils.cluster_objects_multi(h, "left", "right", 1)

        if left_right:
            h = max(left_right, key=lambda x: len(x))

        if len(utils.get_partially_overlapping_objects(utils.get_BoundingBox_from_objects([t for line in self.textlines for t in line]), h))>2:
            self._edges_h =  sorted(h, key=lambda e: e.top)

        else:
            self._edges_h=[]


        self._edges_v =  v

    def horizontally_in_line(self, row, rows):

        if len(rows) == 0:
            return None

        bounding_box = utils.BoundingBox(
            left=self.page.left,
            right=self.page.right,
            top=row[0].top,
            bottom=row[0].bottom,
        )

        for r in rows:
            for token in list(r):
                if token.partially_within(bounding_box):
                    return r
        return None


    def horizontally_within_lines(self, line_bottom, line_top):


        bounding_box = utils.BoundingBox(
            left=self.page.left,
            right=self.page.right,
            top=line_top.top,
            bottom=line_bottom.bottom,
        )



        ll= [line for line in self.textlines if line[0].within(bounding_box)]



        return ll


    def extract(self):

        if 2<len(self._edges_h)<=1.6*len(self.textlines):
            return self.extract_from_lines()
        return self.extract_from_text()

    def extract_from_text(self):
        """
        Returns tokens structured as a table.

        Given an TokenList, tries to extract a structured table by examining which
        tokens are aligned. There must be a clear gap between each row and between each
        column which contains no tokens, and a single cell cannot contain multiple
        tokens.

        If you fail to satisfy any of the other conditions listed above, that case is not
        yet supported.

        Returns:
            list[list]: a list of rows, which are lists of PDFTokens or strings
                (depending on the value of as_text).
        """
        rows = set()
        cols = set()

        for row in self.textlines:

            r=self.horizontally_in_line(row, rows)
            if r:
                rows.remove(r)
                r=list(r)
                r.extend(row)
                rows.add(frozenset(r))
            else:
                rows.add(frozenset(row))
            for token in row:
                col = self.vertically_in_line_with(
                    token, self.textlines, tolerance=0
                )
                col_exists=False
 #               for c in cols:
 #                   if bool(c & col):
 #                       col_exists=True
 #                       break
                if not col_exists:
                    cols.add(col)

        # Check no line is in multiple rows or columns
        self._fix_rows(rows, self.textlines)
        cols=self._fix_cols(cols, self.textlines)

        if sum([len(row) for row in rows]) != len(list(chain.from_iterable(rows))):
            raise TableExtractionError(
                "An line is in multiple rows. If this is expected, you can try passing "
                "fix_token_in_multiple_rows=True"
            )
        if sum([len(col) for col in cols]) != len(list(chain.from_iterable(cols))):
            raise TableExtractionError(
                "An line is in multiple columns. If this is expected, you can try "
                "passing fix_token_in_multiple_cols=True"
            )

        sorted_rows = sorted(
            rows,
            key=lambda row: (
    #            row[0].page_number,
                max((elem.top) for elem in row),
            ),
        )
        sorted_cols = sorted(
            cols, key=lambda col: max(elem.left for elem in col)
        )
        self._data=[]
        for row in sorted_rows:
            table_row = []
            for col in sorted_cols:
                try:
                    line = row.intersection(col)
                except NoTokenFoundError:
                    line = None
                except MultipleTokensFoundError as err:
                    raise TableExtractionError(
                        "Multiple tokens appear to be in the place of one cell in the "
                        "table. It could be worth trying to add a tolerance."
                    ) from err
                table_row.append(line)
            self._data.append([r for r in table_row])

        #        self._validate_table_shape()
        return self

    def extract_from_lines(self):
        bbox = utils.get_BoundingBox_from_objects(self._edges_h)
        if self.textlines is not None and self._edges_h[0].top > self.textlines[0][0].top:
            bbox.top-=(self._edges_h[1].top-self._edges_h[0].top)+4
        self.textlines = [line for line in self.page.text_lines if utils.has_overlap_with_bbox(line[0], bbox)]
        if self.textlines == []:
            return self

        ncols = Counter([len(line) for line in self.textlines]).most_common(1)[0][0]

        for i in range(0, len(self.textlines)):
            if len(self.textlines[i]) != ncols:
                words = [w for token in self.textlines[i] for w in token.original_words]
                if len(words) == ncols:
                    line = [Token(w, self.textlines[i][0].page) for w in words]
                    self.textlines[i] = line

        rows = []
        cols = set()
        z=zip(self._edges_h[1:], self._edges_h[:-1])
        for i, (b, t) in enumerate(z):
            if i == 0:
                if self._edges_h[0].top < self.textlines[0][0].top:
                    header=self.horizontally_within_lines(b, t)
                    rows.extend(self._fix_header_rows(header))
                else:

                    header=[tl for tl in self.textlines if tl[0].top<self._edges_h[0].top]

                    rows.extend(self._fix_header_rows(header))
                    rows.append([item for sublist in self.horizontally_within_lines(b, t) for item in sublist])
            else:
                row=[item for sublist in self.horizontally_within_lines(b, t) for item in sublist]
                if row:
                    rows.append(row)

        for row in rows:
            for token in row:
                col = self.vertically_in_line_with(
                    token, rows, tolerance=0
                )
                col_exists = False
                for c in cols:
                    if bool(c & col):
                        col_exists = True
                        break
                if not col_exists:
                    cols.add(col)
        # Check no line is in multiple rows or columns
        rows=[r for r in rows if r]
        self._fix_rows(rows, rows)
        cols = self._fix_cols(cols, rows)

        sorted_rows = sorted(
            rows,
            key=lambda row: (
                #            row[0].page_number,
                max((elem.top) for elem in row),
            ),
        )
        sorted_cols = sorted(cols, key=lambda col: max(elem.left for elem in col))
        self._data = []
        for row in sorted_rows:
            table_row = []
            row = set(row)
            for col in sorted_cols:
                try:
                    line = row.intersection(col)
                except NoTokenFoundError:
                    line = None
                except MultipleTokensFoundError as err:
                    raise TableExtractionError(
                        "Multiple tokens appear to be in the place of one cell in the "
                        "table. It could be worth trying to add a tolerance."
                    ) from err
                table_row.append(sorted(line, key=lambda x: x.left))
            self._data.append([r for r in table_row])

        return self

    def _validate_table_shape(self):
        """
        Checks that all rows (and therefore all columns) are the same length.
        """
        if len(self._data) < 1:
            return
        first_row_len = len(self._data[0])
        for idx, row in enumerate(self._data[1:]):
            if not len(row) == first_row_len:
                raise InvalidTableError(
                    f"Table not rectangular, row 0 has {first_row_len} tokens but row "
                    f"{idx + 1} has {len(row)}."
                )

    def _fix_rows(self, rows, pdflines) -> None:
        """
        Sometimes a token may span over multiple rows. For example:
        ---------
        | A | B |
        ----|   |
        | C |   |
        ---------
        In this, case, when extract_table scans for token in line with A it will pick up
        A and B. When it scans B it will get A, B and C, and when it scans C it will get B
        and C. This results in three distinct rows, AB, ABC, BC. This function will fix
        this by putting any merged cells into the top row, resulting in one row AB and the
        other with just C.

        To do this, we check which token is in multiple rows, get which rows it is in,
        and then remove it from the lower rows. This should fix the problem. It can result
        in empty rows (since in my example we begin with 3 'rows' when there are only
        really 2), but these can simply be removed.
        """

        sorted_rows = sorted(
            rows,
            key=lambda row: (max(-(elem.right) for elem in row)) )

    #    sorted_rows = [row for row in sorted_rows if not all(utils.get_type(token.Text) == 'Literal' for token in row)]
        for line in pdflines:
            for token in line:
                num_rows = sum(token in row for row in rows)
                if num_rows == 1:
                    continue
                # If we reach here, we've found an token in multiple rows.

                rows_with_token = [row for row in rows if token in row]
                sorted_rows_with_token = sorted(
                    rows_with_token, key=lambda row: sorted_rows.index(row)
                )
                # Remove the token from all but the first row.
                for row in sorted_rows_with_token[1:]:
                    rows.remove(row)
                    new_row = row.remove(token)
                    if new_row:
                        rows.add(new_row)
                        # Update sorted rows
                        sorted_rows = [
                            new_row if some_row == row else some_row for some_row in sorted_rows
                        ]
                    else:
                        sorted_rows.remove(row)




    def _fix_cols(self, cols, tokenlines) -> None:
        """
        The same as _fix_rows, but when an token is in multiple columns, for example
        ---------
        | A | B |
        --------|
        |   C   |
        ---------
        """

 #       if sum([len(col) for col in cols]) == len(set(list(chain.from_iterable(cols)))):
            # No tokens are in multiple cols, return.
 #           return cols

        # We sort by looking at all the tokens and choosing the token which starts
        # most to the right. The ones with tokens which start most to the right
        # will be later on in the sorted list.

        cols = list(cols)

        sorted_columns = sorted(
            cols, key=lambda col: max(elem.left for elem in col)
        )
        for line in tokenlines:
            for token in line:
                num_cols = sum(token in list(col) for col in cols)
                if num_cols == 1:
                    continue
                # If we reach here, we've found an token in multiple cols.

                cols_with_token = [col for col in cols if line in list(col)]
                sorted_cols_with_token = sorted(
                    cols_with_token, key=lambda col: sorted_columns.index(col)
                )
                # Remove the token from all but the first col.
                for col in sorted_cols_with_token[1:]:
                    cols.remove(col)
                    new_col = list(col).remove(token)
                    new_col = col
                    if new_col:
                        set(cols).add(new_col)
                        cols = list(cols)
                        # Update sorted columns
                        sorted_columns = [
                            new_col if some_col == col else some_col
                            for some_col in sorted_columns
                        ]
                    else:
                        sorted_columns.remove(col)
        return cols

    def _fix_header_rows(self, header, tolerance=5):
        """
        First row in a table my contain several sub rows that  typically span multiple columns
        -------------------------
        | A                     |
        ------------------------|
        | B | C | D | E | F | G |
        -------------------------
        """

        if not isinstance(header[0], list):
            return header
        if len(header)==1:
            return header

        header2=[]

        header2.append([Token.copy(h) for h in header[-1]])
        #if the first row is right justified than the first row is not a header row otherwise it is considered as header row
        for i in reversed(range(1 , len(header))):
            next_row_used=False
            for token in header[i-1]:
                if token.left-tolerance> min(t.left for t in header[i]) or len(header[i-1])==len(header2[-1]): # not left justified or as many header as the last row
                    for t in header[i-1]:
                        for j in range(0, len(header2[-1])):
                            if t.left+tolerance>=header2[-1][j].left and t.right-tolerance <=header2[-1][j].right:
                                t_c=Token.copy(t)
                                header2[-1][j]=t_c.combine(header2[-1][j])
                                next_row_used=True
                    break
                else:
                    break
            if not next_row_used:
                h2=[]
                for t in  range(0, len(header[i-1])-1):
                    for h in header2[-1]:
                        if h.right<header[i-1][t+1].left:
                            h_item= Token.copy(header[i-1][t])

                            h_item.left=h.left
                            h_item.right=h.right
                            h2.append(h_item)
                for h in header2[-1]:
                    if h.left >= header[i-1][-1].left:
                        h_item = Token.copy(header[i - 1][-1])

                        h_item.left = h.left
                        h_item.right = h.right
                        h2.append(h_item)

                header2.insert(0,h2)
        self._nb_headers=len(header2)
        return header2

    def __repr__(self):
        return f"<{self.__class__.__name__} shape={self.shape}>"

    def __lt__(self, other):
        if self.page == other.page:
            if self.order < other.order:
                return True
        if self.page < other.page:
            return True
    @property
    def shape(self):
        if len(self._data)==0:
            return (0,0)
        return (len(self. data), len(self._data[0]) if len(self._data[0]) else 0)

    @property
    def data(self):
        """Returns two-dimensional list of strings in table.
        """
        d = []
        for row in self._data:
            d.append([' '.join([c.Text for c in cell]) for cell in row])
        return d

    def to_pandas(self):

        if self.df is None:
            self.df=pd.DataFrame(self.data)



        if not self.df.empty and len(self.df.index)>2:
            if self._nb_headers==1:
                headers = self.df.iloc[0]

                self.df = pd.DataFrame(self.df.values[1:], columns=headers)
            else:
                tuple_index = [(i, *j) for i, *j in zip(*self.data[0:self._nb_headers])]

                pd.MultiIndex.from_tuples(tuple_index)
                self.df = pd.DataFrame(self.data[self._nb_headers:])
                self.df.columns = pd.MultiIndex.from_tuples(tuple_index)

        self.df.iloc[:,0].replace("", np.NaN, inplace=True)
        self.df.iloc[:,0].fillna(method='ffill', inplace=True)
        return self.df

    def to_text(self):
        if self.df is not None:
            return self.df.to_string()
        else:
            ""

    def to_json(self, path, **kwargs):
        """Writes Table to a JSON file.
        For kwargs, check :meth:`pandas.DataFrame.to_json`.
        Parameters
        ----------
        path : str
            Output filepath.
        """
        kw = {"orient": "records"}
        kw.update(kwargs)
        json_string = self.df.to_json(**kw)
        with open(path, "w") as f:
            f.write(json_string)

    def to_excel(self, path, **kwargs):
        """Writes Table to an Excel file.
        For kwargs, check :meth:`pandas.DataFrame.to_excel`.
        Parameters
        ----------
        path : str
            Output filepath.
        """
        kw = {
            "sheet_name": f"page-{self.page}-table-{self.order}",
            "encoding": "utf-8",
        }
        kw.update(kwargs)
        writer = pd.ExcelWriter(path)
        self.df.to_excel(writer, **kw)
        writer.save()

    def to_html(self, path, **kwargs):
        """Writes Table to an HTML file.
        For kwargs, check :meth:`pandas.DataFrame.to_html`.
        Parameters
        ----------
        path : str
            Output filepath.
        """
        html_string = self.df.to_html(**kwargs)
        with open(path, "w") as f:
            f.write(html_string)

class CellGroup(object):
    def __init__(self, cells):
        self.cells = cells
        self.bbox = (
            min(map(itemgetter(0), filter(None, cells))),
            min(map(itemgetter(1), filter(None, cells))),
            max(map(itemgetter(2), filter(None, cells))),
            max(map(itemgetter(3), filter(None, cells))),
        )


class Row(CellGroup):
    pass

class Table2(object):
    def __init__(self, page, cells):
        self.page = page
        self.cells = cells
        self.bbox = (
            min(map(itemgetter(0), cells)),
            min(map(itemgetter(1), cells)),
            max(map(itemgetter(2), cells)),
            max(map(itemgetter(3), cells)),
        )

    @property
    def rows(self):
        _sorted = sorted(self.cells, key=itemgetter(1, 0))
        xs = list(sorted(set(map(itemgetter(0), self.cells))))
        rows = []
        for y, row_cells in itertools.groupby(_sorted, itemgetter(1)):
            xdict = dict((cell[0], cell) for cell in row_cells)
            row = Row([xdict.get(x) for x in xs])
            rows.append(row)
        return rows

    def extract(
        self,
        x_tolerance=DEFAULT_X_TOLERANCE,
        y_tolerance=DEFAULT_Y_TOLERANCE,
    ):

        chars = self.page.chars
        table_arr = []

        def char_in_bbox(char, bbox):
            v_mid = (char["top"] + char["bottom"]) / 2
            h_mid = (char["x0"] + char["x1"]) / 2
            x0, top, x1, bottom = bbox
            return (
                (h_mid >= x0) and (h_mid < x1) and (v_mid >= top) and (v_mid < bottom)
            )

        for row in self.rows:
            arr = []
            row_chars = [char for char in chars if char_in_bbox(char, row.bbox)]

            for cell in row.cells:
                if cell is None:
                    cell_text = None
                else:
                    cell_chars = [
                        char for char in row_chars if char_in_bbox(char, cell)
                    ]

                    if len(cell_chars):
                        cell_text = utils.extract_text(
                            cell_chars, x_tolerance=x_tolerance, y_tolerance=y_tolerance
                        ).strip()
                    else:
                        cell_text = ""
                arr.append(cell_text)
            table_arr.append(arr)

        return table_arr



TABLE_STRATEGIES = ["lines", "lines_strict", "text", "explicit"]
DEFAULT_TABLE_SETTINGS = {

    "edge_min_length": 3,
    "y_tolerance": 1,
    "min_words_vertical": DEFAULT_MIN_WORDS_VERTICAL,
    "min_words_horizontal": DEFAULT_MIN_WORDS_HORIZONTAL,
    "intersection_tolerance": 3,
    "intersection_x_tolerance": 3,
    "intersection_y_tolerance": 3,
}


class TableFinder(object):
    """
    Given a PDF page, find plausible table structures.
    """

    def __init__(self, page, settings={}):
        for k in settings.keys():
            if k not in DEFAULT_TABLE_SETTINGS:
                raise ValueError(f"Unrecognized table setting: '{k}'")
        self.page = page
        self.settings = dict(DEFAULT_TABLE_SETTINGS)
        self.settings.update(settings)


    def find_tables(self):
        table_areas=self.guess_tables()
        for table_area in table_areas:
            text_tokens=utils.get_widthin_BoundingBox( self.page.tokens, table_area)
            line_clusters = utils.cluster_objects(text_tokens, "bottom", self.settings["y_tolerance"])

            if line_clusters is not None:
                text_lines = [line for line in line_clusters]
            else:
                text_lines=[]

            table=Table(self.page, text_lines)
            yield table

    def words_to_edges_h(self, word_threshold=DEFAULT_MIN_WORDS_HORIZONTAL):
        """
        Find (imaginary) horizontal lines that connect the tops
        of at least `word_threshold` words.
        """
        by_top = utils.cluster_objects(self.page.tokens, "bottom", 0.5)
        if by_top is None:
            return []
        large_clusters = list(filter(lambda x: len(x) >= word_threshold, by_top))
        rects = list(map(utils.get_BoundingBox_from_objects, large_clusters))
        if len(rects) == 0:
            return []
        edges = [
            {
                "left": r.left,
                "right": r.right,
                "top": r.bottom,
                "bottom": r.bottom,
                "width": r.right - r.left,
                "orientation": "h",
            }
            for r in rects
        ]

        return [utils.BoundingBox(**e) for e in edges]

    def guess_tables(self):
        horizontal_lines = [line for line in self.page.horizontal_lines if line.width < self.page.root_page.content_width * 0.95]
        all_tables=self._guess_tables_from_rectangles()
        if len(horizontal_lines)>=2:
            tables=self._guess_tables_from_lines(horizontal_lines)
            for table in tables:
                if not utils.is_ovarlaping_with_objects(table, all_tables):
                    all_tables.append(table)

        tables=self._guess_tables_from_lines(self.guess_table_lines())
        for table in tables:
            if not utils.is_ovarlaping_with_objects(table, all_tables):
                all_tables.append(table)

        return all_tables

    def snap_edges(self, edges, tolerance=DEFAULT_SNAP_TOLERANCE):
        """
        Given a list of edges, snap any within `tolerance` pixels of one another
        to their positional average.
        """
        v, h = [list(filter(lambda x: x.orientation == o, edges)) for o in ("v", "h")]

        snap = utils.snap_objects
        snapped = snap(v, "left", tolerance) + snap(h, "top", tolerance)
        return snapped

    def join_edge_group(self, edges, orientation, tolerance=DEFAULT_JOIN_TOLERANCE):
        """
        Given a list of edges along the same infinite line, join those that
        are within `tolerance` pixels of one another.
        """
        if orientation == "h":
            min_prop, max_prop = "left", "right"
        elif orientation == "v":
            min_prop, max_prop = "top", "bottom"
        else:
            raise ValueError("Orientation must be 'v' or 'h'")

        sorted_edges = list(sorted(edges, key=lambda e: getattr(e,min_prop)))
        joined = [sorted_edges[0]]
        for e in sorted_edges[1:]:
            last = joined[-1]
            if getattr(e,min_prop) <= (getattr(last, max_prop) + tolerance):
                if getattr(e, max_prop) > getattr(last,max_prop):
                    # Extend current edge to new extremity
                    joined[-1] = utils.resize_object(last, max_prop, getattr(e,max_prop))
            else:
                # Edge is separate from previous edges
                joined.append(e)

        return joined


    def merge_edges(self, edges, snap_tolerance, join_tolerance):
        """
        Using the `snap_edges` and `join_edge_group` methods above,
        merge a list of edges into a more "seamless" list.
        """

        def get_group(edge):
            if edge.orientation == "h":
                return ("h", edge.top)
            else:
                return ("v", edge.left)

        if snap_tolerance > 0:
            edges = self.snap_edges(edges, snap_tolerance)

        if join_tolerance > 0:
            _sorted = sorted(edges, key=get_group)
            edge_groups = itertools.groupby(_sorted, key=get_group)
            edge_gen = (
                self.join_edge_group(items, k[0], join_tolerance) for k, items in edge_groups
            )
            edges = list(itertools.chain(*edge_gen))
        return edges

    def _guess_tables_from_rectangles(self,  threshold=2):
        rects=[rect for rect in self.page.rects if rect.width>rect.height and rect.height>2]
        left_right = utils.cluster_objects_multi(rects, "left", "right", 0.5)
        if left_right is not None:
            left_right = list(filter(lambda x: len(x) >= threshold, left_right))
        if left_right is None:
            return []

        groups=[]
        for group in left_right:
            sorted(group, key=lambda g: g.top)
            new_group=[group[0]]
            for i in range(0, len(group)-1):
                if np.isclose(group[i].bottom, group[i+1].top, atol=0.1) or  np.isclose(group[i].top, group[i+1].top, atol=0.1):
                    new_group.append(group[i+1])
                else:
                    groups.append(new_group)
                    new_group=[group[i+1]]
            if new_group:
                groups.append(new_group)
        return [utils.get_BoundingBox_from_objects(g) for g in groups if len(g)>=threshold]

    def _guess_tables_from_lines(self, lines, threshold=3):
        min_row_height=40

        left_right = utils.cluster_objects_multi(lines, "left", "right", 0.5)

        if left_right is not None:
            left_right = list(filter(lambda x: len(x) >= threshold, left_right))
        if left_right is None:
            return []
        tables=[]
        for group in left_right:
            group=sorted(group, key=lambda x: x.bottom)
            for i  in range(0, len(group)-1):
                group[i].space_bellow=group[i+1].bottom-group[i].bottom
            group[-1].space_bellow=group[-2].space_bellow


            i=0
            while i<len(group):
                line = group[i]
                if line.space_bellow<=min_row_height:
                    subgroup = [line]
                else:
                    subgroup=[]
                i+=1
                while i < len(group) and np.isclose(line.space_bellow, group[i].space_bellow, atol=2):
                    if group[i].space_bellow<=min_row_height:
                        subgroup.append(group[i])
                    line=group[i]
                    i+=1
                if i < len(group):
                    if group[i].space_bellow <= min_row_height:
                        subgroup.append(group[i])
                    i+=1
                if len(subgroup)>1:
                    tables.append(utils.get_BoundingBox_from_objects(subgroup))

        return tables

    def guess_table_lines(self,token_threshold=3, pruning_cut_off=2):
        h_edges = self.words_to_edges_h(word_threshold=token_threshold)
        v_edges =self.words_to_edges_v(word_threshold=token_threshold)
        v_edges=[e for e in v_edges if e.left>self.page.root_page.left_margin+5]
        h_edges=[e for e in h_edges if not utils.is_ovarlaping_with_objects(e, self.page.graphs)]
        v_edges = [e for e in v_edges if not utils.is_ovarlaping_with_objects(e, self.page.graphs)]

        intersections = self.edges_to_intersections(v_edges + h_edges)

        previous_nb_intersections=0
        nb_intersections=len(intersections)

        while nb_intersections-previous_nb_intersections:
            edges_to_remove=[]
            for edge in h_edges:
                pts=self.get_intersections_for_edge(edge, intersections)
                if len(pts)<=pruning_cut_off:
                    edges_to_remove.append(edge)
                else:
                    edge.left=min([p[0] for p in pts])
                    edge.right=max([p[0] for p in pts])
            for edge in edges_to_remove:
                del h_edges[h_edges.index(edge)]

            edges_to_remove = []
            for edge in v_edges:
                pts=self.get_intersections_for_edge(edge, intersections)
                if len(pts)<=pruning_cut_off:
                    edges_to_remove.append(edge)
                else:
                    edge.top=min([p[1] for p in pts])
                    edge.bottom=max([p[1] for p in pts])

            for edge in edges_to_remove:
                del v_edges[v_edges.index(edge)]
            previous_nb_intersections=nb_intersections
            intersections = self.edges_to_intersections(v_edges + h_edges)
            nb_intersections=len(intersections)

        if nb_intersections==0:
            return []
        return h_edges

    def get_intersections_for_edge(self, edge, intersections):
        intersection_points = []
        for pt, edges in intersections.items():
            edge_v = edges['v'][0]
            edge_h = edges['h'][0]
            if edge == edge_h or edge == edge_v:
                intersection_points.append(pt)

        return intersection_points

    def words_to_edges_v(self, word_threshold=DEFAULT_MIN_WORDS_VERTICAL):
        """
        Find (imaginary) vertical lines that connect the left, right, or
        center of at least `word_threshold` words.
        """
        # Find words that share the same left, right, or centerpoints
        by_left = utils.cluster_objects(self.page.tokens, "left",  1)
        if by_left is None:
            by_left=[]
        else:
            by_left = list(filter(lambda x: len(x) >= word_threshold, by_left))
        by_right = utils.cluster_objects(self.page.tokens, "right", 1)
        if by_right is None:
            by_right=[]
        else:
            by_right = list(filter(lambda x: len(x) >= word_threshold, by_right))
    #    by_center = utils.cluster_objects(words, lambda x: (x.left + x.right) / 2,  0.5)
    #    by_center = list(filter(lambda x: len(x) >= word_threshold, by_center))


        by_left_copy = copy(by_left)
        by_right_copy = copy(by_right)

        for left in by_left:
            for right in by_right:
                inetersection = set(left).intersection(set(right))
                if len(inetersection) >= 2:
                    if len(set(right)) >= len(set(left)):
                        if left in by_left_copy:
                            by_left_copy.remove(left)
                    else:
                        if right in by_right_copy:
                            by_right_copy.remove(right)

        rects = list(map(utils.get_BoundingBox_from_objects, by_left_copy))

        edges = [
            {
                "left": r.left,
                "right": r.left,
                "top": r.top,
                "bottom": r.bottom,
                "height": r.bottom - r.top,
                "justification": "left",
                "orientation": "v",
            }
            for r in rects
        ]

        rects = list(map(utils.get_BoundingBox_from_objects, by_right_copy))

        edges = edges + [
            {
                "left": r.right,
                "right": r.right,
                "top": r.top,
                "bottom": r.bottom,
                "height": r.bottom - r.top,
                "justification": "right",
                "orientation": "v",
            }
            for r in rects
        ]
        # rects= list(map(utils.get_BoundingBox_from_objects, by_center))
        #
        # edges = edges + [
        #     {
        #         "left": (r.right+r.left)/2,
        #         "right": (r.right+r.left)/2,
        #         "top": r.top,
        #         "bottom": r.bottom,
        #         "height": r.bottom - r.top,
        #         "justification": "center",
        #         "orientation": "v",
        #     }
        #     for r in rects
        # ]

        return [utils.BoundingBox(**e) for e in edges]

    def edges_to_intersections(self, edges, x_tolerance=1, y_tolerance=1):
        """
        Given a list of edges, return the points at which they intersect
        within `tolerance` pixels.
        """
        intersections = {}
        v_edges, h_edges = [
            list(filter(lambda x: x.orientation == o, edges)) for o in ("v", "h")
        ]
        for v in sorted(v_edges, key=lambda e: (getattr(e, "left"), getattr(e, "top"))):
            for h in sorted(h_edges, key=lambda e: (getattr(e, "top"), getattr(e, "left"))):
                if (
                        (v.top <= (h.top + y_tolerance))
                        and (v.bottom >= (h.top - y_tolerance))
                        and (v.left >= (h.left - x_tolerance))
                        and (v.left <= (h.right + x_tolerance))
                ):
                    vertex = (v.left, h.top)
                    if vertex not in intersections:
                        intersections[vertex] = {"v": [], "h": []}
                    intersections[vertex]["v"].append(v)
                    intersections[vertex]["h"].append(h)
        return intersections

    def intersections_to_cells(self, intersections):
        """
        Given a list of points (`intersections`), return all rectangular "cells"
        that those points describe.

        `intersections` should be a dictionary with (x0, top) tuples as keys,
        and a list of edge objects as values. The edge objects should correspond
        to the edges that touch the intersection.
        """

        def edge_connects(p1, p2):
            def edges_to_set(edges):
                return set([(e.left, e.top, e.right, e.bottom) for e in edges])

            if p1[0] == p2[0]:
                common = edges_to_set(intersections[p1]["v"]).intersection(
                    edges_to_set(intersections[p2]["v"])
                )
                if len(common):
                    return True

            if p1[1] == p2[1]:
                common = edges_to_set(intersections[p1]["h"]).intersection(
                    edges_to_set(intersections[p2]["h"])
                )
                if len(common):
                    return True
            return False

        points = list(sorted(intersections.keys()))
        n_points = len(points)

        def find_smallest_cell(points, i):
            if i == n_points - 1:
                return None
            pt = points[i]
            rest = points[i + 1:]
            # Get all the points directly below and directly right
            below = [x for x in rest if x[0] == pt[0]]
            right = [x for x in rest if x[1] == pt[1]]
            for below_pt in below:
                if not edge_connects(pt, below_pt):
                    continue

                for right_pt in right:
                    if not edge_connects(pt, right_pt):
                        continue

                    bottom_right = (right_pt[0], below_pt[1])

                    if (
                            (bottom_right in intersections)
                            and edge_connects(bottom_right, right_pt)
                            and edge_connects(bottom_right, below_pt)
                    ):
                        return (pt[0], pt[1], bottom_right[0], bottom_right[1])

        cell_gen = (find_smallest_cell(points, i) for i in range(len(points)))
        return list(filter(None, cell_gen))

    def cells_to_tables(self, cells):
        """
        Given a list of bounding boxes (`cells`), return a list of tables that
        hold those cells most simply (and contiguously).
        """

        def bbox_to_corners(bbox):
            x0, top, x1, bottom = bbox
            return list(itertools.product((x0, x1), (top, bottom)))

        cells = [
            {"available": True, "bbox": bbox, "corners": bbox_to_corners(bbox)}
            for bbox in cells
        ]

        # Iterate through the cells found above, and assign them
        # to contiguous tables

        def init_new_table():
            return {"corners": set([]), "cells": []}

        def assign_cell(cell, table):
            table["corners"] = table["corners"].union(set(cell["corners"]))
            table["cells"].append(cell["bbox"])
            cell["available"] = False

        n_cells = len(cells)
        n_assigned = 0
        tables = []
        current_table = init_new_table()
        while True:
            initial_cell_count = len(current_table["cells"])
            for i, cell in enumerate(filter(itemgetter("available"), cells)):
                if len(current_table["cells"]) == 0:
                    assign_cell(cell, current_table)
                    n_assigned += 1
                else:
                    corner_count = sum(
                        c in current_table["corners"] for c in cell["corners"]
                    )
                    if corner_count > 0 and cell["available"]:
                        assign_cell(cell, current_table)
                        n_assigned += 1
            if n_assigned == n_cells:
                break
            if len(current_table["cells"]) == initial_cell_count:
                tables.append(current_table)
                current_table = init_new_table()

        if len(current_table["cells"]):
            tables.append(current_table)

        _sorted = sorted(tables, key=lambda t: min(t["corners"]))
        filtered = [t["cells"] for t in _sorted if len(t["cells"]) > 1]
        return filtered

    def get_edges(self):
        settings = self.settings

        v_base = utils.filter_edges(self.page._edges, "v")

        v_base_text = self.words_to_edges_v()

        v = v_base + v_base_text

        h_base = utils.filter_edges(self.page._edges, "h")
        h_base_text = self.words_to_edges_h()

        h = h_base + h_base_text

        edges = list(v) + list(h)

        if settings["snap_tolerance"] > 0 or settings["join_tolerance"] > 0:
            edges = self.merge_edges(
                edges,
                snap_tolerance=settings["snap_tolerance"],
                join_tolerance=settings["join_tolerance"],
            )
        return utils.filter_edges(edges, min_length=settings["edge_min_length"])
