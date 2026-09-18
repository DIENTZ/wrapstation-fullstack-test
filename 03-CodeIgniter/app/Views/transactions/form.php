<?= $this->include('layout/header') ?>

<div class="card">

    <h1><?= esc($title ?? 'Tambah Transaksi') ?></h1>

    <?php
    $errors = session()->getFlashdata('errors');
    $userList = $users ?? [];
    $productList = $products ?? [];
    ?>

    <?php if (! empty($errors)): ?>

        <div class="alert alert-error">

            <?php foreach ($errors as $error): ?>

                <div><?= esc($error) ?></div>

            <?php endforeach; ?>

        </div>

    <?php endif; ?>

    <form
        action="<?= site_url('transactions/store') ?>"
        method="post"
    >

        <?= csrf_field() ?>

        <label for="user_id">
            User
        </label>

        <select
            id="user_id"
            name="user_id"
            required
        >

            <option value="">
                -- Pilih User --
            </option>

            <?php foreach ($userList as $user): ?>

                <option
                    value="<?= esc((string) $user['user_id']) ?>"
                    <?= old('user_id') == $user['user_id'] ? 'selected' : '' ?>
                >
                    <?= esc($user['name']) ?>
                </option>

            <?php endforeach; ?>

        </select>


        <label for="product_id">
            Product
        </label>

        <select
            id="product_id"
            name="product_id"
            required
        >

            <option value="">
                -- Pilih Product --
            </option>

            <?php foreach ($productList as $product): ?>

                <?php if ((int) $product['qty_in_stock'] > 0): ?>

                    <option
                        value="<?= esc((string) $product['product_id']) ?>"
                        <?= old('product_id') == $product['product_id'] ? 'selected' : '' ?>
                    >
                        <?= esc($product['product_name']) ?>
                        - Stock:
                        <?= esc((string) $product['qty_in_stock']) ?>
                    </option>

                <?php endif; ?>

            <?php endforeach; ?>

        </select>


        <label for="payment_method">
            Payment Method
        </label>

        <select
            id="payment_method"
            name="payment_method"
            required
        >

            <option value="">
                -- Pilih Pembayaran --
            </option>

            <option
                value="Cash"
                <?= old('payment_method') === 'Cash' ? 'selected' : '' ?>
            >
                Cash
            </option>

            <option
                value="Transfer"
                <?= old('payment_method') === 'Transfer' ? 'selected' : '' ?>
            >
                Transfer
            </option>

            <option
                value="QRIS"
                <?= old('payment_method') === 'QRIS' ? 'selected' : '' ?>
            >
                QRIS
            </option>

        </select>


        <label for="qty">
            Quantity
        </label>

        <input
            type="number"
            id="qty"
            name="qty"
            value="<?= esc(old('qty', '1')) ?>"
            min="1"
            required
        >


        <button type="submit" class="btn">
            Simpan Transaksi
        </button>

        <a
            href="<?= site_url('transactions') ?>"
            class="btn btn-secondary"
        >
            Kembali
        </a>

    </form>

</div>

<?= $this->include('layout/footer') ?>