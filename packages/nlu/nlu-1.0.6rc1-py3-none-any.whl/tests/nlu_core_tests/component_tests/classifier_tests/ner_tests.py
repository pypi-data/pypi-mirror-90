import unittest
from tests.test_utils import get_sample_pdf_with_labels, get_sample_pdf, get_sample_sdf, get_sample_pdf_with_extra_cols, get_sample_pdf_with_no_text_col ,get_sample_spark_dataframe
from nlu import *

class TestNer(unittest.TestCase):

    # def test_ner_tok_bug(self):
    #     text =  ['Zebra stripes and their role in flies']
    #     d = nlu.load('ner', verbose=True).predict(text)
    #     print(d)
    #     print(d.columns)


    def test_ner_pipe(self):
        print("CHUNK")
        df = nlu.load('en.ner.onto.glove.6B_100d', verbose=True ).predict('Donald Trump from America and Angela Merkal from Germany dont share many oppinions.', output_level='chunk' ,metadata=True)
        print(df.columns)
        print(df[[ 'entities', ]])
        print(df[[ 'entities', 'entities_confidence']])
        print(df[[ 'entities', 'ner_confidence']])

        #
        # print("DOCUMENT")
        # df = nlu.load('en.ner.onto.glove.6B_100d', verbose=True ).predict('Donald Trump from America and Angela Merkal from Germany dont share many oppinions.', output_level='document',metadata=True )
        # print(df.columns)
        # print(df[[ 'entities', 'document']])
        # print(df[[ 'entities', 'entities_confidence']])
        # print(df[[ 'entities', 'ner_confidence']])
        # print(df[[ 'document', 'ner_confidence']])
        # print("SENTENCE")
        # df = nlu.load('en.ner.onto.glove.6B_100d', verbose=True ).predict('Donald Trump from America and Angela Merkal from Germany dont share many oppinions.', output_level='sentence' ,metadata=True)
        # print(df.columns)
        # print(df[[ 'entities', 'sentence']])
        # print(df[[ 'entities', 'entities_confidence']])
        # print(df[[ 'entities', 'ner_confidence']])
        # print(df[[ 'sentence', 'ner_confidence']])
        #
        #
        # print("TOKEN")
        # df = nlu.load('en.ner.onto.glove.6B_100d', verbose=True ).predict('Donald Trump from America and Angela Merkal from Germany dont share many oppinions.', output_level='token' ,metadata=True)
        # print(df.columns)
        # print(df[[ 'entities', 'entities_confidence']])
        # print(df[[ 'entities', 'ner_confidence']])
        # print(df[[ 'token', 'ner_confidence']])
        # print(df[[ 'ner', 'ner_confidence']])





    def test_ner_pipe_confidences(self):
        #
        df = nlu.load('en.ner.onto.glove.6B_100d', verbose=True ).predict('Donald Trump from America and Angela Merkal from Germany dont share many oppinions.', output_level='token', metadata=True)
        print(df)
        print(df.columns)
        print(df[[ 'entities', 'entities_confidence']])
        print(df[[ 'entities', 'ner_confidence']])
        print(df[[ 'token', 'ner_confidence']])
        print(df[[ 'ner', 'ner_confidence']])

if __name__ == '__main__':
    unittest.main()

