<?= $this->include('layout/header') ?>

<div class="card">

    <h1><?= esc($title ?? 'Form User') ?></h1>

    <?php
    $errors = session()->getFlashdata('errors');
    ?>

    <?php if (! empty($errors)): ?>

        <div class="alert alert-error">

            <?php foreach ($errors as $error): ?>

                <div><?= esc($error) ?></div>

            <?php endforeach; ?>

        </div>

    <?php endif; ?>

    <?php
    $userData = $user ?? [];
    $isEdit = ! empty($userData);

    if ($isEdit) {
        $action = site_url(
            'users/update/' . $userData['user_id']
        );
    } else {
        $action = site_url('users/store');
    }
    ?>

    <form action="<?= $action ?>" method="post">

        <?= csrf_field() ?>

        <label for="name">
            Nama User
        </label>

        <input
            type="text"
            id="name"
            name="name"
            value="<?= esc($userData['name'] ?? old('name')) ?>"
            placeholder="Masukkan nama user"
            required
        >

        <button type="submit" class="btn">
            <?= $isEdit ? 'Update User' : 'Simpan User' ?>
        </button>

        <a
            href="<?= site_url('users') ?>"
            class="btn btn-secondary"
        >
            Kembali
        </a>

    </form>

</div>

<?= $this->include('layout/footer') ?>