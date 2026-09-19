<?php

namespace App\Controllers;

use App\Models\ProductModel;
use App\Models\TransactionModel;
use App\Models\UserModel;
use CodeIgniter\HTTP\RedirectResponse;

class TransactionController extends BaseController
{
    protected TransactionModel $transactionModel;
    protected ProductModel $productModel;
    protected UserModel $userModel;

    public function __construct()
    {
        $this->transactionModel = new TransactionModel();
        $this->productModel = new ProductModel();
        $this->userModel = new UserModel();
    }

    public function index()
    {
        $data = [
            'title' => 'Data Transaksi',
            'transactions' => $this->transactionModel
                ->select('transactions.*, users.name as user_name, products.name as product_name')
                ->join('users', 'users.id = transactions.user_id')
                ->join('products', 'products.id = transactions.product_id')
                ->orderBy('transactions.id', 'DESC')
                ->findAll(),
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

    public function store(): RedirectResponse
    {
        $userId = (int) $this->request->getPost('user_id');
        $productId = (int) $this->request->getPost('product_id');
        $quantity = (int) $this->request->getPost('quantity');

        $product = $this->productModel->find($productId);

        if (!$product) {
            return redirect()
                ->back()
                ->withInput()
                ->with('error', 'Produk tidak ditemukan.');
        }

        if ($quantity <= 0) {
            return redirect()
                ->back()
                ->withInput()
                ->with('error', 'Jumlah transaksi harus lebih dari 0.');
        }

        if ((int) $product['stock'] < $quantity) {
            return redirect()
                ->back()
                ->withInput()
                ->with(
                    'error',
                    'Stok produk tidak mencukupi. Stok tersedia: ' . $product['stock']
                );
        }

        $totalPrice = (float) $product['price'] * $quantity;

        $transactionData = [
            'user_id' => $userId,
            'product_id' => $productId,
            'quantity' => $quantity,
            'total_price' => $totalPrice,
            'payment_method' => $this->request->getPost('payment_method'),
        ];

        $this->transactionModel->insert($transactionData);

        $newStock = (int) $product['stock'] - $quantity;

        $this->productModel->update($productId, [
            'stock' => $newStock,
        ]);

        return redirect()
            ->to('/transactions')
            ->with('success', 'Transaksi berhasil ditambahkan.');
    }

    public function delete(int $id): RedirectResponse
    {
        $transaction = $this->transactionModel->find($id);

        if (!$transaction) {
            return redirect()
                ->to('/transactions')
                ->with('error', 'Transaksi tidak ditemukan.');
        }

        $product = $this->productModel->find($transaction['product_id']);

        if ($product) {
            $restoredStock = (int) $product['stock'] + (int) $transaction['quantity'];

            $this->productModel->update(
                $transaction['product_id'],
                [
                    'stock' => $restoredStock,
                ]
            );
        }

        $this->transactionModel->delete($id);

        return redirect()
            ->to('/transactions')
            ->with('success', 'Transaksi berhasil dihapus.');
    }
}