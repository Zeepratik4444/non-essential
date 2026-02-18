# Component Patterns Reference

## Compound Component Pattern
Use when building complex UI with shared state (e.g., Tabs, Accordion, Select).

```tsx
interface TabsContextType {
  active: string
  setActive: (id: string) => void
}

const TabsContext = createContext<TabsContextType | null>(null)

function useTabs() {
  const ctx = useContext(TabsContext)
  if (!ctx) throw new Error('useTabs must be used within Tabs')
  return ctx
}

export function Tabs({ children, defaultTab }: TabsProps) {
  const [active, setActive] = useState(defaultTab)
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  )
}

Tabs.Tab = function Tab({ id, children }: TabProps) {
  const { active, setActive } = useTabs()
  return (
    <button
      role="tab"
      aria-selected={active === id}
      onClick={() => setActive(id)}
    >
      {children}
    </button>
  )
}
```

## Render Props Pattern

Use when sharing stateful logic with flexible rendering.

```tsx
interface DataFetcherProps<T> {
  url: string
  render: (data: T | null, loading: boolean, error: string | null) => ReactNode
}

function DataFetcher<T>({ url, render }: DataFetcherProps<T>) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch(url)
      .then(r => r.json())
      .then(setData)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [url])

  return <>{render(data, loading, error)}</>
}
```

## Custom Hook Pattern

Use to extract and reuse stateful logic across components.

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value)

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay)
    return () => clearTimeout(timer)
  }, [value, delay])

  return debounced
}
```

## Server Component vs Client Component (Next.js App Router)

| Use Server Component | Use Client Component |
| :-- | :-- |
| Data fetching | useState / useEffect |
| Static rendering | Event handlers (onClick etc.) |
| No interactivity needed | Browser APIs |
| Heavy dependencies | Real-time updates |

Mark client components with `'use client'` at top of file.
Mark server actions with `'use server'`.
