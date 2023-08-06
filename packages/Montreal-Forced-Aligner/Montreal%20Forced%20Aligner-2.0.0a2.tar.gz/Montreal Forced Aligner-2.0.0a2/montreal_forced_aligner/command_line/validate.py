import shutil
import os
import multiprocessing as mp

from montreal_forced_aligner.corpus.align_corpus import AlignableCorpus
from montreal_forced_aligner.dictionary import Dictionary
from montreal_forced_aligner.validator import CorpusValidator
from montreal_forced_aligner.exceptions import ArgumentError
from montreal_forced_aligner.config import TEMP_DIR
from montreal_forced_aligner.utils import get_available_dict_languages, get_dictionary_path


def validate_corpus(args):
    if not args.temp_directory:
        temp_dir = TEMP_DIR
    else:
        temp_dir = os.path.expanduser(args.temp_directory)
    corpus_name = os.path.basename(args.corpus_directory)
    if corpus_name == '':
        args.corpus_directory = os.path.dirname(args.corpus_directory)
        corpus_name = os.path.basename(args.corpus_directory)
    data_directory = os.path.join(temp_dir, corpus_name)
    shutil.rmtree(data_directory, ignore_errors=True)

    os.makedirs(data_directory, exist_ok=True)

    corpus = AlignableCorpus(args.corpus_directory, data_directory, speaker_characters=args.speaker_characters,
                    num_jobs=getattr(args, 'num_jobs', 3))
    dictionary = Dictionary(args.dictionary_path, data_directory, word_set=corpus.word_set)

    a = CorpusValidator(corpus, dictionary, temp_directory=data_directory,
                        ignore_acoustics=getattr(args, 'ignore_acoustics', False),
                        test_transcriptions=getattr(args, 'test_transcriptions', False), use_mp=not args.disable_mp)
    a.validate()


def validate_args(args, download_dictionaries=None):
    if args.test_transcriptions and args.ignore_acoustics:
        raise ArgumentError('Cannot test transcriptions without acoustic feature generation.')
    if not os.path.exists(args.corpus_directory):
        raise (ArgumentError('Could not find the corpus directory {}.'.format(args.corpus_directory)))
    if not os.path.isdir(args.corpus_directory):
        raise (ArgumentError('The specified corpus directory ({}) is not a directory.'.format(args.corpus_directory)))

    if args.dictionary_path.lower() in download_dictionaries:
        args.dictionary_path = get_dictionary_path(args.dictionary_path.lower())
    if not os.path.exists(args.dictionary_path):
        raise (ArgumentError('Could not find the dictionary file {}'.format(args.dictionary_path)))
    if not os.path.isfile(args.dictionary_path):
        raise (ArgumentError('The specified dictionary path ({}) is not a text file.'.format(args.dictionary_path)))


def run_validate_corpus(args, download_dictionaries=None):
    if download_dictionaries is None:
        download_dictionaries = get_available_dict_languages()
    try:
        args.speaker_characters = int(args.speaker_characters)
    except ValueError:
        pass
    validate_args(args, download_dictionaries)
    validate_corpus(args)


if __name__ == '__main__':  # pragma: no cover
    mp.freeze_support()
    from montreal_forced_aligner.command_line.mfa import validate_parser, fix_path, unfix_path, dict_languages
    validate_args = validate_parser.parse_args()

    fix_path()
    run_validate_corpus(validate_args, dict_languages)
    unfix_path()
