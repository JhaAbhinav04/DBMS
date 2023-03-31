// Import necessary modules and packages
const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();

// Initialize the app and set the port number
const app = express();
const port = process.env.PORT || 3000;

// Set up the SQLite database
const dbPath = path.resolve(__dirname, 'inventory.db');
const db = new sqlite3.Database(dbPath, sqlite3.OPEN_READWRITE, (err) => {
  if (err) {
    console.error(err.message);
  } else {
    console.log('Connected to the inventory database.');
  }
});

// Define the middleware for the app
app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.urlencoded({ extended: true }));

// Define the routes for the app
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/products', (req, res) => {
  db.all('SELECT * FROM products', [], (err, rows) => {
    if (err) {
      console.error(err.message);
      res.sendStatus(500);
    } else {
      res.render('products', { products: rows });
    }
  });
});

app.get('/orders', (req, res) => {
  db.all('SELECT * FROM orders', [], (err, rows) => {
    if (err) {
      console.error(err.message);
      res.sendStatus(500);
    } else {
      res.render('orders', { orders: rows });
    }
  });
});

app.get('/add_product', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'add_product.html'));
});

app.post('/add_product', (req, res) => {
  const { name, description, quantity, price } = req.body;
  db.run('INSERT INTO products (name, description, quantity, price) VALUES (?, ?, ?, ?)', [name, description, quantity, price], (err) => {
    if (err) {
      console.error(err.message);
      res.sendStatus(500);
    } else {
      res.redirect('/products');
    }
  });
});

app.get('/add_order', (req, res) => {
  db.all('SELECT * FROM products', [], (err, rows) => {
    if (err) {
      console.error(err.message);
      res.sendStatus(500);
    } else {
      res.render('add_order', { products: rows });
    }
  });
});

app.post('/add_order', (req, res) => {
  const { customer_name, customer_email, product_id, quantity } = req.body;
  db.run('INSERT INTO orders (customer_name, customer_email, product_id, quantity) VALUES (?, ?, ?, ?)', [customer_name, customer_email, product_id, quantity], (err) => {
    if (err) {
      console.error(err.message);
      res.sendStatus(500);
    } else {
      res.redirect('/orders');
    }
  });
});

// Set up the view engine for the app
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

// Start the server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
