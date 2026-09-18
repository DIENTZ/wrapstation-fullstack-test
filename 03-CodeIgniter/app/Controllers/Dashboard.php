<?php

namespace App\Controllers;

use App\Models\UserModel;
use App\Models\ProductModel;
use App\Models\TransactionModel;

class Dashboard extends BaseController
{
    public function index()
    {
        $userModel = new UserModel();
        $productModel = new ProductModel();
        $transactionModel = new TransactionModel();

        $data = [
            'title' => 'Dashboard',
            'totalUsers' => $userModel->countAll(),
            'totalProducts' => $productModel->countAll(),
            'totalTransactions' => $transactionModel->countAll(),
            'recentTransactions' => $transactionModel->getRecent(5),
        ];

        return view('dashboard', $data);
    }
}