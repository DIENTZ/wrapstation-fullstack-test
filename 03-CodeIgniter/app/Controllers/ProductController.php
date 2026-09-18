<?php

namespace App\Controllers;

use App\Models\ProductModel;

class ProductController extends BaseController
{
    protected $productModel;

    public function __construct()
    {
        $this->productModel = new ProductModel();
    }

    public function index()
    {
        $data = [
            'title' => 'Products',
            'products' => $this->productModel
                ->orderBy('product_id', 'DESC')
                ->findAll(),
        ];

        return view('products/index', $data);
    }

    public function create()
    {
        return view('products/form', [
            'title' => 'Tambah Product',
            'product' => null,
        ]);
    }

    public function store()
    {
        $rules = [
            'product_name' => 'required|min_length[2]|max_length[150]',
            'qty_in_stock' => 'required|integer|greater_than_equal_to[0]',
            'price' => 'required|decimal|greater_than_equal_to[0]',
        ];

        if (! $this->validate($rules)) {
            return redirect()
                ->back()
                ->withInput()
                ->with('errors', $this->validator->getErrors());
        }

        $this->productModel->insert([
            'product_name' => trim($this->request->getPost('product_name')),
            'qty_in_stock' => (int) $this->request->getPost('qty_in_stock'),
            'price' => (float) $this->request->getPost('price'),
        ]);

        return redirect()
            ->to('/products')
            ->with('success', 'Product berhasil ditambahkan.');
    }

    public function edit($id)
    {
        $product = $this->productModel->find($id);

        if (! $product) {
            return redirect()
                ->to('/products')
                ->with('error', 'Product tidak ditemukan.');
        }

        return view('products/form', [
            'title' => 'Edit Product',
            'product' => $product,
        ]);
    }

    public function update($id)
    {
        $product = $this->productModel->find($id);

        if (! $product) {
            return redirect()
                ->to('/products')
                ->with('error', 'Product tidak ditemukan.');
        }

        $rules = [
            'product_name' => 'required|min_length[2]|max_length[150]',
            'qty_in_stock' => 'required|integer|greater_than_equal_to[0]',
            'price' => 'required|decimal|greater_than_equal_to[0]',
        ];

        if (! $this->validate($rules)) {
            return redirect()
                ->back()
                ->withInput()
                ->with('errors', $this->validator->getErrors());
        }

        $this->productModel->update($id, [
            'product_name' => trim($this->request->getPost('product_name')),
            'qty_in_stock' => (int) $this->request->getPost('qty_in_stock'),
            'price' => (float) $this->request->getPost('price'),
        ]);

        return redirect()
            ->to('/products')
            ->with('success', 'Product berhasil diperbarui.');
    }

    public function delete($id)
    {
        $product = $this->productModel->find($id);

        if (! $product) {
            return redirect()
                ->to('/products')
                ->with('error', 'Product tidak ditemukan.');
        }

        $this->productModel->delete($id);

        return redirect()
            ->to('/products')
            ->with('success', 'Product berhasil dihapus.');
    }
}