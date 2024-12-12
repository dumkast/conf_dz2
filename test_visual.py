import unittest
from unittest.mock import patch, MagicMock
import subprocess
from visual import get_commits, check_file_exists_in_commit, build_dependency_graph, generate_mermaid_code

class TestGitDependencyGraph(unittest.TestCase):

    @patch('subprocess.run')
    @patch('os.chdir')
    def test_get_commits_success(self, mock_chdir, mock_run):
        mock_run.return_value = MagicMock(stdout='commit1\ncommit2\ncommit3\n', returncode=0)
        commits = get_commits('/mocked/path/to/repo')
        self.assertEqual(commits, ['commit1', 'commit2', 'commit3'])

    @patch('subprocess.run')
    @patch('os.chdir')
    def test_get_commits_failure(self, mock_chdir, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git rev-list')
        commits = get_commits('/mocked/path/to/repo')
        self.assertEqual(commits, [])

    @patch('subprocess.run')
    def test_check_file_exists_in_commit_success(self, mock_run):
        mock_run.return_value = MagicMock(stdout='file1.txt\nfile2.txt\n', returncode=0)
        exists = check_file_exists_in_commit('commit_hash', 'file1.txt')
        self.assertTrue(exists)

    @patch('subprocess.run')
    def test_check_file_exists_in_commit_not_found(self, mock_run):
        mock_run.return_value = MagicMock(stdout='file2.txt\nfile3.txt\n', returncode=0)
        exists = check_file_exists_in_commit('commit_hash', 'file1.txt')
        self.assertFalse(exists)

    @patch('subprocess.run')
    def test_build_dependency_graph(self, mock_run):

        mock_run.side_effect = [
            MagicMock(stdout='parent1 parent2\n', returncode=0),
            MagicMock(stdout='', returncode=0),
            MagicMock(stdout='', returncode=0)
        ]


        with patch('visual.check_file_exists_in_commit') as mock_check:
            mock_check.side_effect = [True, False, False]
            commits = ['commit1', 'commit2', 'commit3']
            graph = build_dependency_graph('/mocked/path/to/repo', commits, 'file1.txt')

            expected_graph = ({'commit1': ['parent1', 'parent2'], 'commit2': [], 'commit3': []}, ['commit1'])


            self.assertEqual(graph, expected_graph)


if __name__ == '__main__':
    unittest.main()

