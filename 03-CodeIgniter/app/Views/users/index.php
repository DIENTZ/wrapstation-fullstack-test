<?= $this->include('layout/header') ?>

<div class="card">

    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
        <h1 style="margin:0;">Users</h1>

        <a href="<?= site_url('users/create') ?>" class="btn">
            + Tambah User
        </a>
    </div>

    <?php if (empty($users)): ?>

        <p>Belum ada data user.</p>

    <?php else: ?>

        <table>

            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nama</th>
                    <th>Aksi</th>
                </tr>
            </thead>

            <tbody>

                <?php foreach ($users as $user): ?>

                    <tr>

                        <td>
                            <?= esc((string) $user['user_id']) ?>
                        </td>

                        <td>
                            <?= esc($user['name']) ?>
                        </td>

                        <td>

                            <a
                                href="<?= site_url('users/edit/' . $user['user_id']) ?>"
                                class="btn btn-secondary"
                            >
                                Edit
                            </a>

                            <a
                                href="<?= site_url('users/delete/' . $user['user_id']) ?>"
                                class="btn btn-danger"
                                onclick="return confirm('Yakin ingin menghapus user ini?')"
                            >
                                Hapus
                            </a>

                        </td>

                    </tr>

                <?php endforeach; ?>

            </tbody>

        </table>

    <?php endif; ?>

</div>

<?= $this->include('layout/footer') ?>