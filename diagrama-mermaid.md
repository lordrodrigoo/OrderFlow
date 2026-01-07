erDiagram
    User {
        int id
        string first_name
        string last_name
        string password_hash
        int age
        string email
        string phone
        bool is_active
        datetime created_at
        datetime updated_at
    }

    Address {
        int id
        int user_id
        string street
        string number
        string complement
        string neighborhood
        string city
        string state
        string zip_code
        bool is_default
        datetime created_at
    }

    Order {
        int id
        int user_id
        int address_id
        enum status
        decimal total_amount
        decimal delivery_fee
        string notes
        datetime scheduled_date
        datetime created_at
        datetime updated_at
    }

    OrderItem {
        int id
        int order_id
        int product_id
        int quantity
        decimal unit_price
        decimal subtotal
        string notes
    }

    Product {
        int id
        string name
        string description
        int category_id
        decimal price
        string image_url
        bool is_available
        int preparation_time_minutes
        datetime created_at
        datetime updated_at
    }

    Category {
        int id
        string name
        string description
    }

    Review {
        int id
        int order_id
        int user_id
        int rating
        string comment
        datetime created_at
    }

    User ||--o{ Address : has
    User ||--o{ Order : places
    Address ||--o{ Order : used_for
    Order ||--o{ OrderItem : includes
    Product ||--o{ OrderItem : ordered_in
    Category ||--o{ Product : contains
    Order ||--|| Review : generates
    User ||--o{ Review : writes
