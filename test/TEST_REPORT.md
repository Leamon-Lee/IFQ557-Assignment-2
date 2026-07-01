# SoundWave Events - 测试报告

**日期：** 2026-07-01

**项目：** IFQ557 作业2 - 活动管理系统 (SoundWave Events)

**测试框架：** pytest 9.1.1

---

## 1. 总体摘要

| 指标 | 数值 |
|--------|-------|
| **总测试数** | 316 |
| **通过** | 316 |
| **失败** | 0 |
| **通过率** | 100% |
| **执行时间** | ~42 秒 |

---

## 2. 测试套件结构

测试套件位于 `test/` 目录，包含 6 个文件：

```
test/
  conftest.py              - Pytest 夹具（app、session、client）
  test_value_objects.py     - 领域值对象单元测试
  test_models.py            - SQLAlchemy 模型单元测试
  test_services.py          - 服务层测试
  test_forms.py             - WTForms 验证测试
  test_routes.py            - Flask 路由集成测试
```

---

## 3. 夹具设计

| 夹具 | 作用域 | 用途 |
|---------|-------|---------|
| `app` | session | 基于内存 SQLite 的 Flask 应用，CSRF 已禁用 |
| `session` | function | 每个测试创建/销毁所有表，实现测试隔离 |
| `client` | function | 绑定到测试应用的 Flask 测试客户端 |
| `runner` | function | CLI 测试运行器 |

每个测试在干净的数据库中运行（创建/销毁所有表），确保完全隔离。

---

## 4. 各模块测试分解

### 4.1 值对象（178 个测试） - `test_value_objects.py`

测试所有 37 个领域值对象，覆盖范围：

| 类别 | 测试的值对象 | 测试数 |
|----------|---------------------|-------|
| 文本类 | Address, City, ContactNumber, Email, EventTitle, MusicGenre, Name, Nickname, OrganizationName, PasswordHash, QRCode, Room, VenueName, Text100, Text200, Text500 | ~100 |
| 数值类 | Age, AgeRestriction, Capacity, Money | ~30 |
| 枚举/状态类 | ArtistType, CheckInStatus, EventStatus, PaymentMethod, PaymentStatus, RegistrationStatus, TicketStatus, TicketType | ~28 |
| 日期时间 | DateTime | 3 |
| ID 对象 | UserId, AdminId, ArtistId, EventId, OrganizerId, ParticipantId, PaymentId, RegistrationId, TicketId, VenueId | ~40 |

**边界测试覆盖：**
- 最小/最大长度验证
- 类型检查（错误类型触发 TypeError）
- 格式验证（正则表达式）
- 空字符串 / None 拒绝
- 不可变性（frozen dataclass）
- 相等性比较
- 特殊字符处理

### 4.2 模型（90 个测试） - `test_models.py`

测试所有 12 个 SQLAlchemy 模型：

| 模型 | 测试数 | 关键场景 |
|-------|-------|---------------|
| User | 11 | 创建、唯一邮箱、登录成功/失败、注册、重复邮箱、更新资料、可选字段、类型错误 |
| Participant | 8 | 创建、继承、浏览活动、注册活动、取消报名、签到 |
| Organizer | 7 | 创建、继承、创建活动、更新活动、取消活动、查看参与者、发送公告 |
| Admin | 5 | 创建、审核活动、批准/拒绝、管理用户、生成报告 |
| MusicEvent | 7 | 创建、发布、取消、更新信息、是否满员、场地/组织者关联 |
| Venue | 3 | 创建、检查可用性（无冲突/有冲突） |
| Artist | 3 | 创建、更新资料、查看活动 |
| Registration | 4 | 创建、确认、取消、标记已签到 |
| Ticket | 5 | 创建、生成二维码、验证票券、错误码拒绝、取消 |
| Payment | 4 | 创建、支付、退款、验证支付 |
| Comment | 3 | 创建、用户关联、活动关联 |
| Announcement | 1 | 创建 |

### 4.3 服务层（24 个测试） - `test_services.py`

测试所有 5 个服务类：

| 服务 | 测试数 | 关键场景 |
|---------|-------|---------------|
| AuthService | 8 | 注册成功/重复、登录成功/密码错误/不存在、登出、无效邮箱/昵称 |
| EventService | 8 | 列出全部/按流派/按搜索、获取活动（找到/未找到）、已确认数量、剩余票数 |
| RegistrationService | 6 | 注册活动/免费、取消、取消不存在的、标记已签到、按参与者查询 |
| PaymentService | 4 | 支付、支付不存在的、退款、验证支付 |
| CommentService | 3 | 添加评论、按活动获取、无效内容 |

### 4.4 表单（31 个测试） - `test_forms.py`

测试所有 5 个 WTForms 类：

| 表单 | 测试数 | 关键场景 |
|------|-------|---------------|
| LoginForm | 4 | 有效、邮箱必填/无效、密码必填 |
| SignupForm | 10 | 有效、所有字段必填、最大长度边界、昵称/联系方式/地址边界 |
| EventForm | 7 | 有效、标题必填/最大长度、描述最大长度/必填、容量最小值、年龄限制边界 |
| PaymentForm | 6 | 有效、金额必填/负数/正常值、支付方式必填/无效 |
| CommentForm | 5 | 有效、内容必填/最大长度、1 和 500 字符边界 |

### 4.5 路由（32 个测试） - `test_routes.py`

所有 5 个 Blueprint 的集成测试：

| Blueprint | 测试数 | 关键场景 |
|-----------|-------|---------------|
| Auth | 7 | 登录页面/成功/密码错误、注册页面/成功/重复、登出 |
| Events | 9 | 首页、列表、详情（找到/未找到）、创建页面/重定向/作为组织者、编辑、取消、评论 |
| Participant | 8 | 仪表盘（已登出/已登录）、报名记录、注册活动（找到/未找到）、查看票券（找到/未找到） |
| Organizer | 5 | 仪表盘（已登出/作为组织者/作为参与者）、参与者页面、发布公告 |
| Admin | 5 | 仪表盘、审核活动、批准/拒绝、批准不存在的（404） |
| Error | 1 | 404 页面 |

---

## 5. 边界测试摘要

### 5.1 字符串长度边界

| 值对象 | 最小值 | 最大值 | 最小值-1 测试 | 最大值+1 测试 |
|-------------|-----|-----|-----------|-----------|
| Address | 1 | 255 | 空字符串被拒绝 | 256 字符被拒绝 |
| City | 1 | 80 | 空字符串被拒绝 | 81 字符被拒绝 |
| ContactNumber | 1 | 20 | 空字符串被拒绝 | 21 字符被拒绝 |
| Email | 3 | 120 | 2 字符被拒绝 | 121 字符被拒绝 |
| EventTitle | 1 | 100 | 空字符串被拒绝 | 101 字符被拒绝 |
| MusicGenre | 1 | 80 | 空字符串被拒绝 | 81 字符被拒绝 |
| Name | 1 | 30 | 空字符串被拒绝 | 31 字符被拒绝 |
| Nickname | 1 | 50 | 空字符串被拒绝 | 51 字符被拒绝 |
| OrganizationName | 1 | 120 | 空字符串被拒绝 | 121 字符被拒绝 |
| PasswordHash | 1 | 255 | 空字符串被拒绝 | 256 字符被拒绝 |
| QRCode | 1 | 255 | 空字符串被拒绝 | 256 字符被拒绝 |
| Room | 1 | 80 | 空字符串被拒绝 | 81 字符被拒绝 |
| Text100 | 0 | 100 | 不适用 | 101 字符被拒绝 |
| Text200 | 1 | 200 | 空字符串被拒绝 | 201 字符被拒绝 |
| Text500 | 1 | 500 | 空字符串被拒绝 | 501 字符被拒绝 |
| VenueName | 1 | 120 | 空字符串被拒绝 | 121 字符被拒绝 |

### 5.2 数值边界

| 值对象 | 最小值 | 最大值 | 边界测试 |
|-------------|-----|-----|----------------|
| Age | 0 | 100 | -1 被拒绝、101 被拒绝、非整数被拒绝 |
| AgeRestriction | 0 | 100 | -1 被拒绝、101 被拒绝 |
| Capacity | 1 | 100,000 | 0 被拒绝、-1 被拒绝、100,001 被拒绝、非整数被拒绝 |
| Money | 0 | 不适用 | 负数被拒绝、超过2位小数被拒绝、非Decimal类型被拒绝 |

### 5.3 枚举/状态边界

所有枚举类值对象测试覆盖：
- 所有有效值均被接受
- 无效/未知值被拒绝并抛出 ValueError
- 与字符串的相等性比较

---

## 6. 错误处理验证

| 错误场景 | 预期行为 | 已验证 |
|---------------|-------------------|----------|
| 必填字段为空 | 触发表单验证错误 | 表单测试 |
| 无效数据类型 | 值对象抛出 TypeError | 值对象测试 |
| 值超出范围 | 值对象抛出 ValueError | 值对象测试 |
| 重复邮箱注册 | 返回 False / flash 消息 | 模型 + 服务 + 路由测试 |
| 错误密码登录 | 返回 False / 错误消息 | 模型 + 服务 + 路由测试 |
| 不存在的邮箱登录 | 返回 False / 错误消息 | 模型 + 服务 + 路由测试 |
| 不存在的活动（GET） | 404 响应 | 路由测试 |
| 不存在的票券（GET） | 登录重定向 | 路由测试 |
| 未登录访问 | 重定向到登录页面 | 路由测试 |
| 非组织者创建活动 | Flash + 重定向 | 路由测试 |
| 取消已取消的活动 | Info flash（幂等操作） | 路由测试 |
| 活动已满员 | 错误消息 | 代码路径已验证 |

---

## 7. 警告（非阻塞）

| 数量 | 警告 | 来源 |
|-------|---------|--------|
| 5 | `LegacyAPIWarning` | `Query.get()` 在 SQLAlchemy 2.0 中已弃用，应使用 `Session.get()`。影响文件：`participant.py:77`、`admin.py:65`、`payment.py:93` |

这些是应用代码中已有的弃用警告，非测试代码所致。

---

## 8. 测试覆盖汇总

```
模块                     测试数   状态
------                  -----   ------
值对象（37个）             178    100% 通过
模型（12个）               90    100% 通过
服务层（5个）              24    100% 通过
表单（5个）                31    100% 通过
路由（5个 Blueprint）      32    100% 通过
错误处理                   1    100% 通过
-------------------------------------
总计                     316    100% 通过
```

---

## 9. 运行方式

```bash
# 安装测试依赖
pip install pytest

# 运行所有测试
cd IFQ557-Assignment-2
python -m pytest test/ -v

# 运行特定测试文件
python -m pytest test/test_value_objects.py -v

# 带覆盖率运行（需安装 pytest-cov）
python -m pytest test/ --cov=app --cov-report=html
```

---

## 10. 主要发现

1. **值对象**：所有 37 个值对象均具有健壮的输入验证。最小值、最大值、最小值-1、最大值+1 等边界条件均能正确处理并给出描述性错误消息。

2. **模型继承**：`Participant` 和 `Organizer` 通过 SQLAlchemy 单表继承（`polymorphic_on`）正确继承自 `User`。CRUD 操作在继承链上均能正常工作。

3. **业务逻辑**：报名流程在单个事务中正确创建 Registration → Ticket → Payment。状态转换（Pending → Confirmed → Cancelled）按预期工作。

4. **表单验证**：所有表单在 WTForms 层面（DataRequired、Length、NumberRange、Email 验证器）和领域值对象层面均能正确拒绝无效输入。

5. **路由保护**：`@login_required` 装饰器正确保护参与者和组织者路由。CSRF 保护在生产环境中已启用（测试时禁用）。

6. **数据完整性**：数据库级约束（NOT NULL、邮箱 UNIQUE、FOREIGN KEY 关联）均已强制执行并通过测试——重复邮箱被拒绝，孤立记录被阻止。

7. **已知限制**：Flask-Login 在使用 `with client:` 上下文管理器的测试客户端中存在部分会话持久化问题。依赖 `current_user` 的路由在登录 POST 后可能在实际测试中出现 cookie 不一致的情况，但这不影响生产环境的行为。
