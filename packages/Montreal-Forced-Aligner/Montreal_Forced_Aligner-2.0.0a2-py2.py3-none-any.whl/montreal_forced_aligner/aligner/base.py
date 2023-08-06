import os

from .. import __version__
from ..multiprocessing import compile_information
from ..config import TEMP_DIR


class BaseAligner(object):
    """
    Base aligner class for common aligner functions

    Parameters
    ----------
    corpus : :class:`~montreal_forced_aligner.corpus.AlignableCorpus`
        Corpus object for the dataset
    dictionary : :class:`~montreal_forced_aligner.dictionary.Dictionary`
        Dictionary object for the pronunciation dictionary
    align_config : :class:`~montreal_forced_aligner.config.AlignConfig`
        Configuration for alignment
    temp_directory : str, optional
        Specifies the temporary directory root to save files need for Kaldi.
        If not specified, it will be set to ``~/Documents/MFA``
    call_back : callable, optional
        Specifies a call back function for alignment
    """

    def __init__(self, corpus, dictionary, align_config, temp_directory=None,
                 call_back=None, debug=False, verbose=False):
        self.align_config = align_config
        self.corpus = corpus
        self.dictionary = dictionary
        if not temp_directory:
            temp_directory = TEMP_DIR
        self.temp_directory = temp_directory
        self.call_back = call_back
        if self.call_back is None:
            self.call_back = print
        self.verbose = verbose
        self.debug = debug
        self.setup()

    def setup(self):
        self.dictionary.write()
        self.corpus.initialize_corpus(self.dictionary)
        self.align_config.feature_config.generate_features(self.corpus)

    @property
    def meta(self):
        data = {'phones': sorted(self.dictionary.nonsil_phones),
                'version': __version__,
                'architecture': 'gmm-hmm',
                'features': 'mfcc+deltas',
                }
        return data

    def compile_information(self, model_directory, output_directory):
        issues = compile_information(model_directory, self.corpus, self.corpus.num_jobs, self)
        if issues:
            issue_path = os.path.join(output_directory, 'unaligned.txt')
            with open(issue_path, 'w', encoding='utf8') as f:
                for u, r in sorted(issues.items()):
                    f.write('{}\t{}\n'.format(u, r))
            print('There were {} segments/files not aligned. '
                  'Please see {} for more details on why alignment failed for these files.'.format(len(issues),
                                                                                                   issue_path))

    def export_textgrids(self, output_directory):
        """
        Export a TextGrid file for every sound file in the dataset
        """
        raise NotImplementedError
