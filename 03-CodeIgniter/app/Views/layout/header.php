<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title><?= esc($title ?? 'Wrapstation CMS') ?></title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            color: #222;
        }

        nav {
            background: #1f2937;
            padding: 15px 25px;
        }

        nav a {
            color: white;
            text-decoration: none;
            margin-right: 20px;
            font-weight: bold;
        }

        nav a:hover {
            text-decoration: underline;
        }

        main {
            max-width: 1100px;
            margin: 30px auto;
            padding: 0 20px;
        }

        .card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
        }

        .stat {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }

        .stat h3 {
            margin-top: 0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th,
        td {
            border-bottom: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }

        th {
            background: #f1f5f9;
        }

        .btn {
            display: inline-block;
            padding: 9px 14px;
            border-radius: 6px;
            background: #2563eb;
            color: white;
            text-decoration: none;
            border: none;
            cursor: pointer;
        }

        .btn-danger {
            background: #dc2626;
        }

        .btn-secondary {
            background: #6b7280;
        }

        form {
            max-width: 600px;
        }

        label {
            display: block;
            margin-bottom: 6px;
            font-weight: bold;
        }

        input,
        select {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 6px;
        }

        .alert {
            padding: 12px 15px;
            margin-bottom: 20px;
            border-radius: 6px;
            background: #e5e7eb;
        }

        .alert-success {
            background: #dcfce7;
            color: #166534;
        }

        .alert-error {
            background: #fee2e2;
            color: #991b1b;
        }
    </style>
</head>

<body>

<nav>
    <a href="<?= site_url('/') ?>">Dashboard</a>
    <a href="<?= site_url('users') ?>">Users</a>
    <a href="<?= site_url('products') ?>">Products</a>
    <a href="<?= site_url('transactions') ?>">Transactions</a>
</nav>

<main>

<?php if (session()->getFlashdata('success')): ?>
    <div class="alert alert-success">
        <?= esc(session()->getFlashdata('success')) ?>
    </div>
<?php endif; ?>

<?php if (session()->getFlashdata('error')): ?>
    <div class="alert alert-error">
        <?= esc(session()->getFlashdata('error')) ?>
    </div>
<?php endif; ?>

<?php if (session()->getFlashdata('errors')): ?>
    <div class="alert alert-error">
        <?php foreach (session()->getFlashdata('errors') as $error): ?>
            <div><?= esc($error) ?></div>
        <?php endforeach; ?>
    </div>
<?php endif; ?>