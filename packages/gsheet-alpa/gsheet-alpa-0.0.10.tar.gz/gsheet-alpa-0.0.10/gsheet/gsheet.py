'''

GSheet

1. Set-up Google Sheet API based on this:

    https://towardsdatascience.com/google-sheets-pandas-dataframe-6b8666f9cf6

2. Best Google Sheet API python module:
    gspread

3. Add support for Pandas Dataframe
    gspread_dataframe

    pip install gspread_dataframe gspread oauth2client

References:
    https://towardsdatascience.com/google-sheets-pandas-dataframe-6b8666f9cf6
    https://gspread.readthedocs.io/en/latest/
    https://gspread.readthedocs.io/en/latest/user-guide.html#creating-a-spreadsheet
    https://pythonhosted.org/gspread-dataframe/
    https://stackoverflow.com/questions/45540827/appending-pandas-data-frame-to-google-spreadsheet

'''
from logging import getLogger, Formatter, StreamHandler, INFO, DEBUG
import re
import sys

from gspread import service_account, WorksheetNotFound
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_string_dtype


# Set-up Logging
logger = getLogger(__name__)
logger.setLevel(INFO)

ch = StreamHandler(sys.stdout)
ch.setLevel(INFO)

# create formatter and add it to the handlers
formatter = Formatter('%(asctime)s <%(module)s> %(funcName)s | %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)


DEFAULT_CREDENTIAL_FILE = ''
# Same as default Google Sheet size
DEFAULT_NUM_ROWS = "140"
DEFAULT_NUM_COLS = "26"


def cellname2rowcol(cellname: str) -> (int, int):
    """converts cellname to a row, column pair

    e.g.
        A1 -> 1, 1
        J10 -> 10, 10
    Note, only column A-Z are supported

    Parameters
    ----------
    cellname : str
        cellname in '[A-Z][0-9]+' format

    Returns
    -------
    int, int
        row and column number for a cell
        returns 0, 0 if cannot convert
    """
    cellname = cellname.upper()
    pat = re.compile("([A-Z]+)([0-9]+)")
    m = pat.match(cellname)
    if m:
        row = int(m.group(2))
        col_str = m.group(1)
        if len(col_str) == 1:
            # for now, only supports up to 26 columns
            col = ord(col_str) - ord('A') + 1
            return row, col
        else:
            logger.error(f"Column beyond 26th (Z) not supported: {col_str}")
    logger.error(f"Invalid cell: {cellname}")
    return (0, 0)

def rowcol2cellname(row: int, col:int) -> str:
    """converts row, col number to cellname

    col 1 to column 'A'

        1, 1 -> A1
        10, 10 -> J10

    Parameters
    ----------
    row, col : int
    col : int
        The row, col coordinate of a cell

    Returns
    -------
    str
        The cellname (e.g. 'A1', 'J10'). Returns None if cell invalid
    """
    if row < 1 or col < 1:
        logger.error(f"Negative row or column ({row}, {col})")
        return None
    if col > 26:
        logger.error(f"Column beyond 26 not supported: {col}")
        return None
    col_str = chr(ord('A') + col - 1)
    return col_str + str(row)

def relative_cell(cellname: str, row_delta: int, col_delta:int) -> str:
    '''gets the cell name of the cell relative to an original cell

    Parameters
    ----------
    cellname : str
        name of cell (e.g. 'A1')
    row_delta, col_delta : int
        row and column offset.  Supports negative offset
    Returns
    -------
    str
        name of cell (e.g. 'A1'), None if offset leads to negative row/column
        value

    e.g.
        'A1', 1, 1 -> 'B2'
        'J5', 1, 0 -> 'J4'
    '''
    current_row, current_col = cellname2rowcol(cellname)
    new_row = current_row + row_delta
    new_col = current_col + col_delta
    return rowcol2cellname(new_row, new_col)

def add_summation_row(df):
    '''
    add a summation row to the df for all columns which are 'numeric'.
    '''
    rows, cols = df.shape
    to_append = []
    #for j in range(0, cols):
    for col in df.columns:
        if is_numeric_dtype(df[col]):
            #to_append.append(0.0)
            to_append.append('=sum(indirect("R[-{}]C[0]:R[-1]C[0]", false))'.format(rows))
        else:
            to_append.append("")
    a_series = pd.Series(to_append, index = df.columns)
    return  df.append(a_series, ignore_index=True)

class GoogleSheet():
    def __init__(self, sheet_id, credentials_file=DEFAULT_CREDENTIAL_FILE):
        self._gc = service_account(filename=credentials_file)
        self._sh = self._gc.open_by_key(sheet_id)
        self._all_values = {}

    @property
    def gc(self):
        return self._gc

    @property
    def sh(self):
        return self._sh

    def worksheet(self, id=0, title=None):
        '''
        return the worksheet with by title.
        '''
        if title is None:
            # returns the first worksheet
            try:
                return self._sh.get_worksheet(id)
            except WorksheetNotFound:
                return None
        else:
            try:
                return self._sh.worksheet(title)
            except WorksheetNotFound:
                return None

    def worksheets(self):
        '''
        returns the list of worksheets within a workbook
        Returns
        -------
            list : of gspread.models.Worksheet
        '''
        return self._sh.worksheets()


    def worksheet_titles(self):
        titles = []
        all_worksheets = self.worksheets()
        for wks in all_worksheets:
            titles.append(wks.title)

    def read_as_df(self, sheet_name):
        df = get_as_dataframe(self.worksheet(title=sheet_name))
        return df.dropna(axis=0, how='all').dropna(axis=1, how='all')

    def write_df(self, sheet_name, df, anchor_cell=None, row_col=None, include_index=False, include_column_header=True,
            append_summation_row=False):
        if anchor_cell:
            start_row, start_col = cellname2rowcol(anchor_cell)
        elif row_col:
            start_row, start_col = row_col
        else:
            start_row, start_col = (1, 1)
        worksheet = self.worksheet(title=sheet_name)
        if append_summation_row:
            df = add_summation_row(df)
        set_with_dataframe(worksheet, df, include_index=include_index,
            include_column_header=include_column_header,
            row=start_row, col=start_col)
        if include_column_header:
            # Bold header row
            worksheet.format('1:1', {'textFormat': {'bold': True}})
        self.auto_size_columns(worksheet)
        return self.read_as_df(sheet_name)

    def append_df(self, sheet_name, append_df):
        df = self.read_as_df(sheet_name)
        df = df.append(append_df)
        return self.write_df(sheet_name, df)

    def create_worksheet(self, sheet_name, reinitialize=False):
        '''
        Create a new worksheet with the name 'sheet_name'.  If
        reinitialie==True, delete the worksheet and re-create it.
        '''
        worksheet = self.worksheet(title=sheet_name)
        if worksheet:
            if reinitialize:
                self._sh.del_worksheet(worksheet)
                worksheet = self._sh.add_worksheet(title=sheet_name,
                    rows=DEFAULT_NUM_ROWS, cols=DEFAULT_NUM_COLS)
            return worksheet
        else:
            return self._sh.add_worksheet(title=sheet_name,
                    rows=DEFAULT_NUM_ROWS, cols=DEFAULT_NUM_COLS)

    def batch_update(self, sheet_name, data):
        worksheet = self.worksheet(title=sheet_name)
        sheetId = worksheet._properties['sheetId']
        self.sh.batch_update(data)

    def auto_size_columns(self, worksheet):
        sheetId = worksheet._properties['sheetId']
        data = {
            "requests": [
                {
                    "autoResizeDimensions": {
                    "dimensions": {
                        "sheetId": worksheet._properties['sheetId'],
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": worksheet.col_count
                    }
                }
            }]
        }
        return self.sh.batch_update(data)

    def all_values(self, sheet_name, force_update=False):
        '''
        Look all values of a spreadsheet into cache
        '''
        if sheet_name in self._all_values.keys():
            all_values = self._all_values[sheet_name]
            if not force_update:
                return all_values
        worksheet = self.worksheet(title=sheet_name)
        if worksheet:
            all_values = worksheet.get_all_values()
            self._all_values[sheet_name] = all_values
            return all_values
        else:
            return []

    def shape(self, sheet_name, force_update=False):
        all_values = self.all_values(sheet_name, force_update=force_update)
        num_rows = len(all_values)
        if num_rows > 0:
            num_cols = len(all_values[0])
        else:
            num_cols = 0
        return num_rows, num_cols

    def add_summation_row(self, sheet_name, anchor_cell='A1', skip_rows=1, skip_cols=1):
        '''
        Add a summation row.
        Assumption:
        - first row (row 1) is the header row
        - first column (column A) is a category
        - add summation for col 2 to the end
        '''
        start_row, start_col = cellname2rowcol(anchor_cell)
        worksheet = self.worksheet(title=sheet_name)
        num_rows, num_cols = self.shape(sheet_name)
        summary_row_number = num_rows + 1 + start_row - 1
        for j in range(skip_cols+1+start_col-1, num_cols+1+start_col-1):
            col_letter = chr(j +ord('A') - 1)
            formula = "=SUM({0}{1}:{0}{2})".format(col_letter, skip_rows+1, num_rows)
            print(col_letter, formula)
            cell_name = "{}{}".format(col_letter, num_rows+1)
            worksheet.update_acell(cell_name, formula)



