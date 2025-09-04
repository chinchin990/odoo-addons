# AI Odoo 插件开发指南 (AI Odoo Development Guidelines)

**目标：** 本文档为AI助手提供了一套严格的规则，用于开发Odoo插件。必须严格遵守这些规则，以生成高质量、无错误且符合Odoo开发范式的代码。

---

## 第一部分：基础结构与清单文件 (`__manifest__.py`)

### 1. 标准目录结构
- **规则**：必须创建标准的模块目录结构。核心目录包括：
  - `models`: 存放业务逻辑和数据模型的Python文件。
  - `views`: 存放定义用户界面的XML文件。
  - `security`: 存放权限控制相关的XML和CSV文件。
  - `controllers`: 存放HTTP路由和网页控制器。
  - `static`: 存放CSS, JS, 图像等静态资源。
  - `data`: 存放需要在安装/更新时加载的数据文件 (XML, CSV)。
  - `demo`: 存放演示数据 (XML, CSV)。
- **规则**：每个包含Python代码的目录（如 `models`, `controllers`）都必须有一个 `__init__.py` 文件，用于导入该目录下的Python文件。根目录的 `__init__.py` 则用于导入子目录。

### 2. 清单文件规则 (`__manifest__.py`)
- **规则**：`__manifest__.py` 文件是模块的入口点，必须是一个包含以下核心键的Python字典：
  - `name`: (str) 模块的名称，简短且易于理解。
  - `version`: (str) 模块的版本号，遵循 `Odoo系列.x.y.z` 格式 (例如 `17.0.1.0.0`)。
  - `summary`: (str) 模块功能的简短摘要。
  - `author`: (str) 作者名称。
  - `license`: (str) 许可证，通常是 `LGPL-3` 或 `AGPL-3`。
  - `category`: (str) Odoo应用商店中的分类。
  - `website`: (str) 作者或项目的网站。
  - `depends`: (list) 依赖的模块列表。**必须**准确列出所有依赖项，否则模块无法正确安装或运行。
  - `data`: (list) XML和CSV数据文件的路径列表。**必须**遵循正确的加载顺序：通常是 `security/` -> `data/` -> `views/`。
  - `installable`: (bool) 应设为 `True`，表示模块可以被安装。
  - `application`: (bool) 如果模块是一个独立的应用程序，则设为 `True`。

---

## 第二部分：模型 (Models - Python)

### 1. 继承
- **规则**：创建新模型时，使用 `_name = 'your.model.name'` 并继承 `models.Model`。
- **规则**：扩展现有模型时，使用 `_inherit = 'original.model.name'`。**禁止**在扩展时使用 `_name`，因为这会创建一个不相关的副本，而不是扩展。

### 2. 字段定义
- **规则**：字段名必须使用 `snake_case` 风格（例如 `part_number`, `order_line_ids`）。
- **规则**：必须使用正确的字段类型，例如：
  - `fields.Char`, `fields.Text`, `fields.Html`
  - `fields.Integer`, `fields.Float`
  - `fields.Boolean`
  - `fields.Date`, `fields.Datetime`
  - `fields.Selection`
  - `fields.Many2one`, `fields.One2many`, `fields.Many2many`
- **关联字段规则**：
  - `Many2one(comodel_name='res.partner', string='Customer')`: 必须提供 `comodel_name`（关联的模型名）。
  - `One2many(comodel_name='sale.order.line', inverse_name='order_id')`: 必须提供 `comodel_name` 和 `inverse_name`（在关联模型中指向本模型的`Many2one`字段名）。
  - `related='partner_id.country_id'`: 在生成 `related` 字段前，必须**在逻辑上确认路径上的每个字段都真实存在**。这是一个高风险操作，极易产生幻觉。

### 3. 方法与装饰器
- **规则**：`@api.depends('field1', 'field2')`: 用于计算字段 (`compute=...`)。必须列出所有依赖字段。计算方法内部**必须**为计算字段赋值。
- **规则**：`@api.onchange('field1')`: 用于界面交互。方法不应返回值，而是直接修改 `self` 上的其他字段值以在UI上动态更新。
- **规则**：`@api.model` / `@api.model_create_multi`: 用于需要 `cls` 而非 `self` 的模型级方法（例如，不依赖具体记录的辅助方法或重写 `create`）。
- **规则**：重写核心方法（如 `create`, `write`, `unlink`）时，**必须**调用 `super()` 以保留父类功能，除非有明确的意图要完全替换它。调用 `super()` 是保证系统稳定和功能完整的关键。

---

## 第三部分：视图 (Views - XML)

### 1. 文件结构
- **规则**：XML文件必须以 `<?xml version="1.0" encoding="utf-8"?>` 开头，所有内容必须包含在 `<odoo>` 标签内。

### 2. 视图定义与继承
- **规则**：所有视图、窗口动作、菜单项等记录都必须在 `<record>` 标签中定义，并拥有一个**在模块内唯一**的 `id`。
- **规则**：继承并修改现有视图时，必须使用 `<xpath expr="..." position="...">`。
  - `expr`: XPath表达式，用于定位要修改的元素。**表达式必须尽可能精确**，以避免在Odoo版本更新后失效。优先选择具有唯一 `name` 或 `id` 属性的元素作为目标。
  - `position`: `inside`, `after`, `before`, `replace`, `attributes`。
- **规则**：继承视图的 `<record>` 需要通过 `inherit_id` 字段指向原始视图的 `xml_id` (例如 `inherit_id="base.view_partner_form"`)。

### 3. 字段与属性
- **规则**：视图中引用的字段 `name` **必须**与Python模型中定义的字段名完全一致。
- **规则**：使用 `attrs="{'invisible': [('state', '!=', 'draft')]}"` 来动态控制字段的可见性、只读性等。`attrs` 的值是一个Python字典字符串，domain表达式必须正确。
- **规则**：使用 `groups="module_name.group_user"` 来控制字段或视图元素的访问权限。`groups` 的值是安全组的 `xml_id`。

---

## 第四部分：安全 (Security)

### 1. 访问权限 (`ir.model.access.csv`)
- **规则**：此文件用于定义用户组对模型的访问权限。
- **规则**：文件必须包含以下列头：`id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_delete`。
- **规则**：`model_id:id` 必须使用 `model_your_model_name` 的格式（例如 `model_purchase_request`）。
- **规则**：`group_id:id` 必须引用一个安全组的 `xml_id` (例如 `base.group_user`)。

### 2. 记录规则 (Record Rules)
- **规则**：用于行级权限控制。必须定义一个清晰的 `domain_force`，它是一个Odoo domain表达式字符串，用于过滤用户可以访问的记录。

---

## 第五部分：核心反幻觉原则

1.  **绝不假设 (NEVER ASSUME)**：在引用任何模型、字段、视图ID或方法前，必须假定它可能不存在，并以验证其存在为第一步。例如，在添加 `partner_id.phone` 字段到视图前，先确认 `partner_id` 字段存在于当前模型中。这是避免幻觉的第一原则。
2.  **遵循框架 (FOLLOW THE FRAMEWORK)**：严格使用Odoo提供的API和模式。禁止创造不存在的 `position` 属性值、XML标签或Python装饰器。Odoo的框架是确定性的，不要偏离它。
3.  **明确意图 (BE EXPLICIT)**：代码应清晰、自解释。例如，`Many2one` 字段应明确提供 `comodel_name`。继承视图时，`xpath` 表达式应尽可能具体。
4.  **小步快跑 (INCREMENTAL STEPS)**：从最简单的功能（例如，仅添加一个字段和一个基础视图）开始，然后逐步增加复杂性（如添加 `onchange`、计算字段、安全规则等）。每一步都应是逻辑上完整且可验证的。
5.  **验证XML ID (VALIDATE XML IDs)**：在 `ref="..."` 或 `group_id:id` 中引用XML ID时，必须使用 `module_name.id_name` 的完整格式。如果该ID在当前模块中定义，可以省略 `module_name.`。在引用其他模块的ID时，必须假定该模块已在 `depends` 中声明。
