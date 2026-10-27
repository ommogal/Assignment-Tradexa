# Test Cases

| ID | Scenario | Expected Result |
|---|---|---|
| TC01 | One product fits a box | Box is accepted |
| TC02 | Product exceeds every box dimension | Box is rejected |
| TC03 | Product can fit after rotation | Box is accepted |
| TC04 | Total product weight exceeds box capacity | Box is rejected |
| TC05 | Multiple products fit in a box | Box is accepted |
| TC06 | Empty product list | Validation error |
| TC07 | Missing required field | Validation error |
| TC08 | Negative dimension/weight/cost | Validation error |
| TC09 | Two valid boxes | Cheapest valid box is selected |
| TC10 | Equal-cost valid boxes | Lower unused volume is preferred |
