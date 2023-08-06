from __future__ import unicode_literals
import os.path
import shutil
import tempfile
import unittest2 as unittest
from .. import tasks
from yangsuite.paths import set_base_path, get_path
from .utilities import (
    canned_input_data,
    canned_output_str,
    canned_output_data,
)


class TestTasks(unittest.TestCase):
    """Tests for task-related functions in tasks.py."""

    testdir = os.path.join(os.path.dirname(__file__), 'data')

    def setUp(self):
        """Function called before starting test execution."""
        set_base_path(self.testdir)
        self.tmpdir = tempfile.mkdtemp()
        self.maxDiff = None

    def tearDown(self):
        """Remove the test directory."""
        shutil.rmtree(self.tmpdir)

    def test_get_category_list(self):
        """Get list of available categories."""
        result = tasks.TaskHandler.get_category_list(self.testdir)
        self.assertEqual([
            'IETF',
            'Openconfig',
            'Variables',
        ], result)

        result = tasks.TaskHandler.get_category_list(self.testdir,
                                                     generated_only=True)
        self.assertEqual([
            'Openconfig',
        ], result)

    def test_get_task_list(self):
        """Get list of all tasks with their categories."""
        data = tasks.TaskHandler.get_task_list(self.testdir)
        comp = canned_output_data('getTaskList.json')
        for key in sorted(data):
            self.assertEqual(sorted(data[key]), sorted(comp.get(key, [])))

    def test_delete_category(self):
        """Test the delete_category classmethod."""
        # Negative test - no such category
        self.assertRaises(tasks.TaskException,
                          tasks.TaskHandler.delete_category,
                          'test', "nonesuch")

        # Positive test - category deleted with all its tasks
        os.rmdir(self.tmpdir)
        shutil.copytree(self.testdir, self.tmpdir)
        set_base_path(self.tmpdir)
        cat_dir = os.path.join(self.tmpdir, 'users', 'test',
                               'testing', 'replays', 'openconfig')
        self.assertTrue(os.path.isdir(cat_dir))
        # category name will be slugified
        tasks.TaskHandler.delete_category('test', 'OpenConfig')
        self.assertFalse(os.path.exists(cat_dir))

    def test_get_replay_variables(self):
        """Test the get_replay_variables classmethod."""
        self.assertRaises(tasks.TaskNotFoundException,
                          tasks.TaskHandler.get_replay_variables,
                          self.tmpdir, 'nonesuch', 'nope')

        self.assertEqual([], tasks.TaskHandler.get_replay_variables(
            os.path.join(self.testdir, 'users', 'test', 'testing', 'replays'),
            'openconfig',
            'oc-int-get'))

        self.assertEqual(
            ['interface_id_1', 'interface_type'],
            tasks.TaskHandler.get_replay_variables(
                os.path.join(self.testdir, 'users', 'test',
                             'testing', 'replays'),
                'variables', 'native interface var'))

        self.assertEqual(
            ['interface_id_1', 'interface_type'],
            tasks.TaskHandler.get_replay_variables(
                os.path.join(self.testdir, 'users', 'test',
                             'testing', 'replays'),
                'variables',
                'custom-variables'))

    def test_retrieve_task(self):
        """Success path of retrieve_task() API."""
        # Deprecated API
        th = tasks.TaskHandler('OC-int-get',
                               get_path('replays_dir', user='test'),
                               {'category': 'Openconfig'})
        data = th.retrieve_task()
        self.assertEqual(
            canned_output_data('oc-int-get.tsk', 'openconfig'), data['task'])

        # New API
        data = tasks.TaskHandler.get_replay(get_path('replays_dir',
                                            user='test'),
                                            'Openconfig',
                                            'OC-int-get')
        self.assertEqual(
            canned_output_data('oc-int-get.tsk', 'openconfig'), data)

    def test_retrieve_variable_task(self):
        """Retrieve task with inserted variables."""
        # Deprecated API
        th = tasks.TaskHandler(
            'Native interface var',
            get_path('replays_dir', user='test'),
            {
                'category': 'Variables',
                'variables': {
                    'interface_id_1': 2,
                    'interface_type': 'GigabitEthernet',
                }
            })
        data = th.retrieve_task()
        yang = data['task']["segments"][0]["yang"]
        config = yang["modules"]["Cisco-IOS-XE-native"]["configs"]
        self.assertEqual(
            canned_output_data('variable-config.json'), config)

        # New API
        data = tasks.TaskHandler.get_replay(
            get_path('replays_dir', user='test'),
            'Variables',
            'Native interface var',
            {'interface_id_1': 2, 'interface_type': 'GigabitEthernet'})
        yang = data['segments'][0]['yang']
        config = yang['modules']['Cisco-IOS-XE-native']['configs']
        self.assertEqual(
            canned_output_data('variable-config.json'), config)

    def test_retrieve_task_negative(self):
        """Failure paths of retrieve_task() API."""
        # Directory doesn't exist at all - init fails
        with self.assertRaises(tasks.TaskNotFoundException):
            th = tasks.TaskHandler('nonexistentTask', 'nonexistentPath',
                                   {'category': 'nonexistentCategory'})

        # Directory exists but not task file - init succeeds, retrieve fails
        th = tasks.TaskHandler('nonexistentTask',
                               get_path('replays_dir', user='test'),
                               {'category': 'IETF'})
        with self.assertRaises(tasks.TaskNotFoundException):
            th.retrieve_task()
        with self.assertRaises(tasks.TaskNotFoundException):
            tasks.TaskHandler.get_replay(get_path('replays_dir', user='test'),
                                         'IETF',
                                         'nonexistentTask')

    def test_save_task_rpc(self):
        """save_task() should succeed with an RPC dict."""
        th = tasks.TaskHandler(
            "IETF get interface",
            self.tmpdir,
            canned_input_data('get_config_ietf_if.json'))
        th.save_task()
        new_task = th.retrieve_task()
        task = tasks.TaskHandler.get_replay(self.tmpdir,
                                            "IETF",
                                            "IETF get interface")

        self.assertEqual(task, new_task['task'])
        # Make sure output file ordering of data is self-constant.
        self.assertEqual(
            open(get_path('replay_file', user='test', category='IETF',
                          replay='IETF get interface')).read(),
            open(os.path.join(self.tmpdir, 'ietf',
                              'ietf-get-interface.tsk')).read())

    def test_save_task_multirpc(self):
        """save_task() should succeed with a dict containing multiple RPCs."""
        th = tasks.TaskHandler("IETF get 2 interfaces",
                               self.tmpdir,
                               canned_input_data('multi_ietf_if.json'))
        th.save_task()
        new_task = th.retrieve_task()
        task = tasks.TaskHandler.get_replay(self.tmpdir,
                                            "IETF",
                                            "IETF get 2 interfaces")
        self.assertEqual(task, new_task['task'])
        # Make sure output file ordering of data is self-constant.
        self.assertEqual(
            open(get_path('replay_file', user='test', category='IETF',
                          replay='IETF get 2 interfaces')).read(),
            open(os.path.join(self.tmpdir, 'ietf',
                              'ietf-get-2-interfaces.tsk')).read())

    def test_delete_task_rpc(self):
        """del_task() should remove task."""
        th1 = tasks.TaskHandler(
            "IETF get interface",
            self.tmpdir,
            canned_input_data('get_config_ietf_if.json'))
        th1.save_task()
        new_task = th1.retrieve_task()
        task = tasks.TaskHandler.get_replay(self.tmpdir,
                                            "IETF",
                                            "IETF get interface")
        self.assertEqual(task, new_task['task'])
        th1.del_task()
        with self.assertRaises(tasks.TaskNotFoundException):
            new_task = th1.retrieve_task()
        with self.assertRaises(tasks.TaskNotFoundException):
            tasks.TaskHandler.get_replay(self.tmpdir,
                                         "IETF",
                                         "IETF get interface")

    def test_delete_last_task(self):
        """del_task() should only remove one task."""
        th3 = tasks.TaskHandler(
            "IETF get interface first",
            self.tmpdir,
            canned_input_data('get_config_ietf_if.json'))
        th3.save_task()
        th1 = tasks.TaskHandler(
            "IETF get interface",
            self.tmpdir,
            canned_input_data('get_config_ietf_if.json'))
        th1.save_task()
        new_task = th1.retrieve_task()
        task = tasks.TaskHandler.get_replay(self.tmpdir,
                                            "IETF",
                                            "IETF get interface")
        self.assertEqual(task, new_task['task'])
        th1.del_task()
        with self.assertRaises(tasks.TaskNotFoundException):
            new_task = th1.retrieve_task()
        first_task = th3.retrieve_task()
        first_task['task'].pop('name')
        task.pop('name')
        self.assertEqual(task, first_task['task'])

    def test_edit_task_data(self):
        """Edit the contents of a task."""
        th = tasks.TaskHandler(
            "IETF get interface",
            self.tmpdir,
            canned_input_data('get_config_ietf_if.json'))
        th.save_task()
        task = th.retrieve_task()
        data = task['task']
        # user now changes values
        data['description'] = "This is a test"
        data['images'] = ['image1', 'image2', 'image3']
        data['platforms'] = ['csr']
        # send in the new values but lets keep the same name/category
        th2 = tasks.TaskHandler(
            "IETF get interface",
            self.tmpdir,
            data)
        th2.edit_task(data['name'], data['category'])
        task2 = th2.retrieve_task()
        self.assertEqual(data, task2['task'])
        # Make sure output file ordering of data is self-constant.
        self.assertEqual(
            canned_output_str('ietf-get-interface-edited-data.tsk'),
            open(os.path.join(self.tmpdir, 'ietf',
                              'ietf-get-interface.tsk')).read())

    def test_edit_task_name(self):
        """Edit the name of a task."""
        th = tasks.TaskHandler(
            "IETF get interface",
            self.tmpdir,
            canned_input_data('get_config_ietf_if.json'))
        th.save_task()
        task = th.retrieve_task()
        data = task['task']
        th.edit_task('newname', data['category'])
        # th now has newname so lets try to get it with old name
        with self.assertRaises(tasks.TaskNotFoundException):
            tasks.TaskHandler.get_replay(self.tmpdir,
                                         data['category'],
                                         data['name'])
        # do a fresh retrieve with new handler
        data2 = tasks.TaskHandler.get_replay(self.tmpdir,
                                             data['category'],
                                             'newname')
        self.assertEqual(data2['name'], 'newname')
        # rest of task should be the same
        for k, v in data.items():
            if k not in ['name']:
                self.assertEqual(data[k], data2[k])

    def test_edit_task_category(self):
        """Edit the category of a task."""
        th = tasks.TaskHandler(
            "IETF get interface",
            self.tmpdir,
            canned_input_data('get_config_ietf_if.json'))
        th.save_task()
        task = th.retrieve_task()
        data = task['task']
        th.edit_task(data['name'], 'newcategory')
        # task should be in a different category now
        with self.assertRaises(tasks.TaskNotFoundException):
            tasks.TaskHandler.get_replay(self.tmpdir,
                                         data['category'],
                                         data['name'])
        data['category'] = 'newcategory'
        data2 = tasks.TaskHandler.get_replay(self.tmpdir,
                                             'newcategory',
                                             data['name'])
        self.assertEqual(data2['category'], 'newcategory')
        # rest of task should be the same
        for k, v in data.items():
            if k != 'category':
                self.assertEqual(data[k], data2[k])

    def test_edit_task_name_category(self):
        """Edit the name and category of a task."""
        th = tasks.TaskHandler(
            "IETF get interface",
            self.tmpdir,
            canned_input_data('get_config_ietf_if.json'))
        th.save_task()
        task = th.retrieve_task()
        data = task['task']
        th.edit_task('newname', 'newcategory')
        # task should be in a different category now
        with self.assertRaises(tasks.TaskNotFoundException):
            tasks.TaskHandler.get_replay(self.tmpdir,
                                         data['category'],
                                         data['name'])
        data['category'] = 'newcategory'
        data2 = tasks.TaskHandler.get_replay(self.tmpdir,
                                             'newcategory',
                                             'newname')
        self.assertEqual(data2['name'], 'newname')
        self.assertEqual(data2['category'], 'newcategory')
        # rest of task should be the same
        for k, v in data.items():
            if k not in ['name', 'category']:
                self.assertEqual(data[k], data2[k])

    def test_set_replay_path(self):
        """Set replay path to alternative base."""
        os.mkdir(os.path.join(self.tmpdir, 'topreplay'))
        tasks.set_replay_path(os.path.join(self.tmpdir, 'topreplay'))
        self.assertEqual(get_path('replays_dir'),
                         os.path.join(self.tmpdir, 'topreplay', 'replays'))

    def test_reset_replay_dir(self):
        """Set replay path back to default."""
        tasks.reset_replay_path('test')
        self.assertEqual(
            get_path('replays_dir', user='test'),
            os.path.join(get_path('users_dir'), 'test', 'testing', 'replays'))
