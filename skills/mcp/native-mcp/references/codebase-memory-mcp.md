# codebase-memory-mcp

`codebase-memory-mcp` is a high-performance code intelligence MCP server that indexes codebases into a persistent SQLite-backed knowledge graph of functions, classes, call chains, HTTP routes, and cross-service links.

It eliminates the need for expensive file-by-file exploration, achieving up to a 120x reduction in token usage.

## Configuration inside ~/.hermes/config.yaml

You can configure `codebase-memory-mcp` as a stdio server in Hermes Agent's config:

```yaml
mcp_servers:
  codebase-memory:
    command: "codebase-memory-mcp"
    args: []
    # optional configurations:
    # timeout: 120
    # connect_timeout: 60
```

*Note: Ensure the binary is in your PATH. If you installed it via the standard script, it should be available globally.*

## Key Performance & Benchmarks (Apple M3 Pro)
- **Linux Kernel full index:** ~3 min (28M LOC, 75k files -> 4.81M nodes, 7.72M edges)
- **Django full index:** ~6 seconds
- **Query latency (structural & Cypher queries):** <1 ms
- **Token efficiency:** 99.2% reduction in token usage (~3,400 tokens vs. ~412,000 tokens for 5 structural queries compared to file-by-file search).

## 14 Exposed MCP Tools
- **Indexing:** `index_repository`, `index_status`, `list_projects`, `delete_project`
- **Query:** `search_graph`, `trace_call_path`, `query_graph`, `ingest_traces`
- **Analysis:** `detect_changes`, `get_graph_schema`, `get_architecture`
- **Code:** `get_code_snippet`, `search_code`, `manage_adr`

## Algorithmic Features
- **Hybrid LSP Semantic Type Resolution:** A lightweight C implementation of type resolution for 10 major languages (Python, TS/JS, PHP, C#, Go, C/C++, Java, Kotlin, Rust) to resolve imports, generics, inheritance, and stdlib types.
- **Louvain Modularity Optimization:** Used by `get_architecture` to partition the call graph into functional communities.
- **Semantic Code Search:** Powered by local `nomic-embed-code` embeddings.
