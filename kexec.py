# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
This is an example dag for using the Kubernetes Executor.
"""
import os
import time

import airflow
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(0)
}

dag = DAG(
    dag_id='example_kubernetes_executor', default_args=args,
    schedule_interval=None
)

def print_stuff():  # pylint: disable=missing-docstring
    time.sleep(60)
    print("stuff!")


def use_zip_binary():
    """
    Checks whether Zip is installed.
    :return: True if it is installed, False if not.
    :rtype: bool
    """
    return_code = os.system("zip")
    assert return_code == 0


start_task = PythonOperator(
    task_id="start_task", python_callable=print_stuff, dag=dag,
    executor_config={"KubernetesExecutor": {"image": "python:latest"}}
)
