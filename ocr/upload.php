<?php

$process_id = md5(time() . '_' . mt_rand());
$image_dir = './' . $process_id;
$tmp_dir = $image_dir . '_tmp';

if (!isset($_FILES['images']) || !count($_FILES['images']) || file_exists($image_dir) || file_exists($tmp_dir)) {
    http_response_code(400);
    exit;
}

mkdir($image_dir);
mkdir($tmp_dir);

for ($i = 0; $i < count($_FILES['images']['name']); $i++) {
    if (is_uploaded_file($_FILES['images']['tmp_name'][$i])) {
        move_uploaded_file($_FILES['images']['tmp_name'][$i], $image_dir . '/' . $_FILES['images']['name'][$i]);
    }
}

http_response_code(200);
header('Content-Type: application/json; charset=UTF-8');
header("X-Content-Type-Options: nosniff");

echo json_encode([
  'process_id' => $process_id
]);
