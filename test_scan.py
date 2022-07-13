import unittest
import os
from scan import show_aggie_pride, scan_files, get_file_text


# https://docs.python.org/3/library/unittest.html
class ScanTests(unittest.TestCase):
    def test_aggie_pride(self):
        # get the slogans
        slogans = show_aggie_pride()

        self.assertIn('Aggie Pride - Worldwide', slogans)
        self.assertIn('Aggie born aggie bred, when I die Ill be aggie dead', slogans)

        self.assertIn('Aggies Do', slogans)

    def test_scan_files(self):
        # Test to make sure scan_files returns the expected results
        expected_result = ['files/november_statement.pdf',
                           'files/Documents/twitter_info.docx',
                           'files/Documents/Statements/Retirement/ss_info.pdf',
                           'files/Downloads/address_book.xlsx',
                           'files/Downloads/address_book.txt',
                           'files/Documents/twitter_info.docx',
                           'files/Documents/Team 3 Documents/file_withOut_PII.docx',
                           'files/Documents/Team 3 Documents/file_with_PII.docx',
                           'files/Documents/Team 3 Documents/xslxnoPII.xlsx',
                           'files/Documents/Team 3 Documents/xslxwPII.xlsx',
                           'files/Documents/Team 3 Documents/sprint2_withPII.pdf',
                           'files/Documents/Team 3 Documents/sprint2_noPII.pdf'
                           ]

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

    def test_sprint2_withPII(self):
        # create path to sprint2_withPII.pdf
        sprint2_file = os.sep.join(['files', 'Documents', 'Team 3 Documents', 'sprint2_withPII.pdf'])

        # get text from the file
        text = get_file_text(sprint2_file)

        # check for name
        self.assertIn('Name: The Punisher ', text)

        # check for the phone number
        self.assertIn('Number: 555-090-9389 ', text)

        # check for account number
        self.assertIn('Account Number: 7837-03990 ', text)

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

    def test_sprint2_t2_xlsx(self):
        # Full path to the sample document.
        no_pii = 'files/Documents/Team2 Documents/sprint2_team2_xlsx_no_pii.xlsx'
        # Fix seperator for windows (or other platforms).
        if os.sep != '/':
            no_pii = no_pii.replace('/', os.sep)

        # Read the text from the file.
        no_pii_text = get_file_text(no_pii)
        # Make sure the file is there
        self.assertIn('There is no PII here', no_pii_text)

        # Now check the other file
        pii = 'files/Documents/Team2 Documents/sprint2_team2_xlsx_pii.xlsx'

        # Fix seperator for windows (or other platforms).
        if os.sep != '/':
            pii = pii.replace('/', os.sep)
        # Read the text from the file
        pii_text = get_file_text(pii)
        # Make sure the file is there
        self.assertIn('There is sample PII here', pii_text)

    def test_sprint2_t1_xslx(self):
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

    def test_sprint2_t4_xlsx(self):
        # Full path to the xlsx file with no PII in it
        no_pii = 'files/Documents/Team 4 Documents/sprint2_team4_xlsx_no_pii.xlsx'
        # Fix seperator for windows (or other platforms).
        if os.sep != '/':
            no_pii = no_pii.replace('/', os.sep)

        # read the text from the file
        no_pii_text = get_file_text(no_pii)
        self.assertEqual(['Test Document with no PII'], no_pii_text)

        # Full path to the xlsx file that has PII
        pii = 'files/Documents/Team 4 Documents/sprint2_team4_xlsx_with_pii.xlsx'
        # Fix seperator for windows (or other platforms).
        if os.sep != '/':
            pii = no_pii.replace('/', os.sep)

        pii_text = get_file_text(pii)
        self.assertIn('Test Document with PII', pii_text)

    def test_t1_sprint2_docx(self):
        # Full path to the sample document.
        docx_no_pii = 'files/Documents/Team 1 Documents/Sprint2_t1_docx_no_pii.docx'

        # Fix seperator for windows (or other platforms).
        if os.sep != '/':
            docx_no_pii = docx_no_pii.replace('/', os.sep)

        # Read the text from the file.
        docx_no_pii_text = get_file_text(docx_no_pii)
        # make sure the content is there
        self.assertIn('Does not contain a PII', docx_no_pii_text)

        # check the other file for PII.
        docx_pii = 'files/Documents/Team 1 Documents/sprint2_t1_docx_with_pii.docx'

        # Fix seperator for windows (or other platforms).
        if os.sep != '/':
            docx_pii = docx_pii.replace('/', os.sep)

        # read the text from the file
        docx_pii_text = get_file_text(docx_pii)
        # make sure the content is there
        self.assertIn('Contains sample PII', docx_pii_text)

    def test_sprint2_t3_docx(self):
        # full path to the sample document
        no_pii = 'files/Documents/Team 3 Documents/file_withOut_PII.docx'

        # Fix seperator for windows (or other platforms)
        if os.sep != '/':
            no_pii = no_pii.replace('/', os.sep)

        # read the text from the file
        no_pii_text = get_file_text(no_pii)
        # make sure the content is there
        self.assertIn('Sed ut perspiciatis unde omnis iste natus error sit voluptatem', no_pii_text[0])

        # Now check the other file
        pii = 'files/Documents/Team 3 Documents/file_with_PII.docx'

        # Fix seperator for windows (or other platforms)
        if os.sep != '/':
            pii = pii.replace('/', os.sep)

        # read the text from the file
        pii_text = get_file_text(pii)
        # make sure the content is there
        self.assertIn('John Smith', pii_text[0])

    def test_sprint2_t3_xlsx(self):
        # Full path to the sample document.
        xlsx_no_pii = 'files/Documents/Team 3 Documents/xslxnoPII.xlsx'

        # Fix seperator for windows (or other platforms).
        if os.sep != '/':
            xlsx_no_pii = xlsx_no_pii.replace('/', os.sep)

        # Read the text from the file.
        xlsx_no_pii_text = get_file_text(xlsx_no_pii)
        # make sure the content is there
        self.assertIn('Does not contain a PII', xlsx_no_pii_text)

        # Now check the other file.
        xlsx_pii = 'files/Documents/Team 3 Documents/xslxwPII.xlsx'

        # Fix seperator for windows (or other platforms).
        if os.sep != '/':
            xlsx_pii = xlsx_pii.replace('/', os.sep)

        # read the text from the file
        xlsx_pii_text = get_file_text(xlsx_pii)
        # make sure the content is there
        self.assertIn('Jaden ', xlsx_pii_text)

    def test_sprint2_t2_docx(self):
        # full path to the sample document
        no_pii = 'files/Documents/Team2 Documents/sprint2_team2_docx_no_pii.docx'

        # Fix seperator for windows (or other platforms)
        if os.sep != '/':
            no_pii = no_pii.replace('/', os.sep)

        # read the text from the file
        no_pii_text = get_file_text(no_pii)
        # make sure the content is there
        self.assertIn('There is no PII in it', no_pii_text)

        # Now check the other file
        pii = 'files/Documents/Team2 Documents/sprint2_team2_docx_with_pii.docx'

        # Fix seperator for windows (or other platforms)
        if os.sep != '/':
            pii = pii.replace('/', os.sep)

        # read the text from the file
        pii_text = get_file_text(pii)
        # make sure the content is there
        self.assertIn('It contains some sample PII', pii_text)

    def test_sprint2_t4(self):
        # To team members:
        # After creating the file types you need to close your issue,
        # Name them as 'without_pii_{github_username}.{extension}'
        #    Make sure this file contains the text "There is no PII in it"
        # And 'with_pii_{github_username}.{extension}'
        #    Make sure this file contains the text "It contains some sample PII"
        # Then copy the extension next to your name from the array below into the document types array
        # document_types = ['_tashanthornton.xlsx', '_niasia.txt', '_nigeltiany.docx', '_antrays.txt', '_terrelxavier.txt']
        document_types = ['_nigeltiany.docx', '_terrelxavier.docx', '_niasia.txt', '_antrays.txt']

        for document in document_types:
            # Full path to the sample document.
            no_pii = 'files/Documents/Team 4 Documents/without_pii' + document

            # Fix seperator for windows (or other platforms).
            if os.sep != '/':
                no_pii = no_pii.replace('/', os.sep)

            # Read the text from the file.
            no_pii_text = get_file_text(no_pii)
            # make sure the content is there
            self.assertIn('There is no PII in it', no_pii_text)

            # Now check the other file.
            pii = 'files/Documents/Team 4 Documents/with_pii' + document

            # Fix seperator for windows (or other platforms).
            if os.sep != '/':
                pii = pii.replace('/', os.sep)

            # read the text from the file
            pii_text = get_file_text(pii)
            # make sure the content is there
            self.assertIn('It contains some sample PII', pii_text)


if __name__ == '__main__':
    unittest.main()
