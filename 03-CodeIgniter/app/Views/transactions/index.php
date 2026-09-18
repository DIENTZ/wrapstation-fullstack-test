<?= $this->include('layout/header') ?>

<div class="card">

    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
        <h1 style="margin:0;">Transactions</h1>

        <a href="<?= site_url('transactions/create') ?>" class="btn">
            + Tambah Transaksi
        </a>
    </div>

    <?php if (empty($transactions)): ?>

        <p>Belum ada transaksi.</p>

    <?php else: ?>

        <table>

            <thead>
                <tr>
                    <th>ID</th>
                    <th>User</th>
                    <th>Product</th>
                    <th>Qty</th>
                    <th>Harga</th>
                    <th>Pembayaran</th>
                    <th>Tanggal</th>
                    <th>Aksi</th>
                </tr>
            </thead>

            <tbody>

                <?php foreach ($transactions as $transaction): ?>

                    <tr>

                        <td>
                            <?= esc((string) $transaction['transaction_id']) ?>
                        </td>

                        <td>
                            <?= esc($transaction['name'] ?? '-') ?>
                        </td>

                        <td>
                            <?= esc($transaction['product_name'] ?? '-') ?>
                        </td>

                        <td>
                            <?= esc((string) ($transaction['qty'] ?? 0)) ?>
                        </td>

                        <td>
                            Rp <?= number_format(
                                (float) ($transaction['price'] ?? 0),
                                0,
                                ',',
                                '.'
                            ) ?>
                        </td>

                        <td>
                            <?= esc($transaction['payment_method'] ?? '-') ?>
                        </td>

                        <td>
                            <?= esc($transaction['created_at'] ?? '-') ?>
                        </td>

                        <td>

                            <a
                                href="<?= site_url('transactions/delete/' . $transaction['transaction_id']) ?>"
                                class="btn btn-danger"
                                onclick="return confirm('Yakin ingin menghapus transaksi ini? Stock akan dikembalikan.')"
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