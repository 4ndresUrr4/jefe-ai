# Claude Code — Análisis de Arquitectura

> Análisis del código fuente de Claude Code (leak + rewrite Rust).
> Fecha: 2026-04-01
> Última actualización: Incluye análisis completo de los 24,847 LOC de Rust

## Resumen Ejecutivo

Claude Code es un asistente de coding CLI que usa un loop query-asíncrono para conversar con la API de Anthropic, ejecutar herramientas, y manage la memoria de contexto. La reimplementación Rust tiene 9 crates con ~800K+ LOC TypeScript original.

**Hallazgos clave para Jefe de Proyecto:**
- Sistema multi-agente con coordinación centralizada
- Auto-dream system con 3 gates para consolidación de memoria
- Feature gates compilados para eliminar código no usado
- Patron Tool trait con async execution
- Sistema de permisos granular
- 9 crates Rust: cli, query, tools, api, commands, tui, mcp, bridge, core

---

## 0. Estadísticas de Código (24,847 LOC)

| Crate | Archivo | Líneas |
|-------|---------|--------|
| cli | main.rs | 1,163 |
| cli | oauth_flow.rs | 447 |
| commands | lib.rs | 1,723 |
| tui | lib.rs | 1,748 |
| buddy | lib.rs | 1,116 |
| bridge | lib.rs | 998 |
| api | lib.rs | 995 |
| core | lib.rs | 2,045 |
| core | memdir.rs | 879 |
| core | team_memory_sync.rs | 682 |
| mcp | lib.rs | 762 |
| tools | lib.rs | 451 |
| query | lib.rs | 644 |
| query | compact.rs | 290 |
| query | auto_dream.rs | 410 |
| query | coordinator.rs | 173 |
| query | agent_tool.rs | 205 |
| query | cron_scheduler.rs | 114 |
| core | system_prompt.rs | 526 |
| core | analytics.rs | 403 |
| core | migrations.rs | 474 |
| core | keybindings.rs | 485 |
| core | voice.rs | 192 |
| core | output_styles.rs | 347 |
| core | oauth_config.rs | 364 |
| tools | bundled_skills.rs | 574 |
| tools | tasks.rs | 503 |
| tools | cron.rs | 435 |
| tools | grep_tool.rs | 364 |
| tools | worktree.rs | 351 |
| tools | notebook_edit.rs | 298 |
| tools | web_fetch.rs | 236 |
| tools | web_search.rs | 227 |
| tools | skill_tool.rs | 227 |
| tools | file_edit.rs | 152 |
| tools | bash.rs | 199 |
| tools | file_read.rs | 161 |
| tools | glob_tool.rs | 127 |
| tools | todo_write.rs | 127 |
| tools | powershell.rs | 136 |
| tools | mcp_resources.rs | 148 |
| tools | send_message.rs | 149 |
| tools | brief.rs | 151 |
| tools | tool_search.rs | 201 |
| tools | config_tool.rs | 199 |
| tools | enter_plan_mode.rs | 64 |
| tools | exit_plan_mode.rs | 63 |
| tools | sleep.rs | 63 |
| tools | agent_tool.rs | 7 |
| tools | file_write.rs | 110 |
| tools | ask_user.rs | 79 |

---

## 1. Tool System Architecture

### 1.1 Rust Tool Trait (cc-tools)

```rust
#[async_trait]
pub trait Tool {
    fn name(&self) -> &str;
    fn description(&self) -> &str;
    fn permission_level(&self) -> PermissionLevel;
    fn input_schema(&self) -> Value;  // JSON Schema
    async fn execute(&self, input: Value, ctx: &ToolContext) -> ToolResult;
}
```

**ToolContext incluye:**
- `working_dir`, `permission_mode`, `permission_handler`
- `cost_tracker: Arc<CostTracker>`
- `mcp_manager: Option<Arc<cc_mcp::McpManager>>`
- `resolve_path()` helper para paths relativos

**ToolResult:**
```rust
pub struct ToolResult {
    pub content: String,
    pub is_error: bool,
    pub metadata: Option<Value>,  // Para rendering TUI
}
```

**PermissionLevel:** `None`, `ReadOnly`, `Write`, `Execute`, `Dangerous`

### 1.2 TypeScript Tool Framework (src/Tool.ts)

Más sofisticado que Rust:
- `validateInput()` para validación pre-ejecución
- `checkPermissions()` con contexto de permisos
- `renderToolUseMessage()` para React/Ink rendering
- `isConcurrencySafe()`, `isReadOnly()`, `isDestructive()`
- `toAutoClassifierInput()` para ML-based auto-approval

### 1.3 33 Herramientas Implementadas

| Categoría | Herramientas |
|-----------|--------------|
| **File I/O** | Read, Write, Edit, NotebookEdit |
| **Shell** | Bash, PowerShell |
| **Search** | Glob, Grep |
| **Agent** | Task (subagent), SendMessage, TeamCreate, TeamDelete |
| **Task Mgmt** | TaskCreate, TaskGet, TaskUpdate, TaskList, TaskStop, TaskOutput |
| **Web** | WebFetch, WebSearch |
| **MCP** | MCPTool, McpAuthTool, ListMcpResources, ReadMcpResource |
| **Plan** | EnterPlanMode, ExitPlanMode |
| **Scheduling** | CronCreate, CronDelete, CronList |
| **Meta** | ToolSearch, AskUserQuestion, Brief, Skill |
| **System** | Sleep, Config, EnterWorktree, ExitWorktree |

### 1.4 Tool Discovery — Deferred Loading

```
shouldDefer: true → Oculto del prompt inicial
alwaysLoad: true → Siempre incluido
ToolSearchTool → Descubrimiento por keywords o "select:<nombre>"
```

Patrón: herramientas "pesadas" o poco usadas se cargan solo cuando el modelo las solicita.

---

## 2. Plugin Patterns

### 2.1 MCP (Model Context Protocol)

```rust
// cc-mcp/src/lib.rs (762 LOC)
pub trait McpTransport: Send + Sync {
    async fn send(&self, message: &JsonRpcRequest) -> anyhow::Result<()>;
    async fn recv(&self) -> anyhow::Result<Option<JsonRpcResponse>>;
    async fn close(&self) -> anyhow::Result<()>;
}

pub struct StdioTransport { ... }
// Spawns subprocess, pipes stdin/stdout

pub struct HttpTransport { ... }
// HTTP/SSE transport for remote MCP servers
```

**MCP Protocol Types:**
```rust
pub struct InitializeParams {
    pub protocol_version: String,
    pub capabilities: ClientCapabilities,
    pub client_info: ClientInfo,
}

pub struct ServerCapabilities {
    pub tools: Option<ToolsCapability>,
    pub resources: Option<ResourcesCapability>,
    pub prompts: Option<PromptsCapability>,
    pub logging: Option<Value>,
}

pub struct McpTool {
    pub name: String,
    pub description: Option<String>,
    pub input_schema: Value,
}
```

**McpManager** conecta múltiples servers:
- `connect_all()` — conecta todos los servers configurados
- `all_tool_definitions()` — agrega tools con prefijo `"server_name_"`
- `call_tool()` — routing por prefijo
- `list_tools()` — discovery de herramientas
- `list_resources()` — discovery de recursos

**Tool naming:** `mcp__<server>__<tool>` (ej: `mcp__filesystem__read`)

**JSON-RPC 2.0:** Request IDs usan `serde_json::Value` (puede ser string o número)

### 2.2 Skills System

Skills son archivos `.md` en:
- `.claude/commands/` (proyecto)
- `~/.claude/commands/` (usuario)

**SkillTool:**
1. `skill=list` → enumera skills con YAML frontmatter
2. `skill=<name>` → busca y ejecuta
3. Substitución de `$ARGUMENTS` en el contenido

```rust
pub struct SkillTool;
async fn execute(&self, input: Value, ctx: &ToolContext) -> ToolResult {
    // 1. Buscar en project/user commands dirs
    // 2. Strip YAML frontmatter
    // 3. Substituir $ARGUMENTS
    // 4. Return content como ToolResult
}
```

### 2.3 Compile-Time Feature Flags

```typescript
// TypeScript — bun:bundle feature()
feature('KAIROS')     // Always-on assistant
feature('BUDDY')      // Tamagotchi companion
feature('COORDINATOR_MODE')  // Multi-agent
feature('PROACTIVE') // KAIROS always-on mode
```

**Dead-code elimination** en builds externos. Flag = `false` → código eliminado del binario.

### 2.4 Plugin Discovery

```
Plugin dirs: --plugin-dir <path>
Skills dir: ~/.claude/commands/
MCP config: ~/.claude/mcp.json
```

---

## 3. Session Management

### 3.1 ConversationSession (Rust)

```rust
pub struct ConversationSession {
    pub id: String,           // UUID v4
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
    pub messages: Vec<Message>,
    pub model: String,
    pub title: Option<String>,
    pub working_dir: String,
}
```

**Storage:** `~/.claude/conversations/<id>.json`

### 3.2 Cost Tracking

```rust
pub struct CostTracker {
    input_tokens: AtomicU64,
    output_tokens: AtomicU64,
    cache_creation_tokens: AtomicU64,
    cache_read_tokens: AtomicU64,
}

impl CostTracker {
    pub fn total_cost_usd(&self, model: &str) -> f64 {
        // Lookup pricing por modelo
    }
}
```

**Pricing:** Opus $15/$75, Sonnet $3/$15, Haiku $0.80/$4 por MTok

### 3.3 Token Budget System

```rust
pub fn checkTokenBudget(tracker, agentId, budget, globalTurnTokens) -> TokenBudgetDecision {
    // 90% threshold → stop
    // Diminishing returns detection (tokens < 500 por 3+ continuations)
}
```

### 3.4 History Management

**Archivo:** `~/.claude/history.jsonl`

**Patrón de paste referencing:**
```
[Pasted text #1 +10 lines]
[Image #2]
```

Pastes > 1024 bytes → hash reference en vez de contenido inline.

---

## 4. AutoDream System (Memory Consolidation)

### 4.1 Three-Gate Trigger

```
Gate 1: TIME    → 24 horas desde última consolidación
Gate 2: SESSION → 5+ sesiones nuevas desde última consolidación
Gate 3: LOCK    → No otro proceso en consolidación (stale > 1h)
```

### 4.2 AutoDream Struct

```rust
pub struct AutoDream {
    config: AutoDreamConfig,     // min_hours, min_sessions
    memory_dir: PathBuf,
    conversations_dir: PathBuf,
    lock_file: PathBuf,
    state_file: PathBuf,
}

pub struct ConsolidationState {
    pub last_consolidated_at: Option<u64>,
    pub lock_etag: Option<String>,
}
```

### 4.3 Four-Phase Consolidation Prompt

```
Phase 1: Orient — ls memory dir, read MEMORY.md
Phase 2: Gather — daily logs, drifted memories, transcript grep
Phase 3: Consolidate — write/update memory files, convert dates
Phase 4: Prune — keep MEMORY.md < 200 lines, < 25KB
```

**Constraint:** Solo bash read-only para el subagent de consolidación.

---

## 5. Coordinator Mode (Multi-Agent)

### 5.1 Architecture

```
Coordinator (main agent)
├── Worker 1 (spawn via AgentTool)
├── Worker 2 (spawn via AgentTool)
└── ...
```

### 5.2 Coordinator System Prompt

```markdown
## Coordinator Mode
You are operating as an orchestrator for parallel worker agents.

### Task Workflow
1. Research Phase: Spawn workers to gather information in parallel
2. Synthesis Phase: Collect and merge worker findings
3. Implementation Phase: Delegate implementation tasks
4. Verification Phase: Spawn verification workers
```

### 5.3 Internal Tools (Not Delegated)

```rust
const INTERNAL_COORDINATOR_TOOLS: &[&str] = &[
    "Agent",         // No recursion
    "SendMessage",   // Only coordinator uses
    "TaskStop",      // Only coordinator uses
];
```

### 5.4 Environment Gate

```rust
pub fn is_coordinator_mode() -> bool {
    std::env::var("CLAUDE_CODE_COORDINATOR_MODE")
        .map(|v| !v.is_empty() && v != "0" && v != "false")
        .unwrap_or(false)
}
```

---

## 6. Query Loop Architecture

### 6.1 Rust Main Loop

```rust
// cc-query/src/lib.rs (644 LOC)
pub async fn run_query_loop(
    client: &AnthropicClient,
    messages: &mut Vec<Message>,
    tools: &[Box<dyn Tool>],
    ctx: &ToolContext,
    config: &QueryConfig,
    cost_tracker: Arc<CostTracker>,
    event_tx: Option<mpsc::UnboundedSender<QueryEvent>>,
    cancel: CancellationToken,
) -> QueryOutcome {
    loop {
        // 1. Check max_turns, cancel token
        // 2. Build system prompt
        // 3. Call API con streaming
        // 4. On tool_use: execute tools, append results
        // 5. Auto-compact if needed
        // 6. Stop reason → EndTurn, MaxTokens, Error
    }
}
```

### 6.2 QueryOutcome

```rust
pub enum QueryOutcome {
    EndTurn { message: Message, usage: UsageInfo },
    MaxTokens { partial_message: Message, usage: UsageInfo },
    Cancelled,
    Error(ClaudeError),
}
```

### 6.3 QueryConfig

```rust
pub struct QueryConfig {
    pub model: String,
    pub max_tokens: u32,
    pub max_turns: u32,
    pub system_prompt: Option<String>,
    pub append_system_prompt: Option<String>,
    pub output_style: cc_core::system_prompt::OutputStyle,
    pub working_directory: Option<String>,
    pub thinking_budget: Option<u32>,
    pub temperature: Option<f32>,
}
```

### 6.4 QueryEvent (TUI events)

```rust
pub enum QueryEvent {
    Stream(StreamEvent),
    ToolStart { tool_name: String, tool_id: String },
    ToolEnd { tool_name: String, tool_id: String, result: String, is_error: bool },
    TurnComplete { turn: u32, stop_reason: String },
    Status(String),
    Error(String),
}
```

### 6.5 Auto-Compact

```rust
pub const AUTOCOMPACT_TRIGGER_FRACTION: f64 = 0.90;
pub const KEEP_RECENT_MESSAGES: usize = 10;
pub const AUTOCOMPACT_BUFFER_TOKENS: u32 = 13_000;

pub async fn auto_compact_if_needed(
    client: &AnthropicClient,
    messages: &mut Vec<Message>,
    input_tokens: u32,
    model: &str,
    state: &mut AutoCompactState,
) -> Option<Vec<Message>> { ... }
```

**Circuit breaker:** 3 failures consecutivas → disable.

---

## 7. Permission System

### 7.1 PermissionMode

```rust
pub enum PermissionMode {
    Default,         // Read-only auto-allow, writes ask
    AcceptEdits,     // Allow all without prompting
    BypassPermissions, // Allow everything
    Plan,           // Read-only mode
}
```

### 7.2 PermissionHandler Trait

```rust
pub trait PermissionHandler: Send + Sync {
    fn check_permission(&self, tool_name: &str) -> PermissionDecision;
    fn request_permission(&self, request: &PermissionRequest) -> PermissionDecision;
}

pub enum PermissionDecision {
    Allow,
    AllowPermanently,
    Deny,
    DenyPermanently,
}
```

### 7.3 Read-Before-Write Enforcement

FileEditTool y FileWriteTool verifican:
1. Archivo existe en `readFileState` cache
2. mtime no cambió desde última lectura

### 7.4 Hook System

```rust
pub enum HookEvent {
    PreToolUse,
    PostToolUse,
    Stop,
    UserPromptSubmit,
    Notification,
}

pub struct HookEntry {
    pub command: String,
    pub tool_filter: Option<String>,
    pub blocking: bool,
}
```

Hooks reciben JSON en stdin y pueden bloquear operaciones si `blocking=true`.

---

## 8. API Client (cc-api)

### 8.1 Client Architecture

```rust
// cc-api/src/lib.rs (995 LOC)
pub struct AnthropicClient {
    http: reqwest::Client,
    config: ClientConfig,
}

pub struct ClientConfig {
    pub api_key: String,
    pub api_base: String,
    pub api_version: String,
    pub beta_features: String,
    pub max_retries: u32,
    pub initial_retry_delay: Duration,
    pub max_retry_delay: Duration,
    pub request_timeout: Duration,
    pub use_bearer_auth: bool,  // For OAuth tokens vs API keys
}
```

### 8.2 SSE Streaming

```rust
pub enum StreamEvent {
    MessageStart { id: String, model: String, usage: UsageInfo },
    ContentBlockStart { index: usize, content_block: ContentBlock },
    ContentBlockDelta { index: usize, delta: ContentDelta },
    ContentBlockStop { index: usize },
    MessageDelta { stop_reason: Option<String>, usage: Option<UsageInfo> },
    MessageStop,
    Error { error_type: String, message: String },
    Ping,
}

pub enum ContentDelta {
    TextDelta { text: String },
    InputJsonDelta { partial_json: String },
    ThinkingDelta { thinking: String },
    SignatureDelta { signature: String },
}
```

### 8.3 SSE Parser (Manual Implementation)

```rust
pub struct SseLineParser {
    event_type: Option<String>,
    data_buf: String,
}

impl SseLineParser {
    pub fn feed_line(&mut self, line: &str) -> Option<SseFrame> {
        // event: <type>
        // data: <payload>
        // (blank line = end of event)
    }
}
```

### 8.4 Retry Logic

```rust
// 429 (Rate Limit) and 529 (Overloaded) → exponential backoff
// Respects Retry-After header if present
// Max retries: 5 (configurable)

async fn send_with_retry(&self, body: &Value) -> Result<Response, ClaudeError> {
    // Uses Bearer auth for Claude.ai OAuth tokens
    // Uses x-api-key for regular API keys
}
```

### 8.5 Beta Headers

```rust
pub const ANTHROPIC_BETA_HEADER: &str =
    "interleaved-thinking-2025-05-14,token-efficient-tools-2025-02-19,files-api-2025-04-14";
```

---

## 9. Slash Commands (cc-commands)

### 9.1 Command Architecture

```rust
// cc-commands/src/lib.rs (1,723 LOC)
pub struct CommandContext {
    pub config: Config,
    pub cost_tracker: Arc<CostTracker>,
    pub messages: Vec<Message>,
    pub working_dir: PathBuf,
}

#[async_trait]
pub trait SlashCommand: Send + Sync {
    fn name(&self) -> &str;
    fn aliases(&self) -> Vec<&str>;
    fn description(&self) -> &str;
    fn help(&self) -> &str;
    fn hidden(&self) -> bool;
    async fn execute(&self, args: &str, ctx: &mut CommandContext) -> CommandResult;
}

pub enum CommandResult {
    Message(String),
    UserMessage(String),
    ConfigChange(Config),
    ConfigChangeMessage(Config, String),
    ClearConversation,
    SetMessages(Vec<Message>),
    StartOAuthFlow(bool),  // Claude.ai (true) or Console (false)
    Exit,
    Silent,
    Error(String),
}
```

### 9.2 Implemented Commands (27+)

| Command | Aliases | Description |
|---------|---------|-------------|
| help | h, ? | Show commands and usage |
| clear | c | Clear conversation |
| compact | - | Compact conversation to reduce tokens |
| cost | - | Show session token usage and cost |
| exit | quit, q | Exit Claude Code |
| model | - | Show/change model |
| config | - | Show/modify config settings |
| version | - | Show version |
| resume | - | Resume from compact point |
| status | - | Show current status |
| diff | - | Show uncommitted changes |
| memory | - | Memory management |
| bug | - | Submit bug report |
| doctor | - | Run diagnostics |
| login | - | OAuth login flow |
| logout | - | Clear credentials |
| init | - | Initialize project |
| review | - | Code review |
| hooks | - | Manage hooks |
| mcp | - | MCP server management |
| permissions | - | Permission settings |
| plan | - | Enter plan mode |
| tasks | - | Task management |
| session | - | Session management |
| thinking | - | Toggle extended thinking |
| export | - | Export conversation |
| skills | - | List skills |
| rewind | - | Rewind conversation |
| stats | - | Show statistics |
| files | - | File listing |
| rename | - | Rename session |
| effort | - | Effort estimation |
| summary | - | Generate summary |
| commit | - | Commit changes |
| theme | - | Theme settings |
| output-style | - | Output formatting |
| keybindings | - | Keybinding management |
| privacy-settings | - | Privacy settings |

### 9.3 Keybinding Template Generation

```rust
fn generate_keybindings_template() -> anyhow::Result<String> {
    // Generates JSON schema for keybindings:
    // {
    //   "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
    //   "$docs": "https://code.claude.com/docs/en/keybindings",
    //   "bindings": [{ "context": "Global", "bindings": { "ctrl+c": null } }]
    // }
}
```

---

## 10. TUI Architecture (cc-tui)

### 10.1 App State

```rust
// cc-tui/src/lib.rs (1,748 LOC)
pub struct App {
    pub config: Config,
    pub cost_tracker: Arc<CostTracker>,
    pub messages: Vec<Message>,
    pub input: String,
    pub input_history: Vec<String>,
    pub history_index: Option<usize>,
    pub scroll_offset: usize,
    pub is_streaming: bool,
    pub streaming_text: String,
    pub status_message: Option<String>,
    pub should_quit: bool,
    pub show_help: bool,
    pub tool_use_blocks: Vec<ToolUseBlock>,
    pub permission_request: Option<PermissionRequest>,
    pub frame_count: u64,
    pub token_count: u32,
    pub cost_usd: f64,
    pub model_name: String,
    pub agent_status: Vec<(String, String)>,
    pub history_search: Option<HistorySearch>,
    pub cursor_pos: usize,
}
```

### 10.2 Tool Status Tracking

```rust
pub enum ToolStatus { Running, Done, Error }

pub struct ToolUseBlock {
    pub id: String,
    pub name: String,
    pub status: ToolStatus,
    pub output_preview: Option<String>,
}
```

### 10.3 Permission Dialog

```rust
pub struct PermissionRequest {
    pub tool_use_id: String,
    pub tool_name: String,
    pub description: String,
    pub selected_option: usize,
    pub options: Vec<PermissionOption>,
}

impl PermissionRequest {
    pub fn standard(tool_use_id: String, tool_name: String, description: String) -> Self {
        Self {
            options: vec![
                PermissionOption { label: "Allow once".to_string(), key: 'y' },
                PermissionOption { label: "Allow always".to_string(), key: 'a' },
                PermissionOption { label: "Deny".to_string(), key: 'n' },
            ],
            ...
        }
    }
}
```

### 10.4 History Search (Ctrl+R)

```rust
pub struct HistorySearch {
    pub query: String,
    pub matches: Vec<usize>,  // Indices into input_history
    pub selected: usize,
}

impl HistorySearch {
    pub fn update_matches(&mut self, history: &[String]) {
        // Filter by case-insensitive substring match
    }
}
```

### 10.5 Key Bindings

| Key | Action |
|-----|--------|
| Ctrl+C | Cancel streaming / Quit |
| Ctrl+D | Quit (if input empty) |
| Ctrl+R | History search mode |
| F1 or ? | Toggle help overlay |
| Enter | Submit input |
| Up/Down | Navigate input history |
| PageUp/PageDown | Scroll history |
| Left/Right | Move cursor |
| Home/End | Cursor to start/end |

---

## 11. Buddy System (Tamagotchi)

### 11.1 Architecture

```rust
// cc-buddy/src/lib.rs (1,116 LOC)
pub struct Mulberry32 {
    state: u32,  // Seeded PRNG
}

pub fn seed_from_user_id(user_id: &str) -> u32 {
    // SHA-256(user_id + "friend-2026-401"), first 4 bytes
}
```

### 11.2 Species (18 types)

```rust
pub enum Species {
    Duck, Goose, Blob, Cat, Dragon, Octopus, Owl, Penguin,
    Turtle, Snail, Ghost, Axolotl, Capybara, Cactus, Robot,
    Rabbit, Mushroom, Chonk,
}
```

### 11.3 Rarity System

```rust
pub enum Rarity { Common, Uncommon, Rare, Epic, Legendary }

impl Rarity {
    pub fn stars(&self) -> &'static str {
        match self {
            Rarity::Common => "★",
            Rarity::Legendary => "★★★★★",
            ...
        }
    }
    fn stat_floor(&self) -> u8 {  // Higher rarity = higher base stats
        match self {
            Rarity::Common => 5,
            Rarity::Legendary => 50,
            ...
        }
    }
}
```

### 11.4 Buddy Traits

- **Eye**: Dot, Star, X, Circle, At, Degree (6 types)
- **Hat**: None, Crown, Tophat, Propeller, Halo, Wizard, Beanie (7 types)
- **Shiny**: 1% chance

---

## 12. Bridge Protocol (cc-bridge)

### 12.1 Architecture

```rust
// cc-bridge/src/lib.rs (998 LOC)
// Connects local CLI to claude.ai web UI for mobile/web-initiated sessions
```

### 12.2 JWT Utilities

```rust
pub struct JwtClaims {
    pub sub: Option<String>,      // Subject
    pub exp: Option<i64>,          // Expiry timestamp
    pub iat: Option<i64>,          // Issued at
    pub device_id: Option<String>,  // Trusted device ID
    pub session_id: Option<String>,
}

impl JwtClaims {
    pub fn decode(token: &str) -> anyhow::Result<Self> {
        // Strip "sk-ant-si-" prefix if present
        // Base64url decode payload
        // JSON parse
    }
}
```

### 12.3 Device Fingerprint

```rust
pub fn device_fingerprint() -> String {
    // SHA-256(hostname:user:home_dir)
    // Used for trusted-device identification
}
```

### 12.4 BridgeConfig

```rust
pub struct BridgeConfig {
    pub enabled: bool,
    pub server_url: String,
    pub device_id: String,
    pub session_token: Option<String>,
    pub polling_interval_ms: u64,
    pub max_reconnect_attempts: u32,
    pub session_timeout_ms: u64,
}
```

### 12.5 BridgeMessage (Web UI → CLI)

```rust
pub enum BridgeMessage {
    UserMessage { content, session_id, message_id, attachments },
    PermissionResponse { request_id, tool_use_id, decision },
    Cancel { session_id, reason },
    Ping,
}
```

### 12.6 BridgeEvent (CLI → Web UI)

```rust
pub enum BridgeEvent {
    Prompt { message_id, content },
    PermissionRequest { request_id, tool_name, description },
    Cancelled { session_id },
    Pong,
}
```

---

## 13. CLI Entry Point (cc-cli)

### 13.1 Arguments

```rust
// cc-cli/src/main.rs (1,163 LOC)
struct Cli {
    prompt: Option<String>,
    print: bool,                    // -p, --print
    model: String,                  // -m, --model
    permission_mode: CliPermissionMode,
    resume: Option<String>,         // --resume <session-id>
    max_turns: u32,                 // --max-turns
    system_prompt: Option<String>,  // -s, --system-prompt
    append_system_prompt: Option<String>,
    no_claude_md: bool,             // --no-claude-md
    output_format: CliOutputFormat,  // --output-format
    verbose: bool,                  // -v
    api_key: Option<String>,        // --api-key
    max_tokens: Option<u32>,
    cwd: Option<PathBuf>,
    dangerously_skip_permissions: bool,
    dump_system_prompt: bool,       // Hidden
    mcp_config: Option<String>,    // --mcp-config
    no_auto_compact: bool,          // --no-auto-compact
}
```

### 13.2 MCP Tool Wrapper

```rust
struct McpToolWrapper {
    tool_def: ToolDefinition,
    server_name: String,
    manager: Arc<cc_mcp::McpManager>,
}
// Wraps MCP tools to implement the Tool trait
// Prefixes tool names with server_name_
```

### 13.3 Operation Modes

1. **Headless/Print mode** (`-p` or `prompt` arg): Single query, output to stdout
2. **Interactive REPL mode**: Full TUI with ratatui

---

## 14. System Prompt Assembly (cc-core)

### 14.1 SystemPromptPrefix

```rust
// cc-core/src/system_prompt.rs (526 LOC)
pub enum SystemPromptPrefix {
    Cli,        // Standard interactive CLI
    Sdk,        // Sub-agent spawned by SDK
    SdkPreset,  // CLI preset within SDK
    Vertex,     // Vertex AI
    Bedrock,    // AWS Bedrock
    Remote,     // Remote CCR session
}
```

### 14.2 OutputStyle

```rust
pub enum OutputStyle {
    Default,     // No suffix
    Explanatory, // Thorough, educational
    Learning,    // For learners, explain concepts
    Concise,     // Maximally brief
    Formal,      // Professional tone
    Casual,      // Conversational
}
```

### 14.3 Caching Boundary

```rust
pub const SYSTEM_PROMPT_DYNAMIC_BOUNDARY: &str = "__SYSTEM_PROMPT_DYNAMIC_BOUNDARY__";

// Static sections before this marker can be prompt-cached
// Dynamic sections after re-evaluate every turn
```

### 14.4 Section Cache

```rust
fn section_cache() -> &'static Mutex<HashMap<String, Option<String>>>
pub fn clear_system_prompt_sections()
```

---

## 15. Core Crate (cc-core)

### 15.1 Error Types

```rust
// cc-core/src/lib.rs (2,045 LOC)
pub enum ClaudeError {
    Api(String),
    ApiStatus { status: u16, message: String },
    Auth(String),
    PermissionDenied(String),
    Tool(String),
    Io(#[from] std::io::Error),
    Json(#[from] serde_json::Error),
    Http(#[from] reqwest::Error),
    RateLimit,
    ContextWindowExceeded,
    MaxTokensReached,
    Cancelled,
    Config(String),
    Mcp(String),
    Other(String),
}

impl ClaudeError {
    pub fn is_retryable(&self) -> bool {
        matches!(self, RateLimit | ApiStatus { 429, .. } | ApiStatus { 529, .. })
    }
    pub fn is_context_limit(&self) -> bool {
        matches!(self, ContextWindowExceeded | MaxTokensReached)
    }
}
```

### 15.2 ContentBlock Types

```rust
pub enum ContentBlock {
    Text { text: String },
    Image { source: ImageSource },
    ToolUse { id: String, name: String, input: Value },
    ToolResult { tool_use_id: String, content: ToolResultContent, is_error: Option<bool> },
    Thinking { thinking: String, signature: String },
    RedactedThinking { data: String },
    Document { source: DocumentSource, title, context, citations },
}
```

### 15.3 Constants

```rust
// Token limits
DEFAULT_MAX_TOKENS: u32 = 32_000
MAX_TOKENS_HARD_LIMIT: u32 = 65_536
DEFAULT_COMPACT_THRESHOLD: f32 = 0.9
MAX_TURNS_DEFAULT: u32 = 10
MAX_TOOL_ERRORS: u32 = 3

// API
ANTHROPIC_API_BASE: &str = "https://api.anthropic.com"
ANTHROPIC_API_VERSION: &str = "2023-06-01"

// Models
DEFAULT_MODEL: &str = "claude-opus-4-6"
SONNET_MODEL: &str = "claude-sonnet-4-6"
HAIKU_MODEL: &str = "claude-haiku-4-5-20251001"
OPUS_MODEL: &str = "claude-opus-4-6"
```

### 15.4 Config Structure

```rust
pub struct Config {
    pub api_key: Option<String>,
    pub model: Option<String>,
    pub max_tokens: Option<u32>,
    pub permission_mode: PermissionMode,
    pub theme: Theme,
    pub output_style: Option<String>,
    pub auto_compact: bool,
    pub compact_threshold: f32,
    pub verbose: bool,
    pub output_format: OutputFormat,
    pub mcp_servers: Vec<McpServerConfig>,
    pub allowed_tools: Vec<String>,
    pub disallowed_tools: Vec<String>,
    pub env: HashMap<String, String>,
    pub enable_all_mcp_servers: bool,
    pub custom_system_prompt: Option<String>,
    pub append_system_prompt: Option<String>,
    pub disable_claude_mds: bool,
    pub project_dir: Option<PathBuf>,
    pub workspace_paths: Vec<PathBuf>,
    pub hooks: HashMap<HookEvent, Vec<HookEntry>>,
}
```

### 15.5 Context Builder

```rust
pub struct ContextBuilder {
    cwd: PathBuf,
    disable_claude_mds: bool,
}

impl ContextBuilder {
    pub async fn build_system_context(&self) -> String {
        // Platform info, git context
    }
    pub async fn build_user_context(&self) -> String {
        // Date, CLAUDE.md memories
    }
}
```

---

## 16. Memory Directory (cc-core/memdir)

### 16.1 Structure

```
~/.claude/
├── conversations/    # Session history
├── memory/           # Long-term memory files
│   ├── MEMORY.md     # Curated long-term memory
│   └── YYYY-MM-DD.md # Daily logs
├── tasks/           # Task state
├── skills/          # User skills
└── hooks/           # Hook scripts
```

### 16.2 Team Memory Sync

Synchronizes memory across team members via git-backed storage.

---

## 17. Crate Architecture (Resumen)

```
cli (entry point, 1,163 LOC)
├── query (agent loop, 644 LOC)
│   ├── agent_tool (subagents, 205 LOC)
│   ├── auto_dream (memory consolidation, 410 LOC)
│   ├── compact (context window, 290 LOC)
│   ├── coordinator (multi-agent, 173 LOC)
│   └── cron_scheduler (114 LOC)
├── tools (33 implementations, 451 LOC core + 574 LOC bundled)
├── api (Anthropic client + SSE, 995 LOC)
├── commands (slash commands, 1,723 LOC)
├── tui (ratatui terminal UI, 1,748 LOC)
├── mcp (MCP client, 762 LOC)
├── bridge (claude.ai web UI, 998 LOC)
├── buddy (Tamagotchi companion, 1,116 LOC)
└── core (shared types, config, permissions, history, cost, 2,045 LOC)
```

### 18.2 Error Handling

- **thiserror** para `ClaudeError` con `#[from]`
- **`is_retryable()`** y **`is_context_limit()`** para categorización
- **Tool errors nunca hacen panic** — siempre retornan `ToolResult::error()`

### 18.3 Global State

```rust
// DashMap/RwLock con once_cell::sync::Lazy
pub static TASK_STORE: Lazy<Arc<DashMap<String, Task>>> = Lazy::new(...);
pub static INBOX: Lazy<Arc<DashMap<String, Vec<AgentMessage>>>> = Lazy::new(...);
pub static CRON_STORE: Lazy<Arc<RwLock<HashMap<String, CronTask>>>> = Lazy::new(...);
```

### 18.4 Feature Gates

```rust
// Compile-time: feature('FLAG') — dead-code elimination
// Runtime: checkStatsigFeatureGate_CACHED_MAY_BE_STALE()
// Env: isEnvTruthy(process.env.*)
```

### 18.5 Prompts Cache Control

```rust
// cc-api automatically applies CacheControl::ephemeral() a:
// - System prompt blocks
// - Last tool definition (prompt caching)
```

### 18.6 Testing

```rust
#[cfg(test)]
mod tests { ... }
// Tests junto al código, no en archivo separado
// Usa tempfile::TempDir para tests de filesystem
// Mock-friendly: QueryDeps injection pattern
```

---

## 19. Cosas Interesantes Encontradas

### Buddy System (Tamagotchi)
- Gacha system con PRNG Mulberry32 determinístico
- 18 species con rarity, 1% shiny chance
- ASCII art sprites con animación
- `"friend-2026-401"` salt para seeding

### KAIROS (Always-On)
- Append-only daily logs
- 15-second blocking budget para proactive actions
- Exclusive tools: SendUserFile, PushNotification, SubscribePR

### ULTRAPLAN
- Remote CCR session con Opus 4.6
- 30 minutos de pensamiento
- `__ULTRAPLAN_TELEPORT_LOCAL__` sentinel

### Undercover Mode
- Para `USER_TYPE === 'ant'` (empleados Anthropic)
- Previene revelar internal info en commits open-source
- Internal codenames: Capybara, Tengu, Fennec

### Capybara Model
- Nuevo modelo con 1M context
- Fix para premature stopping via "prompt-shape surgery"
- `"Tool loaded."` boundary marker trick

---

## 20. Para Considerar en Proyectos

### Patrones a Adoptar
1. **Three-gate triggers** para background tasks (como AutoDream)
2. **Tool trait async** con permission levels
3. **Coordinator pattern** para parallel multi-agent work
4. **Deferred tool loading** para reducir context waste
5. **Session-based cost tracking** atómico
6. **Read-before-write enforcement** para archivos
7. **Hook system** para extensibilidad
8. **MCP transport abstraction** para plugins

### Patterns a Evitar
1. No hardcodear API keys — usar env vars
2. No panic en tool execution
3. No locks de más de 1 hora para background tasks
4. No compartir estado mutable entre agents sin channels
5. No implementar SSE parsing manually — usar librerías establecidas

---

## 21. Análisis Detallado por Crate

### 21.1 cc-core (2,045 LOC)

**Módulos principales:**
- `error.rs` — ClaudeError con 14 variantes, thiserror
- `types.rs` — ContentBlock, Message, ToolDefinition, UsageInfo
- `config.rs` — Config, Settings, McpServerConfig, HookEvent
- `constants.rs` — TODOS los constants de la app
- `context.rs` — ContextBuilder para system/user context
- `cost.rs` — CostTracker atómico
- `history.rs` — ConversationSession persistence
- `permissions.rs` — PermissionHandler trait
- `hooks.rs` — Hook execution
- `memdir.rs` — ~/.claude directory management
- `team_memory_sync.rs` — Git-backed team memory
- `oauth_config.rs` — OAuth configuration
- `output_styles.rs` — OutputStyle definitions
- `analytics.rs` — Usage analytics
- `keybindings.rs` — Keybinding parsing y defaults
- `system_prompt.rs` — Modular prompt assembly
- `voice.rs` — Voice input handling
- `migrations.rs` — Settings migrations

### 21.2 cc-api (995 LOC)

**Módulos:**
- Tipos request/response para Anthropic API
- `streaming.rs` — StreamEvent, ContentDelta, StreamHandler trait
- `sse_parser.rs` — SSE line parser (manual implementation)
- `client.rs` — AnthropicClient con retry logic

**Key features:**
- Bearer auth para OAuth tokens vs x-api-key para API keys
- Retry con exponential backoff para 429/529
- SSE streaming con channel para select loop
- Request builder pattern con fluent API

### 21.3 cc-mcp (762 LOC)

**Módulos:**
- Tipos JSON-RPC 2.0
- Tipos MCP protocol (initialize, tools, resources, prompts)
- Tipos de contenido (McpContent)
- `transport.rs` — StdioTransport, HttpTransport

**Patrones:**
- Transport trait abstraction para múltiples transports
- Request ID tracking para JSON-RPC
- Tool naming con server prefix

### 21.4 cc-commands (1,723 LOC)

**Comandos principales:**
- help, clear, compact, cost, exit, model, config
- version, resume, status, diff, memory, bug, doctor
- login, logout, init, review, hooks, mcp, permissions
- plan, tasks, session, thinking, export, skills
- rewind, stats, files, rename, effort, summary
- commit, theme, output-style, keybindings, privacy-settings

**Helpers:**
- `open_with_system()` — Cross-platform file opening
- `save_settings_mutation()` — Settings update helper
- `generate_keybindings_template()` — JSON schema generation

### 21.5 cc-tui (1,748 LOC)

**Módulos:**
- `app.rs` — App state y event handling
- `input.rs` — Slash command parsing
- `render.rs` — ratatui rendering

**Features:**
- Raw mode terminal input
- Permission dialogs
- History search (Ctrl+R)
- Tool status tracking
- Streaming response rendering
- Cost/token HUD

### 21.6 cc-buddy (1,116 LOC)

**Sistema de Companion/Tamagotchi:**
- 18 species con stats únicos
- 5 rarity tiers con stat floors
- 6 eye types, 7 hat types
- Shiny chance (1%)
- Deterministic seeding via SHA-256
- Mulberry32 PRNG para rolls

### 21.7 cc-bridge (998 LOC)

**Protocolo de conexión a claude.ai:**
- JWT decode sin verificación de firma
- Device fingerprinting
- BridgeConfig from env
- Long-polling loop
- BridgeMessage (web→cli) y BridgeEvent (cli→web)

### 21.8 cc-query (644 LOC)

**Agentic loop:**
- run_query_loop principal
- QueryConfig, QueryEvent, QueryOutcome
- QueryDeps para dependency injection
- StreamAccumulator para acumular respuestas

**Sub-módulos:**
- `agent_tool.rs` — Subagent spawning
- `auto_dream.rs` — Memory consolidation
- `compact.rs` — Context window management
- `coordinator.rs` — Multi-agent coordination
- `cron_scheduler.rs` — Cron job scheduling

### 21.9 cc-cli (1,163 LOC)

**Entry point:**
- Clap argument parsing
- Mode detection (headless vs REPL)
- MCP tool wrapper
- OAuth flow handling
- Settings loading

### 21.10 cc-tools (varies)

**Tool implementations:**
- file_read.rs, file_write.rs, file_edit.rs, notebook_edit.rs
- bash.rs, powershell.rs
- glob_tool.rs, grep_tool.rs
- web_fetch.rs, web_search.rs
- tasks.rs, todo_write.rs
- skill_tool.rs, tool_search.rs
- mcp_resources.rs, cron.rs
- worktree.rs, brief.rs, ask_user.rs, send_message.rs
- enter_plan_mode.rs, exit_plan_mode.rs, sleep.rs, config_tool.rs
- bundled_skills.rs (574 LOC) — Built-in skill commands

---

*Análisis generado: 2026-04-01*
*Fuentes: /home/jarvis/dept-dev/claude-code/spec/ y /home/jarvis/dept-dev/claude-code/src-rust/crates/*