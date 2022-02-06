#!/usr/bin/python3
import csv
import argparse
import os


class most_active_cookie_finder():
    """
    This class, given a path to a csv file containing "cookie" and "timestamp" columns, 
    as well as a date, will determine the most common cookie for that date.

    """

    def __init__(self, path, day):
        """
        Constructor for the attributes for the finder object.

        Parameters
        ----------
            path : str
                path to a csv file
            day : str
                date of interest for log checking
        """
        self.path = path
        self.day = day

    def validate_file(self):
        '''
        Validation for input file.

        Parameters
        ----------
        None

        Returns
        -------
        (boolean): indicates successful validation
        '''
        file_name = self.path

        def valid_filetype(file_name):
            # validate file type
            return file_name.endswith('.csv')

        def valid_path(path):
            # validate file path
            return os.path.exists(path)

        if not valid_path(file_name):
            INVALID_PATH_MSG = "Error: Invalid file path. Path %s does not exist or not reachable."
            print(INVALID_PATH_MSG % (file_name))
            return False
        elif not valid_filetype(file_name):
            INVALID_FILETYPE_MSG = "Error: Invalid format. %s must be a .csv file."
            print(INVALID_FILETYPE_MSG % (file_name))
            return False
        return True

    def validate_headers(self, header, label):
        """
        Gets the indices for target header label.

        Parameters
        ----------
        header (list): labels for the data
        label (str): a target fearture label

        Returns
        -------
        index (int): the index in header for the target label
        """
        index = None
        for i in range(len(header)):
            if header[i] == label:
                index = i
        if index is None:
            raise ValueError(
                "input CSV must have 'timestamp' and 'cookie' labels")

        return index

    def validate_date(self):
        '''
        Validation for date given.

        Parameters
        ----------
        None

        Returns
        -------
        (boolean): indicates successful validation
        '''
        INVALID_DATE_MSG = "Error: Invalid Date. Date %s does not math YYYY-MM_DD format."

        sep = 0
        sections = 1
        for i in range(len(self.day)):
            if self.day[i] == '-':
                try:
                    int(self.day[sep:i])
                    sep = i
                    sections += 1
                except ValueError:
                    return False
        if sep == 7 and sections == 3:
            return True

    def load_cookie_data(self):
        """
        Loads the cookie data into header and rows lists.

        Parameters
        ----------
        None

        Returns
        -------
        header (list): labels for the data
        rows (list): features for each row in the csv, representing a cookie
        """
        file = open(self.path, encoding='utf-8-sig')
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        rows = []
        for row in csv_reader:
            rows.append(row)
        file.close()
        return header, rows

    def parse_cookie_data(self, header, rows):
        """
        Generates a dictionary of cookies and their count on the given day.

        Parameters
        ----------
        header (list): labels for the data
        rows (list): features for each row in the csv, representing a cookie log

        Returns
        -------
        max_cookie (str): cookie found most often during the target day 
        """
        max_cookie_count = 0
        max_cookies = []
        cookie_dict = dict()
        # indices for cookies and dates
        cookie_i = self.validate_headers(header, "cookie")
        date_i = self.validate_headers(header, "timestamp")

        # go through each row and build the dictionary of cookies
        for r in rows:
            if r[date_i][:10] == self.day:
                cookie = r[cookie_i]
                if r[cookie_i] in cookie_dict.keys():
                    cookie_dict[cookie] += 1
                    if cookie_dict[cookie] > max_cookie_count:
                        max_cookie_count = cookie_dict[cookie]
                else:
                    cookie_dict[cookie] = 1
        for cookie, count in cookie_dict.items():
            if count == max_cookie_count:
                max_cookies.append(cookie)

        return max_cookies


def main():
    parser = argparse.ArgumentParser(description="A cookie counter")
    parser.add_argument("path", help="path to file")
    parser.add_argument("-d", "--date", type=str,
                        metavar="date", help="takes a UTC date")

    args = parser.parse_args()
    cookie_finder = most_active_cookie_finder(args.path, args.date)
    if not cookie_finder.validate_date():
        return
    if not cookie_finder.validate_file():
        return
    h, r = cookie_finder.load_cookie_data()
    cookies = cookie_finder.parse_cookie_data(h, r)
    for cookie in cookies:
        print(cookie)


if __name__ == "__main__":
    main()
