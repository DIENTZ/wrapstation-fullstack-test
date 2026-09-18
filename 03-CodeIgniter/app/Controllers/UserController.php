<?php

namespace App\Controllers;

use App\Models\UserModel;

class UserController extends BaseController
{
    protected $userModel;

    public function __construct()
    {
        $this->userModel = new UserModel();
    }

    public function index()
    {
        $data = [
            'title' => 'Users',
            'users' => $this->userModel
                ->orderBy('user_id', 'DESC')
                ->findAll(),
        ];

        return view('users/index', $data);
    }

    public function create()
    {
        return view('users/form', [
            'title' => 'Tambah User',
            'user' => null,
        ]);
    }

    public function store()
    {
        $rules = [
            'name' => [
                'rules' => 'required|min_length[2]|max_length[100]',
                'errors' => [
                    'required' => 'Nama wajib diisi.',
                    'min_length' => 'Nama minimal 2 karakter.',
                    'max_length' => 'Nama maksimal 100 karakter.',
                ],
            ],
        ];

        if (! $this->validate($rules)) {
            return redirect()
                ->back()
                ->withInput()
                ->with('errors', $this->validator->getErrors());
        }

        $this->userModel->insert([
            'name' => trim($this->request->getPost('name')),
        ]);

        return redirect()
            ->to('/users')
            ->with('success', 'User berhasil ditambahkan.');
    }

    public function edit($id)
    {
        $user = $this->userModel->find($id);

        if (! $user) {
            return redirect()
                ->to('/users')
                ->with('error', 'User tidak ditemukan.');
        }

        return view('users/form', [
            'title' => 'Edit User',
            'user' => $user,
        ]);
    }

    public function update($id)
    {
        $user = $this->userModel->find($id);

        if (! $user) {
            return redirect()
                ->to('/users')
                ->with('error', 'User tidak ditemukan.');
        }

        $rules = [
            'name' => [
                'rules' => 'required|min_length[2]|max_length[100]',
                'errors' => [
                    'required' => 'Nama wajib diisi.',
                    'min_length' => 'Nama minimal 2 karakter.',
                    'max_length' => 'Nama maksimal 100 karakter.',
                ],
            ],
        ];

        if (! $this->validate($rules)) {
            return redirect()
                ->back()
                ->withInput()
                ->with('errors', $this->validator->getErrors());
        }

        $this->userModel->update($id, [
            'name' => trim($this->request->getPost('name')),
        ]);

        return redirect()
            ->to('/users')
            ->with('success', 'User berhasil diperbarui.');
    }

    public function delete($id)
    {
        $user = $this->userModel->find($id);

        if (! $user) {
            return redirect()
                ->to('/users')
                ->with('error', 'User tidak ditemukan.');
        }

        $this->userModel->delete($id);

        return redirect()
            ->to('/users')
            ->with('success', 'User berhasil dihapus.');
    }
}