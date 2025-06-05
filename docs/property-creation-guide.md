# Property Creation Guide

The Open To Close API wrapper now makes property creation incredibly simple! This guide shows you all the different ways to create properties, from simple one-liners to advanced configurations.

## Quick Start

### 1. Simple Title Only
```python
from open_to_close import PropertiesAPI

client = PropertiesAPI()

# Just pass a string - that's it!
property = client.create_property("Beautiful Family Home")
print(f"Created property {property['id']}")
```

### 2. Simple Dictionary Format
```python
# Most common usage - simple and intuitive
property = client.create_property({
    "title": "Luxury Estate with Pool",
    "client_type": "Buyer", 
    "status": "Active",
    "purchase_amount": 650000
})
```

## Complete Examples

### Buyer Property
```python
buyer_property = client.create_property({
    "title": "Downtown Condo",
    "client_type": "Buyer",
    "status": "Active",
    "purchase_amount": 425000
})
```

### Seller Property  
```python
seller_property = client.create_property({
    "title": "Suburban Family Home",
    "client_type": "Seller", 
    "status": "Pre-MLS",
    "purchase_amount": 550000
})
```

### Dual Representation
```python
dual_property = client.create_property({
    "title": "Investment Property",
    "client_type": "Dual",
    "status": "Under Contract", 
    "purchase_amount": 395000
})
```

### Minimal (Uses Defaults)
```python
# Uses defaults: client_type="Buyer", status="Active"
minimal_property = client.create_property({
    "title": "Simple Property"
})
```

## Available Options

### Client Types
- `"Buyer"` (default)
- `"Seller"`  
- `"Dual"`

### Status Options
- `"Pre-MLS"`
- `"Active"` (default)
- `"Under Contract"`
- `"Withdrawn"`
- `"Contract"`
- `"Closed"`
- `"Terminated"`

### Optional Fields
- `purchase_amount`: Dollar amount (number)
- `address`: Street address (string)
- `city`: City name (string)  
- `state`: State/province (string)
- `zip_code`: ZIP/postal code (string)

## Advanced Usage

### Legacy API Format (Still Supported)
```python
# For advanced users who need full control
property = client.create_property({
    "team_member_id": 26392,
    "time_zone_id": 1,
    "fields": [
        {"id": 926565, "key": "contract_title", "value": "Custom Property"},
        {"id": 926553, "key": "contract_client_type", "value": 797212},
        {"id": 926552, "key": "contract_status", "value": 797206}
    ]
})
```

### Custom Team Member
```python
# Override the auto-detected team member
property = client.create_property(
    "Custom Property",
    team_member_id=12345
)
```

## Error Handling

The API provides clear error messages for invalid inputs:

```python
try:
    property = client.create_property({
        "title": "Test Property",
        "client_type": "InvalidType"  # ❌ Will fail
    })
except Exception as e:
    print(f"Error: {e}")
    # Error: Invalid client_type: InvalidType. Must be one of: buyer, seller, dual
```

## What Happens Behind the Scenes

When you use the simple format, the API wrapper automatically:

1. **Auto-detects team member ID** from your teams
2. **Converts simple fields** to the complex API format
3. **Applies sensible defaults** (Buyer + Active status)
4. **Validates all inputs** before sending to API
5. **Provides clear error messages** if something goes wrong

## Migration from Complex Format

**Before (Complex):**
```python
property = client.create_property({
    "team_member_id": 26392,
    "time_zone_id": 1,
    "fields": [
        {"id": 926565, "key": "contract_title", "value": "My Property"},
        {"id": 926553, "key": "contract_client_type", "value": 797212},
        {"id": 926552, "key": "contract_status", "value": 797206},
        {"id": 926554, "key": "purchase_amount", "value": 450000}
    ]
})
```

**After (Simple):**
```python
property = client.create_property({
    "title": "My Property",
    "client_type": "Buyer",
    "status": "Active", 
    "purchase_amount": 450000
})
```

## Best Practices

1. **Use simple format** for 90% of use cases
2. **Always include a descriptive title**
3. **Specify client_type and status** when they differ from defaults
4. **Handle exceptions** gracefully in production code
5. **Use legacy format** only when you need advanced field control

## Need Help?

The wrapper includes comprehensive validation and error messages. If you encounter issues:

1. Check the error message - it usually explains exactly what's wrong
2. Verify your client_type and status values match the available options
3. Ensure your title is not empty
4. Check the API documentation for field-specific requirements

## Full Working Example

```python
#!/usr/bin/env python3
from open_to_close import PropertiesAPI

def create_sample_properties():
    client = PropertiesAPI()
    
    # Create different types of properties
    properties = []
    
    # 1. Simple string
    properties.append(
        client.create_property("🏡 Cozy Starter Home")
    )
    
    # 2. Buyer property
    properties.append(
        client.create_property({
            "title": "🏰 Luxury Estate",
            "client_type": "Buyer",
            "status": "Active",
            "purchase_amount": 850000
        })
    )
    
    # 3. Seller property
    properties.append(
        client.create_property({
            "title": "🏢 Downtown Condo",
            "client_type": "Seller", 
            "status": "Pre-MLS",
            "purchase_amount": 425000
        })
    )
    
    # Print results
    for i, prop in enumerate(properties, 1):
        print(f"Property {i}: ID {prop['id']} created successfully!")

if __name__ == "__main__":
    create_sample_properties()
```

That's it! Property creation is now as simple as it should be. 🎉 