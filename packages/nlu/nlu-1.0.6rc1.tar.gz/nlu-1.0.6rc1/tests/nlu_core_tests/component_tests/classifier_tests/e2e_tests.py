


import unittest
from tests.test_utils import get_sample_pdf_with_labels, get_sample_pdf, get_sample_sdf, get_sample_pdf_with_extra_cols, get_sample_pdf_with_no_text_col ,get_sample_spark_dataframe
from nlu import *

class TestE2E(unittest.TestCase):

    def test_e2e_model(self):
        df = nlu.load('en.classify.e2e',verbose=True).predict('You are so stupid', output_level='document')

        print(df.columns)
        print(df['document'], df[['e2e_classes','e2e_confidences']])

        df = nlu.load('e2e',verbose=True).predict('You are so stupid', output_level='sentence')
        # df = nlu.load('en.classify.sarcasm',verbose=True).predict(sarcasm_df['text'])

        print(df.columns)
        print(df['sentence'], df[['e2e_classes','e2e_confidences']])


    def test_quick(self):
        multi_pipe = nlu.load('en.embed_sentence.electra embed_sentence.bert use')
        res = multi_pipe.predict( get_sample_pdf())
        print(res)
        print(res.columns)

if __name__ == '__main__':
    unittest.main()

