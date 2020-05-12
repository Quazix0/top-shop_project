from flask import render_template,session, request,redirect,url_for,flash,current_app
from shop import app,db, search
from .models import Category,Brand,Addproduct
from .forms import Addproducts
import secrets
import os


def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories

@app.route('/')
def home():
    page = request.args.get('page',1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=8)
    return render_template('products/index.html', products=products,brands=brands(),categories=categories())

@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword, fields=['name','desc'] , limit=6)
    return render_template('products/result.html',products=products,brands=brands(),categories=categories())

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html',product=product,brands=brands(),categories=categories())

@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page',1, type=int)
    get_brand = Brand.query.filter_by(id=id).first_or_404()
    brand = Addproduct.query.filter_by(brand=get_brand).paginate(page=page, per_page=8)
    return render_template('products/index.html',brand=brand,brands=brands(),categories=categories(),get_brand=get_brand)


@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page',1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=8)
    return render_template('products/index.html',get_cat_prod=get_cat_prod,brands=brands(),categories=categories(),get_cat=get_cat)

@app.route('/addbrand',methods=['GET','POST'])
def addbrand():
    if request.method =="POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'Бренд {getbrand} был добавлен в базу данных','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', title='Добавление бренда',brands='brands')

@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash('Войдите в систему','danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method =="POST":
        updatebrand.name = brand
        flash(f'Бренд {updatebrand.name} изменен на {brand}','success')
        db.session.commit()
        return redirect(url_for('brands'))
    brand = updatebrand.name
    return render_template('products/addbrand.html', title='Обновить бренд',brands='brands',updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['GET','POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        flash(f"Бренд {brand.name} был удален из базы данных","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"Бренд {brand.name} не может быть удален из базы данных","warning")
    return redirect(url_for('admin'))

@app.route('/addcat',methods=['GET','POST'])
def addcat():
    if request.method =="POST":
        getcat = request.form.get('category')
        category = Category(name=getcat)
        db.session.add(category)
        flash(f'Категория {getcat} была добавлена в вашу базу данных','success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html', title='Добавить категорию')


@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash('Сначала войдите в систему','danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')  
    if request.method =="POST":
        updatecat.name = category
        flash(f'Категория{updatecat.name} была изменена на {category}','success')
        db.session.commit()
        return redirect(url_for('categories'))
    category = updatecat.name
    return render_template('products/addbrand.html', title='Обновить категорию',updatecat=updatecat)



@app.route('/deletecat/<int:id>', methods=['GET','POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        flash(f"Категория {category.name} была удалена базы данных","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"Категория {category.name} не может быть удалена с базы данных","warning")
    return redirect(url_for('admin'))


@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
    form = Addproducts(request.form)
    brands = Brand.query.all()
    categories = Category.query.all()
    return render_template('products/addproduct.html', form=form, title='Добавить товар', brands=brands,categories=categories)

@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    form = Addproducts(request.form)
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.all()
    categories = Category.query.all()
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method =="POST":
        product.name = form.name.data 
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data 
        product.colors = form.colors.data
        product.desc = form.description.data
        product.category_id = category
        product.brand_id = brand
        flash('Товар был обновлен','success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.description.data = product.desc
    brand = product.brand.name
    category = product.category.name
    return render_template('products/addproduct.html', form=form, title='Обновить товар',getproduct=product, brands=brands,categories=categories)

@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'Товар {product.name} был удален','success')
        return redirect(url_for('adim'))
    flash(f'Невозможно удалить товар','warning')
    return redirect(url_for('admin'))