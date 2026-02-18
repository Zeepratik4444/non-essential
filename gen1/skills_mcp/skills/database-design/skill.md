---
name: database-design
description: >
  Design database schemas, write optimised SQL queries, handle migrations,
  and implement ORM models. Use when user needs table design, indexing
  strategy, query optimisation, relationships, or PostgreSQL/MySQL help.
triggers:
  - "design a schema"
  - "database tables"
  - "sql query"
  - "optimise query"
  - "add index"
  - "migration"
  - "orm model"
  - "foreign key"
  - "database relationship"
---

# Database Design

## When to Use
- Designing relational database schemas (PostgreSQL, MySQL)
- Writing and optimising SQL queries
- Creating indexes for query performance
- Writing SQLAlchemy or Prisma ORM models
- Database migrations (Alembic, Prisma Migrate)
- Relationships: one-to-one, one-to-many, many-to-many

## Protocol
1. Identify the task (schema design, query writing, optimisation, migration)
2. Identify the database engine (PostgreSQL preferred) and ORM if any
3. Load references/schema_patterns.md for normalisation and patterns
4. Design or review following the checklist
5. Return complete SQL or ORM code with explanation

## Schema Design Checklist
- [ ] Every table has a surrogate primary key (`id UUID DEFAULT gen_random_uuid()`)
- [ ] `created_at` and `updated_at` on every table
- [ ] Foreign keys explicitly defined with `ON DELETE` behaviour
- [ ] NOT NULL constraints on all required fields
- [ ] Check constraints for enum-like string fields
- [ ] Indexes on all foreign key columns
- [ ] Composite indexes for common query patterns
- [ ] No stored passwords — only hashed values

## PostgreSQL Table Template
```sql
CREATE TABLE orders (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status      VARCHAR(20) NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending','processing','completed','cancelled')),
    total_cents INTEGER NOT NULL CHECK (total_cents >= 0),
    metadata    JSONB,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);

-- Auto-update updated_at
CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();
```

## SQLAlchemy Model Template
```python
from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMPTZ
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("status IN ('pending','processing','completed','cancelled')"),
        CheckConstraint("total_cents >= 0"),
    )

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id    = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status     = Column(String(20), nullable=False, default="pending")
    total_cents= Column(Integer, nullable=False)
    metadata_  = Column("metadata", JSONB)
    created_at = Column(TIMESTAMPTZ, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMPTZ, nullable=False, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="orders")
```

## Query Optimisation Rules
1. `EXPLAIN ANALYZE` before declaring a query slow
2. Index columns used in `WHERE`, `JOIN ON`, `ORDER BY`
3. Avoid `SELECT *` — always specify columns
4. Use `LIMIT` on all queries returning lists
5. Prefer `EXISTS` over `COUNT` for existence checks
6. Use connection pooling — never open raw connections per request
7. Avoid N+1: use `JOIN` or ORM `.options(selectinload(...))`

## Output Format

### Task: {schema design | query | optimisation | migration}

**Database**: PostgreSQL | MySQL
**ORM**: SQLAlchemy | Prisma | None

#### Schema / Query

```sql
{complete SQL}
```

#### ORM Model

```python / typescript
{complete ORM model}
```

#### Indexes

```sql
{all index definitions}
```

#### Explanation
{why each design decision was made}

## Rules
- Always use UUIDs for primary keys — never auto-increment integers in distributed systems
- Monetary values in cents (integer) — never floats
- Always define `ON DELETE` behaviour on foreign keys explicitly
- Migrations must be reversible — always write `downgrade()` in Alembic
- Never drop columns in production migration — deprecate then remove in next release

## References
- Normalisation and schema patterns: read references/schema_patterns.md
- Query optimisation techniques: read references/query_optimisation.md
- Migration best practices: read references/migration_guide.md
