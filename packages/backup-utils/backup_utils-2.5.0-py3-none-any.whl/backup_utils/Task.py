import subprocess
import re
import docker
from .utils import which


__all__ = ["Task"]


class Task(object):
    """
    Parent Task class,
    if you create a Task, your class must be a child of this class.
    """

    default_cmd = ""

    def __init__(self, **kwargs):
        """
        Create a Task object,
        take the binary command and multiple other params use as config.

        :param kwargs: Other params that will be used for the configuration.
                       Can be very different between each task.
        :type kwargs: dict

        .. seealso:: which()
        """
        self._container = None
        self._config = dict(kwargs)
        cmd = self._config.get("cmd", self.default_cmd)
        container_name = self._config.get("docker_container_name", None)
        if container_name is not None:
            client = docker.from_env()
            for container in client.containers.list():
                if re.match(container_name, container.name):
                    self._container = container
                    break
        else:
            self._cmd = which(cmd)
            if not self._cmd:
                raise ValueError("Can't find '{}' binary".format(cmd))

    def _exec(self, cmds, env=None):
        """
        Method to run a command in the shell and simplify, shortcut of `subprocess.run()`

        :param cmds: Comand and argument to execute.
        :param env: To override the current environment and to add the environment variable.
        :type cmds: iterable
        :type env: dict
        :return: The result of the command.
        :rtype: subprocess.CompletedProcess

        .. seealso:: subprocess.run()
        """
        if self._container is not None:
            exit_code, output = self._container.exec_run(cmds, demux=True)
            return subprocess.CompletedProcess(
                cmds, exit_code, stdout=output[0], stderr=output[1]
            )
        return subprocess.run(
            cmds, env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def _hook(self, hook_name):
        """
        Run fetch and run a hook if this one exists.

        :param hook_name: An ID to differentiated each hook.
        :type hook_name: str
        """
        if hook_name in self._config.keys():
            hook_bin = which(self._config[hook_name])
            if not hook_bin:
                raise ValueError(
                    "Can't find '{}' binary for {} hook".format(hook_bin, hook_name)
                )
            self._exec(hook_bin)

    def _run(self):
        """
        The core of the object which will process the Task.

        .. seealso:: start()
        """
        self._exec(self._cmd)

    def start(self):
        """
        Start a task and launch hook.
        Prefer this method instead of `_run()`.

        .. seealso:: _run()
        """
        self._hook("pre_hook")
        self._run()
        self._hook("post_hook")
