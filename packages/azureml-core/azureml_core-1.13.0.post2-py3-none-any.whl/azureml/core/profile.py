# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Contains functionality for profiling models in Azure Machine Learning."""

import logging
import sys
import time
import json
import warnings
from dateutil.parser import parse

try:
    from abc import ABCMeta
    ABC = ABCMeta('ABC', (), {})
except ImportError:
    from abc import ABC
from abc import abstractmethod

from azureml._model_management._constants import (
    HOW_TO_CREATE_DATASET_URL,
    PROFILE_FAILURE_MESSAGE,
    PROFILE_PARTIAL_SUCCESS_MESSAGE,
    PROFILE_RECOMMENDED_CPU_KEY,
    PROFILE_RECOMMENDED_MEMORY_KEY,
)
from azureml._model_management._util import get_mms_operation, get_operation_output
from azureml.exceptions import WebserviceException, UserErrorException

module_logger = logging.getLogger(__name__)


MIN_PROFILE_CPU = 0.1
MAX_PROFILE_CPU = 3.5
MIN_PROFILE_MEMORY = 0.1
MAX_PROFILE_MEMORY = 15.0


class _ModelEvaluationResultBase(ABC):
    """_ModelEvaluationResultBase abstract object that serves as a base for results of profiling and validation."""

    @property
    @classmethod
    @abstractmethod
    def _model_eval_type(cls):
        return NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def _general_mms_suffix(cls):
        return NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def _expected_payload_keys(cls):
        return NotImplementedError

    @abstractmethod
    def __repr__(self):
        """Return the string representation of the _ModelEvaluationResultBase object.

        :return: String representation of the _ModelEvaluationResultBase object
        :rtype: str
        """
        return NotImplementedError

    @abstractmethod
    def get_details(self):
        """Return the the observed metrics and other details of the model test operation.

        :return: Dictionary of metrics
        :rtype: dict[str, float]
        """
        return NotImplementedError

    _details_keys_success = [
        'requestedCpu',
        'requestedMemoryInGB',
        'requestedQueriesPerSecond',
        'maxUtilizedMemoryInGB',
        'maxUtilizedCpu',
        'totalQueries',
        'successQueries',
        'successRate',
        'averageLatencyInMs',
        'latencyPercentile50InMs',
        'latencyPercentile90InMs',
        'latencyPercentile95InMs',
        'latencyPercentile99InMs',
        'latencyPercentile999InMs',
        'measuredQueriesPerSecond',
        'state',
        'name',
        'createdTime',
        'error'
    ]

    _details_keys_error = [
        'name',
        'state',
        'requestedCpu',
        'requestedMemoryInGB',
        'requestedQueriesPerSecond',
        'error',
        'errorLogsUri',
        'createdTime'
    ]

    def __init__(self, workspace, name):
        """Initialize the _ModelEvaluationResultBase object.

        :param workspace: The workspace object containing the model.
        :type workspace: azureml.core.Workspace
        :param name: The name of the profile to construct and retrieve.
        :type name: str
        :rtype: azureml.core.profile._ModelEvaluationResultBase
        """
        self.workspace = workspace
        self.name = name
        # setting default values for properties needed to communicate with MMS
        self.create_operation_id = None
        self._model_test_result_suffix = None
        self._model_test_result_params = {}

        # TODO: remove once the old workflow is deprecated
        self.image_id = None
        self._expected_payload_keys = self.__class__._expected_payload_keys

        super(_ModelEvaluationResultBase, self).__init__()

    def _initialize(self, obj_dict):
        """Initialize the base properites of an instance of subtype of _ModelEvaluationResultBase.

        This is used because the constructor is used as a getter.

        :param workspace:
        :type workspace: azureml.core.Workspace
        :param obj_dict:
        :type obj_dict: dict
        :return:
        :rtype: None
        """
        self.name = obj_dict.get('name')
        self.description = obj_dict.get('description')
        self.created_time = (
            parse(obj_dict['createdTime']) if 'createdTime' in obj_dict else None
        )
        self.id = obj_dict.get('id')
        container_resource_requirements = obj_dict.get('containerResourceRequirements')
        self.requested_cpu = (
            container_resource_requirements['cpu']
            if container_resource_requirements
            else None
        )
        self.requested_memory_in_gb = (
            container_resource_requirements['memoryInGB']
            if container_resource_requirements
            else None
        )
        self.requested_queries_per_second = obj_dict.get('requestedQueriesPerSecond')
        self.input_dataset_id = obj_dict.get('inputDatasetId')
        self.state = obj_dict.get('state')
        self.model_ids = obj_dict.get('modelIds')
        # detail properties
        self.max_utilized_memory = obj_dict.get('maxUtilizedMemoryInGB')
        self.max_utilized_cpu = obj_dict.get('maxUtilizedCpu')
        self.measured_queries_per_second = obj_dict.get('measuredQueriesPerSecond')
        self.environment = obj_dict.get('environment')
        self.error = obj_dict.get('error')
        self.error_logs_url = obj_dict.get('errorLogsUri')
        self.total_queries = obj_dict.get('totalQueries')
        self.success_queries = obj_dict.get('successQueries')
        self.success_rate = obj_dict.get('successRate')
        self.average_latency_in_ms = obj_dict.get('averageLatencyInMs')
        self.latency_percentile_50_in_ms = obj_dict.get('latencyPercentile50InMs')
        self.latency_percentile_90_in_ms = obj_dict.get('latencyPercentile90InMs')
        self.latency_percentile_95_in_ms = obj_dict.get('latencyPercentile95InMs')
        self.latency_percentile_99_in_ms = obj_dict.get('latencyPercentile99InMs')
        self.latency_percentile_999_in_ms = obj_dict.get('latencyPercentile999InMs')

    # TODO: once old worklflow is deprecated set this method to be a classmethod and use class variable
    def _validate_get_payload(self, payload):
        """Validate the returned _ModelEvaluationResultBase payload.

        :param payload:
        :type payload: dict
        :return:
        :rtype: None
        """
        for payload_key in self._expected_payload_keys:
            if payload_key not in payload:
                raise WebserviceException(
                    'Invalid payload for %s, missing %s:\n %s'
                    % (self.__class__._model_eval_type, payload_key, payload)
                )

    def _get_operation_state(self):
        """Get the current async operation state for the a model test operation.

        :return:
        :rtype: (str, dict)
        """
        resp_content = get_mms_operation(self.workspace, self.create_operation_id)
        state = resp_content['state']
        error = resp_content['error'] if 'error' in resp_content else None
        async_operation_request_id = resp_content['parentRequestId']
        return state, error, async_operation_request_id

    def _update_creation_state(self):
        """Refresh the current state of the in-memory object.

        Perform an in-place update of the properties of the object based on the current state of the
        corresponding cloud object. Primarily useful for manual polling of creation state.

        :raises: azureml.exceptions.WebserviceException
        """
        resp = get_operation_output(self.workspace, self._model_test_result_suffix, self._model_test_result_params)
        if resp.status_code != 200:
            error_message = 'Model {} result with name {}'.format(
                self.__class__._model_eval_type, self.name
            )
            if self.image_id:
                # TODO: deprecate
                error_message += ', Model package {}'.format(self.image_id)
            error_message += ' not found in provided workspace'
            raise WebserviceException(error_message)
        content = resp.content
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        if self.image_id:
            # TODO: deprecate
            model_test_json = json.loads(content)
        else:
            model_test_json = json.loads(content)['value'][0]
        self._validate_get_payload(model_test_json)
        self._initialize(model_test_json)

    @abstractmethod
    def wait_for_completion(self, show_output=False):
        """Wait for the model evaluation process to finish.

        :param show_output: Boolean option to print more verbose output. Defaults to False.
        :type show_output: bool
        """
        if not (self.workspace and self.create_operation_id):
            raise UserErrorException('wait_for_completion operation cannot be performed on this object.'
                                     'Make sure the object was created via the appropriate method '
                                     'in the Model class')
        operation_state, error, request_id = self._get_operation_state()
        self.parent_request_id = request_id
        current_state = operation_state
        if show_output:
            sys.stdout.write('{}'.format(current_state))
            sys.stdout.flush()
        while operation_state not in ['Cancelled', 'Succeeded', 'Failed', 'TimedOut']:
            time.sleep(5)
            operation_state, error, _ = self._get_operation_state()
            if show_output:
                sys.stdout.write('.')
                if operation_state != current_state:
                    sys.stdout.write('\n{}'.format(operation_state))
                    current_state = operation_state
                sys.stdout.flush()
        sys.stdout.write('\n')
        sys.stdout.flush()
        module_logger.info(
            'Model {} operation with name {} finished operation {}\n'.format(
                self.__class__._model_eval_type, self.name, operation_state
            )
        )
        if operation_state == 'Failed':
            if error and 'statusCode' in error and 'message' in error:
                module_logger.info(
                    'Model {} failed with\n'
                    'StatusCode: {}\n'
                    'Message: {}\n'
                    'Operation ID: {}\n'
                    'Request ID: {}\n'.format(
                        self.__class__._model_eval_type,
                        error['statusCode'],
                        error['message'],
                        self.create_operation_id,
                        self.parent_request_id
                    )
                )
            else:
                module_logger.info(
                    'Model profiling failed, unexpected error response:\n'
                    '{}\n'
                    'Operation ID: {}\n'
                    'Request ID: {}\n'.format(
                        error,
                        self.create_operation_id,
                        self.parent_request_id)
                )
        self._update_creation_state()

    def serialize(self):
        """Convert this _ModelEvaluationResultBase object into a json serialized dictionary.

        :return: The json representation of this _ModelEvaluationResultBase
        :rtype: dict
        """
        created_time = self.created_time.isoformat() if self.created_time else None
        return {
            'id': self.id,
            'name': self.name,
            'createdTime': created_time,
            'state': self.state,
            'description': self.description,
            'requestedCpu': self.requested_cpu,
            'requestedMemoryInGB': self.requested_memory_in_gb,
            'requestedQueriesPerSecond': self.requested_queries_per_second,
            'inputDatasetId': self.input_dataset_id,
            'maxUtilizedMemoryInGB': self.max_utilized_memory,
            'totalQueries': self.total_queries,
            'successQueries': self.success_queries,
            'successRate': self.success_rate,
            'averageLatencyInMs': self.average_latency_in_ms,
            'latencyPercentile50InMs': self.latency_percentile_50_in_ms,
            'latencyPercentile90InMs': self.latency_percentile_90_in_ms,
            'latencyPercentile95InMs': self.latency_percentile_95_in_ms,
            'latencyPercentile99InMs': self.latency_percentile_99_in_ms,
            'latencyPercentile999InMs': self.latency_percentile_999_in_ms,
            'modelIds': self.model_ids,
            'environment': self.environment,
            'maxUtilizedCpu': self.max_utilized_cpu,
            'measuredQueriesPerSecond': self.measured_queries_per_second,
            'error': self.error,
            'errorLogsUri': self.error_logs_url
        }


class ModelProfile(_ModelEvaluationResultBase):
    """
    Contains the results of a profiling run.

    A model profile of a model is a resource requirement recommendation. A ModelProfile object is returned from
    the :meth:`azureml.core.model.Model.profile` method of the :class:`azureml.core.model.Model` class.

    .. remarks::

        The following example shows how to return a ModelProfile object.

        .. code-block:: python

            profile = Model.profile(ws, "profilename", [model], inference_config, input_dataset=dataset)
            profile.wait_for_profiling(True)
            profiling_details = profile.get_details()
            print(profiling_details)

    :param workspace: The workspace object containing the model.
    :type workspace: azureml.core.Workspace
    :param image_id: ID of the image associated with the profile name. The 'image_id' property has been deprecated
                        and will be removed in a future release. Please refrain
                        from passing it to the constructor.
    :type image_id: str
    :param name: The name of the profile to create and retrieve.
    :type name: str
    :param description: Field for profile description. 'description' constructor parameter
                        has been deprecated and will be removed in a future release. Please refrain
                        from passing it to the constructor.
    :type description: str
    :param input_data: The input data used for profiling. The 'input_data' constructor parameter
                        has been deprecated and will be removed in a future release. Please refrain
                        from passing it to the constructor.
    :type input_data: varies
    :param tags: Dictionary of mutable tags. 'tags' constructor parameter
                    has been deprecated and will be removed in a future release. Please refrain
                    from passing it to the constructor.
    :type tags: dict[str, str]
    :param properties: Dictionary of appendable properties. The 'properties' constructor parameter
                        has been deprecated and will be removed in a future release. Please refrain
                        from passing it to the constructor.
    :type properties: dict[str, str]
    :param recommended_memory: The memory recommendation result from profiling in GB. The 'recommended_memory'
                                constructor parameter has been deprecated and will be removed in a future release.
                                Please refrain from passing it to the constructor.
    :type recommended_memory: float
    :param recommended_cpu: The cpu recommendation result from profiling in cores. The 'recommended_cpu'
                            constructor parameter has been deprecated and will be removed in a future release.
                            Please refrain from passing it to the constructor.
    :type recommended_cpu: float
    :param recommended_memory_latency: The 90th percentile latency of requests while profiling with
                                        recommended memory value. The 'recommended_memory_latency' constructor
                                        parameter has been deprecated and will be removed in a future release.
                                        Please refrain from passing it to the constructor.
    :type recommended_memory_latency: float
    :param recommended_cpu_latency: The 90th percentile latency of requests while profiling with
                                    recommended cpu value. 'recommended_cpu_latency' constructor
                                    parameter has been deprecated and will be removed in a future release.
                                    Please refrain from passing it to the constructor.
    :type recommended_cpu_latency: float
    :param profile_result_url: URL to profiling results. 'profile_result_url' constructor
                                parameter has been deprecated and will be removed in a future release.
                                Please refrain from passing it to the constructor.
    :type profile_result_url: str
    :param error: The 'error' constructor parameter has been deprecated and will be removed in a future
                       release. Please refrain from passing it to the constructor.
    :type error: str
    :param error_logs: URL to profiling error logs. The 'error_logs' constructor
                        parameter has been deprecated and will be removed in a future release.
                        Please refrain from passing it to the constructor.
    :type error_logs: str
    :rtype: azureml.core.profile.ModelProfile
    :raises: azureml.exceptions.WebserviceException
    """

    _model_eval_type = 'profiling'
    _general_mms_suffix = '/profiles'
    _expected_payload_keys = [
        'name',
        'description',
        'id',
        'state',
        'inputDatasetId',
        'containerResourceRequirements',
        'requestedQueriesPerSecond',
        'createdTime',
        'modelIds'
    ]
    _deprecated_expected_payload_keys = [
        'name',
        'description',
        'imageId',
        'inputData',
        'createdTime',
        'kvTags',
        'properties'
    ]

    _details_keys_success = _ModelEvaluationResultBase._details_keys_success + [
        'recommendedMemoryInGB',
        'recommendedCpu'
    ]

    _deprecated_details_keys_error = ['name', 'state', 'error', 'profilingErrorLogs']

    # TODO: deprecate all the parameters except workspace and name
    def __init__(self, workspace, image_id, name, description=None, input_data=None, tags=None,
                 properties=None, recommended_memory=None, recommended_cpu=None, recommended_memory_latency=None,
                 recommended_cpu_latency=None, profile_result_url=None, error=None, error_logs=None):
        """Initialize the ModelProfile object.

        :param workspace: The workspace object containing the model.
        :type workspace: azureml.core.Workspace
        :param image_id: ID of the image associated with the profile name. 'image_id' property has been deprecated
                         and will be removed in a future release. Please migrate to using the new profiling
                         workflow with input_dataset parameter.
        :type image_id: str
        :param name: The name of the profile to create and retrieve.
        :type name: str
        :param description: Field for profile description. 'description' constructor parameter
                            has been deprecated and will be removed in a future release. Please refrain
                            from passing it to the constructor.
        :type description: str
        :param input_data: The input data used for profiling. 'input_data' constructor parameter
                           has been deprecated and will be removed in a future release. Please refrain
                           from passing it to the constructor.
        :type input_data: varies
        :param tags: Dictionary of mutable tags. 'tags' constructor parameter
                     has been deprecated and will be removed in a future release. Please refrain
                     from passing it to the constructor.
        :type tags: dict[str, str]
        :param properties: Dictionary of appendable properties. 'properties' constructor parameter
                           has been deprecated and will be removed in a future release. Please refrain
                           from passing it to the constructor.
        :type properties: dict[str, str]
        :param recommended_memory: The memory recommendation result from profiling in GB. 'recommended_memory'
                                   constructor parameter has been deprecated and will be removed in a future release.
                                   Please refrain from passing it to the constructor.
        :type recommended_memory: float
        :param recommended_cpu: The cpu recommendation result from profiling in cores. 'recommended_cpu'
                                constructor parameter has been deprecated and will be removed in a future release.
                                Please refrain from passing it to the constructor.
        :type recommended_cpu: float
        :param recommended_memory_latency: The 90th percentile latency of requests while profiling with
                                           recommended memory value. 'recommended_memory_latency' constructor
                                           parameter has been deprecated and will be removed in a future release.
                                           Please refrain from passing it to the constructor.
        :type recommended_memory_latency: float
        :param recommneded_cpu_latency: The 90th percentile latency of requests while profiling with
                                        recommended cpu value. 'recommneded_cpu_latency' constructor
                                        parameter has been deprecated and will be removed in a future release.
                                        Please refrain from passing it to the constructor.
        :type recommended_cpu_latency: float
        :param profile_result_url: URL to profiling results. 'profile_result_url' constructor
                                   parameter has been deprecated and will be removed in a future release.
                                   Please refrain from passing it to the constructor.
        :type profile_result_url: str
        :param error: 'error' constructor parameter has been deprecated and will be removed in a future
                       release. Please refrain from passing it to the constructor.
        :type error: str
        :param error_logs: URL to profiling error logs. 'error_logs' constructor
                           parameter has been deprecated and will be removed in a future release.
                           Please refrain from passing it to the constructor.
        :type error_logs: str
        :rtype: azureml.core.profile.ModelProfile
        :raises: azureml.exceptions.WebserviceException
        """
        super(ModelProfile, self).__init__(workspace, name)

        # TODO: deprecate. Old Workflow support
        if image_id:
            warnings.warn('image_id property has been deprecated and will be removed in a future release.'
                          ' Please migrate to using the new profiling workflow with input_dataset parameter.'
                          ' Learn how to create datasets: %s.' %
                          HOW_TO_CREATE_DATASET_URL, category=DeprecationWarning, stacklevel=2)
            self.image_id = image_id
            self._expected_payload_keys = (
                self._deprecated_expected_payload_keys
            )
            if workspace and name:
                self._model_test_result_suffix = '/images/{0}/profiles/{1}'.format(
                    image_id, name
                )
        # new endpoint
        elif workspace and name:
            self._model_test_result_suffix = self._general_mms_suffix
            self._model_test_result_params = {'name': name}

        if self._model_test_result_suffix:
            # retrieve object from MMS and update state
            self._update_creation_state()
        else:
            # sets all properties associated with profiling result to None
            self._initialize({})
        if (description or input_data or tags or properties or recommended_memory or recommended_cpu or
           recommended_memory_latency or recommended_cpu_latency or profile_result_url or error or error_logs):
            warnings.warn('All ModelProfile constructor parameters except for "workspace" and "name"'
                          ' have been deprecated and will be removed in a future release. Please refrain'
                          ' from passing them to the constructor.', category=DeprecationWarning, stacklevel=2)

    def _initialize(self, obj_dict):
        """Initialize the Profile instance.

        This is used because the constructor is used as a getter.

        :param workspace:
        :type workspace: azureml.core.Workspace
        :param obj_dict:
        :type obj_dict: dict
        :return:
        :rtype: None
        """
        super(ModelProfile, self)._initialize(obj_dict)
        self.recommended_memory = obj_dict.get('recommendedMemoryInGB')
        self.recommended_cpu = obj_dict.get('recommendedCpu')
        if self.image_id:
            # TODO: deprecate
            # old workflow required properties
            self.imageId = obj_dict.get('imageId')
            self.tags = obj_dict.get('kvTags')
            self.properties = obj_dict.get('properties')
            # old workflow detail properties
            # once  the new workflow is extended to test on a grid, recommendationLatencyInMs should be removed
            # since the details latency metrics will reflect the latency measurements on the recommended instance.
            self.recommendation_latency = obj_dict.get('recommendationLatencyInMs')
            self.recommended_memory_latency = obj_dict.get(
                'recommendedMemoryLatencyInMs'
            )
            self.recommended_cpu_latency = obj_dict.get('recommendedCpuLatencyInMs')
            self.input_data = obj_dict.get('inputData')
            self.profile_result_url = obj_dict.get('profileRunResult')
            self.error_logs = obj_dict.get('profilingErrorLogs')

    def wait_for_completion(self, show_output=False):
        """Wait for the model to finish profiling.

        :param show_output: Boolean option to print more verbose output. Defaults to False.
        :type show_output: bool
        """
        super().wait_for_completion(show_output)
        if self.state == 'Failed':
            warnings.warn(PROFILE_FAILURE_MESSAGE % (self.error['message'], self.parent_request_id),
                          category=UserWarning, stacklevel=2)
        elif self.error:
            warnings.warn(PROFILE_PARTIAL_SUCCESS_MESSAGE % self.error['message'],
                          category=UserWarning, stacklevel=2)

    # TODO: needs to be deprecated
    def wait_for_profiling(self, show_output=False):
        """Wait for the model to finish profiling.

        DEPRECATED. The ``wait_for_profiling`` method has been deprecated and will be removed in a future release.
        Migrate to the :meth:`wait_for_completion` method.

        :param show_output: Whether to print more verbose output. Defaults to False.
        :type show_output: bool
        """
        warnings.warn('ModelProfile.wait_for_profiling() method has been deprecated and will be removed'
                      ' in a future release. Please migrate to ModelProfile.wait_for_completion().',
                      category=DeprecationWarning, stacklevel=2)
        self.wait_for_completion(show_output)

    def serialize(self):
        """Convert this Profile into a JSON serialized dictionary.

        :return: The JSON representation of this Profile
        :rtype: dict
        """
        if self.image_id:
            # TODO: old workflow - to be deprecated
            created_time = self.created_time.isoformat() if self.created_time else None
            return {
                'name': self.name,
                'createdTime': created_time,
                'description': self.description,
                'inputData': self.input_data,
                'tags': self.tags,
                'properties': self.properties,
                'recommendedMemoryInGB': self.recommended_memory,
                'recommendedCpu': self.recommended_cpu,
                'recommendationLatencyInMs': self.recommendation_latency,
                'recommendedMemoryLatencyInMs': self.recommended_memory_latency,
                'recommendedCpuLatencyInMs': self.recommended_cpu_latency,
                'profileRunResult': self.profile_result_url,
                'state': self.state,
                'error': self.error,
                'profilingErrorLogs': self.error_logs
            }
        dict_repr = super(ModelProfile, self).serialize()
        dict_repr.update(
            {
                'recommendedMemoryInGB': self.recommended_memory,
                'recommendedCpu': self.recommended_cpu
            }
        )
        return dict_repr

    def __repr__(self):
        """Return the string representation of the ModelProfile object.

        :return: String representation of the ModelProfile object
        :rtype: str
        """
        if self.image_id:
            # TODO: old workflow - to be deprecated
            return (
                '{}(workspace={}, image_id={}, name={}, input_data={}, recommended_memory={}, recommended_cpu={}, '
                'profile_result_url={}, error={}, error_logs={}, tags={}, '
                'properties={})'.format(
                    self.__class__.__name__,
                    self.workspace.__repr__(),
                    self.image_id,
                    self.name,
                    self.input_data,
                    self.recommended_memory,
                    self.recommended_cpu,
                    self.profile_result_url,
                    self.error,
                    self.error_logs_url,
                    self.tags,
                    self.properties
                )
            )
        str_repr = []
        str_repr.append(('workspace' + '=%s') % repr(self.workspace))
        for key in self.__dict__:
            if key[0] != '_' and key not in ['workspace']:
                str_repr.append((key + '=%s') % self.__dict__[key])
        str_repr = '%s(%s)' % (self.__class__.__name__, ', '.join(str_repr))
        return str_repr

    def get_details(self):
        """Get the details of the profiling result.

        Return the the observed metrics (various latency percentiles, maximum utilized cpu and memory, etc.)
        and recommended resource requirements in case of a success.

        :return: A dictionary of recommended resource requirements.
        :rtype: dict[str, float]
        """
        dict_repr = self.serialize()
        if dict_repr['state'] == 'Succeeded':
            success_repr = {
                k: dict_repr[k]
                for k in dict_repr
                if (
                    dict_repr[k] is not None and
                    k in self.__class__._details_keys_success
                )
            }
            if 'error' in success_repr:
                warnings.warn(
                    PROFILE_PARTIAL_SUCCESS_MESSAGE % success_repr['error']['message'],
                    category=UserWarning, stacklevel=2)
            return success_repr
        if self.image_id:
            # TODO: deprecate old workflow for failure case
            return {
                k: dict_repr[k]
                for k in dict_repr
                if (
                    dict_repr[k] is not None and
                    k in self.__class__._deprecated_details_keys_error
                )
            }
        return {
            k: dict_repr[k]
            for k in dict_repr
            if (dict_repr[k] is not None and k in self.__class__._details_keys_error)
        }

    # TODO: deprecate the get_results method in favor of get_details
    def get_results(self):
        """Return the recommended resource requirements from the profiling run to the user.

        DEPRECATED. The ``get_results`` method has been deprecated and will be removed in a future release.
        Migrate to the :meth:`get_details` method.

        :return: Dictionary of recommended resource requirements
        :rtype: dict[str, float]
        """
        warnings.warn('ModelProfile.get_results() method has been deprecated and will be removed in a future release.'
                      ' Please migrate to ModelProfile.get_details().', category=DeprecationWarning, stacklevel=2)
        if self.image_id:
            # TODO: deprecate old workflow
            if self.recommended_cpu is None or self.recommended_memory is None:
                operation_state, _, _ = self._get_operation_state()
                module_logger.info(
                    'One or more of the resource recommendations are missing.\n'
                    'The model profiling operation with name {}, for model package {}, is '
                    'in {} state.\n'.format(self.name, self.image_id, operation_state)
                )
                if self.error_logs:
                    module_logger.info('Error logs: {}\n'.format(self.error_logs))
                else:
                    module_logger.info(
                        'If the profiling run is not in a terminal state, use the '
                        'wait_for_profiling(True) method to wait for the model to finish profiling.\n'
                    )

            return {
                PROFILE_RECOMMENDED_CPU_KEY: self.recommended_cpu,
                PROFILE_RECOMMENDED_MEMORY_KEY: self.recommended_memory,
            }
        return self.get_details()
