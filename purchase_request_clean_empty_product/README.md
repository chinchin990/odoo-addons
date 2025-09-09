# Purchase Request Clean Empty Product

[English] | [中文说明](README.zh.md)

Automatically removes purchase request lines that do not have a product selected. Keeps requests clean and consistent by filtering out empty product lines on create/write.

## Features
- Cleans lines with missing `product_id` during create and write
- Supports all one2many command formats (0,1,2,3,4,5,6)
- Works silently without interrupting users
- Compatible with OCA `purchase_request`

## Installation
- Dependency: `purchase_request`
- Install via Apps or CLI; no configuration required

