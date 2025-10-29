import streamlit as st
# Page configuration
import pandas as pd
import json
from datetime import datetime
import os
from PIL import Image
from pathlib import Path

st.set_page_config(
    page_title="Tany Foods Orders",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- helpers ---
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def _path(name: str) -> Path:
    return DATA_DIR / name

def load_json(name: str, default):
    p = _path(name)
    try:
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        pass  # corrupted file → fall back
    return default

def save_json(name: str, obj):
    p = _path(name)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(p)

USERS_FILE = "users.json"
PRODUCTS_FILE = "products.json"
ORDERS_FILE = "orders.json"

def load_data():
    st.session_state.users_db    = load_json(USERS_FILE, {})
    st.session_state.products_db = load_json(PRODUCTS_FILE, [])
    st.session_state.orders_db   = load_json(ORDERS_FILE, [])

def save_users():
    save_json(USERS_FILE, st.session_state.users_db)

def save_products():
    save_json(PRODUCTS_FILE, st.session_state.products_db)

def save_orders():
    save_json(ORDERS_FILE, st.session_state.orders_db)

# Baseline defaults
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("user_data", {})
st.session_state.setdefault("cart", {})
st.session_state.setdefault("users_db", {})
st.session_state.setdefault("products_db", [])
st.session_state.setdefault("orders_db", [])
st.session_state.setdefault("current_page", "catalog")

# Load persisted data (overwrites the empty defaults if files exist)
load_data()

st.markdown("""
<style>
/* Be very specific so we beat Streamlit theme rules */
div.send-order div.stButton > button,
div.send-order button[data-testid="baseButton-secondary"],
div.send-order button[kind="secondary"],
div.send-order button {
  background-color: #28a745 !important;  /* green */
  color: #ffffff !important;
  border: 1px solid #1e7e34 !important;
  box-shadow: none !important;
}
div.send-order div.stButton > button:hover,
div.send-order button[data-testid="baseButton-secondary"]:hover,
div.send-order button[kind="secondary"]:hover,
div.send-order button:hover {
  filter: brightness(0.95);
}
</style>
""", unsafe_allow_html=True)

# helper to reduce space
def ellipsize(text: str, max_chars: int = 28) -> str:
    text = str(text or "")
    return (text[:max_chars-1] + "…") if len(text) > max_chars else text

def product_image_src(p: dict) -> str:
    # Prefer Sheets direct URL; fall back to local path; handle missing keys safely
    return (str(p.get("image_url") or p.get("image_path") or "")).strip()

# Admin credentials (hardcoded - in production, use environment variables)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def load_logo():
    """Load the Tany Foods logo"""
    logo_path = "ariannacabrera/Downloads/Tany Foods Logo.png"
    if os.path.exists(logo_path):
        return Image.open(logo_path)
    return None

def signup_page():
    """User signup page"""
    st.title("🍽️ Tany Foods Orders")
    
    # Display logo if available
    logo = load_logo()
    if logo:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(logo, use_container_width=True)
    
    st.subheader("Create Your Account")
    
    with st.form("signup_form"):
        first_name = st.text_input("First Name*")
        last_name = st.text_input("Last Name*")
        company_name = st.text_input("Company Name*")
        email = st.text_input("Email*")
        password = st.text_input("Password*", type="password")
        confirm_password = st.text_input("Confirm Password*", type="password")
        
        submit = st.form_submit_button("Sign Up")
        
        if submit:
            if not all([first_name, last_name, company_name, email, password]):
                st.error("Please fill in all required fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif email in st.session_state.users_db:
                st.error("Email already registered. Please log in.")
            else:
                st.session_state.users_db[email] = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'company_name': company_name,
                    'password': password
                }
                save_users()
                st.success("Account created successfully! Please log in.")
                st.rerun()
    
    st.markdown("---")
    if st.button("Already have an account? Log In"):
        st.session_state.show_signup = False
        st.rerun()

def login_page():
    """User login page"""
    st.title("🍽️ Tany Foods Orders")
    
    # Display logo if available
    logo = load_logo()
    if logo:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(logo, use_container_width=True)
    
    st.subheader("Welcome Back!")
    
    tab1, tab2 = st.tabs(["Customer Login", "Admin Login"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Log In")
            
            if submit:
                if email in st.session_state.users_db:
                    if st.session_state.users_db[email]['password'] == password:
                        st.session_state.logged_in = True
                        st.session_state.user_data = st.session_state.users_db[email]
                        st.session_state.user_data['email'] = email
                        st.session_state.is_admin = False
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Incorrect password")
                else:
                    st.error("Email not found. Please sign up.")
        
        if st.button("Don't have an account? Sign Up"):
            st.session_state.show_signup = True
            st.rerun()
    
    with tab2:
        with st.form("admin_login_form"):
            admin_user = st.text_input("Admin Username")
            admin_pass = st.text_input("Admin Password", type="password")
            admin_submit = st.form_submit_button("Admin Log In")
            
            if admin_submit:
                if admin_user == ADMIN_USERNAME and admin_pass == ADMIN_PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.is_admin = True
                    st.session_state.user_data = {'first_name': 'Admin'}
                    st.success("Admin login successful!")
                    st.rerun()
                else:
                    st.error("Invalid admin credentials")

def product_catalog_page():
    """Main product catalog page"""
    st.title("🍽️ Tany Foods - Product Catalog")
    
    # Welcome message
    st.write(f"Welcome, {st.session_state.user_data.get('first_name', 'User')}!")
    
    # Search bar
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔍 Search products", placeholder="Search by item code or description...")
    with col2:
        st.write("")
        st.write("")
        if st.button("🛒 View Cart", use_container_width=True):
            st.session_state.current_page = 'cart'
            st.rerun()
    
    # Category filter
    categories = list(set([p.get('category', 'Uncategorized') for p in st.session_state.products_db]))
    selected_category = st.selectbox("Filter by Category", ["All"] + categories)
    
    # Filter products
    filtered_products = st.session_state.products_db
    if search_query:
        filtered_products = [p for p in filtered_products if 
                           search_query.lower() in p.get('item_code', '').lower() or 
                           search_query.lower() in p.get('description', '').lower()]
    if selected_category != "All":
        filtered_products = [p for p in filtered_products if p.get('category') == selected_category]
    
    # Display image (supports Google Drive direct URLs or local paths)
    img = product_image_src(product)
    if img:
        # show URL or local file if it exists; else fallback
        if img.startswith("http") or os.path.exists(img):
            st.image(img, use_container_width=True)
        else:
            st.image("https://via.placeholder.com/150", use_container_width=True)
    else:
        st.image("https://via.placeholder.com/150", use_container_width=True)

def product_detail_page():
    """Dedicated product detail page with back navigation"""
    product = st.session_state.get('selected_product')
    if not product:
        st.warning("No product selected.")
        if st.button("← Back to Catalog", use_container_width=True, key="back_no_product"):
            st.session_state.current_page = 'catalog'
            st.rerun()
        return

    pid = product.get('item_code', 'unknown').replace(' ', '_')

    # Top bar
    left, mid, right = st.columns([1, 4, 1])
    with left:
        if st.button("← Back to Catalog", use_container_width=True, key=f"back_{pid}"):
            st.session_state.current_page = 'catalog'
            st.rerun()
    with mid:
        st.title(f"Product: {product.get('item_code')}")
        st.caption(product.get('description', ''))
    with right:
        if st.button("🛒 View Cart", use_container_width=True, key=f"view_cart_{pid}"):
            st.session_state.current_page = 'cart'
            st.rerun()

    # Body
    col1, col2 = st.columns([2, 1])
    with col1:
        img = product_image_src(product)
        if img and (img.startswith("http") or os.path.exists(img)):
            st.image(img, use_container_width=True)
        else:
            st.image("https://via.placeholder.com/600x400", use_container_width=True)

    with col2:
        st.markdown(f"**Category:** {product.get('category', 'N/A')}")
        if product.get('brand'):
            st.markdown(f"**Brand:** {product.get('brand')}")

        # UOM
        uom_options = []
        if product.get('allow_case', True): uom_options.append("Case")
        if product.get('allow_each', True): uom_options.append("Each")
        if not uom_options:
            st.error("This product is not available for purchase.")
            return

        selected_uom = st.radio(
            "Unit of Measure",
            uom_options,
            horizontal=True,
            key=f"uom_{pid}"
        )

        # Quantity
        qty_key = f"qty_{pid}"  # or f"qty_{product.get('item_code')}"
        if qty_key not in st.session_state:
            st.session_state[qty_key] = 1

        qty = st.number_input(
            "Quantity",
            min_value=1,
            value=st.session_state[qty_key],
            key=f"qty_input_{pid}"
        )
        st.session_state[qty_key] = qty

        # Give this a unique key
        if st.button("🛒 Add to Cart", use_container_width=True, key=f"add_to_cart_{pid}"):
            cart_key = product["item_code"] 
            if cart_key in st.session_state.cart:
                st.warning("This item is already in your cart. Edit the quantity in the cart.")
            else:
                st.session_state.cart[cart_key] = {
                    "item_code": product["item_code"],
                    "description": product["description"],
                    "brand": (product.get("brand") or "").strip(),
                    "uom": selected_uom,
                    "quantity": int(st.session_state[qty_key]),
                }
                st.success("✅ Added to cart!")

def cart_page():
    """Shopping cart page"""
    st.title("🛒 Your Shopping Cart")
    
    if st.button("← Back to Catalog"):
        st.session_state.current_page = 'catalog'
        st.rerun()
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Start shopping!")
        return

    # Display cart items
    st.subheader(f"Items in Cart: {len(st.session_state.cart)}")
    
    # Column widths: Item, Description, Brand, UOM, Qty, Action
    COLS = [1.5, 3, 1.5, 1, 1, 1]   # description gets more room

    # Header
    h1, h2, h3, h4, h5, h6 = st.columns(COLS)
    with h1: st.markdown("**Item**")
    with h2: st.markdown("**Description**")
    with h3: st.markdown("**Brand**")
    with h4: st.markdown("**UOM**")
    with h5: st.markdown("**Qty**")
    with h6: st.markdown("**Action**")
    st.divider()
    
    # Rows
    for cart_key, item in list(st.session_state.cart.items()):
        c1, c2, c3, c4, c5, c6 = st.columns(COLS, gap="small")
    
        with c1:
            st.markdown(f"**{item.get('item_code','')}**")
        with c2:
            st.write(ellipsize(item.get('description', ''), max_chars=40))  # more chars fit now
        with c3:
            st.write(item.get('brand', '—'))
        with c4:
            st.write(item.get('uom', ''))
        with c5:
            new_qty = st.number_input(
                label="",                
                label_visibility="collapsed",  
                min_value=1,
                step=1,
                value=int(item['quantity']),
                key=f"cart_qty_{cart_key}"
            )
            if new_qty != item['quantity']:
                st.session_state.cart[cart_key]['quantity'] = new_qty
        with c6:
            if st.button("🗑️ Remove", key=f"remove_{cart_key}", use_container_width=True):
                del st.session_state.cart[cart_key]
                st.rerun()
    
    # Send order button (green via CSS)
    st.markdown('<div class="send-order">', unsafe_allow_html=True)
    if st.button("📤 Send Order", use_container_width=True, key="send_order"):
        st.session_state.show_order_confirmation = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Order confirmation modal
    if st.session_state.get('show_order_confirmation', False):
        st.markdown("---")
        st.warning("⚠️ Are you sure you want to submit this order?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Submit Order", use_container_width=True):
                submit_order()
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.show_order_confirmation = False
                st.rerun()

def submit_order():
    """Submit the order"""
    order = {
        'order_id': f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'customer_name': f"{st.session_state.user_data['first_name']} {st.session_state.user_data['last_name']}",
        'company_name': st.session_state.user_data['company_name'],
        'email': st.session_state.user_data['email'],
        'items': list(st.session_state.cart.values())
    }
    
    st.session_state.orders_db.append(order)
    save_orders()
    
    st.session_state.cart = {}
    st.session_state.show_order_confirmation = False
    st.success(f"✅ Order {order['order_id']} submitted successfully!")
    st.balloons()
    st.rerun()

def admin_dashboard():
    """Admin dashboard"""
    st.title("Admin Dashboard - Tany Foods Orders")
    
    tab1, tab2 = st.tabs(["📦 Orders Management", "📋 Product Management"])
    
    with tab1:
        st.subheader("All Orders")
        
        if not st.session_state.orders_db:
            st.info("No orders received yet.")
        else:
            # Display orders summary
            st.metric("Total Orders", len(st.session_state.orders_db))
            
            # Convert orders to DataFrame for display and download
            orders_data = []
            for order in st.session_state.orders_db:
                for item in order['items']:
                    orders_data.append({
                        'Order ID': order['order_id'],
                        'Timestamp': order['timestamp'],
                        'Customer Name': order['customer_name'],
                        'Company Name': order['company_name'],
                        'Email': order['email'],
                        'Item Code': item['item_code'],
                        'Description': item['description'],
                        'Quantity': item['quantity'],
                        'UOM': item['uom']
                    })
            
            df_orders = pd.DataFrame(orders_data)
            st.dataframe(df_orders, use_container_width=True)
            
            # Download buttons
            col1, col2 = st.columns(2)
            with col1:
                csv = df_orders.to_csv(index=False)
                st.download_button(
                    "📥 Download as CSV",
                    csv,
                    "tany_foods_orders.csv",
                    "text/csv",
                    use_container_width=True
                )
            with col2:
                excel_buffer = pd.ExcelWriter('temp.xlsx', engine='xlsxwriter')
                df_orders.to_excel(excel_buffer, index=False, sheet_name='Orders')
                excel_buffer.close()
                
                with open('temp.xlsx', 'rb') as f:
                    st.download_button(
                        "📥 Download as Excel",
                        f,
                        "tany_foods_orders.xlsx",
                        "application/vnd.ms-excel",
                        use_container_width=True
                    )
    
    with tab2:
        st.subheader("Product Database Management")
        
        # Upload product database
        st.write("**Upload Product Database (CSV/Excel)**")
        uploaded_file = st.file_uploader(
            "Upload file with columns: item_code, description, brand, category, allow_case, allow_each",
            type=['csv', 'xlsx']
        )
        
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                # Convert DataFrame to product list
                products = []
                for _, row in df.iterrows():
                    products.append({
                        'item_code': row.get('item_code', ''),
                        'description': row.get('description', ''),
                        'category': row.get('category', 'Uncategorized'),
                        'brand': row.get('brand', ''),
                        'allow_case': row.get('allow_case', True),
                        'allow_each': row.get('allow_each', True),
                        'image_path': row.get('image_path', '')
                    })
                
                st.session_state.products_db = products
                save_products()
                st.success(f"✅ Uploaded {len(products)} products successfully!")
                st.dataframe(df, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error uploading file: {str(e)}")
        
        # Display current products
        if st.session_state.products_db:
            st.write(f"**Current Products: {len(st.session_state.products_db)}**")
            df_products = pd.DataFrame(st.session_state.products_db)
            st.dataframe(df_products, use_container_width=True)

# Main app logic
def main():
    # Logout button
    if st.session_state.logged_in:
        if st.sidebar.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_data = {}
            st.session_state.cart = {}
            st.session_state.is_admin = False
            st.session_state.current_page = 'catalog'
            st.rerun()
    
    # Route to appropriate page
    if not st.session_state.logged_in:
        if st.session_state.get('show_signup', False):
            signup_page()
        else:
            login_page()
    else:
        if st.session_state.get('is_admin', False):
            admin_dashboard()
        else:
            if st.session_state.current_page == 'catalog':
                product_catalog_page()
            elif st.session_state.current_page == 'cart':
                cart_page()
            elif st.session_state.current_page == 'product_detail':  # NEW
                product_detail_page()

if __name__ == "__main__":
    main()
