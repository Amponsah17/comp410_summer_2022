import unittest
import os
from scan import show_aggie_pride, scan_files, get_file_text


# https://docs.python.org/3/library/unittest.html
class ScanTests(unittest.TestCase):
    def test_aggie_pride(self):
        # get the slogans
        slogans = show_aggie_pride()

        self.assertIn('Aggie Pride - Worldwide', slogans)

    def test_scan_files(self):
        # Test to make sure scan_files returns the expected results
        expected_result = ['files/november_statement.pdf',
                           'files/Documents/twitter_info.docx',
                           'files/Documents/Statements/Retirement/ss_info.pdf',
                           'files/Downloads/address_book.xlsx',
                           'files/Downloads/address_book.txt']

        # Make expected_result os safe by checking the seperator
        if os.sep != '/':
            for i in range(len(expected_result)):
                expected_result[i] = expected_result[i].replace('/', os.sep)

        # Make sure all the expected files are actually found
        scan = scan_files()
        for f in expected_result:
            self.assertIn(f, scan)

    def test_get_file_text(self):
        # Will rely on other tests to make sure all information in a file
        # is being read correctly.  For this test will focus on negative tests
        # make sure an empty file returns an empty list
        empty = os.path.join('files', 'empty.txt')
        text = get_file_text(empty)
        self.assertEqual(text, [])

        # Test an unsupported file raises an exception
        with self.assertRaises(RuntimeError):
            get_file_text('unsupported.xyz')

    def test_november_statement_pdf(self):
        # get a platform safe path to a test pdf file
        pdf_file = os.path.join('files', 'november_statement.pdf')

        # get the text from this file
        text = get_file_text(pdf_file)

        self.assertIn('Name: John Smith', text)

        # Check for the account number
        self.assertIn('Account Number: 3942-29992', text)

    def test_ss_info_pdf(self):
        # Create an OS safe path to ss_info.pdf
        ss_file = os.sep.join(['files', 'Documents', 'Statements', 'Retirement', 'ss_info.pdf'])

        # Get the text from the file
        text = get_file_text(ss_file)

        # Check for the ss number
        self.assertIn('Number: 000-12-1234', text)

    def test_twitter_info_docx(self):
        # test to make sure we can read a docx ok
        doc = 'files/Documents/twitter_info.docx'

        # Fix seperator for windows (or other platforms)
        if os.sep != '/':
            doc = doc.replace('/', os.sep)

        # Read test document which contains a twitter handle
        text = get_file_text(doc)
        self.assertIn('My twitter handle is @john_jones but I’d like to keep this a secret', text)

    def test_address_book_xlsx(self):
        xlsx = 'files/Downloads/address_book.xlsx'

        # Fix seperator for windows (or other platforms)
        if os.sep != '/':
            xlsx = xlsx.replace('/', os.sep)

        text = get_file_text(xlsx)

        # check to make sure we found all the phone numbers
        self.assertIn('336-555-1212', text)
        self.assertIn('919-555-1212', text)
        self.assertIn('970-555-1212', text)

    def test_address_book_txt(self):
        txt = 'files/Downloads/address_book.txt'

        # Fix seperator for windows (or other platforms)
        if os.sep != '/':
            txt = txt.replace('/', os.sep)

        # read the text file
        text = get_file_text(txt)

        # check to make sure we found all the names
        self.assertIn('John Jones,336-555-1212', text)
        self.assertIn('James Johnson,919-555-1212', text)
        self.assertIn('Roger Jones,970-555-1212', text)

    def test_sprint2_t0_docx(self):
        # full path to the sample document
        no_pii = 'files/Documents/Team0 Documents/sprint2_team0_docx_no_pii.docx'

        # Fix seperator for windows (or other platforms)
        if os.sep != '/':
            no_pii = no_pii.replace('/', os.sep)

        # read the text from the file
        no_pii_text = get_file_text(no_pii)
        # make sure the content is there
        self.assertIn('There is no PII in it', no_pii_text)

        # Now check the other file
        pii = 'files/Documents/Team0 Documents/sprint2_team0_docx_with_pii.docx'

        # Fix seperator for windows (or other platforms)
        if os.sep != '/':
            pii = pii.replace('/', os.sep)

        # read the text from the file
        pii_text = get_file_text(pii)
        # make sure the content is there
        self.assertIn('It contains some sample PII', pii_text)

    def test_sprint2_t2_txt(self):
        no_pii = 'files/Documents/Team2 Documents/sprint2_team2_txt_no_pii.txt'
        if os.sep != '/':
            no_pii = no_pii.replace('/', os.sep)
        no_pii_text = get_file_text(no_pii)
        self.assertIn('Test document with no PII.', no_pii_text)

        pii = 'files/Documents/Team2 Documents/sprint2_team2_txt_with_pii.txt'
        if os.sep != '/':
            pii = pii.replace('/', os.sep)
        pii_text = get_file_text(pii)
        self.assertIn('Test document with PII.', pii_text)
    
    def test_sprint2_t1_xlsx(self):
        # Full path to the sample document.
        no_pii = 'files/Documents/Team 1 Documents/Sprint2_Team1_xlsx_no_pii.xlsx'

        # Fix seperator for windows (or other platforms).
        if os.sep != '/':
            no_pii = no_pii.replace('/', os.sep)

        # Read the text from the file.
        no_pii_text = get_file_text(no_pii)
        # make sure the content is there
        self.assertIn('There is no PII in it', no_pii_text)

        # Now check the other file.
        pii = 'files/Documents/Team 1 Documents/Sprint2_Team1_xlsx_with_pii.xlsx'

        # Fix seperator for windows (or other platforms).
        if os.sep != '/':
            pii = pii.replace('/', os.sep)

        # read the text from the file
        pii_text = get_file_text(pii)
        # make sure the content is there
        self.assertIn('It contains some sample PII', pii_text)


if __name__ == '__main__':
    unittest.main()
