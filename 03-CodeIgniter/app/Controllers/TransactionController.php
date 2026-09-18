<?php

namespace App\Controllers;

use App\Models\ProductModel;
use App\Models\TransactionModel;
use App\Models\UserModel;

class TransactionController extends BaseController
{
    protected $transactionModel;
    protected $productModel;
    protected $userModel;

    public function __construct()
    {
        $this->transactionModel = new TransactionModel();
        $this->productModel = new ProductModel();
        $this->userModel = new UserModel();
    }

    public function index()
    {
        $data = [
            'title' => 'Transactions',
            'transactions' => $this->transactionModel
                ->getAllWithDetails(),
        ];

        return view('transactions/index', $data);
    }

public function create()
{
    $data = [
        'title' => 'Tambah Transaksi',
        'users' => $this->userModel->findAll(),
        'products' => $this->productModel->findAll(),
    ];

    return view('transactions/form', $data);
}

    public function store()
    {
        $rules = [
            'user_id' => 'required|integer',
            'product_id' => 'required|integer',
            'payment_method' => 'required|in_list[Cash,Transfer,QRIS]',
            'qty' => 'required|integer|greater_than[0]',
        ];

        if (! $this->validate($rules)) {
            return redirect()
                ->back()
                ->withInput()
                ->with('errors', $this->validator->getErrors());
        }

        $userId = (int) $this->request->getPost('user_id');
        $productId = (int) $this->request->getPost('product_id');
        $qty = (int) $this->request->getPost('qty');
        $paymentMethod = $this->request->getPost('payment_method');

        $user = $this->userModel->find($userId);
        $product = $this->productModel->find($productId);

        if (! $user) {
            return redirect()
                ->back()
                ->withInput()
                ->with('error', 'User tidak ditemukan.');
        }

        if (! $product) {
            return redirect()
                ->back()
                ->withInput()
                ->with('error', 'Product tidak ditemukan.');
        }

        if ($qty > (int) $product['qty_in_stock']) {
            return redirect()
                ->back()
                ->withInput()
                ->with(
                    'error',
                    'Stock tidak mencukupi. Stock tersedia: '
                    . $product['qty_in_stock']
                );
        }

        $db = \Config\Database::connect();

        $db->transStart();

        $this->transactionModel->insert([
            'user_id' => $userId,
            'product_id' => $productId,
            'payment_method' => $paymentMethod,
            'qty' => $qty,
            'created_at' => date('Y-m-d H:i:s'),
        ]);

        $newStock = (int) $product['qty_in_stock'] - $qty;

        $this->productModel->update($productId, [
            'qty_in_stock' => $newStock,
        ]);

        $db->transComplete();

        if ($db->transStatus() === false) {
            return redirect()
                ->back()
                ->withInput()
                ->with(
                    'error',
                    'Transaksi gagal disimpan.'
                );
        }

        return redirect()
            ->to('/transactions')
            ->with(
                'success',
                'Transaksi berhasil dibuat dan stock telah diperbarui.'
            );
    }

    public function delete($id)
    {
        $transaction = $this->transactionModel->find($id);

        if (! $transaction) {
            return redirect()
                ->to('/transactions')
                ->with(
                    'error',
                    'Transaksi tidak ditemukan.'
                );
        }

        $product = $this->productModel
            ->find($transaction['product_id']);

        $db = \Config\Database::connect();

        $db->transStart();

        if ($product) {
            $restoredStock =
                (int) $product['qty_in_stock']
                + (int) $transaction['qty'];

            $this->productModel->update(
                $transaction['product_id'],
                [
                    'qty_in_stock' => $restoredStock,
                ]
            );
        }

        $this->transactionModel->delete($id);

        $db->transComplete();

        if ($db->transStatus() === false) {
            return redirect()
                ->to('/transactions')
                ->with(
                    'error',
                    'Transaksi gagal dihapus.'
                );
        }

        return redirect()
            ->to('/transactions')
            ->with(
                'success',
                'Transaksi berhasil dihapus dan stock dikembalikan.'
            );
    }
}