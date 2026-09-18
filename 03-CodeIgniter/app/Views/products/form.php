<?= $this->include('layout/header') ?>

<div class="card">

    <h1><?= esc($title ?? 'Form Product') ?></h1>

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
    $productData = $product ?? [];
    $isEdit = ! empty($productData);

    if ($isEdit) {
        $action = site_url(
            'products/update/' . $productData['product_id']
        );
    } else {
        $action = site_url('products/store');
    }
    ?>

    <form action="<?= $action ?>" method="post">

        <?= csrf_field() ?>

        <label for="product_name">
            Nama Product
        </label>

        <input
            type="text"
            id="product_name"
            name="product_name"
            value="<?= esc($productData['product_name'] ?? old('product_name')) ?>"
            placeholder="Masukkan nama product"
            required
        >

        <label for="qty_in_stock">
            Stock
        </label>

        <input
            type="number"
            id="qty_in_stock"
            name="qty_in_stock"
            value="<?= esc($productData['qty_in_stock'] ?? old('qty_in_stock', 0)) ?>"
            min="0"
            required
        >

        <label for="price">
            Harga
        </label>

        <input
            type="number"
            id="price"
            name="price"
            value="<?= esc($productData['price'] ?? old('price', 0)) ?>"
            min="0"
            step="0.01"
            required
        >

        <button type="submit" class="btn">
            <?= $isEdit ? 'Update Product' : 'Simpan Product' ?>
        </button>

        <a
            href="<?= site_url('products') ?>"
            class="btn btn-secondary"
        >
            Kembali
        </a>

    </form>

</div>

<?= $this->include('layout/footer') ?>