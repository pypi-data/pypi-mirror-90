#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020-2021 The WorkflowHub Team.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from typing import Dict, List, Optional

from .abstract_recipe import WorkflowRecipe
from ...common.file import FileLink
from ...common.task import Task
from ...common.workflow import Workflow


class SeismologyRecipe(WorkflowRecipe):
    """A Seismology workflow recipe class for creating synthetic workflow traces.

    :param num_pairs: The number of pair of signals to estimate earthquake STFs.
    :type num_pairs: int
    :param data_footprint: The upper bound for the workflow total data footprint (in bytes).
    :type data_footprint: int
    :param num_tasks: The upper bound for the total number of tasks in the workflow.
    :type num_tasks: int
    :param runtime_factor: The factor of which tasks runtime will be increased/decreased.
    :type runtime_factor: float
    :param input_file_size_factor: The factor of which tasks input files size will be increased/decreased.
    :type input_file_size_factor: float
    :param output_file_size_factor: The factor of which tasks output files size will be increased/decreased.
    :type output_file_size_factor: float
    """

    def __init__(self,
                 num_pairs: Optional[int] = 2,
                 data_footprint: Optional[int] = 0,
                 num_tasks: Optional[int] = 3,
                 runtime_factor: Optional[float] = 1.0,
                 input_file_size_factor: Optional[float] = 1.0,
                 output_file_size_factor: Optional[float] = 1.0
                 ) -> None:
        """Create an object of the Seismology workflow recipe."""
        super().__init__("Seismology",
                         data_footprint,
                         num_tasks,
                         runtime_factor,
                         input_file_size_factor,
                         output_file_size_factor)

        self.num_pairs: int = num_pairs

    @classmethod
    def from_num_tasks(cls,
                       num_tasks: int,
                       runtime_factor: Optional[float] = 1.0,
                       input_file_size_factor: Optional[float] = 1.0,
                       output_file_size_factor: Optional[float] = 1.0
                       ) -> 'SeismologyRecipe':
        """
        Instantiate a Seismology workflow recipe that will generate synthetic workflows up to
        the total number of tasks provided.

        :param num_tasks: The upper bound for the total number of tasks in the workflow (at least 3).
        :type num_tasks: int
        :param runtime_factor: The factor of which tasks runtime will be increased/decreased.
        :type runtime_factor: float
        :param input_file_size_factor: The factor of which tasks input files size will be increased/decreased.
        :type input_file_size_factor: float
        :param output_file_size_factor: The factor of which tasks output files size will be increased/decreased.
        :type output_file_size_factor: float

        :return: A Seismology workflow recipe object that will generate synthetic workflows up
                 to the total number of tasks provided.
        :rtype: SeismologyRecipe
        """
        if num_tasks < 3:
            raise ValueError("The upper bound for the number of tasks should be at least 3.")

        return cls(num_pairs=num_tasks - 1,
                   data_footprint=None,
                   num_tasks=num_tasks,
                   runtime_factor=runtime_factor,
                   input_file_size_factor=input_file_size_factor,
                   output_file_size_factor=output_file_size_factor)

    @classmethod
    def from_num_pairs(cls,
                       num_pairs: int,
                       runtime_factor: Optional[float] = 1.0,
                       input_file_size_factor: Optional[float] = 1.0,
                       output_file_size_factor: Optional[float] = 1.0
                       ) -> 'SeismologyRecipe':
        """
        Instantiate a Seismology workflow recipe that will generate synthetic workflows using
        the defined number of pairs.

        :param num_pairs: The number of pair of signals to estimate earthquake STFs (at least 2).
        :type num_pairs: int
        :param runtime_factor: The factor of which tasks runtime will be increased/decreased.
        :type runtime_factor: float
        :param input_file_size_factor: The factor of which tasks input files size will be increased/decreased.
        :type input_file_size_factor: float
        :param output_file_size_factor: The factor of which tasks output files size will be increased/decreased.
        :type output_file_size_factor: float

        :return: A Seismology workflow recipe object that will generate synthetic workflows
                 using the defined number of pairs.
        :rtype: SeismologyRecipe
        """
        if num_pairs < 2:
            raise ValueError("The number of pairs should be at least 2.")

        return cls(num_pairs=num_pairs,
                   data_footprint=None,
                   num_tasks=None,
                   runtime_factor=runtime_factor,
                   input_file_size_factor=input_file_size_factor,
                   output_file_size_factor=output_file_size_factor)

    def build_workflow(self, workflow_name: Optional[str] = None) -> Workflow:
        """Generate a synthetic workflow trace of a Seismology workflow.

        :param workflow_name: The workflow name
        :type workflow_name: int

        :return: A synthetic workflow trace object.
        :rtype: Workflow
        """
        workflow = Workflow(name=self.name + "-synthetic-trace" if not workflow_name else workflow_name, makespan=None)
        self.task_id_counter: int = 1
        sg1iterdecon_tasks: List[Task] = []

        for _ in range(0, self.num_pairs):
            # sG1IterDecon task
            task_name = self._generate_task_name("sG1IterDecon")
            sg1iterdecon_task = self._generate_task('sG1IterDecon', task_name,
                                                    files_recipe={FileLink.INPUT: {".lht": 2}})
            sg1iterdecon_tasks.append(sg1iterdecon_task)
            workflow.add_node(task_name, task=sg1iterdecon_task)

        # wrapper_siftSTFByMisfit task
        input_files = []
        for j in sg1iterdecon_tasks:
            for f in j.files:
                if f.link == FileLink.OUTPUT:
                    input_files.append(f)

        task_name = self._generate_task_name('wrapper_siftSTFByMisfit')
        wrapper_task = self._generate_task('wrapper_siftSTFByMisfit', task_name, input_files)
        workflow.add_node(task_name, task=wrapper_task)
        for j in sg1iterdecon_tasks:
            workflow.add_edge(j.name, wrapper_task.name)

        self.workflows.append(workflow)
        return workflow

    def _workflow_recipe(self) -> Dict:
        """
        Recipe for generating synthetic traces of the Seismology workflow. Recipes can be
        generated by using the :class:`~workflowhub.trace.trace_analyzer.TraceAnalyzer`.

        :return: A recipe in the form of a dictionary in which keys are task prefixes.
        :rtype: Dict[str, Any]
        """
        return {
            "sG1IterDecon": {
                "runtime": {
                    "min": 0.087,
                    "max": 5.615,
                    "distribution": {
                        "name": "argus",
                        "params": [
                            3.2918805879481845e-05,
                            -0.7183748055932565,
                            1.7191511240068986
                        ]
                    }
                },
                "input": {
                    ".lht": {
                        "distribution": {
                            "name": "trapz",
                            "params": [
                                1.0,
                                1.0,
                                -0.10500000000000001,
                                1.2
                            ]
                        },
                        "min": 1024,
                        "max": 16012
                    }
                },
                "output": {
                    ".stf": {
                        "distribution": {
                            "name": "trapz",
                            "params": [
                                1.0,
                                1.0,
                                -0.10500000000000001,
                                1.2
                            ]
                        },
                        "min": 1144,
                        "max": 17016
                    }
                }
            },
            "wrapper_siftSTFByMisfit": {
                "runtime": {
                    "min": 0.089,
                    "max": 1.351,
                    "distribution": {
                        "name": "arcsine",
                        "params": [
                            -0.2258070520586602,
                            1.2258070520586604
                        ]
                    }
                },
                "input": {
                    ".stf": {
                        "distribution": {
                            "name": "trapz",
                            "params": [
                                1.0,
                                1.0,
                                -0.10500000000000001,
                                1.2
                            ]
                        },
                        "min": 1144,
                        "max": 17016
                    },
                    ".py": {
                        "distribution": "None",
                        "min": 0,
                        "max": 0
                    },
                    "siftSTFByMisfit": {
                        "distribution": "None",
                        "min": 1386,
                        "max": 1386
                    }
                },
                "output": {
                    ".gz": {
                        "distribution": {
                            "name": "arcsine",
                            "params": [
                                -0.2258070520586602,
                                1.2258070520586604
                            ]
                        },
                        "min": 63471,
                        "max": 687098
                    }
                }
            }
        }
