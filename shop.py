from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'prettysecret'

products = [
    {'id': 1, 'name': 'Bitch Bag', 'price': 30, 'image': 'bitchbag', 'description': 'Carry your trauma in style. Pink, petty, perfect.', 'category': 'accessories'},
    {'id': 2, 'name': 'Brave Necklace', 'price': 13, 'image': 'brave', 'description': "For nights when you're scared… but horny.", 'category': 'accessories'},
    {'id': 3, 'name': 'Young Charm', 'price': 14, 'image': 'cha', 'description': "To pretty to behave", 'category': 'clothes'},
    {'id': 4, 'name': 'Main Character Dress', 'price': 35, 'image': 'dress', 'description': "Walk in. Ruin the plot. Walk out.", 'category': 'clothes'},
    {'id': 5, 'name': 'Fluffy Attack Slippers', 'price': 20, 'image': 'flo', 'description': "Too soft to fight. Too sexy to care.", 'category': 'shoes'},
    {'id': 6, 'name': 'Fuckboy Repellent', 'price': 13, 'image': 'fuc', 'description': "Spray twice. Walk away. Let him cry in the group chat.", 'category': 'accessories'},
    {'id': 7, 'name': 'Vamp Barbie Purse', 'price': 30, 'image': 'gri', 'description': "Glamour, but make it bite.", 'category': 'accessories'},
    {'id': 8, 'name': 'Sugar Trap Clips', 'price': 11, 'image': 'ha', 'description': "He thought you were sweet. Now he is crying in lowercase.", 'category': 'accessories'},
    {'id': 9, 'name': 'Heartbreaker Heels', 'price': 35, 'image': 'heart', 'description': "He fell in love. You kept walking. Mission complete.", 'category': 'shoes'},
    {'id': 10, 'name': 'Play Your Boy', 'price': 35, 'image': 'ho', 'description': "Spell it out, baby. If he’s confused — read your lobes.", 'category': 'shoes'},
    {'id': 11, 'name': 'Drama Hoop Earrings', 'price': 18, 'image': 'hoop', 'description': "Earrings that scream before you do.", 'category': 'accessories'},
    {'id': 12, 'name': 'Leopard Lust', 'price': 65, 'image': 'leot', 'description': "Not for the zoo. For the kill.", 'category': 'shoes'},
    {'id': 13, 'name': 'Playtime Platforms', 'price': 40, 'image': 'play', 'description': "Barbie dreams with Bratz rage. Step on them.", 'category': 'shoes'},
    {'id': 14, 'name': 'Bitch Ring', 'price': 15, 'image': 'ring', 'description': "Flash it when you’re lying. Or slaying. Or both.", 'category': 'accessories'},
    {'id': 15, 'name': 'Trashcore Top', 'price': 22, 'image': 'rt', 'description': "Cropped, cursed, and way too hot for him.", 'category': 'clothes'},
    {'id': 16, 'name': 'Bratz Pink Claws', 'price': 29, 'image': 'sho', 'description': "Stomp like you own the club — even if it’s just your kitchen.", 'category': 'shoes'},
    {'id': 17, 'name': 'Mean Girl Skirt', 'price': 23, 'image': 'skirt', 'description': "Cute in the front, deadly in the back.", 'category': 'clothes'},
    {'id': 18, 'name': 'Baby Devil Top', 'price': 22, 'image': 'top', 'description': "Cute enough to sin. Hot enough to repent.", 'category': 'clothes'},
    {'id': 19, 'name': 'Deadly Rose Skirt', 'price': 30, 'image': 'rose', 'description': 'Sweet blooms, sharp moves. Romance was murdered here.', 'category': 'clothes'},
    {'id': 20, 'name': 'Jungle Drama Bag', 'price': 35, 'image': 'jungle', 'description': 'She purrs, then roars. For wild nights and bitchy brunches.', 'category': 'accessories'},
    {'id': 21, 'name': 'Toxic Barbie Dress', 'price': 30, 'image': '12', 'description': 'Heels clicking, hearts breaking. Just another Tuesday.', 'category': 'clothes'},
    {'id': 22, 'name': 'Stardust Trash Heels', 'price': 40, 'image': 'b', 'description': 'Sparkle like you mean it. Stomp like you own it.', 'category': 'shoes'},
    {'id': 23, 'name': 'Drama Queen Pins', 'price': 12, 'image': '45', 'description': 'Say it with your head.', 'category': 'accessories'}
]

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/shop')
def shop():
    category = request.args.get('category')
    filtered_products = [p for p in products if p['category'] == category] if category else products
    return render_template('stuff.html', products=filtered_products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/update_cart/<int:product_id>/<action>')
def update_cart(product_id, action):
    cart = session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        if action == 'plus':
            cart[product_id_str] += 1
        elif action == 'minus':
            cart[product_id_str] -= 1
            if cart[product_id_str] <= 0:
                del cart[product_id_str]
        session['cart'] = cart
        session.modified = True
        
    return redirect(url_for('cart'))

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_items = []
    total = 0
    cart = session.get('cart', {})
    
    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str)
        p = next((item for item in products if item['id'] == product_id), None)
        
        if p:
            item = p.copy()
            item['quantity'] = quantity
            subtotal = int(p['price']) * int(quantity)
            item['subtotal'] = subtotal
            total += subtotal
            cart_items.append(item)
            
    return render_template('cart.html', cart=cart_items, total=total)

@app.route('/contact', methods=['GET'])
def show_contact_form():
    return render_template('contact.html', submitted=False)

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    print(f"Name: {name}, Email: {email}, Message: {message}")
    return render_template('contact.html', submitted=True)

if __name__ == '__main__':
    app.run(debug=True)