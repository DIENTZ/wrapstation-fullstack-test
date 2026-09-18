<?php

namespace App\Models;

use CodeIgniter\Model;

class TransactionModel extends Model
{
    protected $table = 'transactions';

    protected $primaryKey = 'transaction_id';

    protected $returnType = 'array';

    protected $allowedFields = [
        'user_id',
        'product_id',
        'payment_method',
        'qty',
        'created_at',
    ];

    public function getAllWithDetails(): array
    {
        return $this->select(
            'transactions.*, users.name, products.product_name, products.price'
        )
        ->join(
            'users',
            'users.user_id = transactions.user_id'
        )
        ->join(
            'products',
            'products.product_id = transactions.product_id'
        )
        ->orderBy(
            'transactions.transaction_id',
            'DESC'
        )
        ->findAll();
    }

    public function getRecent(int $limit = 5): array
    {
        return $this->select(
            'transactions.*, users.name, products.product_name, products.price'
        )
        ->join(
            'users',
            'users.user_id = transactions.user_id'
        )
        ->join(
            'products',
            'products.product_id = transactions.product_id'
        )
        ->orderBy(
            'transactions.transaction_id',
            'DESC'
        )
        ->findAll($limit);
    }
}