"""Built-in task definitions."""

import typing

from . import _task
from . import _types

if typing.TYPE_CHECKING:  # pragma: no cover
    from . import _context


# Fix Engine documentation when updating this.
__all__ = ['Assert', 'Block', 'Fail', 'Log', 'Return', 'Vars']


class Assert(_task.Task):
    """An assertion.

    Fails if at least one of the provided statements is false:

    .. code-block:: yaml

        - vars:
            some_value: 42

        - assert:
            - some_value is defined
            - some_value == 42

    .. versionadded:: 1.1
    """

    required_params = {"that": None}
    """Requires one or more statements as a list or a string."""

    optional_params = {"fail_msg": None}
    """Can accept an optional failure message."""

    singleton_param = "that"
    """The statement list can be provided directly to ``assert``."""

    def validate(
        self,
        params: '_context.Namespace',
        context: '_context.Context',
    ) -> None:
        super().validate(params, context)
        that = params.get_raw('that')
        if isinstance(that, str):
            params['that'] = [that]
        elif not isinstance(that, list):
            raise TypeError(f"'that' must be a list or a string, got '{that}'")

    def execute(
        self,
        params: '_context.Namespace',
        context: '_context.Context',
    ) -> None:
        that = params.get_raw('that')
        for expr in that:
            value = self.engine.environment.evaluate_code(str(expr), context)
            if not value:
                fail_msg = params.get('fail_msg')
                if not fail_msg:
                    fail_msg = f"`{expr}` evaluated to False"
                raise AssertionError(fail_msg)


class Block(_task.Task):
    """Grouping of tasks.

    Blocks can be used to share top-level parameters, e.g. a condition:

    .. code-block:: yaml

        - block:
            - task1:
            - task2:
            - task3:
          when: enable_all_three_tasks
    """

    required_params = {"tasks": list}
    """Requires a task list."""

    singleton_param = "tasks"
    """The task list can be provided directly to ``block``."""

    def validate(
        self,
        params: '_context.Namespace',
        context: '_context.Context',
    ) -> None:
        super().validate(params, context)
        tasks = [self.engine._load_task(task) for task in params['tasks']]
        params['tasks'] = tasks

    def execute(
        self,
        params: typing.Mapping[str, typing.Any],
        context: '_context.Context',
    ) -> None:
        for task in params["tasks"]:
            task(context)


class Fail(_task.Task):
    """Fail the execution.

    Often used in combination with some condition.

    .. code-block:: yaml

        - name: fail if the path is not defined
          fail: path must be defined
          when: path is undefined
    """

    required_params = {'msg': str}
    """Requires a string message."""

    singleton_param = 'msg'
    """The message can be provided directly to ``fail``."""

    def execute(
        self,
        params: typing.Mapping[str, typing.Any],
        context: '_context.Context',
    ) -> None:
        raise _types.Aborted(params["msg"])


class Log(_task.Task):
    """Log something.

    Uses standard Python logging and understands 4 levels: ``debug``, ``info``,
    ``warning`` and ``error``.

    .. code-block:: yaml

        - log:
            info: "checking of something bad has happened..."
        - log:
            error: "oh no, something bad has happened!"
          when: something_bad is happened
    """

    optional_params = {
        key: str for key in ("debug", "info", "warning", "error")}
    """Requires at least one of the levels and its message."""

    allow_empty = False

    def execute(
        self,
        params: typing.Mapping[str, typing.Any],
        context: '_context.Context'
    ) -> None:
        for key, value in params.items():
            getattr(self.engine.logger, key)(value)


class Return(_task.Task):
    """Return a value to the caller.

    This is a unique feature of MiniScript not present in Ansible. The value
    will be returned from :meth:`Engine.execute`.

    .. code-block:: yaml

        - name: return the answer
          return: 42
    """

    optional_params = {'result': None}
    """Optionally accepts a result (otherwise the result is ``None``)."""

    singleton_param = 'result'
    """The result can be provided directly to ``return``."""

    def execute(
        self,
        params: typing.Mapping[str, typing.Any],
        context: '_context.Context',
    ) -> None:
        raise _types.FinishScript(params.get('result'))


class Vars(_task.Task):
    """Set variables.

    Similar to ``set_fact`` in Ansible, but we don't have facts. The variables
    are stored in the context.

    .. code-block:: yaml

        - vars:
            num1: 2
            num2: 2
        - log:
            info: "Look ma, I can multiply: {{ num1 * num2 }}"
    """

    free_form = True
    """Accepts any parameters."""

    def execute(
        self,
        params: typing.Mapping[str, typing.Any],
        context: '_context.Context'
    ) -> None:
        for key, value in params.items():
            context[key] = value
