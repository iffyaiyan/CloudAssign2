from flask import render_template, redirect, url_for, request, flash, current_app
from app import app
from app.models import Product
from app.utils import upload_to_blob_storage

@app.route('/')
def index():
    """Homepage - redirects to product list."""
    return redirect(url_for('product_list'))

@app.route('/products')
def product_list():
    """List all products."""
    products = Product.get_all()
    return render_template('product_list.html', products=products)

@app.route('/products/<int:product_id>')
def product_detail(product_id):
    """Display a single product."""
    product = Product.get_by_id(product_id)
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('product_list'))
    return render_template('product_detail.html', product=product)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    """Add a new product."""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        
        # Form validation
        errors = []
        if not name:
            errors.append('Product name is required')
        if not price:
            errors.append('Product price is required')
        else:
            try:
                price = float(price)
                if price <= 0:
                    errors.append('Price must be greater than zero')
            except ValueError:
                errors.append('Price must be a number')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('add_product.html')
        
        # Handle file upload
        image_url = None
        if 'image' in request.files and request.files['image'].filename:
            file = request.files['image']
            image_url = upload_to_blob_storage(file)
            if not image_url:
                flash('Failed to upload image. Please try again.', 'danger')
                return render_template('add_product.html')
        
        # Create and save product
        product = Product(
            name=name,
            description=description,
            price=price,
            image_url=image_url
        )
        product.save()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('product_list'))
    
    return render_template('add_product.html')

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return render_template('500.html'), 500