import os
from collections import Counter
import yaml

from ..exceptions import ConfigError

from ..trainers import MonophoneTrainer, TriphoneTrainer, LdaTrainer, SatTrainer, IvectorExtractorTrainer

from ..features.config import FeatureConfig


TEMP_DIR = os.path.expanduser('~/Documents/MFA')


class BaseConfig(object):
    def update(self, data):
        for k, v in data.items():
            if not hasattr(self, k):
                raise ConfigError('No field found for key {}'.format(k))
            setattr(self, k, v)


class TrainingConfig(BaseConfig):
    def __init__(self, training_configs):
        self.training_configs = training_configs
        counts = Counter([x.train_type for x in self.training_configs])
        self.training_identifiers = []
        curs = {x.train_type: 1 for x in self.training_configs}
        for t in training_configs:
            i = t.train_type
            if counts[t.train_type] != 1:
                i += str(curs[t.train_type])
                curs[t.train_type] += 1
            self.training_identifiers.append(i)

    def keys(self):
        return self.training_identifiers

    def values(self):
        return self.training_configs

    def items(self):
        return zip(self.training_identifiers, self.training_configs)

    def __getitem__(self, item):
        if item not in self.training_identifiers:
            raise KeyError('{} not a valid training identifier'.format(item))
        return self.training_configs[self.training_identifiers.index(item)]

    @property
    def uses_lda(self):
        for k in self.keys():
            if k.startswith('lda'):
                return True
        return False

    @property
    def uses_sat(self):
        for k in self.keys():
            if k.startswith('sat'):
                return True
        return False


class AlignConfig(BaseConfig):
    def __init__(self, feature_config):
        self.transition_scale = 1.0
        self.acoustic_scale = 0.1
        self.self_loop_scale = 0.1
        self.feature_config = feature_config
        self.boost_silence = 1.0
        self.beam = 10
        self.retry_beam = 40
        self.data_directory = None # Gets set later
        self.use_mp = True

    @property
    def feature_file_base_name(self):
        return self.feature_config.feature_id

    def update(self, data):
        for k, v in data.items():
            if k == 'use_mp':
                self.feature_config.use_mp = v
            if not hasattr(self, k):
                raise ConfigError('No field found for key {}'.format(k))
            setattr(self, k, v)


class TranscribeConfig(BaseConfig):
    def __init__(self, feature_config):
        self.transition_scale = 1.0
        self.acoustic_scale = 0.083333
        self.self_loop_scale = 0.1
        self.feature_config = feature_config
        self.silence_weight = 0.01
        self.beam = 10
        self.max_active = 7000
        self.fmllr = False
        self.fmllr_update_type = 'full'
        self.lattice_beam = 6
        self.first_beam = None
        self.first_max_active = None
        self.max_fmllr_jobs = 12
        self.language_model_weight = 10
        self.word_insertion_penalty = 0.5
        self.data_directory = None # Gets set later
        self.use_mp = True

    def params(self):
        return {
            'transition_scale': self.transition_scale,
            'acoustic_scale': self.acoustic_scale,
            'self_loop_scale': self.self_loop_scale,
            'silence_weight': self.silence_weight,
            'beam': self.beam,
            'max_active': self.max_active,
            'fmllr': self.fmllr,
            'fmllr_update_type': self.fmllr_update_type,
            'lattice_beam': self.lattice_beam,
            'first_beam': self.first_beam,
            'first_max_active': self.first_max_active,
            'max_fmllr_jobs': self.max_fmllr_jobs,
            'language_model_weight': self.language_model_weight,
            'word_insertion_penalty': self.word_insertion_penalty,
            'use_mp': self.use_mp,
                }

    @property
    def feature_file_base_name(self):
        return self.feature_config.feature_id

    def update(self, data):
        for k, v in data.items():
            if k == 'use_mp':
                self.feature_config.use_mp = v
            if not hasattr(self, k):
                raise ConfigError('No field found for key {}'.format(k))
            setattr(self, k, v)


class TrainLMConfig(BaseConfig):
    def __init__(self):
        self.order = 3
        self.method = 'kneser_ney'
        self.prune = False
        self.count_threshold = 1
        self.prune_thresh_small = 0.0000003
        self.prune_thresh_medium = 0.0000001


def train_yaml_to_config(path):
    with open(path, 'r', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        global_params = {}
        training = []
        training_params = []
        global_feature_params = {}
        for k, v in data.items():
            if k == 'training':
                for t in v:
                    for k2, v2 in t.items():
                        feature_config = FeatureConfig()
                        if k2 == 'monophone':
                            training.append(MonophoneTrainer(feature_config))
                        elif k2 == 'triphone':
                            training.append(TriphoneTrainer(feature_config))
                        elif k2 == 'lda':
                            training.append(LdaTrainer(feature_config))
                        elif k2 == 'sat':
                            training.append(SatTrainer(feature_config))
                        elif k2 == 'ivector':
                            training.append(IvectorExtractorTrainer(feature_config))
                        training_params.append(v2)
            elif k == 'features':
                global_feature_params.update(v)
            else:
                global_params[k] = v
        feature_config = FeatureConfig()
        feature_config.update(global_feature_params)
        align_config = AlignConfig(feature_config)
        align_config.update(global_params)
        training_config = None
        if training:
            for i, t in enumerate(training):
                if i == 0 and t.train_type != 'mono':
                    raise ConfigError('The first round of training must be monophone.')
                t.update(global_params)
                t.update(training_params[i])
            training_config = TrainingConfig(training)
        align_config.feature_config.lda = training_config.uses_lda
        if training_config.uses_lda:
            align_config.feature_config.set_features_to_use_lda()
        align_config.feature_config.fmllr = training_config.uses_sat
        if align_config.beam >= align_config.retry_beam:
            raise ConfigError('Retry beam must be greater than beam.')
        return training_config, align_config


def align_yaml_to_config(path):
    with open(path, 'r', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        global_params = {}
        feature_config = FeatureConfig()
        for k, v in data.items():
            if k == 'features':
                feature_config.update(v)
            else:
                global_params[k] = v
        align_config = AlignConfig(feature_config)
        align_config.update(global_params)
        if align_config.beam >= align_config.retry_beam:
            raise ConfigError('Retry beam must be greater than beam.')
        return align_config


def transcribe_yaml_to_config(path):
    with open(path, 'r', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        global_params = {}
        feature_config = FeatureConfig()
        for k, v in data.items():
            if k == 'features':
                feature_config.update(v)
            else:
                global_params[k] = v
        config = TranscribeConfig(feature_config)
        config.update(global_params)
        return config


def load_basic_align():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    align_config = align_yaml_to_config(os.path.join(base_dir, 'basic_align.yaml'))
    return align_config


def load_basic_transcribe():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config = transcribe_yaml_to_config(os.path.join(base_dir, 'basic_transcribe.yaml'))
    return config


def load_basic_train():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    training_config, align_config = train_yaml_to_config(os.path.join(base_dir, 'basic_train.yaml'))
    return training_config, align_config


def load_basic_train_ivector():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    training_config, align_config = train_yaml_to_config(os.path.join(base_dir, 'basic_train_ivector.yaml'))
    return training_config, align_config


def load_test_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    training_config, align_config = train_yaml_to_config(os.path.join(base_dir, 'test_config.yaml'))
    return training_config, align_config


def train_lm_yaml_to_config(path):
    with open(path, 'r', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        config = TrainLMConfig()
        config.update(data)
    return config


def load_basic_train_lm():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    training_config = train_lm_yaml_to_config(os.path.join(base_dir, 'basic_train_lm.yaml'))
    return training_config


def save_config(config, path):
    with open(path, 'w', encoding='utf8') as f:
        yaml.dump(config.params(), f)
