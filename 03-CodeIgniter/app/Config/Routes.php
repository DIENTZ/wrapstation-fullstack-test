<?php

use CodeIgniter\Router\RouteCollection;

/**
 * @var RouteCollection $routes
 */

$routes->get('/', 'Dashboard::index');

/*
|--------------------------------------------------------------------------
| Users
|--------------------------------------------------------------------------
*/

$routes->get('users', 'UserController::index');
$routes->get('users/create', 'UserController::create');
$routes->post('users/store', 'UserController::store');
$routes->get('users/edit/(:num)', 'UserController::edit/$1');
$routes->post('users/update/(:num)', 'UserController::update/$1');
$routes->get('users/delete/(:num)', 'UserController::delete/$1');

/*
|--------------------------------------------------------------------------
| Products
|--------------------------------------------------------------------------
*/

$routes->get('products', 'ProductController::index');
$routes->get('products/create', 'ProductController::create');
$routes->post('products/store', 'ProductController::store');
$routes->get('products/edit/(:num)', 'ProductController::edit/$1');
$routes->post('products/update/(:num)', 'ProductController::update/$1');
$routes->get('products/delete/(:num)', 'ProductController::delete/$1');

/*
|--------------------------------------------------------------------------
| Transactions
|--------------------------------------------------------------------------
*/

$routes->get('transactions', 'TransactionController::index');
$routes->get('transactions/create', 'TransactionController::create');
$routes->post('transactions/store', 'TransactionController::store');
$routes->get('transactions/delete/(:num)', 'TransactionController::delete/$1');