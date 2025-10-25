# Tany Foods Orders - Streamlit Mobile App

A complete ordering system for Tany Foods with customer and admin interfaces.

---

## 🚀 Quick Deployment to GitHub & Streamlit Cloud

### Step 1: Set Up GitHub Repository

**Create a new GitHub repository:**

1. Go to github.com  
2. Click **New Repository**  
3. Name it: `tany-foods-orders`  
4. Make it **Public** (required for free Streamlit deployment)  
5. Click **Create Repository**

**Upload files to GitHub:**

- Click **uploading an existing file**  
- Drag and drop these files:
  - `app.py` (the main Python code)
  - `requirements.txt`
  - `sample_products.csv`
  - Create a folder structure: `Arianna/Downloads/` and upload your `Tany Foods Logo.png` there
- Click **Commit changes**

### Step 2: Deploy to Streamlit Cloud

1. Go to **share.streamlit.io**  
2. Sign in with your GitHub account  
3. Click **New app**  
4. Fill in the details:
   - **Repository:** `your-username/tany-foods-orders`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **Deploy**

Your app will be live at:  
`https://your-username-tany-foods-orders.streamlit.app`

---

## 📁 File Structure

```
tany-foods-orders/
├── app.py                          # Main application file
├── requirements.txt                # Python dependencies
├── sample_products.csv             # Example product database
├── Arianna/
│   └── Downloads/
│       └── Tany Foods Logo.png     # Your logo (REQUIRED)
└── README.md                       # This file
```

---

## 🔐 Default Admin Credentials

- **Username:** `admin`  
- **Password:** `admin123`  

> ⚠️ IMPORTANT: Change these credentials in the code before deployment for security!

---

## 📋 Features

### Customer Features
- ✅ Sign up / Login system  
- ✅ Product catalog with search and category filters  
- ✅ Product details with unit of measure selection (Case/Each)  
- ✅ Quantity selector with +/- buttons and manual input  
- ✅ Shopping cart with duplicate prevention  
- ✅ Order confirmation before submission  
- ✅ Company and user information tracking  

### Admin Features
- ✅ View all orders in a dashboard  
- ✅ Download orders as CSV or Excel  
- ✅ Upload product database (CSV/Excel)  
- ✅ View current product inventory  
- ✅ Order details include: customer name, company, item code, description, quantity, UOM  

---

## 📊 Product Database Format

Your product CSV/Excel file should have these columns:

| Column Name | Type    | Description                               | Example                |
|-------------|---------|-------------------------------------------|------------------------|
| item_code   | Text    | Unique product identifier                  | B-0-01-009             |
| description | Text    | Product description                        | Yogurt Coco 9 x 64 oz  |
| category    | Text    | Product category for filtering             | Yogurt                 |
| allow_case  | Boolean | Can be purchased by case (TRUE/FALSE)      | TRUE                   |
| allow_each  | Boolean | Can be purchased individually              | FALSE                  |
| image_path  | Text    | Optional: Path to product image            | (blank or a file path) |

**Example CSV:**

```csv
item_code,description,category,allow_case,allow_each,image_path
B-0-01-009,Yogurt Coco 9 x 64 oz,Yogurt,TRUE,FALSE,
B-0-01-010,Yogurt Guava 9 x 64 oz,Yogurt,TRUE,FALSE,
B-0-01-011,Yogurt Mango 9 x 64 oz,Yogurt,TRUE,FALSE,
```

---

## 🔧 How to Update the App

**To update product database:**
1. Login as admin  
2. Go to **Product Management** tab  
3. Upload new CSV/Excel file  
4. Products will update immediately

**To modify the code:**
1. Edit files in your GitHub repository  
2. Commit changes  
3. Streamlit will automatically redeploy (takes 1–2 minutes)

---

## ⚠️ Important Notes

- **Logo File:** Make sure your logo is uploaded to exactly this path: `Arianna/Downloads/Tany Foods Logo.png`
- **Data Persistence:** Currently, all data (users, products, orders) is stored in **session state**. This means:
  - Data resets when the app restarts
  - For production, integrate a proper database (e.g., Firebase, PostgreSQL, MongoDB)

**Security:**
- Change admin credentials before going live  
- In production, implement proper password hashing  
- Use environment variables for sensitive data

**Mobile Optimization:** The app is designed to be mobile-responsive using Streamlit's layout features.

---

## 🔄 Future Enhancements (Optional)
- Add database integration (Firebase/Supabase)  
- Email notifications for orders  
- Order history for customers  
- Price information and order totals  
- Payment integration  
- Product images hosted on cloud storage  
- User profile management  
- Order status tracking  

---

## 📞 Support
For issues or questions:
- Check Streamlit logs in the deployment dashboard  
- Review GitHub repository files  
- Test locally first: `streamlit run app.py`

---

## 📱 Testing the App

**As a Customer:**
1. Click **Don't have an account? Sign Up**  
2. Fill in your details  
3. Login with your credentials  
4. Browse products  
5. Add items to cart  
6. Submit an order

**As an Admin:**
1. Click **Admin Login** tab  
2. Login with admin credentials  
3. Upload product database  
4. View and download orders

---
