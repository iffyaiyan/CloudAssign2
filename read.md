# Product Catalogue Application - Architecture Document

## 1. Overview

This document outlines the architecture and design decisions for the Product Catalogue application deployed on Microsoft Azure. The application allows users to manage a catalogue of products, including adding new products with images and viewing product details.

## 2. Feature Added - Azure Blob Storage for Product Images

Beyond the basic requirements, I have added the ability to upload and store product images using Azure Blob Storage. This feature enhances the user experience by:

1. Allowing users to upload images for products
2. Storing images efficiently in a scalable cloud storage solution
3. Serving images directly from Azure's CDN network for fast loading
4. Generating unique filenames to avoid conflicts
5. Validating file types to ensure only images are uploaded

## 3. Architecture Diagram

```
+---------------------+        +----------------------+
|                     |        |                      |
|   Web Browser       |<------>|   Azure App Service  |
|                     |        |   (Flask Web App)    |
|                     |        |                      |
+---------------------+        +----------+-----------+
                                          |
                                          |
                      +-------------------v------------------+
                      |                                      |
                      |                                      |
           +----------v-----------+            +------------v------------+
           |                      |            |                         |
           |   Azure SQL Database |            |   Azure Blob Storage    |
           |   (Product Data)     |            |   (Product Images)      |
           |                      |            |                         |
           +----------------------+            +-------------------------+
```

## 4. Architecture Decisions
I have prior understanding of the Azure and the Flash, so have chosen this.
### 4.1 Azure App Service

**Decision:** Host the web application on Azure App Service.

**Rationale:**
- Managed platform with built-in infrastructure maintenance
- Easy deployment and scaling capabilities
- Support for Python applications
- Automatic SSL certificate management
- Integrated logging and monitoring

### 4.2 Azure SQL Database

**Decision:** Use Azure SQL Database for product data storage.

**Rationale:**
- Fully managed SQL database service
- High availability and disaster recovery built in
- Automatic scaling options
- Strong data consistency guarantees
- Familiar SQL syntax for queries
- Secure connection with firewall rules and encryption

### 4.3 Azure Blob Storage

**Decision:** Use Azure Blob Storage for storing product images.

**Rationale:**
- Optimized for storing and serving large unstructured data like images
- Cost-effective compared to storing binary data in SQL
- Built-in CDN capabilities for faster content delivery
- Highly durable and available storage
- Secure access control with SAS tokens
- Pay only for what you use pricing model

### 4.4 Web Framework

**Decision:** Use Flask for the web application framework.

**Rationale:**
- I have prior knowledge of Flask and it's compatible with Python
- Lightweight framework suitable for simple applications
- Easy to understand and modify
- Good integration with Azure services
- Minimalistic approach reduces overhead

## 5. URL to Access Application

# The application can be accessed at:
# I have done the deployment using the GitHub Actions
`https://product-catalogue-app-irfan-assign2.azurewebsites.net/`

<!-- Though I have disabled the above hosting, as the database and other things incur cost, and I am working on some other project parallely.
Do let me know at the time of evaluation, I will up it -->


## 6. Code Organization and Explanation
**The application follows a modular structure:**

- app/init.py: Initializes the Flask application and database connection
- app/config.py: Contains configuration settings loaded from environment variables
- app/models.py: Defines the Product model and database operations
- app/routes.py: Contains all the application routes and view functions
- app/utils.py: Utility functions for blob storage operations
- app/templates/: HTML templates for the application views
- static/: CSS and JavaScript files for frontend functionality
- app.py: Entry point for running the application locally
- setup.py: Helper script to initialize Azure resources

**Key Features Explained**

  1. Product Management:

   - Add new products with name, description, price, and image
   - List all products in a responsive grid layout
   - View detailed information about each product


  2. Image Handling with Azure Blob Storage:

   - Images are uploaded directly to Azure Blob Storage
   - Unique filenames are generated to prevent conflicts
   - File type validation ensures only images are uploaded
   - Images are served directly from Azure Blob Storage


  3. Responsive UI:

   - Bootstrap-based responsive design
   - Mobile-friendly interface
   - Image preview when adding products

## 7. Future Enhancements

1. Add user authentication and authorization
2. Implement product categories and search functionality
3. Add inventory management features
4. Implement Azure CDN for better image delivery performance
5. Add Azure Application Insights for monitoring and telemetry