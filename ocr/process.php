<?php
require_once "../vendor/autoload.php";
use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\Process;

if (!isset($_GET['process_id']) || !file_exists('./' . $_GET['process_id'])) {
    exit;
}

$python_path = '~/.anyenv/envs/pyenv/shims/python';

set_time_limit(3600);
header("Content-type: application/octet-stream");

$image_dir = './' . $_GET['process_id'];
$tmp_dir = $image_dir . '_tmp';

$process = new Process([$python_path, '-u', 'ocr.py', $image_dir, $tmp_dir]);

$process->run(function ($type, $buffer) {
    echo $buffer . str_repeat(' ', 4096);
});

function remove_directory($dir)
{
    $files = array_diff(scandir($dir), ['.', '..']);
    foreach ($files as $file) {
        if (is_dir("$dir/$file")) {
            remove_directory("$dir/$file");
        } else {
            unlink("$dir/$file");
        }
    }
    return rmdir($dir);
}

remove_directory($image_dir);
remove_directory($tmp_dir);
