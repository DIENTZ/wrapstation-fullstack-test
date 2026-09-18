<?= $this->include('layout/header') ?>

<h1>Dashboard</h1>

<div class="grid">

    <div class="stat">
        <h3>Total Users</h3>
        <p><?= esc((string) ($totalUsers ?? 0)) ?></p>
    </div>

    <div class="stat">
        <h3>Total Products</h3>
        <p><?= esc((string) ($totalProducts ?? 0)) ?></p>
    </div>

    <div class="stat">
        <h3>Total Transactions</h3>
        <p><?= esc((string) ($totalTransactions ?? 0)) ?></p>
    </div>

</div>

<div class="card">

    <h2>Transaksi Terbaru</h2>

    <?php if (empty($recentTransactions)): ?>

        <p>Belum ada transaksi.</p>

    <?php else: ?>

        <table>

            <thead>
                <tr>
                    <th>User</th>
                    <th>Product</th>
                    <th>Qty</th>
                    <th>Pembayaran</th>
                </tr>
            </thead>

            <tbody>

                <?php foreach ($recentTransactions as $transaction): ?>

                    <tr>
                        <td><?= esc($transaction['name'] ?? '-') ?></td>
                        <td><?= esc($transaction['product_name'] ?? '-') ?></td>
                        <td><?= esc((string) ($transaction['qty'] ?? 0)) ?></td>
                        <td><?= esc($transaction['payment_method'] ?? '-') ?></td>
                    </tr>

                <?php endforeach; ?>

            </tbody>

        </table>

    <?php endif; ?>

</div>

<?= $this->include('layout/footer') ?>