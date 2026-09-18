<?= $this->include('layout/header') ?>

<div class="card">

    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
        <h1 style="margin:0;">Products</h1>

        <a href="<?= site_url('products/create') ?>" class="btn">
            + Tambah Product
        </a>
    </div>

    <?php if (empty($products)): ?>

        <p>Belum ada data product.</p>

    <?php else: ?>

        <table>

            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nama Product</th>
                    <th>Stock</th>
                    <th>Harga</th>
                    <th>Aksi</th>
                </tr>
            </thead>

            <tbody>

                <?php foreach ($products as $product): ?>

                    <tr>

                        <td>
                            <?= esc((string) $product['product_id']) ?>
                        </td>

                        <td>
                            <?= esc($product['product_name']) ?>
                        </td>

                        <td>
                            <?= esc((string) $product['qty_in_stock']) ?>
                        </td>

                        <td>
                            Rp <?= number_format((float) $product['price'], 0, ',', '.') ?>
                        </td>

                        <td>

                            <a
                                href="<?= site_url('products/edit/' . $product['product_id']) ?>"
                                class="btn btn-secondary"
                            >
                                Edit
                            </a>

                            <a
                                href="<?= site_url('products/delete/' . $product['product_id']) ?>"
                                class="btn btn-danger"
                                onclick="return confirm('Yakin ingin menghapus product ini?')"
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