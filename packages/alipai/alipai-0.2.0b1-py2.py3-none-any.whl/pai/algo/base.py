from __future__ import absolute_import

from pai.core.estimator import AlgoBaseEstimator
from pai.core.transformer import AlgoBaseTransformer


class _MaxComputeAlgoMixin(object):
    _enable_sparse = False
    XFlowProjectDefault = "algo_public"

    def __init__(self, execution=None, core_num=None, mem_size_per_core=None):
        self.execution = execution
        self.core_num = core_num
        self.mem_size_per_core = mem_size_per_core

    def get_maxc_args(self):
        return {
            "execution": self.execution,
        }

    def _compile_args(self, *inputs, **kwargs):
        args = self.get_maxc_args()
        if type(self)._enable_sparse and kwargs.get("enable_sparse"):
            args["enableSparse"] = True
            sparse_delimiter = kwargs["sparse_delimiter"]
            item_delimiter, kv_delimiter = sparse_delimiter
            args["itemDelimiter"] = item_delimiter
            args["kvDelimiter"] = kv_delimiter
        args["coreNum"] = kwargs.get("coreNum")
        args["memSizePerCore"] = kwargs.get("mem_size_per_core")

        return args


class MaxComputeEstimator(AlgoBaseEstimator, _MaxComputeAlgoMixin):
    _pmml_model = False

    def __init__(
        self,
        execution=None,
        pmml_gen=None,
        pmml_oss_path=None,
        pmml_oss_endpoint=None,
        pmml_oss_rolearn=None,
        pmml_oss_bucket=None,
        **kwargs
    ):
        AlgoBaseEstimator.__init__(
            self,
            pmml_gen=pmml_gen,
            pmml_oss_path=pmml_oss_path,
            pmml_oss_endpoint=pmml_oss_endpoint,
            pmml_oss_rolearn=pmml_oss_rolearn,
            pmml_oss_bucket=pmml_oss_bucket,
            **kwargs
        )
        _MaxComputeAlgoMixin.__init__(self, execution=execution)

    def _compile_args(self, *inputs, **kwargs):
        args = super(MaxComputeEstimator, self)._compile_args(*inputs, **kwargs)
        if type(self)._pmml_model and kwargs.get("pmml_gen"):
            args["pmmlOssPath"] = kwargs.get("pmml_oss_path")
            args["pmmlOssEndpoint"] = kwargs.get("pmml_oss_endpoint")
            args["roleArn"] = kwargs.get("pmml_oss_rolearn")
            args["pmmlOssBucket"] = kwargs.get("pmml_oss_bucket")
            args["generatePmml"] = kwargs.get("pmml_gen")

        return args


class MaxComputeTransformer(AlgoBaseTransformer, _MaxComputeAlgoMixin):
    def __init__(self, execution=None, **kwargs):
        AlgoBaseTransformer.__init__(self, **kwargs)
        _MaxComputeAlgoMixin.__init__(self, execution=execution)
