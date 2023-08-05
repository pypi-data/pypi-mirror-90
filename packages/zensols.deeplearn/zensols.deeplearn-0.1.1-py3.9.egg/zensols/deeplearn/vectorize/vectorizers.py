"""Vectorizer implementations.

"""
__author__ = 'Paul Landes'

from typing import Set, List, Iterable, Union, Any, Tuple
from dataclasses import dataclass, field
import logging
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import torch
from torch import Tensor
from zensols.deeplearn import TorchTypes, TorchConfig
from . import (
    EncodableFeatureVectorizer,
    TensorFeatureContext,
    SparseTensorFeatureContext,
    FeatureContext,
    MultiFeatureContext,
)

logger = logging.getLogger(__name__)


@dataclass
class IdentityEncodableFeatureVectorizer(EncodableFeatureVectorizer):
    """An identity vectorizer, which encodes tensors verbatim, or concatenates a
    list of tensors in to one tensor of the same dimension.

    """
    DESCRIPTION = 'identity function encoder'

    def _get_shape(self):
        return -1,

    def _encode(self, obj: Union[list, Tensor]) -> Tensor:
        if isinstance(obj, Tensor):
            arr = obj
        else:
            tc = self.torch_config
            if len(obj[0].shape) == 0:
                arr = tc.singleton(obj, dtype=obj[0].dtype)
            else:
                arr = torch.cat(obj)
        return TensorFeatureContext(self.feature_id, arr)


@dataclass
class CategoryEncodableFeatureVectorizer(EncodableFeatureVectorizer):
    """A base class that vectorizies nominal categories in to integer indexes.

    :shape: ``(1, |categories|)``

    :param categories: a list of string enumerated values

    """
    categories: Set[str]

    def __post_init__(self):
        super().__post_init__()
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(self.categories)

    def _get_shape(self):
        return 1, len(self.categories)

    def get_classes(self, nominals: Iterable[int]) -> List[str]:
        """Return the label string values for indexes ``nominals``.

        """
        return self.label_encoder.inverse_transform(nominals)


@dataclass
class NominalEncodedEncodableFeatureVectorizer(CategoryEncodableFeatureVectorizer):
    """Map each label to a nominal, which is useful for class labels.

    :param data_type: the type to use for encoding, which if a string, must be
                      a key in of :obj:`.TorchTypes.NAME_TO_TYPE`

    :param decode_one_hot: if ``True``, during decoding create a one-hot
                           encoded tensor of shape ``(N, |labels|)``

    """
    DESCRIPTION = 'nominal encoder'
    data_type: Union[str, None, torch.dtype] = field(default=None)
    decode_one_hot: bool = field(default=False)

    def __post_init__(self):
        super().__post_init__()
        self.data_type = self._str_to_dtype(self.data_type, self.torch_config)

    def _str_to_dtype(self, data_type: str,
                      torch_config: TorchConfig) -> torch.dtype:
        if data_type is None:
            data_type = torch.int64
        else:
            data_type = TorchTypes.type_from_string(data_type)
        return data_type

    def _encode(self, category_instances: List[str]) -> FeatureContext:
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'categories: {category_instances} ' +
                         f'(one of {self.categories})')
        if not isinstance(category_instances, (tuple, list)):
            raise ValueError(
                f'expecting list but got: {type(category_instances)}')
        indicies = self.label_encoder.transform(category_instances)
        singleton = self.torch_config.singleton
        arr = singleton(indicies, dtype=self.data_type)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'encoding cat arr: {arr.dtype}')
        return TensorFeatureContext(self.feature_id, arr)

    def _decode(self, context: FeatureContext) -> Tensor:
        arr = super()._decode(context)
        if self.decode_one_hot:
            batches = arr.shape[0]
            he = self.torch_config.zeros((batches, len(self.categories)),
                                         dtype=torch.long)
            for row in range(batches):
                idx = arr[row]
                he[row][idx] = 1
            del arr
            arr = he
        return arr


@dataclass
class OneHotEncodedEncodableFeatureVectorizer(CategoryEncodableFeatureVectorizer):
    """Vectorize from a list of nominals.  This is useful for encoding labels for
    the categorization machine learning task.

    """
    DESCRIPTION = 'category encoder'

    optimize_bools: bool = field(default=True)

    def __post_init__(self):
        super().__post_init__()
        le = self.label_encoder
        llen = len(le.classes_)
        if not self.optimize_bools or llen != 2:
            arr = self.torch_config.zeros((llen, llen))
            for i in range(llen):
                arr[i][i] = 1
            self.identity = arr

    def _get_shape(self):
        n_classes = len(self.label_encoder.classes_)
        if self.optimize_bools and n_classes == 2:
            return 1,
        else:
            return -1, n_classes

    def _encode(self, category_instances: List[str]) -> FeatureContext:
        tc = self.torch_config
        indicies = self.label_encoder.transform(category_instances)
        is_one_row = self.shape[0] == 1
        if is_one_row:
            arr = tc.singleton(indicies)
        else:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f'creating: {self.identity.shape}')
            arr = tc.empty((len(category_instances), self.identity.shape[0]))
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f'created: {arr.dtype}')
            for i, idx in enumerate(indicies):
                arr[i] = self.identity[idx]
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'encoding cat arr: {arr.dtype}')
        if is_one_row or True:
            return TensorFeatureContext(self.feature_id, arr)
        else:
            return SparseTensorFeatureContext.instance(
                self.feature_id, arr, self.torch_config)


@dataclass
class AggregateEncodableFeatureVectorizer(EncodableFeatureVectorizer):
    """Use another vectorizer to vectorize each instance in an iterable.  Each
    iterable is then concatenated in to a single tensor on decode.

    **Important**: you must add the delegate vectorizer to the same vectorizer
    manager set as this instance since it uses the manager to find it.

    :shape: (-1, delegate.shape[1] * (2 ^ add_mask))

    :param delegate: the feature ID of the delegate vectorizer to use
                     (configured in same vectorizer manager)

    :param add_mask: if ``True``, every data item includes a mask (1 if the
                     data item is present, 0 if not) in the row directly after
                     the respective data row

    """
    DESCRIPTION = 'aggregate vectorizer'

    delegate_feature_id: str
    size: int
    add_mask: bool = field(default=False)

    def _get_shape(self):
        return -1, self.delegate.shape[1] * 2 if self.add_mask else 1

    @property
    def delegate(self) -> EncodableFeatureVectorizer:
        return self.manager[self.delegate_feature_id]

    def _encode(self, datas: Iterable[Iterable[Any]]) -> FeatureContext:
        vec = self.delegate
        ctxs = tuple(map(lambda d: vec.encode(d), datas))
        return MultiFeatureContext(self.feature_id, ctxs)

    def _decode(self, context: MultiFeatureContext) -> Tensor:
        vec = self.delegate
        srcs = tuple(map(lambda c: vec.decode(c), context.contexts))
        clen = len(srcs) * (2 if self.add_mask else 1)
        tc = self.torch_config
        first = srcs[0]
        dtype = first.dtype
        mid_dims = first.shape[1:]
        arr = tc.zeros((clen, self.size, *mid_dims), dtype=dtype)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'num contexts: {clen}, dtype={dtype}, ' +
                         f'src={first.shape}, dst={arr.shape}, ' +
                         f'mid_dims={mid_dims}')
        sz = self.size
        rowix = 0
        if self.add_mask:
            ones = tc.ones((self.size, *mid_dims), dtype=dtype)
        ctx: TensorFeatureContext
        for carr in srcs:
            lsz = min(carr.size(0), sz)
            if carr.dim() == 1:
                arr[rowix, :lsz] = carr[:lsz]
            elif carr.dim() == 2:
                arr[rowix, :lsz, :] = carr[:lsz, :]
            elif carr.dim() == 3:
                arr[rowix, :lsz, :, :] = carr[:lsz, :, :]
            if self.add_mask:
                arr[rowix + 1, :lsz] = ones[:lsz]
            rowix += (2 if self.add_mask else 1)
        return arr


@dataclass
class MaskTokenFeatureContext(FeatureContext):
    """A feature context used for the :class:`.MaskTokenContainerFeatureVectorizer`
    vectorizer.

    :param sequence_lengths: the lengths of all each row to mask

    """
    sequence_lengths: Tuple[int]


@dataclass
class MaskTokenContainerFeatureVectorizer(EncodableFeatureVectorizer):
    """Creates masks where the first N elements of a vector are 1's with the rest
    0's.

    :shape: (-1, ``size``)

    :param size: the length of all mask vectors

    :param data_type: the mask tensor type, which defaults to the int type that
                      matches the resolution of the manager's ``torch_config``

    """
    DESCRIPTION = 'mask'

    size: int
    data_type: Union[str, None, torch.dtype] = field(default=None)

    def __post_init__(self):
        super().__post_init__()
        self.data_type = self._str_to_dtype(self.data_type, self.torch_config)
        self.ones = self.torch_config.ones((self.size,), dtype=self.data_type)

    def _str_to_dtype(self, data_type: str,
                      torch_config: TorchConfig) -> torch.dtype:
        if data_type is None:
            data_type = torch_config.int_type
        else:
            data_type = TorchTypes.type_from_string(data_type)
        return data_type

    def _get_shape(self):
        return -1, self.size,

    def _encode(self, datas: Iterable[Iterable[Any]]) -> FeatureContext:
        lens = tuple(map(lambda d: sum(1 for _ in d), datas))
        return MaskTokenFeatureContext(self.feature_id, lens)

    def _decode(self, context: MaskTokenFeatureContext) -> Tensor:
        tc = self.torch_config
        batch_size = len(context.sequence_lengths)
        ones = self.ones
        arr = tc.zeros((batch_size, self.size), dtype=self.data_type)
        for bix, slen in enumerate(context.sequence_lengths):
            arr[bix, :slen] = ones[:slen]
        return arr


@dataclass
class SeriesEncodableFeatureVectorizer(EncodableFeatureVectorizer):
    """Vectorize a Pandas series, such as a list of rows.  This vectorizer has an
    undefined shape since both the number of columns and rows are not specified
    at runtime.

    :shape: (-1, 1)

    """
    DESCRIPTION = 'pandas series'

    def _get_shape(self):
        return -1, -1

    def _encode(self, rows: Iterable[pd.Series]) -> FeatureContext:
        narrs = []
        tc = self.torch_config
        nptype = tc.numpy_data_type
        for row in rows:
            narrs.append(row.to_numpy(dtype=nptype))
        arr = np.stack(narrs)
        arr = tc.from_numpy(arr)
        return TensorFeatureContext(self.feature_id, arr)


@dataclass
class AttributeEncodableFeatureVectorizer(EncodableFeatureVectorizer):
    """Vectorize a iterable of floats.  This vectorizer has an undefined shape
    since both the number of columns and rows are not specified at runtime.

    :shape: (1,)

    """
    DESCRIPTION = 'single attribute'

    def _get_shape(self):
        return 1,

    def _encode(self, data: Iterable[float]) -> FeatureContext:
        arr = self.torch_config.from_iterable(data)
        return TensorFeatureContext(self.feature_id, arr)
